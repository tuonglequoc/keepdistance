from pydantic import BaseModel, Field


class CinemaRoomModel(BaseModel):
    height: int = Field(..., gt=0)
    width: int = Field(..., gt=0)
    min_distance: int = Field(1, gt=0)