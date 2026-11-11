from pydantic import BaseModel, ConfigDict
import datetime


class User(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    create_at: datetime.datetime