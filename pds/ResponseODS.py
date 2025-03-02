from pydantic import BaseModel, Field
from typing import List

class ResponseODS(BaseModel):
    """
    Output Data Schema for ResponseChain
    """

    cleaned_query: str = Field(..., title="Cleaned Query", description="the normalized and cleaned version of the query.")