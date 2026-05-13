import math
import time
import heapq
from typing import List, Tuple, Dict, Set
from pydantic import BaseModel

class State(BaseModel):
    x: int
    y: int
    z: int

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

class Environment:
    def __init__(self, bounds, start, goal, obstacles, no_fly_zones):
        self.bounds = bounds # (max_x, max_y, max_z)
        self.start = State(**start.dict() if hasattr(start, 'dict') else start)
        self.goal = State(**goal.dict() if hasattr(goal, 'dict') else goal)
        self.impassable = set()
        for obs in obstacles:
            self.impassable.add((obs.x, obs.y, obs.z))
        for nf in no_fly_zones:
            self.impassable.add((nf.x, nf.y, nf.z))
        
        # Calculate max obstacle height for building-aware heuristic
        self.h_obs = 0
        if obstacles:
            self.h_obs = max(obs.z for obs in obstacles)

    def is_valid(self, state: State):
        return (0 <= state.x <= self.bounds[0] and
                0 <= state.y <= self.bounds[1] and
                0 <= state.z <= self.bounds[2] and
                (state.x, state.y, state.z) not in self.impassable)

    def get_neighbors(self, state: State):
        neighbors = []
        # Movement actions: horizontal, upward, downward
        # Horizontal
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            new_s = State(x=state.x + dx, y=state.y + dy, z=state.z)
            if self.is_valid(new_s):
                neighbors.append((new_s, 1)) # cost 1
        
        # Upward
        new_s_up = State(x=state.x, y=state.y, z=state.z + 1)
        if self.is_valid(new_s_up):
            neighbors.append((new_s_up, 2)) # cost 2
            
        # Downward
        new_s_down = State(x=state.x, y=state.y, z=state.z - 1)
        if self.is_valid(new_s_down):
            neighbors.append((new_s_down, 1)) # cost 1
            
        return neighbors

def manhattan_heuristic(state: State, goal: State, env: Environment):
    return abs(state.x - goal.x) + abs(state.y - goal.y) + abs(state.z - goal.z)

def euclidean_heuristic(state: State, goal: State, env: Environment):
    return math.sqrt((state.x - goal.x)**2 + (state.y - goal.y)**2 + (state.z - goal.z)**2)

def building_aware_heuristic(state: State, goal: State, env: Environment):
    d_xy = abs(state.x - goal.x) + abs(state.y - goal.y)
    return d_xy + max(0, env.h_obs - state.z)

def search(env: Environment, algorithm: str):
    start_time = time.time()
    
    pq = []
    # heapq format: (f_score, get_tie_breaker, g_score, state_tuple, path, state_obj)
    counter = 0
    state_tuple = (env.start.x, env.start.y, env.start.z)
    heapq.heappush(pq, (0, counter, 0, state_tuple, [env.start], env.start))
    
    visited_g = {state_tuple: 0}
    nodes_expanded = 0
    
    while pq:
        f, _, g, curr_tuple, path, curr_state = heapq.heappop(pq)
        
        if visited_g.get(curr_tuple, float('inf')) < g:
            continue
            
        if curr_tuple == (env.goal.x, env.goal.y, env.goal.z):
            runtime = time.time() - start_time
            # Return result format matching Pydantic response
            return {
                "path": [{"x": s.x, "y": s.y, "z": s.z} for s in path],
                "cost": g,
                "nodes_expanded": nodes_expanded,
                "runtime": runtime
            }
            
        nodes_expanded += 1
        
        for neighbor, cost in env.get_neighbors(curr_state):
            new_g = g + cost
            neighbor_tuple = (neighbor.x, neighbor.y, neighbor.z)
            
            if new_g < visited_g.get(neighbor_tuple, float('inf')):
                visited_g[neighbor_tuple] = new_g
                new_path = list(path)
                new_path.append(neighbor)
                
                h = 0
                if algorithm == "astar_manhattan":
                    h = manhattan_heuristic(neighbor, env.goal, env)
                elif algorithm == "astar_euclidean":
                    h = euclidean_heuristic(neighbor, env.goal, env)
                elif algorithm == "astar_building":
                    h = building_aware_heuristic(neighbor, env.goal, env)
                # else ucs uses h=0
                    
                f_score = new_g + h
                counter += 1
                heapq.heappush(pq, (f_score, counter, new_g, neighbor_tuple, new_path, neighbor))
                
    return {
        "path": [],
        "cost": -1,
        "nodes_expanded": nodes_expanded,
        "runtime": time.time() - start_time
    }
