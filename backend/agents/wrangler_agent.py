import pandas as pd
import numpy as np
import json
import re
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from data_interpreter import DataInterpreter
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict

GEMINI_API_KEY= os.getenv("GEMINI_API")


class AuditLogEntry(BaseModel):
    step: int
    action: str
    details: str

class SchemaValidation(BaseModel):
    status: str
    missing_columns: List[str]
    type_mismatches: Dict[str, str]

class MissingData(BaseModel):
    summary: Dict[str, Dict[str, str | int]]
    total_rows_dropped: int

class DataTypes(BaseModel):
    converted: Dict[str, str]
    invalid_values_handled: Dict[str, List[str]]

class Outliers(BaseModel):
    detected: Dict[str, Dict[str, float]]
    treatment: str

class Deduplication(BaseModel):
    exact_duplicates_removed: int
    partial_duplicates_checked: List[str]
    rows_after_cleaning: int

class CategoricalEncoding(BaseModel):
    columns_encoded: List[str]
    values_normalized: Dict[str, str | List[str]]

class FinalDatasetMetrics(BaseModel):
    original_shape: List[int]
    final_shape: List[int]
    total_transformations: int

class DataWranglerOutput(BaseModel):
    audit_log: List[AuditLogEntry]
    schema_validation: SchemaValidation
    missing_data: MissingData
    data_types: DataTypes
    outliers: Outliers
    deduplication: Deduplication
    categorical_encoding: CategoricalEncoding
    final_dataset_metrics: FinalDatasetMetrics
    generated_code: str



class DataWranglerAgent():
    def __init__(self):
        self.model_client = OpenAIChatCompletionClient(
            model="gemini-2.5-flash",
            api_key=GEMINI_API_KEY,
        )  
        
        schema_json = json.dumps(DataWranglerOutput.model_json_schema(), indent=2)

        
        self.system_message = f"""
        You are a senior data engineer responsible for preparing raw data for analysis.
        Your job is to perform comprehensive data wrangling with full auditability.

        You must output a JSON object that conforms exactly to the following JSON schema:
        {schema_json}

        Rules:
        1. NEVER make irreversible changes without logging
        2. For missing values, suggest strategy but default to 'flag only' if ambiguous
        3. Convert strings to numeric/datetime where possible
        4. Normalize categorical values to lowercase
        5. Detect outliers using IQR
        6. Drop exact duplicates only
        7. Output ONLY valid JSON (no markdown, no commentary)
        8. Include every transformation in audit_log
        9. The generated_code MUST be a Python function named 'clean_data' that takes a DataFrame as input and returns the cleaned DataFrame
        10. Example generated_code format:
        ```
        def clean_data(df):
            # Your data cleaning code here
            # Apply transformations to df
            return df
        ```
        """
        
        self.agent = AssistantAgent(
            name="DataWrangler",
            model_client=self.model_client,
            system_message=self.system_message
        )
        
    
    async def wrangle(self , csv_path : str) -> Dict:
        
        df = pd.read_csv(csv_path)
        original_shape = df.shape
        
        interpreter = DataInterpreter()
        
        
        #getting context from interpreter
        context = await interpreter.analyze(csv_path)
        
        # Prepare dataset summary for the agent
        dataset_summary = {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.to_dict(),
            "sample_data": df.head(3).to_dict(),
            "null_counts": df.isnull().sum().to_dict(),
            "duplicate_count": df.duplicated().sum()
        }
        
        user_message = f"""
        Perform comprehensive data wrangling on this dataset.

        DATASET SUMMARY:
        {json.dumps(dataset_summary, indent=2, default=str)}

        CONTEXT FROM DATA INTERPRETER:
        {json.dumps(context.model_dump(), indent=2)}

        TASKS:
        1. SCHEMA VALIDATION: Verify columns and types
        2. MISSING DATA: Identify and suggest handling
        3. TYPE NORMALIZATION: Convert strings to datetime/numeric
        4. OUTLIER DETECTION: Use IQR method
        5. DEDUPLICATION: Remove exact duplicates
        6. CATEGORICAL NORMALIZATION: Lowercase values
        7. AUDIT TRAIL: Log every transformation

        Output in the required JSON format with generated_code.
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
            result = DataWranglerOutput.model_validate_json(json_content)
    
        except ValidationError as e:
            raise ValueError(f"LLM output validation failed: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in response: {e}")


        
        try:
            # Print the generated code for debugging
            print("Generated code to execute:")
            print(result.generated_code)
            print("-" * 50)
            
            local_scope = {'pd': pd, 'np': np}  # Make pandas available in the local scope
            exec(result.generated_code, globals(), local_scope)
            clean_data = local_scope.get('clean_data')
            if clean_data:
                print(f"Original DataFrame shape: {df.shape}")
                df_cleaned = clean_data(df)
                print(f"Cleaned DataFrame shape: {df_cleaned.shape}")
                
                # Verify the changes actually happened
                if df_cleaned.shape[0] != df.shape[0]:
                    print(f"Successfully removed {df.shape[0] - df_cleaned.shape[0]} rows")
                else:
                    print("Warning: No rows were actually removed despite claims in audit log")
            else:
                raise ValueError("clean_data function not found in generated code")
        except Exception as e:
            print(f"Code execution failed: {e}. Returning original df")
            df_cleaned = df.copy()
            
        ##saving cleaned csv
        base,ext = os.path.splitext(csv_path)
        cleaned_path_csv = f"{base}_cleaned{ext}"
        df_cleaned.to_csv(cleaned_path_csv , index=False)
        
        # Update the final dataset metrics with actual values
        result_dict = result.model_dump()
        result_dict["final_dataset_metrics"] = {
            "original_shape": list(original_shape),
            "final_shape": list(df_cleaned.shape),
            "total_transformations": len(result.audit_log),
            "rows_removed": original_shape[0] - df_cleaned.shape[0],
            "actual_duplicates_removed": original_shape[0] - df_cleaned.shape[0] if 'deduplication' in str(result.audit_log) else 0
        }
        
        # Convert DataFrame with potential Timestamp objects to JSON-serializable format
        cleaned_sample = df_cleaned.head(3).copy()
        for col in cleaned_sample.select_dtypes(include=['datetime64']).columns:
            cleaned_sample[col] = cleaned_sample[col].astype(str)
            
        return {
            "cleaned_csv_path": cleaned_path_csv,
            "wrangling_report": result_dict,
            "cleaned_sample": cleaned_sample.to_dict(),
            "original_shape": original_shape,
            "final_shape": df_cleaned.shape
        }

if __name__ == "__main__":
    import sys
    import asyncio
    async def main():
        if len(sys.argv) < 2:
            print("Usage: python data_interpreter.py <path_to_csv>")
            return

        csv_path = sys.argv[1]
        wrangler = DataWranglerAgent()
        def json_serialize(obj):
            if isinstance(obj, (pd.Timestamp, pd.DatetimeIndex)):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(obj, np.int64):
                return int(obj)
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
                
        try:
            result = await wrangler.wrangle(csv_path)
            print(f"final results of wrangler :", json.dumps(result, indent=2, default=json_serialize))
        except Exception as e:
            print(f"Error: {e}")

    asyncio.run(main())