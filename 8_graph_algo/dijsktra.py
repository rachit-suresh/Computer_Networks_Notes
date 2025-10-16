import heapq
import math

# graph looks like graph[A]=[(B,2),(C,3)]

def dijsktra(graph, start):
  visited = set()
  distances ={}

  for vertex in graph:
    distances[vertex] = math.inf
  distances[start]=0

  priority_queue=[]
  heapq.heappush(priority_queue, (0,start))

  while len(priority_queue)>0:
    curr_dist, curr_vertex = heapq.heappop(priority_queue)

    if curr_vertex in visited:
      continue

    visited.add(curr_vertex)

    neighbours = graph[curr_vertex]

    for neighbour, weight in neighbours:
      distance = curr_dist + weight

      if distance<distances[neighbour]:
        distances[neighbour] = distance
        heapq.heappush(priority_queue,(distance,neighbour))
  
  return distances
