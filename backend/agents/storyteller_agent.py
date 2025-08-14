import json
import re
from pydantic import BaseModel, Field, ValidationError
from typing import List,Dict, Any, Optional

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