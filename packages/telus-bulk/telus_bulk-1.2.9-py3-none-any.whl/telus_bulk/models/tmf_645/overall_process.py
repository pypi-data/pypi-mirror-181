from datetime import datetime
from enum import Enum
from typing import Any, Optional

from fastapi_camelcase import CamelModel


class OverallProcessorType(Enum):
    """
    Statis for locations objects in over_all_process collection
    """

    QUICK = "quick"
    FULL = "full"

    def __str__(self) -> str:
        return str(self.value)


class OverallProcessStatus(Enum):
    """
    Statis for locations objects in over_all_process collection
    """

    PENDING = "pending"
    SENT = "sent"
    DONE = "done"
    PROCESSING = "processing"

    def __str__(self) -> str:
        return str(self.value)


class OverallProcess(CamelModel):
    """
    docstring
    """

    location: Optional[str] = None
    status: Optional[str] = OverallProcessStatus.PENDING.value
    csq_id: Optional[str] = None
    csq_ref: Optional[str] = None
    id: Optional[str] = None
    created_at = datetime.now()


OverallProcess.update_forward_refs()


class OverallData(CamelModel):
    """
    docstring
    """

    location_id: Optional[str] = None
    location_obj: Optional[dict] = None
    partner: Optional[str] = None
    to_whom: Optional[str] = None
    offers: Optional[list[dict]] = []
    csq_id: Optional[str] = None
    csq_ref: Optional[str] = None
    id: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime | Any] = None
    updated_at: Optional[str | Any] = None
    created_at_fancy: Optional[str | Any] = None
    updated_at_fancy: Optional[str | Any] = None
    processor_type: Optional[str] = None


OverallData.update_forward_refs()
