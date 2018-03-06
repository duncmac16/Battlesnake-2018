import astar, math, sys, random

def grid_setup(food, width, height, snakes, mySnake, mySnakeID):

    generic_grid = []
    #General grid setup
    for y in range(0, height):
        new_list = []
        for x in range(0, width):
            new_list.append(1)
        generic_grid.append(new_list)

    food_grid = []
    #Food locations
    for point in food:
        locationX = point.get("x")
        locationY = point.get("y")
        food_grid.append([locationX, locationY])

    #Snake locations:
    for snake in snakes:
        body = snake.get("body").get("data")
        snakeID = snake.get("id")
        if snakeID != mySnakeID:
            head = body[0]
            headX = head.get("x")
            headY = head.get("y")

            top = headY - 1
            bottom = headY + 1
            left = headX - 1
            right = headX + 1

            if top > 0:
                generic_grid[top][headX] = 0
            if bottom < height:
                generic_grid[bottom][headX] = 0
            if left > 0:
                generic_grid[headY][left] = 0
            if right < width:
                generic_grid[headY][right] = 0

        for point in body:
            pointX = point.get("x")
            pointY = point.get("y")
            #print("new point Y = {}, new point X = {} grid x length = {}, grid y length = {}".format(pointY, pointX,len(generic_grid[0]), len(generic_grid)))
            generic_grid[pointY][pointX] = 0

    grid_options = []

    grid_options.append(generic_grid)
    grid_options.append(food_grid)

    '''print('')
    for y in range(0, width):
        print('')
        for x in range(0, height):
            if generic_grid[y][x] == 0 :
                print('X', end='')
            else:
                print('0', end='')'''

    return grid_options

def get_crows_dist(me, you):
    (x1, y1) = me
    (x2, y2) = you
    return abs(math.hypot(x2 - x1, y2 - y1))

def get_my_snake_coordinates(snakes, your_id):
    for snake in snakes:
        if snake.get('id') == your_id:
            return snake.get('coords')

#NOTE returns a position tuple of closest food pellet
def get_closest_food(food_list, head_x, head_y):
    current_minimum = 10000
    for position in food_list:
        pellet_distance = get_crows_dist((head_x, head_y),position)
        if pellet_distance < current_minimum:
            current_minimum = pellet_distance
            target_position = position
    return tuple(target_position)

def get_neighbors(node, lines, height, width):
    (x, y) = node #changed from x, y
    return[(nx, ny) for nx, ny in[(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if 0 <= nx < width and 0 <= ny < height and lines[ny][nx] == 1]

def get_move_letter(start, end):
    currX = start[0]
    currY = start[1]
    nextX = end[0]
    nextY = end[1]
    deltaX = nextX - currX
    deltaY = nextY - currY
    if deltaX > 0:
        return 'right'
    elif deltaY > 0:
        return 'down'
    elif deltaX < 0:
        return 'left'
    elif deltaY < 0:
        return 'up'


def move_to_food(a_star_object, food_list, head_x, head_y):
    current_minimum = float('inf')
    current_path = None
    for food in food_list:
        path = a_star_object.astar((head_x, head_y), tuple(food))
        if path:
            path = list(path)
            if len(path) < current_minimum:
                current_minimum = len(path)
                current_path = path
    if current_path:
        return get_move_letter((head_x, head_y), list(current_path)[1])
    return None

def chase_tail(a_star_object, grid_options, mySnake, head_x, head_y, isGonnaGrow, height, width):
    myTail = (mySnake[-1].get("x"), mySnake[-1].get("y"))
    grid_options[0][myTail[1]][myTail[0]] = 1
    path = a_star_object.astar((head_x, head_y), myTail)
    grid_options[0][myTail[1]][myTail[0]] = 0
    if path:
        if not isGonnaGrow:
            return get_move_letter((head_x, head_y), list(path)[1])
        else:
            neighbours = get_neighbors(myTail, grid_options[0], height, width)
            for neighbour in neighbours:
                path = a_star_object.astar((head_x, head_y), neighbour)
                if path:
                    return get_move_letter((head_x, head_y), list(path)[1])


    return None

def get_move(grid_options, target, head_x, head_y, height, width, mySnake, myHealth):
    a_star_object = astar.AStarAlgorithm(grid_options[0], width, height)

    myLength = len(mySnake)
    move = move_to_food(a_star_object, grid_options[1], head_x, head_y)

    #NOTE FIND TAIL MODE
    if myLength > 3 and myHealth > 75 or move == None: #85
        gonnaGrow = False
        if myHealth == 100:
            gonnaGrow = True
        move = chase_tail(a_star_object, grid_options, mySnake, head_x, head_y, gonnaGrow, height, width)


    if move:
        return move
    else:
        neighbours = get_neighbors((head_x, head_y), grid_options[0], height, width)
        if neighbours:
            return get_move_letter((head_x, head_y), neighbours[0])
        else:
            return 'left'
