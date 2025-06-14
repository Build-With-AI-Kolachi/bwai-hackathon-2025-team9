from pydantic import BaseModel, Field, validator
from typing import List, Dict

# class ResercherODS(BaseModel):
#     """
#     Output Data Schema for Orchestration Chain - Context Extraction
#     """

#     context: str = Field(..., title="Context", description="Extracted Context")
#     # intents: List[str] = Field(..., title="Intents", description=" the list of identified intents.")
#     # is_legal: bool = Field({}, title="Is Legal", description="Boolean indicating whether a query is legal or not.")

class AnalystODS(BaseModel):
    """
    Output Data Schema for Orchestration Chain - Context Analysis
    """
    answer: str = Field(..., title="Answer", description="Answer to the query")

class AnalysisODS(BaseModel):
    """
    Output Data Schema for Orchestration Chain - Analysis
    """
    main_principle: str = Field(..., title="Main Principle", description="The main principle derived from the analysis. Note: should follow json formatting.")
    points: List[Dict[str, str]] = Field(..., title="Points", description="List of points with principles and sections. Note: should follow json formatting.")


class VerifierODS(BaseModel):
    """
    Output Data Schema for Orchestration Chain - Context Interpretation Verification
    """
    analysis: List[AnalysisODS] = Field(..., title="Analysis", description="Dict of Detailed analysis provided by the verifier. Note: should follow json formatting.")
