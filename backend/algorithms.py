import math
import sys
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

def bidirectional_astar(env: Environment):
    """
    Bidirectional A* search: searches from both start and goal simultaneously.
    Works by running alternating A* searches from both ends and detecting when paths meet.
    """
    start_time = time.time()
    
    # Forward search: start -> goal using A* with Manhattan heuristic
    forward_pq = []
    forward_counter = 0
    start_tuple = (env.start.x, env.start.y, env.start.z)
    heapq.heappush(forward_pq, (0, forward_counter, 0, start_tuple, [env.start], env.start))
    forward_g = {start_tuple: 0}
    forward_closed = set()
    
    # Backward search: goal -> start using A* with Manhattan heuristic  
    backward_pq = []
    backward_counter = 0
    goal_tuple = (env.goal.x, env.goal.y, env.goal.z)
    heapq.heappush(backward_pq, (0, backward_counter, 0, goal_tuple, [env.goal], env.goal))
    backward_g = {goal_tuple: 0}
    backward_closed = set()
    
    nodes_expanded = 0
    best_path = None
    best_cost = float('inf')
    path_limit = float('inf')
    
    while forward_pq and backward_pq:
        # Forward search step
        while forward_pq and (not best_path or len(forward_pq) <= len(backward_pq)):
            f, _, g, curr_tuple, path, curr_state = heapq.heappop(forward_pq)
            
            if curr_tuple in forward_closed:
                continue
            forward_closed.add(curr_tuple)
            nodes_expanded += 1
            
            # Check if goal reached
            if curr_tuple == goal_tuple:
                if g < best_cost:
                    best_cost = g
                    best_path = path
                break
            
            # Check meeting point
            if curr_tuple in backward_g and g + backward_g[curr_tuple] < best_cost:
                best_cost = g + backward_g[curr_tuple]
            
            # Prune if path cost exceeds best found
            if g >= best_cost:
                continue
            
            for neighbor, cost in env.get_neighbors(curr_state):
                new_g = g + cost
                neighbor_tuple = (neighbor.x, neighbor.y, neighbor.z)
                
                if neighbor_tuple not in forward_closed and new_g < forward_g.get(neighbor_tuple, float('inf')):
                    forward_g[neighbor_tuple] = new_g
                    new_path = list(path)
                    new_path.append(neighbor)
                    
                    h = manhattan_heuristic(neighbor, env.goal, env)
                    f_score = new_g + h
                    forward_counter += 1
                    heapq.heappush(forward_pq, (f_score, forward_counter, new_g, neighbor_tuple, new_path, neighbor))
        
        # Backward search step
        while backward_pq and (not best_path or len(backward_pq) < len(forward_pq)):
            f, _, g, curr_tuple, path, curr_state = heapq.heappop(backward_pq)
            
            if curr_tuple in backward_closed:
                continue
            backward_closed.add(curr_tuple)
            nodes_expanded += 1
            
            # Check if start reached
            if curr_tuple == start_tuple:
                if g < best_cost:
                    best_cost = g
                    best_path = path[::-1]  # Reverse for correct direction
                break
            
            # Check meeting point
            if curr_tuple in forward_g and g + forward_g[curr_tuple] < best_cost:
                best_cost = g + forward_g[curr_tuple]
            
            # Prune if path cost exceeds best found
            if g >= best_cost:
                continue
            
            for neighbor, cost in env.get_neighbors(curr_state):
                new_g = g + cost
                neighbor_tuple = (neighbor.x, neighbor.y, neighbor.z)
                
                if neighbor_tuple not in backward_closed and new_g < backward_g.get(neighbor_tuple, float('inf')):
                    backward_g[neighbor_tuple] = new_g
                    new_path = list(path)
                    new_path.append(neighbor)
                    
                    h = manhattan_heuristic(neighbor, env.start, env)
                    f_score = new_g + h
                    backward_counter += 1
                    heapq.heappush(backward_pq, (f_score, backward_counter, new_g, neighbor_tuple, new_path, neighbor))
        
        # Early termination check
        if best_path is not None:
            min_f_forward = forward_pq[0][0] if forward_pq else float('inf')
            min_f_backward = backward_pq[0][0] if backward_pq else float('inf')
            if best_cost <= min(min_f_forward, min_f_backward):
                break
    
    if best_path is not None:
        runtime = time.time() - start_time
        return {
            "path": [{"x": s.x, "y": s.y, "z": s.z} for s in best_path],
            "cost": best_cost,
            "nodes_expanded": nodes_expanded,
            "runtime": runtime
        }
    
    # No path found
    runtime = time.time() - start_time
    return {
        "path": [],
        "cost": -1,
        "nodes_expanded": nodes_expanded,
        "runtime": runtime
    }

