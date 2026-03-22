#home page

from fastapi import FastAPI,Query, HTTPException
from pydantic import BaseModel,Field
from typing import Optional, List



app=FastAPI()

#-------------------HOME--------------------

@app.get("/")
def home():
    return {"message" : "Welcome to Hotel booking API"}


#room data

rooms=[
{"id" : 1,"room_type" : "Single","price" : 1500,"available" : True},
{"id" : 2,"room_type" : "Double","price" : 3000,"available" : True},
{"id" : 3,"room_type" : "Delux" ,"price" : 5000,"available" : True},
{"id" : 4,"room_type" : "Suite" ,"price" : 8000,"available" : True},
{"id" : 5,"room_type" :"Quad" ,"price" : 10000,"available" : False}
]


#HELPERS

def find_room(room_id):
    for room in rooms:
        if room["id"] == room_id:
            return room
    return None

def is_room_booked(room_id):
    for booking in bookings:
        if booking["room_id"] == room_id and booking["status"] != "checked-out":
            return True
    return False


#get all rooms

@app.get("/rooms")
def get_rooms():
    return {
        "rooms" : rooms,
        "total" : len(rooms)
    }



#count total rooms

@app.get("/rooms/count")
def count_of_rooms():
    return{"total rooms": len(rooms)}



#get by search

@app.get ("/rooms/search")
def search_rooms(room_type: Optional [str] = Query(None)):
    result = []
    for room in rooms:
        if room_type and room_type.lower() in room["room_type"].lower():
            result.append(room)
    return {"results": result}





#get by filter

@app.get("/rooms/filter")
def filter_room(min_price : int = 0, available : bool = True):
    result = []
    for room in rooms:
        if room["price"] >= min_price and room["available"] == available:
            result.append(room)
    return {"filtered_rooms": result}



#get by sort

@app.get("/rooms/sort")
def sort_rooms(order : str = "asc"):
    sorted_rooms = sorted(rooms,key = lambda x: x["price"],reverse = (order == "desc"))
    return {"rooms" : sorted_rooms}




#get by page

@app.get("/rooms/page")
def paginate_rooms(page: int = 1,limit: int = 2):
    start = (page - 1) * limit
    end = start + limit
    return {"page" : page, "data" : rooms[start:end]}


#get room by id

@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    for room in rooms:
        if room["id"] == room_id:
            return room
    raise HTTPException (status_code = 404, detail="Room not found")


#----------------create room-------------------

class Room (BaseModel):
    type : str
    price : int
    available : bool


#create POST API
@app.post("/rooms")
def add_room(room:Room):
    new_room = room.dict()
    new_room["id"] = len(rooms) + 1
    new_room ["room_type"] = new_room.pop("type")
    rooms.append(new_room)
    return {"message" : "Room added successsfully" , "room" : new_room}


#Update room (put)
@app.put("/rooms/{room_id}")
def update_room(room_id: int,updated: Room):
    for room in rooms:
        if room["id"] == room_id:
            room["room_type"] = updated.type
            room["price"] = updated.price
            room["available"] = updated.available
            return {"message": "Room updated", "room" : room}
    raise HTTPException(status_code=404, detail = "Room not found")



#delete model

@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):
    for room in rooms:
        if room["id"] == room_id:
            rooms.remove(room)
            return {"message": "Room deleted"}
    raise HTTPException(status_code=404, detail="Room not found")




#-------------------customers------------------
#add customer API

customers = []

class Customer(BaseModel):
    name : str
    phone : str


@app.post("/customers")
def add_customer(customer : Customer):
    new_customer = customer.dict()
    new_customer["id"] = len(customers) + 1
    customers.append(new_customer)
    return{
        "message" : "customer added successfully",
        "customer" : new_customer
    }



@app.get ("/customers", response_model=List[Customer])
def get_customers():
    return customers


@app.get("/customers")
def get_customers():
    return{"customers": customers,
           "total": len(customers)
           }


#----------------bookings-----------------

#create booking system

bookings = []
 
class Booking(BaseModel):
    customer_id : int
    room_id : int

#create booking class

@app.post("/bookings")
def create_booking(booking : Booking):

    #check customer exists
    customer = None
    for c in customers:
        if c["id"] == booking.customer_id:
            customer = c

    if not customer:
         raise HTTPException(status_code = 404,
                             detail = "Customer not found")



    #checking room existance and availability

    room = None
    for r in rooms:
        if r["id"] == booking.room_id:
            room = r

    if not room:
        raise HTTPException (status_code = 404, detail= "Room not found")

    if not room["available"]:
        raise HTTPException(status_code=400, detail = "Room not available") 
    
    for b in bookings:
        if b["room_id"] == booking.room_id and b["status"] !="checked-out":
            raise HTTPException (status_code = 400 , detail = "Room already booked")

    #cretae booking

    new_booking = booking.dict()
    new_booking["id"] = len(bookings) + 1
    new_booking["status"] = "booked"

    bookings.append(new_booking)

    #mark room unavailable
    room["available"] = False

    return{
        "message" : "Booking successful",
        "booking" : new_booking

    }

#check -in API

@app.post("/checkin/{booking_id}")
def check_in (booking_id : int):
    for booking in bookings:
        if booking["id"] == booking_id:
            booking["status"] = "checked-in"
            return {
                "message" : "check-in successful",
                "booking" : booking
            }
    raise HTTPException (status_code=404, detail= "Booking not found")

@app.post("/checkout/{booking_id}")
def check_out(booking_id : int):
    for booking in bookings:
        if booking["id"] == booking_id:

            #finding rooms
            for room in rooms:
                if room["id"] == booking["room_id"]:
                    room["available"] = True

            booking["status"] = "checked-out"

            return{
                "message" : "Check-out successful",
                "booking" : booking
            }
    raise HTTPException (status_code = 404, detail="Booking not found")


@app.delete("/bookings/{booking_id}")
def cancel_booking(booking_id: int):
    for b in bookings:
        if b["id"] == booking_id:

            for r in rooms:
                if r["id"] == b["room_id"]:
                    r["available"] = True

                bookings.remove(b)

                return {"message" : "Booking cancelled"}
    raise HTTPException (status_code = 404,detail = "Booking not found")


#get all bokings

@app.get("/bookings")
def get_bookings():
    return {
        "bookings" : bookings,
        "total" : len(bookings)
    }



@app.get("/bookings/{customer_id}")
def get_customer_bookings(customer_id : int):
    result=[]
    for b in bookings:
        if b["customer_id"] == customer_id:
            result.append(b)
    return {"bookings" : result}


#----------------Summary-----------------

@app.get("/summary")
def summary():
    available = 0
    active = 0
    
    for r in rooms:
        if r["available"]:
            available+=1

    for b in bookings:
        if b ["status"] != "checked-out":
            active +=1

    return {
        "total_rooms" : len (rooms),
        "available_rooms" : len([r for r in rooms if r["available"]]),
        "total_customers" : len(customers),
        "total_booking" : len (bookings),
        "active_bookings" : len ([b for b in bookings if b["status"] != "cheked-out"])

    }     
            
            
    
