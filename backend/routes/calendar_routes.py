from fastapi import APIRouter, HTTPException
from typing import List
from models import CalendarEvent
from database import db_manager

router = APIRouter()

@router.post("/api/events", response_model=CalendarEvent)
def create_event(event: CalendarEvent):
    """
    Create a new calendar event.
    """
    query = """
        INSERT INTO calendar_events (title, date, type, id_enseignant)
        VALUES (?, ?, ?, ?)
    """
    try:
        result = db_manager.execute_query(query, (event.title, event.date, event.type, event.id_enseignant))
        event_id = result[0]['id']
        # Pydantic V2 uses model_dump(), V1 uses dict()
        event_data = event.model_dump() if hasattr(event, 'model_dump') else event.dict()
        return {**event_data, "id": event_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create event: {e}")

@router.get("/api/events/{enseignant_id}", response_model=List[CalendarEvent])
def get_events_by_enseignant(enseignant_id: int):
    """
    Get all calendar events for a specific teacher.
    """
    query = "SELECT id, title, date, type, id_enseignant FROM calendar_events WHERE id_enseignant = ?"
    try:
        events = db_manager.execute_query(query, (enseignant_id,))
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve events: {e}")

@router.delete("/api/events/{event_id}", status_code=204)
def delete_event(event_id: int):
    """
    Delete a specific calendar event.
    """
    query = "DELETE FROM calendar_events WHERE id = ?"
    try:
        db_manager.execute_query(query, (event_id,))
        return {"message": "Event deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete event: {e}")
