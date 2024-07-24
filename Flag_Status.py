from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import mysql.connector
from mysql.connector import Error

app = FastAPI()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='EKYC',
            user='root',
            password='kharbanda'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
    return None

@app.on_event("shutdown")
def shutdown():
    connection = get_db_connection()
    if connection and connection.is_connected():
        connection.close()

class UserOut(BaseModel):
    NAME: str
    EMAIL: str
    STATUS: str
    AADHAR_NO: Optional[str]
    PAN_NO: Optional[str]
    ADDRESS: Optional[str]
    GENDER: Optional[str]
    DOB: Optional[str]
    PASSWORD: Optional[str]

@app.get("/check_kyc/", response_model=UserOut)
def check_kyc(name: str, email: str):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection error")

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE NAME = %s AND EMAIL = %s"
    cursor.execute(query, (name, email))
    user = cursor.fetchone()

    if user is None:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="User not found")

    cursor.close()
    connection.close()

    if user["STATUS"] == "1":
        return {"message": "Thank you, your KYC is complete", "redirect": "/final_page"}

    return {"message": "Your KYC is pending", "redirect": "/landing"}

@app.post("/create_user/")
def create_user(user: UserOut):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection error")

    cursor = connection.cursor()
    insert_query = """
    INSERT INTO users (NAME, EMAIL, STATUS, AADHAR_NO, PAN_NO, ADDRESS, GENDER, DOB, PASSWORD) VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (user.NAME, user.EMAIL, user.STATUS, user.AADHAR_NO, user.PAN_NO, user.ADDRESS, user.GENDER, user.DOB, user.PASSWORD)

    try:
        cursor.execute(insert_query, values)
        connection.commit()
    except Error as e:
        connection.rollback()
        cursor.close()
        connection.close()
        raise HTTPException(status_code=500, detail="Failed to insert record into MySQL table: " + str(e))

    cursor.close()
    connection.close()
    return {"message": "User created successfully"}

#@app.post("/verify")
def verify(name: str, email: str):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection error")

    cursor = connection.cursor(dictionary=True)
    query = "SELECT STATUS FROM users WHERE NAME = %s AND EMAIL = %s"
    cursor.execute(query, (name, email))
    user = cursor.fetchone()

    if user is None:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="User not found")

    status_bool = user["STATUS"] == "1"
    
    cursor.close()
    connection.close()

    if status_bool:
        return {"message": "Thank you, your KYC is complete", "redirect": "/final_page"}
    else:
        return {"message": "Your KYC is pending", "redirect": "/landing"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
