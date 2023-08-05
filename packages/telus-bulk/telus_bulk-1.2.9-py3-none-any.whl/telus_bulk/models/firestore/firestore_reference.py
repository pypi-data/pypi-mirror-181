from fastapi_camelcase import CamelModel
from typing import List
from loguru import logger
from google.cloud.firestore_v1.document import DocumentReference


class FirestoreReference(CamelModel):
    reference_id: str
    path: str


def manage_document_references(
    references: List[DocumentReference],
) -> List[FirestoreReference]:
    firestore_references: List[FirestoreReference] = []
    for ref in references:
        try:
            firestore_references.append(
                FirestoreReference.parse_obj(
                    {
                        "reference_id": ref.id,
                        "path": ref.path,
                    }
                )
            )
        except Exception:
            logger.warning("Invalid reference")
    return firestore_references
