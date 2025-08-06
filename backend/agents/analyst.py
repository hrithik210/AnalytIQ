import pandas as pd
import re
import json
from typing import Dict , Any
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from data_interpreter import DataInterpreter
import os
from dotenv import load_dotenv
import sys
import asyncio


GEMINI_API_KEY= os.getenv("GEMINI_API")

class Analyst:
    def __init__(self):
        self.model_client = OpenAIChatCompletionClient(
            model="gemini-2.5-flash",
            api_key=GEMINI_API_KEY,
        ) 
        
        self.system_message = """
        You are a senior data analyst. Your job is to:
        - Run descriptive statistics on numeric data
        - Identify trends, correlations, and patterns
        - Use the interpreter's schema and suggested analysis to guide your work
        - Output STRICTLY in this JSON format:

        {
            "descriptive_stats": {
                "numeric_column": {
                    "count": 100,
                    "mean": 50.5,
                    "std": 15.2,
                    "min": 10,
                    "25%": 40,
                    "50%": 50,
                    "75%": 60,
                    "max": 99
                }
            },
            "trends": [
                "Sales increased 15% monthly",
                "Q4 revenue 40% higher than Q1"
            ],
            "correlations": [
                ["ad_spend", "sales", 0.85]
            ],
            "outliers": [
                {"column": "revenue", "values": [9999], "count": 1}
            ],
            "data_summary": "3-sentence narrative summary of key findings"
        }

        Rules:
        1. ONLY analyze numeric columns for stats/correlations
        2. For categorical data, focus on distribution and trends (e.g., 'Source: 40% from LinkedIn')
        3. Use 'suggested_analysis' from interpreter to prioritize work (e.g., 'conversion_funnel_analysis')
        4. If 'Deal Stage' exists, analyze conversion rates
        5. Output ONLY valid JSON
        6. NEVER invent data not in the CSV
        """
        
        self.agent = AssistantAgent(
            name="Analyst",
            model_client=self.model_client,
            system_message=self.system_message
        )


    async def run_analysis(self , csv_path : str):
        df = pd.read_csv(csv_path)
        
        ## running interpreter
        interpreter = DataInterpreter()
        
        context = await interpreter.analyze(csv_path)
        
        
        user_message = f"""
        Analyze this dataset: {df} using the interpreter's insights.

        INTERPRETER OUTPUT:
        {json.dumps(context, indent=2)}
        

        Your task:
        1. Use 'suggested_analysis' to guide your work
        2. Run descriptive stats on numeric columns
        3. Analyze categorical trends (e.g., deal stages, lead sources)
        4. Identify any patterns or outliers
        5. Output in the required JSON format
        """
        
        ##llm response
        response = await self.agent.run(task = user_message)
        
        json_match = re.search(r'\{[\s\S]*\}', response.messages[-1].content)
        
        if not json_match:
            raise ValueError("failed to parse json")
        
        return json.loads(json_match.group())
    


if __name__ == "__main__":
    

    async def main():
        if len(sys.argv) < 2:
            print("Usage: python data_interpreter.py <path_to_csv>")
            return

        csv_path = sys.argv[1]
        analyst_agent = Analyst()
        try:
            result = await analyst_agent.run_analysis(csv_path)
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Error: {e}")

    asyncio.run(main())
        