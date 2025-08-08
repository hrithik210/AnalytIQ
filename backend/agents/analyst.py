import pandas as pd
import re
import json
from typing import Dict , Any, Union
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from data_interpreter import DataInterpreter
from wrangler_agent import DataWranglerAgent
import os
from dotenv import load_dotenv
import sys
import asyncio
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict


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
    descriptive_stats: Dict[str, NumericStats] = Field(..., description="Dictionary mapping column names to their descriptive statistics for numeric columns")
    trends: List[str] = Field(..., description="List of identified trends, patterns, and insights from the data analysis")
    correlation: List[tuple[str, str, float]] = Field(..., description="List of correlations between columns as tuples of (column1, column2, correlation_coefficient)")
    outliers: List[Outlier] = Field(..., description="List of outliers detected in numeric columns with their details")
    data_summary: str = Field(..., description="Comprehensive summary of key insights, patterns, and findings from the dataset analysis")

class Analyst:
    def __init__(self):
        self.model_client = OpenAIChatCompletionClient(
            model="gemini-2.5-flash",
            api_key=GEMINI_API_KEY,
        ) 
        
        self.schema_json = json.dumps(AnalystOutput.model_json_schema())
        
        self.system_message = f"""You are a senior data analyst. Your job is to:
        - Run descriptive statistics on numeric data
        - Identify trends, correlations, and patterns
        - Use the interpreter's schema and suggested analysis to guide your work

        You must output a JSON object that conforms exactly to this schema:
        {self.schema_json}

        Rules:
        1. Focus on **numeric columns** for descriptive statistics and correlations.
        2. For **categorical data**, analyze distributions and trends (e.g., "Category A: 40% of total").
        3. Use **contextual hints** (e.g., 'suggested_analysis') to prioritize and guide your analysis.
        4. If the dataset contains **time-series data**, analyze trends over time (e.g., growth rates, seasonality).
        5. For **hierarchical data**, analyze group-level summaries and patterns (e.g., by region, department).
        6. Identify and report **outliers** in numeric data using statistical methods (e.g., IQR, z-scores).
        7. Ensure all findings are **data-driven** and avoid assumptions or invented data.
        8. Always include a **summary** of key insights and patterns in the dataset.
        9. Output **only valid JSON** that conforms to the provided schema.
        10. Ensure the analysis is **reproducible** and can be validated by others.
        """
        
        self.agent = AssistantAgent(
            name="Analyst",
            model_client=self.model_client,
            system_message=self.system_message,
        )


    async def run_analysis(self , csv_path : str):
        
        ## running interpreter
        interpreter = DataInterpreter()
        wrangler = DataWranglerAgent()
        
        interpreter_res = await interpreter.analyze(csv_path)
        wrangler_res = await wrangler.wrangle(csv_path)
        

        
        interpreter_dict = interpreter_res.model_dump()

        
        user_message = f"""
        Analyze this dataset: {wrangler_res['cleaned_csv_path']}.

        INTERPRETER OUTPUT:
        {json.dumps(interpreter_dict, indent=2)}
        
        WRANGLER_OUTPUT:
        {json.dumps(wrangler_res['wrangling_report'], indent=2)}

        Your task:
        1. Use 'suggested_analysis' from interpreter to guide your work
        2. Run descriptive stats on numeric columns
        3. Analyze categorical trends (e.g., deal stages, lead sources)
        4. Identify any patterns or outliers
        5. Output in the required JSON format
        
        IMPORTANT: Always include the 'descriptive_stats' field even if empty. Ensure your response is ONLY valid JSON.
        """
        
        ##llm response
        response = await self.agent.run(task = user_message)
        
        response_text = response.messages[-1].content.strip()
        
        json_match = re.search(r'```json\s*\n(.*?)\n```', response_text, re.DOTALL)
        
        if json_match:
            json_content = json_match.group(1)
        else:
            # Try to find JSON without markdown wrapper
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_content = json_match.group(0)
            else:
                json_content = response_text
    
        try:
            parsed = AnalystOutput.model_validate_json(json_content)

            print(f"Analyst output : {json.dumps(parsed.model_dump(), indent=2)}")
        except ValidationError as e:
            raise ValueError(f"LLM output validation failed: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in response: {e}")

        return parsed

if __name__ == "__main__":
    

    async def main():
        if len(sys.argv) < 2:
            print("Usage: python data_interpreter.py <path_to_csv>")
            return

        csv_path = sys.argv[1]
        analyst_agent = Analyst()
        try:
            result = await analyst_agent.run_analysis(csv_path)
            print(f"Analyst output : {json.dumps(result.model_dump(), indent=2)}")
        except Exception as e:
            print(f"Error: {e}")

    asyncio.run(main())
