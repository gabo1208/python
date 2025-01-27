arr = [3, 5, 7, 1, 2, 4, 6, 10]

# find the shortest path from to an element from an starting position, either going step by step to the left
# or to the right, it is like a circular array. If the element is not in the array return -1 or it is in the starting
# position, return 0


def find_path_right(starting_pos, elem):
    n = len(arr)
    current_index = starting_pos
    path = 0
    for i in range(0, n):
        if arr[current_index] == elem:
            return path
        current_index = (current_index + 1) % n
        path += 1

    return -1


def find_path_left(starting_pos, elem):
    current_index = starting_pos
    path = 0
    for i in range(0, len(arr)):
        if arr[current_index] == elem:
            return path

        current_index = current_index - 1
        path += 1

    return -1


def find_shortest_path(starting_pos, elem):
    return min(find_path_right(starting_pos, elem), find_path_left(starting_pos, elem))


print(find_shortest_path(0, 6))
print(find_shortest_path(3, 6))
print(find_shortest_path(0, 3))
print(find_shortest_path(0, 1000))
