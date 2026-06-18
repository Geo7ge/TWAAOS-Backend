from fastapi import APIRouter, HTTPException, status

from schemas.file import FileCreate, FileUpdate, FileResponse
from services.file_service import FileService

router = APIRouter(prefix="/files", tags=["files"])


# ✅ CREATE
@router.post("/", response_model=FileResponse, status_code=201)
def create_file(file_data: FileCreate):
    file = FileService.create_file(file_data)

    if not file:
        raise HTTPException(status_code=400, detail="Could not create file")

    return file


# ✅ GET ALL
@router.get("/", response_model=list[FileResponse])
def get_all_files():
    return FileService.get_all_files()


# ✅ GET BY ID
@router.get("/{file_id}", response_model=FileResponse)
def get_file_by_id(file_id: int):
    file = FileService.get_file_by_id(file_id)

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return file


# ✅ GET BY EVENT ID
@router.get("/event/{event_id}", response_model=list[FileResponse])
def get_files_by_event(event_id: int):
    return FileService.get_files_by_event(event_id)


# ✅ UPDATE
@router.put("/{file_id}", response_model=FileResponse)
def update_file(file_id: int, file_data: FileUpdate):
    file = FileService.update_file(file_id, file_data)

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return file


# ✅ DELETE
@router.delete("/{file_id}", status_code=204)
def delete_file(file_id: int):
    success = FileService.delete_file(file_id)

    if not success:
        raise HTTPException(status_code=404, detail="File not found")

    return