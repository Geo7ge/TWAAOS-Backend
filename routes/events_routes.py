from fastapi import APIRouter, HTTPException, status
from schemas.events import (
    EventCreate,
    EventUpdate,
    EventResponse,
)
from services.events_service import EventService

router = APIRouter(prefix="/events", tags=["events"])


@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_event(event_data: EventCreate):
    """Create a new event"""
    event = EventService.create_event(event_data)

    if not event:
        raise HTTPException(
            status_code=400,
            detail="Could not create event",
        )

    return EventResponse(
        id=event["id"],
        title=event["title"],
        description=event.get("description"),
        start_time=event.get("start_time"),
        end_time=event.get("end_time"),
        location_id=event.get("location_id"),
        category_name=event.get("category_name"),
        organizer_id=event.get("organizer_id"),
        participation_type=event.get("participation_type"),
        registration_link=event.get("registration_link"),
        qr_code=event.get("qr_code"),
        max_participants=event.get("max_participants"),
        deadline=event.get("deadline"),
        created_at=event.get("created_at"),
    )


@router.get("/", response_model=list[EventResponse])
def get_events():
    """Get all events"""
    events = EventService.get_all_events()

    return [
        EventResponse(
            id=event["id"],
            title=event["title"],
            description=event.get("description"),
            start_time=event.get("start_time"),
            end_time=event.get("end_time"),
            location_id=event.get("location_id"),
            category_name=event.get("category_name"),
            organizer_id=event.get("organizer_id"),
            participation_type=event.get("participation_type"),
            registration_link=event.get("registration_link"),
            qr_code=event.get("qr_code"),
            max_participants=event.get("max_participants"),
            deadline=event.get("deadline"),
            created_at=event.get("created_at"),
        )
        for event in events
    ]


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int):
    """Get event by ID"""
    event = EventService.get_event_by_id(event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    return EventResponse(
        id=event["id"],
        title=event["title"],
        description=event.get("description"),
        start_time=event.get("start_time"),
        end_time=event.get("end_time"),
        location_id=event.get("location_id"),
        category_name=event.get("category_name"),
        organizer_id=event.get("organizer_id"),
        participation_type=event.get("participation_type"),
        registration_link=event.get("registration_link"),
        qr_code=event.get("qr_code"),
        max_participants=event.get("max_participants"),
        deadline=event.get("deadline"),
        created_at=event.get("created_at"),
    )


@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: int, event_data: EventUpdate):
    """Update event"""
    event = EventService.update_event(event_id, event_data)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    return EventResponse(
        id=event["id"],
        title=event["title"],
        description=event.get("description"),
        start_time=event.get("start_time"),
        end_time=event.get("end_time"),
        location_id=event.get("location_id"),
        category_name=event.get("category_name"),
        organizer_id=event.get("organizer_id"),
        participation_type=event.get("participation_type"),
        registration_link=event.get("registration_link"),
        qr_code=event.get("qr_code"),
        max_participants=event.get("max_participants"),
        deadline=event.get("deadline"),
        created_at=event.get("created_at"),
    )


@router.delete("/{event_id}")
def delete_event(event_id: int):
    """Delete event"""
    result = EventService.delete_event(event_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    return result