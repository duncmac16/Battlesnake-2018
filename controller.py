import a_star, graph, math, sys

def setup(food, width, height, snakes):

    generic_grid = []
    #General grid setup
    for x in range(0, width):
        new_list = []
        for y in range(0, height):
            new_list.append(None)
        generic_grid.append(new_list)

    food_grid = generic_grid[:][:]
    general_grid = generic_grid[:][:]
    snake_grid = generic_grid[:][:]

    #Food locations
    for [x, y] in food:
        food_grid[x][y] = 1
        general_grid[x][y] = 1

    #Snake locations:
    for snake in snakes:
        current_snake_coordinates = snake.get('coords')
        for [x, y] in current_snake_coordinates:
            snake_grid[x][y] = 1
            general_grid[x][y] = 1

    grid_options = []

    grid_options.append(snake_grid)
    grid_options.append(food_grid)
    grid_options.append(general_grid)

    return grid_options

def get_my_snake_coordinates(snakes, your_id):
    for snake in snakes:
        if snake.get('id') == your_id:
            return snake.get('coords')

#NOTE returns a position tuple of closest food pellet
def get_closest_food(food_grid, head_x, head_y):
    current_minimum = 10000
    for position in food_grid:
        print('head x: {}'.format(head_x))
        print('head y: {}'.format(head_y))
        print('Target: {}'.format(position))
        pellet_distance = a_star.euclidean((head_x, head_y),position)
        if pellet_distance < current_minimum:
            current_minimum = pellet_distance
            target_position = position
    return target_position

def get_move_letter(start, end):
    currX = start[0]
    currY = start[1]
    nextX = end[0]
    nextY = end[1]
    deltaX = nextX - currX
    deltaY = nextY - currY
    if deltaX > 0: return 'right'
    elif deltaY > 0: return 'up'
    elif deltaX < 0: return 'left'
    elif deltaY < 0: return 'down'
    else: return 'right'


def get_move(grid_options, target, head_x, head_y, height, width):
    path = a_star.a_star(grid_options[0], (head_x, head_y), target, height, width)
    print(grid_options[0])
    if path:
        desired_next_position = path[1] #NOTE the 0'th coordinate is the current position
    else:
        return "left"

    return get_move_letter((head_x, head_y), desired_next_position)
