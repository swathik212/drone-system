import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 30000, // 30 s — prevents UI hanging on slow algorithms like IDA*
});

export type Coordinate = { x: number, y: number, z: number };

export interface EnvironmentRequest {
  bounds: [number, number, number];
  start: Coordinate;
  goal: Coordinate;
  obstacles: Coordinate[];
  no_fly_zones: Coordinate[];
  algorithm: string;
}

export interface PathResponse {
  path: Coordinate[];
  cost: number;
  nodes_expanded: number;
  runtime: number;
}

export const findPath = async (req: EnvironmentRequest): Promise<PathResponse> => {
  const response = await api.post('/pathfind', req);
  return response.data;
};
