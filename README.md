# 🏨 Hotel Booking System API

This is a FastAPI backend project built as part of an internship program.
It demonstrates real-world API development using FastAPI for managing hotel bookings.

---

## 🚀 Features

* REST APIs using FastAPI
* Pydantic data validation
* CRUD operations (Create, Read, Update, Delete)
* Multi-step workflow (Booking → Check-in → Check-out → Cancel)
* Search functionality
* Sorting results
* Pagination support
* Summary dashboard

---

## 📂 Project Structure

hotel_booking_project/
│── main.py
│── requirements.txt
│── README.md
│── screenshots/

---

## 🛠 Tech Stack

* FastAPI
* Pydantic
* Uvicorn

---

## ▶️ How to Run

### 1. Install dependencies

pip install -r requirements.txt

### 2. Run FastAPI server

uvicorn main:app --reload

### 3. Open Swagger UI

http://127.0.0.1:8000/docs

---

## 📸 Screenshots

All API endpoints are tested using Swagger UI.
Screenshots are available in the screenshots/ folder.

---

## 📌 API Functionalities

### ✅ GET APIs

* Home route
* Get all rooms
* Get room by ID
* Get all customers
* Get all bookings
* Summary endpoint

---

### ✅ POST APIs

* Create new room
* Add customer
* Create booking
* Check-in
* Check-out

---

### ✅ Helper Functions

* find_room()
* Booking validation logic
* Availability checking

---

### ✅ CRUD Operations

* Create room
* Update room
* Delete room

**Status Codes Used:**

* 201 Created
* 404 Not Found
* 400 Bad Request

---

### ✅ Multi-Step Workflow

* Book room
* Check-in
* Check-out
* Cancel booking

---

### ✅ Advanced Features

* Search rooms
* Filter rooms
* Sort rooms
* Pagination
* Booking summary

---

## 🎯 Objective

This project demonstrates the ability to:

* Design RESTful APIs
* Structure backend systems
* Implement real-world booking workflows
* Apply FastAPI concepts effectively

---

## 🙌 Acknowledgment

Grateful for the learning opportunity at Innomatics Research Labs.

---

## 👨‍💻 Author

Amalapurapu Durga Rama Sirija


##GitHub Repository

https://github.com/sirijaamalapurapu-maker/fastapi_hotel_room_booking/tree/main
