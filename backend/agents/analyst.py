import pandas as pd
import re
import json
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv
import sys
import asyncio
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Union, Any, Optional


load_dotenv()

GEMINI_API_KEY= os.getenv("GEMINI_API")

class NumericStats(BaseModel):
	count: int = Field(..., description="Number of non-null entries in this column")
	mean: float = Field(..., description="Arithmetic mean of the column values")
	std: float = Field(..., description="Standard deviation of the column values")
	min: float = Field(..., description="Minimum value in the column")
	percent_25: float = Field(..., alias="25%", description="25th percentile value")
	percent_50: float = Field(..., alias="50%", description="Median (50th percentile) value")
	percent_75: float = Field(..., alias="75%", description="75th percentile value")
	max: float = Field(..., description="Maximum value in the column")
   
class Outlier(BaseModel):
	column: str = Field(..., description="Name of the column containing outliers")
	values: List[Union[int, float]] = Field(..., description="List of outlier values identified in the column")
	count: int = Field(..., description="Total number of outliers found in this column")
	


class AnalystOutput(BaseModel):
	cleaned_csv_path: str = Field(..., description="Path to the cleaned CSV file used for the analysis")
	descriptive_stats: Dict[str, NumericStats] = Field(..., description="Dictionary mapping column names to their descriptive statistics for numeric columns")
	trends: List[str] = Field(..., description="List of identified trends, patterns, and insights from the data analysis")
	correlation: List[tuple[str, str, float]] = Field(..., description="List of correlations between columns as tuples of (column1, column2, correlation_coefficient)")
	outliers: List[Outlier] = Field(..., description="List of outliers detected in numeric columns with their details")
	data_summary: str = Field(..., description="Comprehensive summary of key insights, patterns, and findings from the dataset analysis")
	strict : bool = Field(
		True,
		description="If True, the agent will strictly follow the schema and rules without deviations."
	)

class Analyst:
	def __init__(self):
		self.model_client = OpenAIChatCompletionClient(
			model="gemini-2.5-flash",
			api_key=GEMINI_API_KEY,
		) 
		
		self.schema_json = json.dumps(AnalystOutput.model_json_schema())
		
		self.system_message = f"""You are a senior data analyst. Instead of writing prose, you write robust, testable Python to analyze dataframes.
	Your job is to:
	- Compute descriptive statistics on numeric columns
	- Identify trends, correlations, and outliers
	- Produce a concise human-readable summary

	You must OUTPUT ONLY valid Python code that defines a single function:
	def analyze_data(df: pd.DataFrame) -> dict:
		"""Return a dict matching the following schema keys exactly"""
		return {{
			"descriptive_stats": <mapping of column -> dict(count, mean, std, min, 25%, 50%, 75%, max)>,
			"trends": <list[str]>,
			"correlation": <list[ [col1, col2, float] ]>,
			"outliers": <list[ {{"column": str, "values": list[float|int], "count": int}} ]>,
			"data_summary": <str>
		}}

	Rules:
	1. Do NOT import libraries; assume pandas and numpy are available as pd/np.
	2. Handle empty or non-numeric safely.
	3. For correlations, use Pearson on numeric columns; return only significant absolute values >= 0.3.
	4. Detect outliers per numeric column with IQR.
	5. Never print; no markdown; only pure Python code. No backticks.
	6. Do not read files; only work with the provided df.
	7. The returned dict MUST be JSON-serializable.
	"""
		
		self.agent = AssistantAgent(
			name="Analyst",
			model_client=self.model_client,
			system_message=self.system_message,
		)


	async def run_analysis(self , cleaned_csv_path : str , interpreter_dict : Dict[str , Any] , wrangling_report : Dict[str , Any], retrieved_context: Optional[Dict[str, List[str]]] = None) -> AnalystOutput:
		# Load but do not pass full df; create summary context instead
		df = pd.read_csv(cleaned_csv_path)
		dataset_summary = {
			"shape": df.shape,
			"columns": df.columns.tolist(),
			"dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
			"sample_rows": df.head(3).to_dict(),
		}
		rag_snippets = []
		if retrieved_context:
			for key in ["schema", "wrangler"]:
				rag_snippets.extend(retrieved_context.get(key, []))
		retrieved_text = "\n\n".join(rag_snippets[:6]) if rag_snippets else ""
		
		user_message = f"""
	Develop the analyze_data(df) function per the rules. Use the dataset summary and any retrieved context for guidance.

	DATASET SUMMARY:
	{json.dumps(dataset_summary, indent=2, default=str)}

	INTERPRETER OUTPUT (selected):
	{json.dumps({"suggested_analysis": interpreter_dict.get("suggested_analysis", []), "data_types": interpreter_dict.get("data_types", {})}, indent=2)}

	WRANGLER HINTS (high-level keys only):
	{json.dumps(list((wrangling_report or {{}}).keys()) if isinstance(wrangling_report, dict) else str(type(wrangling_report)), indent=2)}

	RETRIEVED CONTEXT:
	{retrieved_text}
	"""
		
		# Get code from LLM
		response = await self.agent.run(task = user_message)
		response_text = response.messages[-1].content.strip()
		
		# Extract Python code: since we instructed no markdown, take full content
		code_text = response_text
		
		try:
			local_scope: Dict[str, Any] = {"pd": pd}
			exec(code_text, {}, local_scope)
			analyze_data = local_scope.get("analyze_data")
			if not callable(analyze_data):
				raise ValueError("analyze_data function not found in generated code")
			raw_result = analyze_data(df)
			if not isinstance(raw_result, dict):
				raise ValueError("analyze_data did not return a dict")
			# Ensure cleaned_csv_path is present
			raw_result["cleaned_csv_path"] = cleaned_csv_path
			json_content = json.dumps(raw_result)
			parsed = AnalystOutput.model_validate_json(json_content)
			print(f"Analyst output : {json.dumps(parsed.model_dump(), indent=2)}")
			return parsed
		except Exception as e:
			raise ValueError(f"Failed to execute or validate analyst code: {e}")

if __name__ == "__main__":
	

	async def main():
		if len(sys.argv) < 2:
			print("Usage: python data_interpreter.py <path_to_csv>")
			return
		csv_path = sys.argv[1]
		analyst_agent = Analyst()
		try:
			result = await analyst_agent.run_analysis(csv_path, {}, {}, None)
			print(f"Analyst output : {json.dumps(result.model_dump(), indent=2)}")
		except Exception as e:
			print(f"Error: {e}")
	
	asyncio.run(main())
