import pygame, random
import numpy as np

# Colors

EMPTY_CELL_COLOR = (0, 0, 0) #(213, 196, 161) # Sand
GRID_COLOR = (0, 0, 0) # Black-ish

FRAMES_PER_SECOND = 60
SPEED = 1
STARVATION_VALUE = 2

ALFA = 0.01 # 0 to 1
BETA = 1 # 0 to 1

SUSCEPTIBLE_COUNT = 5000
INFECTED_COUNT = 100
RECOVERED_COUNT = 0

SUSCEPTIBLE_COLOR = (31, 119, 180) # Blue
INFECTED_COLOR = (255, 127, 15) # Orange
RECOVERED_COLOR = (45, 160, 45) # Green

def new_susceptible():
    return {
        'type': 'susceptible',
        'color': SUSCEPTIBLE_COLOR,
    }

def new_infected():
    return {
        'type': 'infected',
        'color': INFECTED_COLOR,
    }

def new_recovered():
    return {
        'type': 'recovered',
        'color': RECOVERED_COLOR,
    }

def new_empty():
    return {
        'type': 'empty',
    }

def initialize_grid(cell_count_x, cell_count_y):
    content_list = []

    for i in range(SUSCEPTIBLE_COUNT):
        content_list.append(new_susceptible())
    for i in range(INFECTED_COUNT):
        content_list.append(new_infected())
    for i in range(RECOVERED_COUNT):
        content_list.append(new_recovered())
    for i in range((cell_count_x * cell_count_y - SUSCEPTIBLE_COUNT - INFECTED_COUNT - RECOVERED_COUNT)):
        content_list.append(new_empty())

    random.shuffle(content_list)

    content_1Darray = np.array(content_list)
    grid = np.reshape(content_1Darray, (cell_count_y, cell_count_x)) # First argument is for which row, the second arg. is for which column in that row

    return grid

def get_neighbours(grid, row_index, column_index):
    # collects the indexes of the neighbouring cells
    row_min, column_min = 0, 0
    row_max, column_max = grid.shape
    row_max, column_max = row_max - 1, column_max - 1 # it's off by one
    # r-1,c-1 | r-1,c  | r-1,c+1
    # --------|--------|---------
    # r  ,c-1 | r  ,c  | r  ,c+1
    # --------|--------|---------
    # r+1,c-1 | r+1,c  | r+1,c+1
    neighbours = []

    # r-1:
    if row_index - 1 >= row_min :
        if column_index - 1 >= column_min: neighbours.append((row_index - 1, column_index - 1))
        neighbours.append((row_index - 1, column_index))  # c is inside the grid
        if column_index + 1 <= column_max: neighbours.append((row_index - 1, column_index + 1))
    # r:
    if column_index - 1 >= column_min: neighbours.append((row_index, column_index - 1))
    # skip center (r,c) since we are listing its neighbour positions
    if column_index + 1 <= column_max: neighbours.append((row_index, column_index + 1))
    # r+1:
    if row_index + 1 <= row_max:
        if column_index - 1 >= column_min: neighbours.append((row_index + 1, column_index - 1))
        neighbours.append((row_index + 1, column_index))  # c is inside cur
        if column_index + 1 <= column_max: neighbours.append((row_index + 1, column_index + 1))
    return neighbours

def sort_neighbours(grid, neighbours):
    susceptible_neighbours = []
    infected_neighbours = []
    recovered_neighbours = []
    empty_neighbours = []

    for neighbour in neighbours:
        if grid[neighbour]['type'] == 'susceptible':
            susceptible_neighbours.append(neighbour)
        elif grid[neighbour]['type'] == 'infected':
            infected_neighbours.append(neighbour)
        elif grid[neighbour]['type'] == 'recovered':
            recovered_neighbours.append(neighbour)
        elif grid[neighbour]['type'] == 'empty':
            empty_neighbours.append(neighbour)

    return susceptible_neighbours, infected_neighbours, recovered_neighbours, empty_neighbours

