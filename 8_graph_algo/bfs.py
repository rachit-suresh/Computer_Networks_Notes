from collections import deque


def bsf(graph, start_vertex):
  visited = set()
  queue = deque()
  
  queue.append(start_vertex)
  visited.add(start_vertex)

  bfs_traversal = []

  while len(queue)>0:
    current_vertex = queue.popleft()
    bfs_traversal.append(current_vertex)

    neighbours = graph[current_vertex]
    for neighbour in neighbours:
      if neighbour not in visited:
        queue.append(start_vertex)
        visited.add(neighbour)

  return bfs_traversal
