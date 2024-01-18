from pydantic import BaseModel
from typing import List, Optional


from pydantic import BaseModel
from typing import Optional, List, Any


class Job(BaseModel):
    url_msg_id: Optional[str] = None
    thumbnail_url: str
    streams: List[Any]
    title: str
    video_id: str
