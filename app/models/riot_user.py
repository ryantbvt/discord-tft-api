''' Riot User Model '''

from pydantic import BaseModel

class RiotUser(BaseModel):
    username: str
    tag_line: str
