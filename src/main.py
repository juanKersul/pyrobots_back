from fastapi import FastAPI
from routers.users_controller import user_end_points
from routers.match_controller import match_end_points
from routers.simulation_controller import simulation_end_points
from routers.robot_controller import robot_end_points
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


# Agregando cors urls
origins = ["http://localhost:3000", "localhost:3000"]
# Agregando middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_end_points)
app.include_router(match_end_points)
app.include_router(robot_end_points)
app.include_router(simulation_end_points)
