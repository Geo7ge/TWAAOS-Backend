from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from typing import List
from schemas.registration import RegistrationCreate, RegistrationResponse, RegistrationUpdate
from services.registration_service import RegistrationService

router = APIRouter(prefix="/registrations", tags=["registrations"])

@router.post(
    "/",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_registration(registration_data: RegistrationCreate, background_tasks: BackgroundTasks):
    """Înregistrează un utilizator la un eveniment"""
    result = RegistrationService.create_registration(registration_data)
    
    # Verificăm dacă serviciul a returnat o eroare (ex: utilizator deja înscris)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create registration"
        )

    background_tasks.add_task(
        RegistrationService.send_registration_confirmation,
        registration_data.user_id,
        registration_data.event_id,
    )
        
    return result

@router.get("/user/{user_id}", response_model=List[RegistrationResponse])
def get_user_registrations(user_id: int):
    """Obține toate înscrierile unui anumit utilizator"""
    registrations = RegistrationService.get_user_registrations(user_id)
    return registrations

@router.get("/event/{event_id}", response_model=List[RegistrationResponse])
def get_event_registrations(event_id: int):
    """Obține toți participanții înscriși la un eveniment"""
    registrations = RegistrationService.get_event_registrations(event_id)
    return registrations

@router.put("/{registration_id}", response_model=RegistrationResponse)
def update_registration(
    registration_id: int,
    update_data: RegistrationUpdate
):
    """Actualizează complet statusul unei înscrieri"""
    
    updated_reg = RegistrationService.update_registration_status(
        registration_id,
        update_data.status
    )
    
    if not updated_reg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    return updated_reg

@router.delete("/{registration_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_registration(registration_id: int):
    """Șterge/Anulează o înscriere"""
    result = RegistrationService.delete_registration(registration_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    return None