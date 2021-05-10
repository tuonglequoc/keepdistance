from fastapi import FastAPI, Body, Query, HTTPException
from enum import Enum
from typing import List, Tuple, Optional, Set
from models import CinemaRoomModel
from config import CINEMA_ROOM
from controllers import CinemaRoomController

import numpy as np


# Get default values from config
default_height = CINEMA_ROOM["default"]["HEIGHT"]
default_width = CINEMA_ROOM["default"]["WIDTH"]
default_min_distance = CINEMA_ROOM["default"]["MIN_DISTANCE"]

# Init
cinema_controller = CinemaRoomController(default_height, default_width, default_min_distance)
app = FastAPI()


# Router
@app.get("/")
async def root():
    """Get status of cinema room."""
    result = {"seats_status": cinema_controller.get_seats_status(),
            "min_distance": cinema_controller.get_min_distance()}
    return result

@app.post("/init")
async def init(cinema_room: CinemaRoomModel):
    """Re-initialize a new cinema room with specified size and minimum distance."""
    global cinema_controller   
    cinema_controller = CinemaRoomController(cinema_room.height, cinema_room.width, cinema_room.min_distance)
    result = {"message": "Initialize new cinema room with size {}x{}, min distance is {}.".format(
            cinema_room.height, 
            cinema_room.width, 
            cinema_room.min_distance)
            }
    return result

@app.post("/reserve")
async def reserve(reserved_seats: Set[Tuple[int, int]] = Body(...)):
    """Reserve a set of seats."""
    result = cinema_controller.reserve_seats(reserved_seats)
    if result:
        return {"message": "Reserved successfully"}
    else:
        raise HTTPException(status_code=400, detail="Seats are already booked or doesn't meet distance rule.")

@app.get("/available_seats")
async def get_available_seats_set(num_of_seats: int = Query(1, ge=1), only_one: Optional[bool] = Query(None)):
    """Get currently available seats for purchase with given numer of seats that is needed."""
    if only_one:
        result = {"available_seats": cinema_controller.get_available_seats(num_of_seats, True)}
    else:
        result = {"available_seats": cinema_controller.get_available_seats(num_of_seats)}
    return result
