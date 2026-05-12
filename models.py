from pydantic import BaseModel
from typing import List, Tuple

class Coordinate(BaseModel):
    x: int
    y: int
    z: int

class EnvironmentRequest(BaseModel):
    bounds: Tuple[int, int, int]
    start: Coordinate
    goal: Coordinate
    obstacles: List[Coordinate]
    no_fly_zones: List[Coordinate]
    algorithm: str

class PathResponse(BaseModel):
    path: List[Coordinate]
    cost: float
    nodes_expanded: int
    runtime: float
