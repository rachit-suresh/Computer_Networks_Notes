import math

def bellman_ford(graph, start):

  distances={}
  for vertex in graph:
    distances[vertex]=math.inf

  distances[start]=0
  
  for _ in range(len(graph)-1):
    for vertex in graph:
      for neighbour, weight in graph[vertex]:
        new_distance = distances[vertex]+weight

        if new_distance<distances[neighbour]:
          distances[neighbour]=new_distance

  negative_cycle = False
  for vertex in graph:
      for neighbour, weight in graph[vertex]:
        new_distance = distances[vertex]+weight

        if new_distance<distances[neighbour]:
          negative_cycle=True
  
  return distances, negative_cycle