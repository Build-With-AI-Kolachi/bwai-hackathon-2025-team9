from pydantic import BaseModel, Field
from typing import List

class AnalysisODS(BaseModel):
    """
    Output Data Schema for AnalysisChain - Domain Classification
    """

    domain: str = Field(..., title="Domain", description="classified domain of the query. Note: should follow json formatting.")
    sub_category: str = Field(..., title="Doamin", description="the identified sub category. Note should follow json formatting.")
    priority: str = Field(..., title="Priority", description="the identified priority level. Note should follow json formatting.")
    # intents: List[str] = Field(..., title="Intents", description=" the list of identified intents.")
    # is_legal: bool = Field({}, title="Is Legal", description="Boolean indicating whether a query is legal or not.")