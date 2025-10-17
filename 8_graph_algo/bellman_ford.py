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

  for _ in range(len(graph)):
    for vertex in graph:
      for neighbour, weight in graph[vertex]:
        new_distance = distances[vertex]+weight

        if new_distance<distances[neighbour]:
          distances[neighbour]=-math.inf

  for vertex in distances:
    if distances[vertex]==math.inf:
      distances[vertex]=-1
    elif distances[vertex]==-math.inf:
      distances[vertex]=100000000
  
  return distances