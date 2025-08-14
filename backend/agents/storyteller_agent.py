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
    
    
    