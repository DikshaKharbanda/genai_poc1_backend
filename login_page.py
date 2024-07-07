from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error

app = FastAPI()

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login")
async def login(request: LoginRequest):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='EKYC',
            user='root',
            password='xyz'
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE EMAIL = %s AND PASSWORD = %s"
            cursor.execute(query, (request.email, request.password))
            user = cursor.fetchone()
            
            if user:
                # Return the landing page URL upon successful login
                return {"message": "Login successful", "redirect_url": "/landing-page"}
            else:
                raise HTTPException(status_code=401, detail="Invalid email or password")
    except Error as e:
        raise HTTPException(status_code=500, detail="Database connection failed")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Endpoint for the landing page
@app.get("/landing-page")
async def landing_page():
    return {"message": "Welcome to the landing page!"}

# Run the server using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