# Maximum node expansions before IDA* gives up (prevents infinite hangs on large grids)
_IDA_STAR_NODE_LIMIT = 100_000

def ida_star(env: Environment):
    """
    IDA* (Iterative Deepening A*): depth-first search with an f-cost threshold
    that iteratively increases. Memory-efficient: O(depth) space.
    Uses Manhattan heuristic. Aborts if node expansions exceed _IDA_STAR_NODE_LIMIT.
    """
    start_time = time.time()
    nodes_expanded = [0]
    limit_hit = [False]
    goal_tuple = (env.goal.x, env.goal.y, env.goal.z)

    # Ensure recursion depth is sufficient for the grid size
    max_depth = env.bounds[0] * env.bounds[1] * env.bounds[2] + 50
    prev_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max(prev_limit, max_depth + 100))

    def dfs(path: list, path_set: set, g: float, threshold: float):
        if nodes_expanded[0] >= _IDA_STAR_NODE_LIMIT:
            limit_hit[0] = True
            return float('inf')

        current = path[-1]
        f = g + manhattan_heuristic(current, env.goal, env)

        if f > threshold:
            return f  # exceeded — return minimum f that surpassed threshold

        if (current.x, current.y, current.z) == goal_tuple:
            return ('FOUND', g)

        nodes_expanded[0] += 1
        minimum = float('inf')

        for neighbor, cost in env.get_neighbors(current):
            ntuple = (neighbor.x, neighbor.y, neighbor.z)
            if ntuple in path_set:
                continue

            path.append(neighbor)
            path_set.add(ntuple)
            result = dfs(path, path_set, g + cost, threshold)

            if isinstance(result, tuple) and result[0] == 'FOUND':
                return result  # propagate found result without popping (path intact)

            if result < minimum:
                minimum = result
            path.pop()
            path_set.remove(ntuple)

        return minimum

    threshold = manhattan_heuristic(env.start, env.goal, env)
    path = [env.start]
    path_set = {(env.start.x, env.start.y, env.start.z)}

    while threshold != float('inf'):
        result = dfs(path, path_set, 0, threshold)

        if limit_hit[0]:
            sys.setrecursionlimit(prev_limit)
            return {
                "path": [],
                "cost": -2,  # -2 signals node-limit exceeded (not "no path")
                "nodes_expanded": nodes_expanded[0],
                "runtime": time.time() - start_time
            }

        if isinstance(result, tuple) and result[0] == 'FOUND':
            sys.setrecursionlimit(prev_limit)
            runtime = time.time() - start_time
            return {
                "path": [{"x": s.x, "y": s.y, "z": s.z} for s in path],
                "cost": result[1],
                "nodes_expanded": nodes_expanded[0],
                "runtime": runtime
            }

        if result == float('inf'):
            break  # no path exists

        threshold = result

    sys.setrecursionlimit(prev_limit)
    return {
        "path": [],
        "cost": -1,
        "nodes_expanded": nodes_expanded[0],
        "runtime": time.time() - start_time
    }


def search(env: Environment, algorithm: str):
    # IDA* handled separately (recursive DFS, not heap-based)
    if algorithm == "idastar":
        return ida_star(env)

    # Unidirectional search: UCS, A* variants, and Weighted A*
    start_time = time.time()

    WEIGHTED_ASTAR_W = 1.5  # weight for Weighted A*

    pq = []
    # heapq format: (f_score, tie_breaker, g_score, state_tuple, path, state_obj)
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
                elif algorithm == "weighted_astar":
                    h = WEIGHTED_ASTAR_W * manhattan_heuristic(neighbor, env.goal, env)
                # ucs uses h=0

                f_score = new_g + h
                counter += 1
                heapq.heappush(pq, (f_score, counter, new_g, neighbor_tuple, new_path, neighbor))

    return {
        "path": [],
        "cost": -1,
        "nodes_expanded": nodes_expanded,
        "runtime": time.time() - start_time
    }
