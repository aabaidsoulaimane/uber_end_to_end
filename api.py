from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from connection import send_to_event_hub, generate_uber_ride_confirmation

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def booking_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/book")
def book_ride(request: Request):  
    ride = generate_uber_ride_confirmation()
    result = send_to_event_hub(ride)
    return templates.TemplateResponse("confirmation.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
