from pydantic import BaseModel, Field
from typing import List

class ValidationODS(BaseModel):
    """
    Output Data Schema for ValiationChain
    """

    is_true: bool = Field(..., title="Is True", description="Boolean indicating whether the conition is true. Note: should follow json formatting")