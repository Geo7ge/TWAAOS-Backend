from fastapi import APIRouter, HTTPException, status

from schemas.event_sponsor import (
    EventSponsorCreate,
    EventSponsorUpdate,
    EventSponsorResponse
)
from services.event_sponsor_service import EventSponsorService

router = APIRouter(prefix="/event-sponsors", tags=["event_sponsors"])


# ✅ CREATE
@router.post("/", response_model=EventSponsorResponse, status_code=201)
def create_event_sponsor(data: EventSponsorCreate):
    es = EventSponsorService.create_event_sponsor(data)

    if not es:
        raise HTTPException(status_code=400, detail="Could not create relation")

    return es


# ✅ GET ALL
@router.get("/", response_model=list[EventSponsorResponse])
def get_all():
    return EventSponsorService.get_all()


# ✅ GET BY ID
@router.get("/{es_id}", response_model=EventSponsorResponse)
def get_by_id(es_id: int):
    es = EventSponsorService.get_by_id(es_id)

    if not es:
        raise HTTPException(status_code=404, detail="Not found")

    return es


# ✅ GET BY EVENT ID
@router.get("/event/{event_id}", response_model=list[EventSponsorResponse])
def get_by_event(event_id: int):
    return EventSponsorService.get_by_event_id(event_id)


# ✅ GET BY SPONSOR ID
@router.get("/sponsor/{sponsor_id}", response_model=list[EventSponsorResponse])
def get_by_sponsor(sponsor_id: int):
    return EventSponsorService.get_by_sponsor_id(sponsor_id)


# ✅ UPDATE
@router.put("/{es_id}", response_model=EventSponsorResponse)
def update(es_id: int, data: EventSponsorUpdate):
    es = EventSponsorService.update_event_sponsor(es_id, data)

    if not es:
        raise HTTPException(status_code=404, detail="Not found")

    return es


# ✅ DELETE
@router.delete("/{es_id}", status_code=204)
def delete(es_id: int):
    success = EventSponsorService.delete_event_sponsor(es_id)

    if not success:
        raise HTTPException(status_code=404, detail="Not found")

    return