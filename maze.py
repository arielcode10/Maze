from random import shuffle
import pygame

pygame.init()

MAZE_SIZE = 41
maze = [[0 for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]

CELL_SIZE = 15
ROWS = len(maze)
COLS = len(maze[0])

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

VISITED_CELL = 0
UNVISITED_CELL = 1
DISCOVERED_CELL = 2
DONE_CELL = 3

MAZE_EXIT = (MAZE_SIZE - 2, MAZE_SIZE - 1)

stack = []
correct_path = []

# Stores every step taken while generating the maze
build_steps = []

# Stores every cell visited while solving
solve_steps = []


def draw_maze(screen):
    for y in range(ROWS):
        for x in range(COLS):

            if maze[y][x] == VISITED_CELL:
                color = (30, 30, 30)

            elif maze[y][x] == UNVISITED_CELL:
                color = (220, 220, 220)

            elif maze[y][x] == DISCOVERED_CELL:
                color = (0, 200, 50)

            else:
                color = (200, 30, 0)

            pygame.draw.rect(
                screen,
                color,
                (
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
            )

            pygame.draw.rect(
                screen,
                (100, 100, 100),
                (
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                ),
                1
            )


def show_maze_building(screen):

    # Start with a completely empty/walled maze
    for y in range(ROWS):
        for x in range(COLS):
            maze[y][x] = VISITED_CELL

    # Replay the generation steps
    for step in build_steps:

        x, y = step

        maze[y][x] = UNVISITED_CELL

        draw_maze(screen)

        pygame.display.flip()

        pygame.time.wait(5)


def show_maze_solving(screen):

    # Reset all path cells
    for y in range(ROWS):
        for x in range(COLS):

            if maze[y][x] == DONE_CELL:
                maze[y][x] = UNVISITED_CELL

    # Show cells being explored
    for cell in solve_steps:

        x, y = cell

        maze[y][x] = DONE_CELL

        draw_maze(screen)

        pygame.display.flip()

        pygame.time.wait(30)

    # Show final solution
    for cell in correct_path:

        x, y = cell

        maze[y][x] = DISCOVERED_CELL

        draw_maze(screen)

        pygame.display.flip()

        pygame.time.wait(50)


def solve_maze(x, y):

    global correct_path

    stack.append((x, y))

    solve_steps.append((x, y))

    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0)
    ]

    for direct_x, direct_y in directions:

        new_x = direct_x + x
        new_y = direct_y + y

        # Check exit
        if (new_x, new_y) == MAZE_EXIT:

            correct_path = stack.copy()
            correct_path.append((new_x, new_y))

            return True

        # Invalid position
        if new_x <= 0 or new_x >= MAZE_SIZE - 1:
            continue

        if new_y <= 0 or new_y >= MAZE_SIZE - 1:
            continue

        # Not a path
        if maze[new_y][new_x] != UNVISITED_CELL:
            continue

        maze[new_y][new_x] = DONE_CELL

        if solve_maze(new_x, new_y):
            return True

    stack.pop()

    return False


def create_maze(x, y):

    # Record this cell
    build_steps.append((x, y))

    directions = [
        (0, 2),
        (0, -2),
        (2, 0),
        (-2, 0)
    ]

    shuffle(directions)

    for direct_x, direct_y in directions:

        new_x = direct_x + x
        new_y = direct_y + y

        # Invalid position
        if new_x <= 0 or new_x >= MAZE_SIZE - 1:
            continue

        if new_y <= 0 or new_y >= MAZE_SIZE - 1:
            continue

        # Already generated
        if maze[new_y][new_x] == UNVISITED_CELL:
            continue

        wall_x = direct_x // 2 + x
        wall_y = direct_y // 2 + y

        # Remove wall
        maze[wall_y][wall_x] = UNVISITED_CELL

        # Carve new cell
        maze[new_y][new_x] = UNVISITED_CELL

        # Record both the wall and new cell
        build_steps.append((wall_x, wall_y))
        build_steps.append((new_x, new_y))

        create_maze(new_x, new_y)


def create_entrance_exit():

    # Entrance
    maze[0][1] = UNVISITED_CELL

    # Exit
    maze[MAZE_EXIT[1]][MAZE_EXIT[0]] = UNVISITED_CELL


def main():

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze")


    maze[1][1] = UNVISITED_CELL

    create_maze(1, 1)

    create_entrance_exit()

    show_maze_building(screen)
    
    maze[1][1] = DONE_CELL

    solve_maze(1, 1)

    show_maze_solving(screen)

    clock = pygame.time.Clock()

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


main()