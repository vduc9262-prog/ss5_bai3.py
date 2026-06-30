from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel

app = FastAPI()

students = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Thi B"},
    {"id": 3, "name": "Le Van C"}
]
courses = [
    {"id": 1, "name": "FastAPI Basic", "capacity": 2},
    {"id": 2, "name": "Python OOP", "capacity": 2}
]
registrations = [
    {"id": 1, "student_id": 1, "course_id": 1},
    {"id": 2, "student_id": 2, "course_id": 1}
]

class RegistrationCreate(BaseModel):
    student_id: int 
    course_id:int

@app.post("/registrations", status_code=status.HTTP_201_CREATED)
def create_registration(registration: RegistrationCreate):

    student = None
    for s in students:
        if s["id"] == registration.student_id:
            student = s
            break

    if student is None:
        raise HTTPException(status_code=404,detail="Student not found")

    course = None
    for c in courses:
        if c["id"] == registration.course_id:
            course = c
            break

    if course is None:
        raise HTTPException(status_code=404,detail="Course not found")

    for item in registrations:
        if (
            item["student_id"] == registration.student_id
            and item["course_id"] == registration.course_id
        ):
            raise HTTPException(status_code=400,detail="Student already registered this course")

    count = 0

    for item in registrations:
        if item["course_id"] == registration.course_id:
            count += 1

    if count >= course["capacity"]:
        raise HTTPException(status_code=400,detail="Course is full")

    new_registration = {
        "id": len(registrations) + 1,
        "student_id": registration.student_id,
        "course_id": registration.course_id
    }

    registrations.append(new_registration)

    return {
        "message": "Đăng ký thành công",
        "data": new_registration
    }