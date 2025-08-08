import pandas as pd
import json
import re
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict
load_dotenv()


class DataInterpreterOutput(BaseModel):
    schema_summary: str = Field(..., description="Concise 2-sentence overview of the dataset")
    key_questions: List[str] = Field(..., description="Questions for clarification")
    data_types: Dict[str, str] = Field(..., description="Column name to type mapping")
    missing_values: Dict[str, int] = Field(..., description="NaN counts per column")
    suggested_analysis: List[str] = Field(..., description="Analysis types like trend_analysis, outlier_detection")

GEMINI_API_KEY = os.getenv("GEMINI_API")


import asyncio

# async def main():
#     response = await model_client.create([UserMessage(content="how does autogen work?", source="user")])
#     print(response)
#     await model_client.close()

# asyncio.run(main())


class DataInterpreter:
    def __init__(self):
        self.model_client = OpenAIChatCompletionClient(
            model="gemini-2.5-flash",
            api_key=GEMINI_API_KEY,
        ) 
        
        self.schema_json = DataInterpreterOutput.model_json_schema()
        field_descriptions = "\n".join(
            f"- {name}: {field.description}" 
            for name, field in DataInterpreterOutput.model_fields.items()
        )
        
        self.system_message = f"""
            You are a world-class CSV schema analyst.

            You must output **only** JSON that matches the schema below.

            FIELD REQUIREMENTS:
            {field_descriptions}

            JSON SCHEMA:
            {json.dumps(self.schema_json, indent=2)}

            Rules:
            1. Output only JSON.
            2. All fields are required and types must match exactly.
            3. Never add commentary.
            4. NEVER add extra fields or explanations
            5. For missing_values, count NaN/empty values per column
            6. Suggest 2-3 analysis types based on data patterns
            7. If timestamp column exists, add "time_series" to suggested_analysis
            8. Output ONLY valid JSON
        """
        
        self.agent = AssistantAgent(
            name='Interpreter',
            model_client=self.model_client,
            system_message=self.system_message
        )
    
    async def analyze(self , csv_path : str) -> DataInterpreterOutput:
        df = pd.read_csv(csv_path)
        
        context =  {
        "dataset_info": {
            "file_name": os.path.basename(csv_path),
            "shape": {"rows": len(df), "columns": len(df.columns)},
            "size_estimate_mb": round(os.path.getsize(csv_path) / (1024 * 1024), 2)
        },
        
        "columns": {
            "names": list(df.columns),
            "count": len(df.columns),
            # Structural hints (not analysis)
            "potential_identifiers": [
                col for col in df.columns 
                if any(keyword in col.lower() for keyword in ['id', 'key', 'index', 'uuid', 'code'])
            ],
            "potential_timestamps": [
                col for col in df.columns 
                if any(keyword in col.lower() for keyword in ['date', 'time', 'timestamp', 'created', 'updated', 'modified'])
            ],
            "potential_categorial": [
                col for col in df.columns 
                if df[col].dtype == 'object' and df[col].nunique() < 50  # Just flag, don't analyze
            ],
            "potential_numerical": [
                col for col in df.columns 
                if pd.api.types.is_numeric_dtype(df[col])
            ]
        },
        
        "data_quality": {
            "missing_values": df.isnull().sum().to_dict(),
            "missing_percentage": (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
            "duplicate_rows": int(df.duplicated().sum()),
            "duplicate_percentage": round(df.duplicated().sum() / len(df) * 100, 2)
        },
        
        "data_types": {
            "per_column": df.dtypes.apply(lambda x: str(x)).to_dict(),
            "category": "numeric" if len(df.select_dtypes(include=['number']).columns) > len(df.columns)/2 else "mixed"
        },
        
        "sample_data": {
            "first_3_rows": df.head(3).to_dict(),
            "random_sample": df.sample(min(2, len(df))).to_dict() if len(df) > 3 else None
        },
        
        "data_patterns": {
            "has_time_series_potential": any(
                keyword in ' '.join(df.columns).lower() 
                for keyword in ['date', 'time', 'daily', 'monthly', 'yearly']
            ),
            "has_geographical_data": any(
                geo_term in ' '.join(df.columns).lower()
                for geo_term in ['lat', 'lon', 'city', 'country', 'state', 'province', 'zip', 'postal', 'address']
            ),
            "has_financial_data": any(
                fin_term in ' '.join(df.columns).lower()
                for fin_term in ['price', 'cost', 'revenue', 'profit', 'amount', 'value', 'fee', 'charge', 'income', 'expense']
            ),
            "potential_target_indicators": [
                col for col in df.columns 
                if any(kw in col.lower() for kw in ['target', 'label', 'class', 'outcome', 'result', 'status', 'flag'])
            ]
        }
    }
        
        user_message = f"""
        Analyze this comprehensive CSV dataset structure:
        
        DATASET OVERVIEW:
        {json.dumps(context['dataset_info'], indent=2)}
        
        COLUMN ANALYSIS:
        {json.dumps(context['columns'], indent=2)}
        
        DATA QUALITY ASSESSMENT:
        {json.dumps(context['data_quality'], indent=2)}
        
        DATA TYPES & STRUCTURE:
        {json.dumps(context['data_types'], indent=2)}
        
        DATA PATTERNS DETECTED:
        {json.dumps(context['data_patterns'], indent=2)}
        
        SAMPLE DATA:
        {json.dumps(context['sample_data'], indent=2)}
        
        Based on this comprehensive analysis, provide your expert assessment in the required JSON format.
        Consider the data quality, patterns, potential use cases, and recommended analysis approaches.
    """
        
        #agent response
        
        response = await self.agent.run(task=user_message)
        
  
        response_text = response.messages[-1].content.strip()
        
        # # Write response to a text file
        # with open('agent_response.txt', 'w') as f:
        #     f.write(response_text)
        

        # Extract JSON from markdown code blocks if present
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
            parsed = DataInterpreterOutput.model_validate_json(json_content)
            
            print(json.dumps(parsed.model_dump(), indent=2))
        except ValidationError as e:
            raise ValueError(f"LLM output validation failed: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in response: {e}")

        return parsed
    
    


if __name__ == "__main__":
    import sys

    async def main():
        if len(sys.argv) < 2:
            print("Usage: python data_interpreter.py <path_to_csv>")
            return

        csv_path = sys.argv[1]
        interpreter = DataInterpreter()
        try:
            result = await interpreter.analyze(csv_path)
            print(json.dumps(result.model_dump(), indent=2))
        except Exception as e:
            print(f"Error: {e}")

    asyncio.run(main())