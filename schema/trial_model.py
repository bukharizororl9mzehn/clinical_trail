from pydantic import BaseModel
from typing import List

class TrialInfo(BaseModel):
    title: str
    condition: str
    phase: str
    study_type: str
    inclusion_criteria: List[str]
    exclusion_criteria: List[str]
