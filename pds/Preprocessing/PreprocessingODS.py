from pydantic import BaseModel, Field
from typing import List

class PreprocessingODS(BaseModel):
    """
    Output Data Schema for PreprocessingChain
    """

    cleaned_query: str = Field(..., title="Cleaned Query", description="the normalized and cleaned version of the query. Note: should follow json formatting.")
    # intents: List[str] = Field(..., title="Intents", description=" the list of identified intents.")
    # is_legal: bool = Field({}, title="Is Legal", description="Boolean indicating whether a query is legal or not.")