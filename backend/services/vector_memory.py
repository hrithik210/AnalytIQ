import os
from typing import Any, Dict, List, Optional, Tuple

import chromadb
from chromadb.utils import embedding_functions


class VectorMemory:
	"""
	Lightweight wrapper around ChromaDB persistent client to store and retrieve
	relevant analysis artifacts for RAG:
	- Interpreter schema/context
	- Wrangler reports
	- Analyst findings
	- Visualization recommendations

	Documents are chunked with overlap for better recall.
	"""

	def __init__(self, db_path: Optional[str] = None, model_name: str = "all-MiniLM-L6-v2") -> None:
		self.db_path = db_path or os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
		os.makedirs(self.db_path, exist_ok=True)

		self.client = chromadb.PersistentClient(path=self.db_path)
		self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
			model_name=model_name
		)

		# Collections per artifact type
		self.schema_collection = self.client.get_or_create_collection(
			name="schema_collection", embedding_function=self.embedding_function
		)
		self.wrangling_collection = self.client.get_or_create_collection(
			name="wrangling_collection", embedding_function=self.embedding_function
		)
		self.analyst_collection = self.client.get_or_create_collection(
			name="analyst_collection", embedding_function=self.embedding_function
		)
		self.visualization_collection = self.client.get_or_create_collection(
			name="visualization_collection", embedding_function=self.embedding_function
		)

	def _chunk_text(self, text: str, chunk_size: int = 1200, chunk_overlap: int = 200) -> List[str]:
		"""Simple character-based chunking with overlap."""
		if not text:
			return []
		text = str(text)
		chunks: List[str] = []
		start = 0
		length = len(text)
		while start < length:
			end = min(start + chunk_size, length)
			chunks.append(text[start:end])
			if end == length:
				break
			start = max(end - chunk_overlap, 0)
		return chunks

	def _add_documents(self, collection, report_id: str, documents: List[str], metadatas: List[Dict[str, Any]], id_prefix: str) -> None:
		if not documents:
			return
		ids = [f"{id_prefix}-{report_id}-{i}" for i in range(len(documents))]
		collection.add(documents=documents, metadatas=metadatas, ids=ids)

	def store_schema(self, report_id: str, interpreter_dict: Dict[str, Any]) -> None:
		schema_text = (
			f"Dataset Summary: {interpreter_dict.get('schema_summary', '')}\n"
			f"Columns: {', '.join(interpreter_dict.get('data_types', {}).keys())}\n"
			f"Data Types: {interpreter_dict.get('data_types', {})}\n"
			f"Missing Values: {interpreter_dict.get('missing_values', {})}\n"
			f"Suggested Analysis: {interpreter_dict.get('suggested_analysis', [])}\n"
		)
		chunks = self._chunk_text(schema_text)
		metas = [{"report_id": report_id, "type": "schema", "seq": i} for i, _ in enumerate(chunks)]
		self._add_documents(self.schema_collection, report_id, chunks, metas, id_prefix="schema")

	def store_wrangler(self, report_id: str, wrangler_output: Dict[str, Any]) -> None:
		wrangling_text = (
			f"Cleaned CSV Path: {wrangler_output.get('cleaned_csv_path', '')}\n"
			f"Wrangling Report: {wrangler_output.get('wrangling_report', '')}\n"
			f"Original Shape: {wrangler_output.get('original_shape', [])}\n"
			f"Final Shape: {wrangler_output.get('final_shape', [])}\n"
		)
		chunks = self._chunk_text(wrangling_text)
		metas = [{"report_id": report_id, "type": "wrangler", "seq": i} for i, _ in enumerate(chunks)]
		self._add_documents(self.wrangling_collection, report_id, chunks, metas, id_prefix="wrangler")

	def store_analyst(self, report_id: str, analyst_output: Dict[str, Any]) -> None:
		analyst_text = (
			f"Descriptive Stats Keys: {list((analyst_output or {}).get('descriptive_stats', {}).keys())}\n"
			f"Trends: {(analyst_output or {}).get('trends', [])}\n"
			f"Correlation: {(analyst_output or {}).get('correlation', [])}\n"
			f"Outliers: {(analyst_output or {}).get('outliers', [])}\n"
		)
		chunks = self._chunk_text(analyst_text)
		metas = [{"report_id": report_id, "type": "analyst", "seq": i} for i, _ in enumerate(chunks)]
		self._add_documents(self.analyst_collection, report_id, chunks, metas, id_prefix="analyst")

	def store_visualization(self, report_id: str, visualizer_res: Dict[str, Any]) -> None:
		visualization_text = f"Visualization Code Snippets: {', '.join(visualizer_res.get('plotly_code_snippets', []))}"
		chunks = self._chunk_text(visualization_text)
		metas = [{"report_id": report_id, "type": "visualization", "seq": i} for i, _ in enumerate(chunks)]
		self._add_documents(self.visualization_collection, report_id, chunks, metas, id_prefix="viz")

	def _retrieve(self, collection, query: str, n_results: int = 4) -> List[str]:
		try:
			res = collection.query(query_texts=[query], n_results=n_results)
			docs = res.get("documents") or []
			if not docs:
				return []
			return docs[0]
		except Exception:
			return []

	def retrieve_interpreter_context(self, query: str, n_results: int = 4) -> List[str]:
		return self._retrieve(self.schema_collection, query, n_results)

	def retrieve_wrangler_context(self, query: str, n_results: int = 4) -> List[str]:
		return self._retrieve(self.wrangling_collection, query, n_results)

	def retrieve_analyst_context(self, query: str, n_results: int = 4) -> List[str]:
		return self._retrieve(self.analyst_collection, query, n_results)

	def retrieve_visualizer_context(self, query: str, n_results: int = 4) -> List[str]:
		return self._retrieve(self.visualization_collection, query, n_results)