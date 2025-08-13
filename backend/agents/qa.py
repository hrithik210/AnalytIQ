import json
import re
from typing import Dict, List, Any
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field,ValidationError

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API")


class QAReviewItem(BaseModel):
    agent : str = Field(... , description="Name of the agent being reviewed (e.g., 'Interpreter', 'Analyst')")
    check : str = Field(... , description="description of the check performed")
    status: str = Field(..., description="Result of the check ('Pass', 'Warning', 'Fail')")
    details: str = Field(..., description="Explanation of the finding or issue")
    
class QAOutput(BaseModel):
    overall_status : str = Field(... , description="Overall health of the analysis ('Good', 'Needs Review', 'Critical Issues')")
    review_items  : List[QAReviewItem] = Field(... , description="List of individual checks and their results")
    summary : str = Field(... , description="a concise summary of the QA findings")
    strict : bool = Field(
        True,
        description="If True, the agent will strictly follow the schema and rules without deviations."
    )
    
class QAAgent:
    def __init__(self):
        self.model_client = OpenAIChatCompletionClient(
            model="gemini-2.5-flash",
            api_key=GEMINI_API_KEY,
            
        )
        
        self.schema_json = json.dumps(QAOutput.model_json_schema() , indent=2)
        self.system_message = f"""
        You are a meticulous Quality Assurance expert for data analysis pipelines. Your task is to review the outputs of the Data Interpreter, Data Wrangler, Analyst, and Visualizer agents for correctness, consistency, and plausibility.

        You MUST produce a JSON response that strictly conforms to the following schema:
        {self.schema_json}

        **Instructions:**
        1.  Analyze the provided outputs from each agent.
        2.  Perform logical checks, such as:
            *   **Consistency:** Do column names/types mentioned in Interpreter match those in Wrangler/Analyst?
            *   **Plausibility:** Are the statistics (mean, min, max) reported by Analyst physically possible given the data sample?
            *   **Completeness:** Does Wrangler's audit log account for major transformations seen in the cleaned sample?
            *   **Logic:** Do the trends/correlations identified by Analyst align with the data descriptions?
            *   **Feasibility:** Can the charts recommended by Visualizer be created with the specified columns and data types?
        3.  For each check, create a `QAReviewItem` detailing the agent, the check, the `status` ('Pass', 'Warning', 'Fail'), and `details`.
        4.  Determine an `overall_status` based on the review items.
        5.  Provide a concise `summary` of your findings.
        6.  Ensure the final output is ONLY the valid JSON object matching the schema. Do not include any markdown code block wrappers (like ```json) or extra text.
        """
        
        self.agent = AssistantAgent(
            name = "QA",
            model_client=self.model_client,
            system_message=self.system_message
        )
    
    async def run_qa_review(
        self ,
        interpreter_output : Dict[str , Any] ,
        wrangler_output : Dict[str, Any] , 
        analyst_output : Dict[str, Any],
        visualizer_output: Dict[str, Any],
        cleaned_csv_sample: Dict[str, Any]):
        
        
        context = {
            "interpreter_output" : interpreter_output,
            "wrangler_output" : wrangler_output,
            "analyst_output" : analyst_output,
            "visualizer_output" : visualizer_output,
            "cleaned_data_sample" : cleaned_csv_sample 
        }
        
        user_message = f"""
        Please perform a quality assurance review on the following data analysis pipeline outputs.

        CONTEXT FOR REVIEW:
        {json.dumps(context, indent=2, default=str)}

        Please provide your detailed QA report in the specified JSON format.
        """
        
        print("🔍 QA Agent: Running review...")
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
            parsed = QAOutput.model_validate_json(json_content)
            
            print(json.dumps(parsed.model_dump(), indent=2))
        except ValidationError as e:
            raise ValueError(f"LLM output validation failed: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in response: {e}")

        return parsed