import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from ..containers import ApplicationContainer
from ..services.mediacollectionservice import MediacollectionService

logger = logging.getLogger(__name__)
mediacollection_router = APIRouter(
    prefix="/mediacollection",
    tags=["mediacollection"],
)


@mediacollection_router.get("/getitems")
@inject
def api_getitems(
    mediacollection_service: MediacollectionService = Depends(
        Provide[ApplicationContainer.services.mediacollection_service]
    ),
):
    try:
        return mediacollection_service.db_get_images_as_dict()
    except Exception as exc:
        logger.exception(exc)
        raise HTTPException(status_code=500, detail=f"something went wrong, Exception: {exc}") from exc


@mediacollection_router.get("/delete", status_code=status.HTTP_204_NO_CONTENT)
@inject
def api_gallery_delete(
    image_id: str,
    mediacollection_service: MediacollectionService = Depends(
        Provide[ApplicationContainer.services.mediacollection_service]
    ),
):
    logger.info(f"gallery_delete requested, id={image_id}")
    try:
        mediacollection_service.delete_image_by_id(image_id)
    except Exception as exc:
        logger.exception(exc)
        raise HTTPException(500, f"deleting failed: {exc}") from exc


@mediacollection_router.get("/delete_all", status_code=status.HTTP_204_NO_CONTENT)
@inject
def api_gallery_delete_all(
    mediacollection_service: MediacollectionService = Depends(
        Provide[ApplicationContainer.services.mediacollection_service]
    ),
):
    """Warning: deletes all files permanently without any further confirmation

    Raises:
        HTTPException: _description_
    """
    logger.info("delete_all media items requested")
    try:
        mediacollection_service.delete_images()
        logger.info("all media successfully deleted")
    except Exception as exc:
        logger.exception(exc)
        raise HTTPException(500, f"deleting all media items failed: {exc}") from exc
