import json
import re
from typing import Dict, List, Any
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field

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