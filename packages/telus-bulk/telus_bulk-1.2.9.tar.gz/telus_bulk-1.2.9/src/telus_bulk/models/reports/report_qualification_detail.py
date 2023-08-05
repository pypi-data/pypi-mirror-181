from typing import List, Optional, Any
from datetime import datetime
from fastapi_camelcase import CamelModel
from google.cloud.firestore_v1 import DocumentReference


class ReportQualification(CamelModel):
    csq_id: Optional[str] = None
    product_type: str
    created_at: Optional[datetime | str | Any] = None
    address: List[Any]  # DocumentReference can not be used as type
