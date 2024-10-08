from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import select
from database.connection import get_session
from models.events import Event, EventUpdate

from typing import List

event_router = APIRouter(
    tags=['Event']
)

events = []


@event_router.get('/', response_model=List[Event])
async def retreive_all_events(session=Depends(get_session)) -> List[Event]:
    statement = select(Event)
    events = session.exec(statement).all()
    return events


@event_router.delete('/')
async def delete_all_events(session=Depends(get_session)) -> dict:
    statement = select(Event)
    events = session.exec(statement).all()
    for _ in events:
        session.delete(_)
        session.commit()

    return {
        'message': 'Все события были успешно удалены.'
    }


@event_router.get('/{id}', response_model=Event)
async def retrieve_event(id: int, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Событие с ID ({id}) не найдено.'
    )


@event_router.post('/new')
async def create_event(new_event: Event, session=Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)

    return {
        'message': 'Событие успешно создано.'
    }


@event_router.delete('/delete/{id}')
async def delete_event(id: int, session=Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()

        return {
            'message': 'Событие успешно удалено'
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Событие с ID ({id}) не найдено.'
    )


@event_router.put('/edit/{id}', response_model=Event)
async def update_evennt(id: int, new_data: EventUpdate, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        event_data = new_data.dict(exclude_unset=True)
        for k, v in event_data.items():
            setattr(event, k, v)

        session.add(event)
        session.commit()
        session.refresh(event)

        return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Событие с ID ({id}) не найдено.'
    )
