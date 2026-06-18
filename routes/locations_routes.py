from fastapi import APIRouter, HTTPException, status
from schemas.locations import (
    LocationCreate,
    LocationUpdate,
    LocationResponse,
)
from services.locations_service import LocationService

router = APIRouter(prefix="/locations", tags=["locations"])


@router.post(
    "/",
    response_model=LocationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_location(location_data: LocationCreate):
    """Create a new location"""
    location = LocationService.create_location(location_data)

    if not location:
        raise HTTPException(
            status_code=400,
            detail="Could not create location",
        )

    return LocationResponse(
        id=location["id"],
        name=location["name"],
        address=location["address"],
        city=location["city"],
        created_at=location.get("created_at"),
    )


@router.get("/", response_model=list[LocationResponse])
def get_locations():
    """Get all locations"""
    locations = LocationService.get_all_locations()

    return [
        LocationResponse(
            id=location["id"],
            name=location["name"],
            address=location["address"],
            city=location["city"],
            created_at=location.get("created_at"),
        )
        for location in locations
    ]


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: int):
    """Get location by ID"""
    location = LocationService.get_location_by_id(location_id)

    if not location:
        raise HTTPException(
            status_code=404,
            detail="Location not found",
        )

    return LocationResponse(
        id=location["id"],
        name=location["name"],
        address=location["address"],
        city=location["city"],
        created_at=location.get("created_at"),
    )


@router.put("/{location_id}", response_model=LocationResponse)
def update_location(location_id: int, location_data: LocationUpdate):
    """Update location"""
    location = LocationService.update_location(location_id, location_data)

    if not location:
        raise HTTPException(
            status_code=404,
            detail="Location not found",
        )

    return LocationResponse(
        id=location["id"],
        name=location["name"],
        address=location["address"],
        city=location["city"],
        created_at=location.get("created_at"),
    )


@router.delete("/{location_id}")
def delete_location(location_id: int):
    """Delete location"""
    result = LocationService.delete_location(location_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Location not found",
        )

    return result