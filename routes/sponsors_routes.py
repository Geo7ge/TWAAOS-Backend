from fastapi import APIRouter, HTTPException, status
from schemas.sponsors import (
    SponsorCreate,
    SponsorUpdate,
    SponsorResponse,
)
from services.sponsors_service import SponsorService

router = APIRouter(prefix="/sponsors", tags=["sponsors"])


@router.post(
    "/",
    response_model=SponsorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_sponsor(sponsor_data: SponsorCreate):
    """Create a new sponsor"""
    sponsor = SponsorService.create_sponsor(sponsor_data)

    if not sponsor:
        raise HTTPException(
            status_code=400,
            detail="Could not create sponsor",
        )

    return SponsorResponse(
        id=sponsor["id"],
        name=sponsor["name"],
        logo_url=sponsor["logo_url"],
    )


@router.get("/", response_model=list[SponsorResponse])
def get_sponsors():
    """Get all sponsors"""
    sponsors = SponsorService.get_all_sponsors()

    return [
        SponsorResponse(
            id=sponsor["id"],
            name=sponsor["name"],
            logo_url=sponsor["logo_url"],
        )
        for sponsor in sponsors
    ]


@router.get("/{sponsor_id}", response_model=SponsorResponse)
def get_sponsor(sponsor_id: int):
    """Get sponsor by ID"""
    sponsor = SponsorService.get_sponsor_by_id(sponsor_id)

    if not sponsor:
        raise HTTPException(
            status_code=404,
            detail="Sponsor not found",
        )

    return SponsorResponse(
        id=sponsor["id"],
        name=sponsor["name"],
        logo_url=sponsor["logo_url"],
    )


@router.put("/{sponsor_id}", response_model=SponsorResponse)
def update_sponsor(sponsor_id: int, sponsor_data: SponsorUpdate):
    """Update sponsor"""
    sponsor = SponsorService.update_sponsor(sponsor_id, sponsor_data)

    if not sponsor:
        raise HTTPException(
            status_code=404,
            detail="Sponsor not found",
        )

    return SponsorResponse(
        id=sponsor["id"],
        name=sponsor["name"],
        logo_url=sponsor["logo_url"],
    )


@router.delete("/{sponsor_id}")
def delete_sponsor(sponsor_id: int):
    """Delete sponsor"""
    result = SponsorService.delete_sponsor(sponsor_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Sponsor not found",
        )

    return result