def susceptible_rules(grid, row_index, column_index, infected_neighbours, empty_neighbours):
    random_number = random.random()
    
    if (random_number <= (BETA * ((9 - len(infected_neighbours)) % 9))):
        grid[row_index, column_index] = new_infected()

    row_index_new, column_index_new = random.choice(empty_neighbours)
    grid[row_index_new, column_index_new] = grid[row_index, column_index]
    grid[row_index, column_index] = new_empty()

    # # if the fish is older for it to be able to breed, change the color
    # if (grid[row_index, column_index]['age'] >= FISH_BREED_AGE):
    #     grid[row_index, column_index]['color'] = BREEDING_FISH_COLOR
    # else:
    #     grid[row_index, column_index]['color'] = YOUNG_FISH_COLOR

    # # if the fish is about to die, change the color
    # if grid[row_index, column_index]['food'] <= STARVATION_VALUE:
    #     grid[row_index, column_index]['color'] = STARVING_FISH_COLOR

    # # if there is a plant, eat it
    # if len(plant_neighbours) > 0:
    #     grid[row_index, column_index]['food'] = INITIAL_FISH_FOOD
    #     row_index_plant, column_index_plant = random.choice(plant_neighbours)
    #     plant_neighbours.remove((row_index_plant, column_index_plant))
    #     empty_neighbours.append((row_index_plant, column_index_plant))
    #     grid[row_index_plant, column_index_plant] = new_empty()
    # else:
    #     grid[row_index, column_index]['food'] -= 1

    # # breeding time
    # if (grid[row_index, column_index]['age'] >= FISH_BREED_AGE and len(empty_neighbours) > 0):
    #     # fish breeds to an empty cell
    #     row_index_new, column_index_new = random.choice(empty_neighbours)
    #     grid[row_index_new, column_index_new] = new_fish()
    #     fish_neighbours.append((row_index_new, column_index_new))
    #     empty_neighbours.remove((row_index_new, column_index_new))

    # # fish dies (overcrowding or starving or natural death from probability)
    # if (len(fish_neighbours) >= FISH_OVERCROWDING) or (grid[row_index, column_index]['food'] <= 0):
    #     grid[row_index, column_index] = new_empty()
    # else:
    #     random_number = random.randint(7, 60) # Determines whether the fish dies of natural causes or not :)
    #     fish_age = grid[row_index, column_index]['age']

    #     if (random_number <= fish_age):
    #         grid[row_index, column_index] = new_empty()
    #     elif (len(empty_neighbours) > 0):
    #         # move the fish to an empty cell
    #         row_index_new, column_index_new = random.choice(empty_neighbours)
    #         grid[row_index_new, column_index_new] = grid[row_index, column_index]
    #         grid[row_index, column_index] = new_empty()

    return grid

def infected_rules(grid, row_index, column_index, empty_neighbours):
    random_number = random.random()
    
    if (random_number <= ALFA):
        grid[row_index, column_index] = new_recovered()

    row_index_new, column_index_new = random.choice(empty_neighbours)
    grid[row_index_new, column_index_new] = grid[row_index, column_index]
    grid[row_index, column_index] = new_empty()

    return grid

def recovered_rules(grid, row_index, column_index, empty_neighbours):
    row_index_new, column_index_new = random.choice(empty_neighbours)
    grid[row_index_new, column_index_new] = grid[row_index, column_index]
    grid[row_index, column_index] = new_empty()

    return grid
# def bear_rules(grid, row_index, column_index, fish_neighbours, empty_neighbours):
#     # if the bear is older for it to be able to breed, change the color
#     if grid[row_index, column_index]['age'] >= BEAR_BREED_AGE:
#         grid[row_index, column_index]['color'] = BREEDING_BEAR_COLOR
#     else:
#         grid[row_index, column_index]['color'] = YOUNG_BEAR_COLOR

#     # if the bear is about to starve, change the color
#     if grid[row_index, column_index]['food'] <= STARVATION_VALUE:
#         grid[row_index, column_index]['color'] = STARVING_BEAR_COLOR

#     # if there is a fish eat it
#     if len(fish_neighbours) > 0:
#         grid[row_index, column_index]['food'] = INITIAL_BEAR_FOOD
#         row_index_fish, column_index_fish = random.choice(fish_neighbours)
#         fish_neighbours.remove((row_index_fish, column_index_fish))
#         empty_neighbours.append((row_index_fish, column_index_fish))
#         grid[row_index_fish, column_index_fish] = new_empty()
#     else:
#         grid[row_index, column_index]['food'] -= 1

#     # if the bear starves it dies
#     if grid[row_index, column_index]['food'] <= 0:
#         grid[row_index, column_index] = new_empty()
#     else:  # if the bear is not dead it, first, it tries to breed
#         if grid[row_index, column_index]['age'] >= BEAR_BREED_AGE and len(empty_neighbours) > 0:
#             # bear breeds to an empty cell
#             row_index_new, column_index_new = random.choice(empty_neighbours)
#             grid[row_index_new, column_index_new] = new_bear()
#             empty_neighbours.remove((row_index_new, column_index_new))

