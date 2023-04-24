from fastapi import FastAPI
from routers.users_controller import user_end_points
from routers.match_controller import match_end_points
from routers.simulation_controller import simulation_end_points
from routers.robot_controller import robot_end_points
from routers.session_controller import session_end_points
from fastapi.middleware.cors import CORSMiddleware
from db.database import map_database
from db.database import database

# Definiendo la aplicacion
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

# mapear base de datos
map_database(database, provider="sqlite", filename="database.sqlite", create_db=True)

# Agregando los routers
app.include_router(user_end_points)
app.include_router(match_end_points)
app.include_router(robot_end_points)
app.include_router(simulation_end_points)
app.include_router(session_end_points)
