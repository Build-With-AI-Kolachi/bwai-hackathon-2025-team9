from pydantic import BaseModel, Field
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
    interpretation: str = Field(..., title="Interpretation", description="Interpretation of the context")
    references: List[str] = Field(..., title="References", description="List of references related to the context")

class AnalysisODS(BaseModel):
    """
    Output Data Schema for Orchestration Chain - Analysis
    """
    main_principle: str = Field(..., title="Main Principle", description="The main principle derived from the analysis.")
    points: List[Dict[str, str]] = Field(..., title="Points", description="List of points with principles and sections.")

class VerifierODS(BaseModel):
    """
    Output Data Schema for Orchestration Chain - Context Interpretation Verification
    """
    analysis: Dict[str,AnalysisODS] = Field(..., title="Analysis", description="Dict of Detailed analysis provided by the verifier.")
