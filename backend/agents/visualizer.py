import re
import pandas as pd
import json
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv
import sys
import asyncio
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict , Any

load_dotenv()

GEMINI_API_KEY= os.getenv("GEMINI_API")

class ChartRecommendation(BaseModel):
    """Represents a single chart recommendation."""
    chart_type: str = Field(..., description="Type of chart recommended (e.g., 'bar', 'line', 'scatter')")
    reason: str = Field(..., description="Reason for recommending this chart type")
    data_columns: List[str] = Field(..., description="List of column names to be used in the chart")
    title: str = Field(..., description="Suggested title for the chart")

class VisualizationOutput(BaseModel):
    """Structured output for the Visualizer Agent."""
    chart_recommendations: List[ChartRecommendation] = Field(
        ..., 
        description="List of recommended charts based on analysis"
    )
    plotly_code_snippets: List[str] = Field(
        ..., 
        description="List of Python code snippets using Plotly to generate the recommended charts"
    )
    strict : bool = Field(
        True,
        description="If True, the agent will strictly follow the schema and rules without deviations."
    )
    
    
class Visualizer:
    def __init__(self):
        self.model_client = OpenAIChatCompletionClient(
            model="gemini-2.5-flash",
            api_key=GEMINI_API_KEY,
        ) 
        
        self.schema_json  = json.dumps(VisualizationOutput.model_json_schema(), indent=2)
        
        
        self.system_message = f"""
        You are a senior data visualization expert. Your task is to analyze the provided data analysis report and recommend appropriate charts, along with Python code to generate them using Plotly Express.

        You MUST produce a JSON response that strictly conforms to the following schema:
        {self.schema_json}

        **Instructions:**
        1.  Analyze the 'descriptive_stats', 'trends', 'correlation', and 'outliers' from the Analyst's report.
        2.  Recommend 2-4 charts that best visualize the key findings.
        3.  For each chart:
            *   Specify the `chart_type` (e.g., 'bar', 'line', 'scatter', 'histogram', 'box').
            *   Provide a clear `reason` for choosing this chart based on the analysis.
            *   List the required `data_columns` from the original dataset.
            *   Suggest a descriptive `title`.
        4.  Generate a Python code snippet for each recommended chart using `plotly.express` (imported as `px`).
            *   Assume the cleaned DataFrame is available as `df`.
            *   The code should create the figure (e.g., `fig = px.bar(...)`) but does not need to call `fig.show()`.
            *   Handle potential issues like outliers if relevant (e.g., filtering before plotting).
            *   Code should be syntactically correct and executable.
            *   When using value_counts().reset_index(), the reset_index() creates columns with the original column name and 'count'. Use the actual column names, not 'index'.
            *   For value_counts operations, use .reset_index(name='Count') and reference the original column name directly.
            *   CRITICAL: Test your column references! When you do df['column'].value_counts().reset_index(name='Count'), the resulting DataFrame has columns [original_column_name, 'Count']. Use the original column name, NOT 'index'.
            *   Example: department_counts = df['Department'].value_counts().reset_index(name='Count') creates columns ['Department', 'Count'], so use x='Department', not x='index'.
        5.  Ensure the final output is ONLY the valid JSON object matching the schema. Do not include any markdown code block wrappers (like ```json) or extra text.
        """
        
        self.agent = AssistantAgent(
            name="Visualizer_agent",
            model_client= self.model_client,
            system_message=self.system_message
        )
        
    async def create_visualization(self, cleaned_csv_path: str ,analyst_output ):
            
            # Read the CSV file
            df = pd.read_csv(cleaned_csv_path)
            
            context = {
            "analyst_report": analyst_output,
            "dataset_sample": df.head(5).to_dict() if not df.empty else {},
            "available_columns": list(df.columns) if not df.empty else []
            }
            
            user_message = f"""
            Based on the following data analysis report and dataset context, recommend charts and generate Plotly code.

            ANALYST REPORT:
            {json.dumps(context['analyst_report'], indent=2)}

            DATASET CONTEXT (Sample):
            {json.dumps(context['dataset_sample'], indent=2)}

            AVAILABLE COLUMNS:
            {json.dumps(context['available_columns'], indent=2)}

            Please provide your recommendations and code in the specified JSON format.
            """
            
            print("🔍 Visualizer Agent: Generating chart recommendations and code...")
            response = await self.agent.run(task=user_message)
            
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
                parsed = VisualizationOutput.model_validate_json(json_content)
                print(f"Visualizer output: {json.dumps(parsed.model_dump(), indent=2)}")
                return parsed
            except ValidationError as e:
                raise ValueError(f"LLM output validation failed: {e}")
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format in response: {e}")


if __name__ == "__main__":
    
    async def main():
        if len(sys.argv) < 2:
            print("Usage: python visualizer.py <path_to_csv>")
            return

        csv_path = sys.argv[1]
        visualizer = Visualizer()
        try:
            result = await visualizer.create_visualization(csv_path)
            # Note: create_visualization doesn't currently return anything
            # so this will print None unless you update the method to return something
            if result:
                print(f"Visualizer output: {json.dumps(result.model_dump(), indent=2)}")
        except Exception as e:
            print(f"Error: {e}")

    asyncio.run(main())
