import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

class VectorMemory:
    
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        try:
            self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
            print("Embedding function initialized successfully.")
        except Exception as e:
            print(f"Error initializing embedding function: {e}")
            self.embedding_function = None
            
        
        self.schema_collection = self.client.get_or_create_collection(
            name = "schema_collection",
            embedding_functions=self.embedding_function
        
        )
        
        self.wrangling_collection = self.client.get_or_create_collection(
            name = "wrangling_collection",
            embedding_functions=self.embedding_function
        )
        
        self.analyst_collection = self.client.get_or_create_collection(
            name = "analyst_collection",
            embedding_functions=self.embedding_function
        )
        
        self.visualization_collection = self.client.get_or_create_collection(
            name = "visualization_collection",
            embedding_functions=self.embedding_function
        )
        
        print("Vector memory initialized with collections.")
    
    def store_schema(self ,report_id: str, interpreter_dict: Dict[str, Any]) -> None:
        
        schema_text = f"""
        Dataset Summary: {interpreter_dict.get('schema_summary', '')}
        Columns: {', '.join(interpreter_dict.get('data_types', {}).keys())}
        Data Types: {interpreter_dict.get('data_types', {})}
        Missing Values: {interpreter_dict.get('missing_values', {})}
        Suggested Analysis: {interpreter_dict.get('suggested_analysis', [])}
        Key Questions: {' '.join(interpreter_dict.get('key_questions', []))}
        """

        self.schema_collection.add(
            documents=[schema_text],
            metadatas=[interpreter_dict],
            ids=[report_id],
        )
        
        print(f"[VectorMemory] Schema for report {report_id} stored.")
    
    def store_wrangler(self, report_id: str, wrangler_output: Dict[str, Any]) -> None:
        
        wrangling_text = f"""
        Cleaned CSV Path: {wrangler_output.get('cleaned_csv_path', '')}
        Wrangling Report: {wrangler_output.get('wrangling_report', '')}
        cleaned Sample: {wrangler_output.get('cleaned_sample', {})}
        Original Shape: {wrangler_output.get('original_shape', [])}
        Final Shape: {wrangler_output.get('final_shape', [])}
        
        """

        self.wrangling_collection.add(
            documents=[wrangling_text],
            metadatas=[wrangler_output],
            ids=[report_id],
        )

        print(f"[VectorMemory] Wrangling for report {report_id} stored.")
    
    def store_analyst(self, report_id: str, analyst_output: Dict[str, Any]) -> None:
        
        analyst_text = f"""
        Analysis Report: {analyst_output.get('analysis_report', '')}
        Key Findings: {analyst_output.get('key_findings', [])}
        """

        self.analyst_collection.add(
            documents=[analyst_text],
            metadatas=[analyst_output],
            ids=[report_id],
        )
        
        print(f"[VectorMemory] Analyst report for {report_id} stored.")
    
    def store_visualization(self, report_id: str, visualizer_res: Dict[str, Any]) -> None:
        
        visualization_text = f"""
        Visualization Code Snippets: {', '.join(visualizer_res.get('plotly_code_snippets', []))}
        """

        self.visualization_collection.add(
            documents=[visualization_text],
            metadatas=[visualizer_res],
            ids=[report_id],
        )
        
        print(f"[VectorMemory] Visualization for report {report_id} stored.")
    
    def retrieve_relevant_data(self, query: str, collection_name: str , n_results : int = 1) -> List[Dict[str, Any]]:
        
        print(f"[VectorMemory] Retrieving relevant data for query: {query} from collection: {collection_name}")
        
        try:
            collection = self.client.get_collection(name=collection_name)
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            retrieved_data = []
            
            if results['metadatas'] and results['metadatas'][0]:
                 for metadata in results['metadatas'][0]:
                    retrieved_data.append(metadata)
            
            print(f"[VectorMemory] Retrieved {len(retrieved_data)} results from {collection_name}.")
            return retrieved_data
        except Exception as e:
            print(f"[VectorMemory] Error retrieving data: {e}")
            return [] 


def retrieve_interpreter_context(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
    return self.retrieve_relevant_data(query, "schema_collection", n_results)

def retrieve_wrangler_context(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
    return self.retrieve_relevant_data(query, "wrangling_collection", n_results)

def retrieve_analyst_context(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
    return self.retrieve_relevant_data(query, "analyst_collection", n_results)

def retrieve_visualizer_context(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
    return self.retrieve_relevant_data(query, "visualization_collection", n_results)

vector_memory = VectorMemory()