import pygame
import random
import os

pygame.init()

# Constants
TILE_SIZE = 120
GRID_SIZE = 6  # 6x6 = 36 tiles
WIDTH, HEIGHT = TILE_SIZE * GRID_SIZE, TILE_SIZE * GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game - 18 Cars")

# Load images from both folders
image_folder1 = "images"
image_folder2 = "images1"

car_images1 = [pygame.image.load(os.path.join(image_folder1, f"button{i}.png")) for i in range(1, 10)]
car_images2 = [pygame.image.load(os.path.join(image_folder2, f"button{i}.png")) for i in range(1, 10)]

car_images = car_images1 + car_images2  # Total 18 images
car_images = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in car_images]

# Create pairs and shuffle
tiles = car_images * 2  # 18 pairs = 36 tiles
random.shuffle(tiles)

# Game state
revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
matched = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
first_selection = None
cursor_row, cursor_col = 0, 0
clock = pygame.time.Clock()
running = True

def draw_board():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            tile_index = row * GRID_SIZE + col

            pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 2)

            if revealed[row][col] or matched[row][col]:
                image = tiles[tile_index]
                if image:
                    screen.blit(image, (x, y))

    # Highlight current cursor position
    highlight_x = cursor_col * TILE_SIZE
    highlight_y = cursor_row * TILE_SIZE
    pygame.draw.rect(screen, (255, 0, 0), (highlight_x, highlight_y, TILE_SIZE, TILE_SIZE), 4)

def get_tile(pos):
    x, y = pos
    return y // TILE_SIZE, x // TILE_SIZE

while running:
    screen.fill((200, 200, 200))
    draw_board()
    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_tile(pygame.mouse.get_pos())
            tile_index = row * GRID_SIZE + col

            if not revealed[row][col] and not matched[row][col]:
                revealed[row][col] = True

                if first_selection is None:
                    first_selection = (row, col)
                else:
                    r1, c1 = first_selection
                    r2, c2 = row, col
                    i1 = r1 * GRID_SIZE + c1
                    i2 = r2 * GRID_SIZE + c2
                    if tiles[i1] == tiles[i2] and tiles[i1] is not None:
                        matched[r1][c1] = True
                        matched[r2][c2] = True
                    else:
                        pygame.time.delay(500)
                        revealed[r1][c1] = False
                        revealed[r2][c2] = False
                    first_selection = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                cursor_row = (cursor_row - 1) % GRID_SIZE
            elif event.key == pygame.K_DOWN:
                cursor_row = (cursor_row + 1) % GRID_SIZE
            elif event.key == pygame.K_LEFT:
                cursor_col = (cursor_col - 1) % GRID_SIZE
            elif event.key == pygame.K_RIGHT:
                cursor_col = (cursor_col + 1) % GRID_SIZE
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                row, col = cursor_row, cursor_col
                tile_index = row * GRID_SIZE + col

                if not revealed[row][col] and not matched[row][col]:
                    revealed[row][col] = True

                    if first_selection is None:
                        first_selection = (row, col)
                    else:
                        r1, c1 = first_selection
                        r2, c2 = row, col
                        i1 = r1 * GRID_SIZE + c1
                        i2 = r2 * GRID_SIZE + c2
                        if tiles[i1] == tiles[i2] and tiles[i1] is not None:
                            matched[r1][c1] = True
                            matched[r2][c2] = True
                        else:
                            pygame.time.delay(500)
                            revealed[r1][c1] = False
                            revealed[r2][c2] = False
                        first_selection = None

pygame.quit()