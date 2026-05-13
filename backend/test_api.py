import requests
import json

url = "http://localhost:8000/pathfind"

req_data = {
    "bounds": [10, 10, 10],
    "start": {"x": 0, "y": 0, "z": 0},
    "goal": {"x": 9, "y": 9, "z": 9},
    "obstacles": [{"x": 5, "y": 5, "z": z} for z in range(6)],
    "no_fly_zones": [],
    "algorithm": "ucs"
}

def test_alg(alg):
    req_data["algorithm"] = alg
    try:
        res = requests.post(url, json=req_data)
        data = res.json()
        print(f"--- Algorithm: {alg} ---")
        print(f"Cost: {data.get('cost')}")
        print(f"Nodes Expanded: {data.get('nodes_expanded')}")
        print(f"Runtime: {data.get('runtime'):.5f}s\n")
    except Exception as e:
        print(f"Failed for {alg}: {e}")

if __name__ == "__main__":
    for alg in ["ucs", "astar_manhattan", "astar_euclidean", "astar_building"]:
        test_alg(alg)
