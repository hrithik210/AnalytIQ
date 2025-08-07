import pandas as pd
import json
import re
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from data_interpreter import DataInterpreter

GEMINI_API_KEY= os.getenv("GEMINI_API")

class DataWranglerAgent():
    def __init__(self):
        self.model_client = OpenAIChatCompletionClient(
            model="gemini-2.5-flash",
            api_key=GEMINI_API_KEY,
        )  
        
        self.system_message = """
You are a senior data engineer responsible for preparing raw data for analysis. 
Your job is to perform comprehensive data wrangling with full auditability.

OUTPUT STRICTLY IN THIS JSON FORMAT:
{
    "audit_log": [
        {"step": 1, "action": "Schema validation", "details": "All required columns present"},
        {"step": 2, "action": "Missing data handling", "details": "Filled 'age' with median (15 values)"}
    ],
    "schema_validation": {
        "status": "valid",
        "missing_columns": [],
        "type_mismatches": {"revenue": "expected: float, found: str"}
    },
    "missing_data": {
        "summary": {"column_a": {"missing_count": 5, "strategy": "filled with median"}},
        "total_rows_dropped": 0
    },
    "data_types": {
        "converted": {"date": "datetime", "revenue": "float"},
        "invalid_values_handled": {"revenue": ["$1,000" → 1000]}
    },
    "outliers": {
        "detected": {"revenue": {"count": 3, "percentage": 1.5}},
        "treatment": "flagged, not removed"
    },
    "deduplication": {
        "exact_duplicates_removed": 2,
        "partial_duplicates_checked": ["email"],
        "rows_after_cleaning": 98
    },
    "categorical_encoding": {
        "columns_encoded": [],
        "values_normalized": {"status": ["Active", "active", "ACTIVE"] → "active"}
    },
    "final_dataset_metrics": {
        "original_shape": [100, 14],
        "final_shape": [98, 14],
        "total_transformations": 6
    },
    "generated_code": "import pandas as pd\\ndef clean_data(df):\\n    df = df.copy()\\n    # Convert date\\n    df['date'] = pd.to_datetime(df['date'], errors='coerce')\\n    return df"
}

RULES:
1. NEVER make irreversible changes (e.g., dropping rows) without logging
2. For missing  suggest strategy but default to 'flag only' if ambiguous
3. Convert strings to numeric/datetime where possible
4. Normalize categorical values to lowercase
5. Detect outliers using IQR (Q1 - 1.5*IQR, Q3 + 1.5*IQR)
6. Drop exact duplicates only
7. Output ONLY valid JSON
8. Include every transformation in audit_log
"""
        self.agent = AssistantAgent(
            name="DataWrangler",
            model_client=self.model_client,
            system_message=self.system_message
        )
        
    
    async def wrangle(self , csv_path : str):
        
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
        {json.dumps(context, indent=2)}

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
        json_match = re.search(r'\{[\s\S]*\}', response.messages[-1].content)
        
        if not json_match:
            raise ValueError("failed to parse json")
        
        result = json.loads(json_match.group())
        print("Data wrangler output")
        print(json.dumps(result, indent=2))
        
        try:
            # Print the generated code for debugging
            print("Generated code to execute:")
            print(result['generated_code'])
            print("-" * 50)
            
            local_scope = {'pd': pd}  # Make pandas available in the local scope
            exec(result['generated_code'], globals(), local_scope)
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
        result["final_dataset_metrics"] = {
            "original_shape": list(original_shape),
            "final_shape": list(df_cleaned.shape),
            "total_transformations": len(result["audit_log"]),
            "rows_removed": original_shape[0] - df_cleaned.shape[0],
            "actual_duplicates_removed": original_shape[0] - df_cleaned.shape[0] if 'deduplication' in str(result["audit_log"]) else 0
        }
        
        return {
            "cleaned_csv_path": cleaned_path_csv,
            "wrangling_report": result,
            "cleaned_sample": df_cleaned.head(3).to_dict(),
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
        try:
            result = await wrangler.wrangle(csv_path)
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Error: {e}")

    asyncio.run(main())