from enum import Enum

import numpy as np


class Status(Enum):
    """
    Enum class used to present status of seat
    """
    AVAILABLE = 0
    BOOKED = 1
    BLOCKED = 2

class CinemaRoomController():
    """
    A controller class for CinemaRoom

    Attributes
    ----------
    _height : int 
        height of 2-dim seat matrix
    _width : int
        width of 2-dim seat matrix
    _seats : List[List[int]]
        2 dimensional array contains status of all seats in the room
    _min_distance : int
        minimum Manhattan distance

    Methods
    ------
    get_seats_status()
        Get status of all the seats
    get_min_distance()
        Get minimum Manhattan distance
    get_available_seats(num_of_seats, only_one=False)
        Get currently available seats for purchase
    reserve_seats(reserved_seats)
        Reserve a set of seats
    _block_seats_in_distance(*booked_seat)
        Block seats that are in min distance
    """
    def __init__(self, height, width, min_distance=0):
        """
        Parameters
        ---------
        height : int
            height of 2-dim seat matrix
        width : int
            width of 2-dim seat matrix
        min_distance : int, optional
            minimum Manhattan distance
        """
        self._height = height
        self._width = width
        self._seats = np.full((height, width), Status.AVAILABLE)
        self._min_distance = min_distance

    def get_seats_status(self):
        """
        Get status of all the seats

        Returns
        ------
        List[List[int]]
            2 dimensional array contains status of all the seats
        """
        return self._seats.tolist()

    def get_min_distance(self):
        """
        Get minimum Manhattan distance

        Returns
        ------
        int
            minimum distance
        """
        return self._min_distance

    def get_available_seats(self, num_of_seats, only_one=False):
        """
        Get currently available seats for purchase

        Parameters
        ---------
        num_of_seats : int
            number of seats that are needed to reserve
        only_one: bool, optional
            flag to get one or all
        """
        # Get position of seats that are available
        available_seats_list = np.argwhere(self._seats == Status.AVAILABLE).tolist()
        result = []
        # Find available chain seats
        if only_one:
            for x_pos, y_pos in available_seats_list:
                if y_pos + num_of_seats - 1 < self._width and \
                        all([status == Status.AVAILABLE for status in self._seats[x_pos][y_pos:y_pos + num_of_seats]]):
                    return [(x_pos, _y) for _y in range(y_pos, y_pos + num_of_seats)]
        else:
            for x_pos, y_pos in available_seats_list:
                if y_pos + num_of_seats - 1 < self._width and \
                        all([status == Status.AVAILABLE for status in self._seats[x_pos][y_pos:y_pos + num_of_seats]]):
                    result.append([(x_pos, _y) for _y in range(y_pos, y_pos + num_of_seats)])
        return result

    def reserve_seats(self, reserved_seats):
        """
        Reserve a set of seats

        Parameters
        ---------
        reserved_seats : List[Tuple[int,int]]
            a set of seats that want to reserve

        Returns
        ------
        bool
            success or not
        """
        if all([self._seats[x][y] == Status.AVAILABLE for x, y in reserved_seats]):
            for x_pos, y_pos in reserved_seats:
                self._seats[x_pos][y_pos] = Status.BOOKED
                self._block_seats_in_distance(x_pos, y_pos)
            return True
        else:
            return False

    def _block_seats_in_distance(self, x, y):
        """
        Block seats that are in min distance

        Parameter
        --------
        x : int
            x position of reserved seat
        y : int
            y position of reserved seat
        """
        for i in range(1 - self._min_distance, self._min_distance):
            for j in range(abs(i) - self._min_distance + 1, self._min_distance - abs(i)):
                if 0 <= x + i < self._height and 0 <= y + j < self._width:
                    if self._seats[x + i][y+ j] == Status.AVAILABLE:
                        self._seats[x + i][y+ j] = Status.BLOCKED