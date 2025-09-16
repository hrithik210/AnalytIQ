import json
import re
from pydantic import BaseModel, Field, ValidationError
from typing import List,Dict, Any, Optional
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API")



class StorytellerOutput(BaseModel):
    executive_summary: str = Field(
        ..., 
        description="A high-level, concise summary of the entire analysis, suitable for executives."
    )
    key_findings: List[str] = Field(
        ..., 
        description="A list of the most important findings from the data analysis."
    )
    data_overview: str = Field(
        ..., 
        description="A description of the dataset itself (size, columns, etc.) based on the interpreter's findings."
    )
    analysis_narrative: str = Field(
        ..., 
        description="A detailed narrative explaining the analysis performed, the trends found, and their significance."
    )
    visualizations_summary: str = Field(
        ..., 
        description="A summary of the recommended visualizations and what insights they provide."
    )
    qa_considerations: Optional[str] = Field(
        None, 
        description="A note on any significant QA findings that might affect the interpretation of the results."
    )
    conclusion: str = Field(
        ..., 
        description="A concluding statement summarizing the implications of the findings."
    )
    strict : bool = Field(
        True,
        description="If True, the agent will strictly follow the schema and rules without deviations."
    )
    

class StoryTeller:
    def __init__(self):
        self.model_client = OpenAIChatCompletionClient(
            model="gemini-2.5-flash",
            api_key=GEMINI_API_KEY
        )
        
        self.schema_json = json.dumps(StorytellerOutput.model_json_schema() , indent=2)
        
        self.system_message = f"""
        You are a skilled data science communicator. Your task is to transform the technical outputs from a data analysis pipeline into a clear, engaging, and insightful narrative report.

        You MUST produce a JSON response that strictly conforms to the following schema:
        {self.schema_json}

        **Instructions:**
        1.  **Executive Summary:** Write a concise paragraph summarizing the dataset, the main analytical goals, the key findings, and the primary implications. Aim for 3-4 sentences.
        2.  **Key Findings:** List 4-6 of the most significant and actionable insights discovered in the analysis. Be specific and data-driven.
        3.  **Data Overview:** Describe the dataset based on the Interpreter's findings (size, columns, data types, quality). What does this data represent?
        4.  **Analysis Narrative:** Provide a detailed explanation of the analysis process and findings:
            *   What descriptive statistics were key?
            *   What major trends or patterns were identified by the Analyst?
            *   What notable correlations or outliers were found?
            *   Explain the significance of these findings in context.
        5.  **Visualizations Summary:** Summarize the charts recommended by the Visualizer. Explain what each chart type is best suited to show and why it's useful for understanding the data.
        6.  **QA Considerations (Optional but important):** Briefly mention any 'Warning' or 'Fail' status items from the QA report that could impact the interpretation of the results. If the QA report is 'Good', you can state that.
        7.  **Conclusion:** Conclude with the broader implications of the findings. What should the reader take away? What might be the next steps or areas for further investigation?

        **Rules:**
        *   Write in clear, professional, yet engaging English.
        *   Avoid jargon; explain technical terms if necessary.
        *   Be objective and data-driven.
        *   Ensure the final output is ONLY the valid JSON object matching the schema. Do not include any markdown code block wrappers (like ```json) or extra text.
        """
        
        self.agent = AssistantAgent(
            name = "Storyteller",
            model_client=self.model_client,
            system_message=self.system_message
        )

    async def createNarrative(
        self,
        interpreter_output : Dict[str, Any],
        analyst_output : Dict[str, Any],
        visualizer_output : Dict[str, Any],
        qa_report : Dict[str, Any],
        retrieved_context: Optional[Dict[str, List[str]]] = None
    ) -> StorytellerOutput:
        
        context = {
            "interpreter_output" : interpreter_output,
            "analyst_output" : analyst_output,
            "visualizer_output" : visualizer_output,
            "qa_report" : qa_report
        }
        rag_text = "\n\n".join(sum((retrieved_context.values() if retrieved_context else []), [])) if retrieved_context else ""
        
        user_message = f"""
        Create a compelling narrative report based on the following data analysis outputs.

        ANALYSIS CONTEXT:
        {json.dumps(context, indent=2)}

        RETRIEVED CONTEXT:
        {rag_text}

        Please provide your comprehensive narrative report in the specified JSON format.
        """
        
        print("✍️ Storyteller Agent: Crafting the narrative...")
        
        response = await self.agent.run(task=user_message)
        
        response_text = response.messages[-1].content.strip()
        
        json_match = re.search(r"```json\s*\n(.*?)\n```" , response_text, re.DOTALL)
        
        if json_match:
            json_content = json_match.group(1)
        else:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_content = json_match.group(0)
            else:
                json_content = response_text
        
        try:
            parsed = StorytellerOutput.model_validate_json(json_content)
        except ValidationError as e:
            raise ValueError(f"validation failed from llm : {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"invalid json format in response  : {e}")  
        
        return parsed