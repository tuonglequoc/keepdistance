# Cinema Booking

This app supports the cinema follows social distance rule, built by FastAPI, provides REST services to:
- Initialize or refresh a new cinema room with specified number of seats and minimum Manhattan distance that is allowed.
- Get status of all seats in room (Available, Booked, Blocked)
- Get currently available seats for purchase with given how many needed seats (The seats will be together)
- Reserve a set of seats

## How to run the app
Install uvicorn:
```
$ pip install uvicorn[standard]
```
Install require dependencies:
```
$ pip install -r requirements.txt
```
Run app:
```
$ uvicorn main:app
```

## REST services
### Get status of all seats
Request:
```
$ curl 'http://127.0.0.1:8000'
```
Response:
```
{"seats_status":[[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]],"min_distance":3}
```
Status will be responsed as 2 dimensional array structure.

Status 0 for Available, 1 for Booked and 2 for Blocked.

Default cinema size is 10x10 with min distance is 3. You can also configure default value in keepdistance/config.py
```
CINEMA_ROOM = {
    "default": {
        "HEIGHT": 10,
        "WIDTH": 10,
        "MIN_DISTANCE": 3
    }
}
```

### Re-Initialize cinema room
Request:
```
$ curl 'http://127.0.0.1:8000/init' -d '{"height": 15, "width": 5, "min_distance": 2}'
```
Response:
```
{"message":"Initialize new cinema room with size 15x5, min distance is 2."}
```
Now, send get request to `http://127.0.0.1:8000` again. You will get:
```
{"seats_status":[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],"min_distance":2}
```

### Get currently available seats
Request:
```
$ curl 'http://127.0.0.1:8000/available_seats?num_of_seats=2'
```
Query "number_of_seats" is optional, if not define, default value will be 1.

Response:
```
{"available_seats":[[[0,0],[0,1]],[[0,1],[0,2]],[[0,2],[0,3]],[[0,3],[0,4]],[[1,0],[1,1]],[[1,1],[1,2]],[[1,2],[1,3]],[[1,3],[1,4]],[[2,0],[2,1]],[[2,1],[2,2]],[[2,2],[2,3]],[[2,3],[2,4]],[[3,0],[3,1]],[[3,1],[3,2]],[[3,2],[3,3]],[[3,3],[3,4]],[[4,0],[4,1]],[[4,1],[4,2]],[[4,2],[4,3]],[[4,3],[4,4]],[[5,0],[5,1]],[[5,1],[5,2]],[[5,2],[5,3]],[[5,3],[5,4]],[[6,0],[6,1]],[[6,1],[6,2]],[[6,2],[6,3]],[[6,3],[6,4]],[[7,0],[7,1]],[[7,1],[7,2]],[[7,2],[7,3]],[[7,3],[7,4]],[[8,0],[8,1]],[[8,1],[8,2]],[[8,2],[8,3]],[[8,3],[8,4]],[[9,0],[9,1]],[[9,1],[9,2]],[[9,2],[9,3]],[[9,3],[9,4]],[[10,0],[10,1]],[[10,1],[10,2]],[[10,2],[10,3]],[[10,3],[10,4]],[[11,0],[11,1]],[[11,1],[11,2]],[[11,2],[11,3]],[[11,3],[11,4]],[[12,0],[12,1]],[[12,1],[12,2]],[[12,2],[12,3]],[[12,3],[12,4]],[[13,0],[13,1]],[[13,1],[13,2]],[[13,2],[13,3]],[[13,3],[13,4]],[[14,0],[14,1]],[[14,1],[14,2]],[[14,2],[14,3]],[[14,3],[14,4]]]}
```
Response data will list all set of seats currently available for purchase in cinema room. Number of seats in each set depends on "number_of_seats" in query (2 in above example).

You can request only one set of seats that first met requirements for better performance. Add query "only_one=true" to url:
```
$ curl 'http://127.0.0.1:8000/available_seats?num_of_seats=2&only_one=true'
```
Response:
```
{"available_seats":[[0,0],[0,1]]}
```

### Reserve set of seats
Request:
```
$ curl 'http://127.0.0.1:8000/reserve' -d '[[0,0],[0,1]]'
```
Response:
```
{"message":"Reserved successfully"}
```
If we reserve another seats that are in min distance:
```
$ curl 'http://127.0.0.1:8000/reserve' -d '[[0,2],[0,3]]'
```
Response:
```
< HTTP/1.1 400 Bad Request >

{"detail":"Seats are already booked or doesn't meet distance rule."}
```
Now, get currently status of seats in cinema room again:
```
$ curl 'http://127.0.0.1:8000'
```
Response:
```
{"seats_status":[[1,1,2,0,0],[2,2,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],"min_distance":2}
```

## API docs
http://127.0.0.1:8000/docs