from typing import Annotated
import json
from . import database
from . import models



def get_state(
        group: int,
    ):
    if group != 0:
        events = database.dict_query("SELECT *, CAST(EXTRACT(epoch FROM date) AS int) as date FROM event WHERE id=%s LIMIT 1", (group,))
        if len(events) < 1:
            return {"error": "Event not found"}
        event = events[0]
        songs = database.dict_query("""
                SELECT title, credits, usage FROM songuse
                    JOIN song on songuse.song_id = song.id
                    WHERE songuse.event_id = %s
        """, (group,))
        return {"event": event, "songs": songs}
    else:
        events = database.dict_query("SELECT *, CAST(EXTRACT(epoch FROM date) AS int) as date FROM event ORDER BY event.date DESC")
        if len(events) < 1:
            return {"error": "No events found"}
        return {"events": events}