#         random_number = random.randint(9, 40) # Determines whether the bear dies of natural causes or not :)
#         bear_age = grid[row_index, column_index]['age']

#         if (random_number <= bear_age):
#             grid[row_index, column_index] = new_empty()
#         elif len(empty_neighbours) > 0: # it tries to move to an empty cell
#             row_index_new, column_index_new = random.choice(empty_neighbours)
#             grid[row_index_new, column_index_new] = grid[row_index, column_index]
#             grid[row_index, column_index] = new_empty()

#     return grid

# def plant_rules(grid, row_index, column_index, plant_neighbours, empty_neighbours):
#     # if the plant is older for it to be able to spread, change the color
#     if (grid[row_index, column_index]['age'] >= PLANT_SPREADING_AGE):
#         grid[row_index, column_index]['color'] = SPREADING_PLANT_COLOR
#     else:
#         grid[row_index, column_index]['color'] = YOUNG_PLANT_COLOR

#     # plant spreads
#     if (grid[row_index, column_index]['age'] >= PLANT_SPREADING_AGE and len(empty_neighbours) > 0):
#         # plant spread to an empty cell
#         row_index_new, column_index_new = random.choice(empty_neighbours)
#         grid[row_index_new, column_index_new] = new_plant()
#         plant_neighbours.append((row_index_new, column_index_new))
#         empty_neighbours.remove((row_index_new, column_index_new))

#     # plant has a chance to die from overcrowding or natural causes :)
#     if (len(plant_neighbours) >= PLANT_OVERCROWDING):
#         grid[row_index, column_index] = new_empty()
#     else:
#         random_number = random.randint(7, 60) # Determines whether the plants dies of natural causes or not :)
#         plant_age = grid[row_index, column_index]['age']

#         if (random_number <= plant_age):
#             grid[row_index, column_index] = new_empty()

#     return grid

def update_grid(grid):
    # for each cell
    for row_index, column_index in np.ndindex(grid.shape):
        # if the cell is not empty
        if (grid[row_index, column_index]['type'] != 'empty'):
            # calculate neighbours and sort them
            neighbours = get_neighbours(grid, row_index, column_index)
            susceptible_neighbours, infected_neighbours, recovered_neighbours, empty_neighbours = sort_neighbours(grid, neighbours)

            if (grid[row_index, column_index]['type'] == 'susceptible'):
                grid = susceptible_rules(grid, row_index, column_index, infected_neighbours, empty_neighbours)

            if (grid[row_index, column_index]['type'] == 'infected'):
                grid = infected_rules(grid, row_index, column_index, empty_neighbours)

            if (grid[row_index, column_index]['type'] == 'recovered'):
                grid = recovered_rules(grid, row_index, column_index, empty_neighbours)

            # # if it is a bear
            # elif (grid[row_index, column_index]['type'] == 'bear'):
            #     grid = bear_rules(grid, row_index, column_index, fish_neighbours, empty_neighbours)

            # # if it is a plant
            # elif (grid[row_index, column_index]['type'] == 'plant'):
            #     grid = plant_rules(grid, row_index, column_index, plant_neighbours, empty_neighbours)
    return grid

def draw_grid(surface, grid, cell_size):
    for row_index, column_index in np.ndindex(grid.shape):
        cell_color = EMPTY_CELL_COLOR
        if grid[row_index, column_index]['type'] != 'empty':
            cell_color = grid[row_index, column_index]['color']
        pygame.draw.rect(surface, cell_color, (column_index * cell_size, row_index * cell_size, cell_size - 1, cell_size - 1))

def main(cell_count_x, cell_count_y, cell_size):
    pygame.init()
    surface = pygame.display.set_mode((cell_count_x * cell_size, cell_count_y * cell_size))
    pygame.display.set_caption("Covid-19 spread")

    grid = initialize_grid(cell_count_x, cell_count_y)

    clock = pygame.time.Clock()
    speed_count = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        surface.fill(GRID_COLOR)
        if (speed_count % SPEED == 0):
            grid = update_grid(grid)
        draw_grid(surface, grid, cell_size)
        pygame.display.update()
        clock.tick(FRAMES_PER_SECOND)
        speed_count += 1

if __name__ == "__main__":
    cell_count_x = 200 # 40
    cell_count_y = 200 # 10
    cell_size = 6 # 16

    main(cell_count_x, cell_count_y, cell_size)
