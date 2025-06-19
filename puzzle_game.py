import pygame
from PIL import Image
import random
import time

FPS = 30
BUTTON_AREA_HEIGHT = 40
HEADER_HEIGHT = 50
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30
BUTTON_MARGIN = 10

def split_image(path, grid_size, tile_size):
    img = Image.open(path)
    img = img.resize((grid_size * tile_size, grid_size * tile_size))
    tiles = []
    for i in range(grid_size):
        for j in range(grid_size):
            box = (j*tile_size, i*tile_size, (j+1)*tile_size, (i+1)*tile_size)
            tile = img.crop(box)
            tiles.append(tile)
    return tiles

def pil_to_pygame(pil_img):
    return pygame.image.fromstring(pil_img.tobytes(), pil_img.size, pil_img.mode)

def get_tile_index(pos, grid_size, tile_size):
    x, y = pos
    if y < BUTTON_AREA_HEIGHT + HEADER_HEIGHT:
        return None
    y -= (BUTTON_AREA_HEIGHT + HEADER_HEIGHT)
    row = y // tile_size
    col = x // tile_size
    if row >= grid_size or col >= grid_size:
        return None
    return row * grid_size + col

def is_solved(positions):
    return positions == list(range(len(positions)))

def show_win(screen, font, move_count, total_time, full_image_surface, grid_size, tile_size):
    screen.fill((255, 255, 255))
    screen.blit(full_image_surface, (0, BUTTON_AREA_HEIGHT + HEADER_HEIGHT))

    overlay = pygame.Surface((grid_size*tile_size, 100))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, BUTTON_AREA_HEIGHT + HEADER_HEIGHT + (grid_size*tile_size)//2 - 50))

    text1 = font.render("🎉 You Win! 🎉", True, (255, 255, 255))
    text2 = font.render(f"🕒 Time: {int(total_time)}s | 🔁 Moves: {move_count}", True, (255, 255, 255))

    screen.blit(text1, text1.get_rect(center=(grid_size*tile_size // 2, BUTTON_AREA_HEIGHT + HEADER_HEIGHT + (grid_size*tile_size) // 2 - 20)))
    screen.blit(text2, text2.get_rect(center=(grid_size*tile_size // 2, BUTTON_AREA_HEIGHT + HEADER_HEIGHT + (grid_size*tile_size) // 2 + 20)))

    pygame.display.flip()
    time.sleep(3)

def draw_buttons(screen):
    restart_rect = pygame.Rect(BUTTON_MARGIN, 5, BUTTON_WIDTH, BUTTON_HEIGHT)
    back_rect = pygame.Rect(BUTTON_MARGIN + BUTTON_WIDTH + 10, 5, BUTTON_WIDTH, BUTTON_HEIGHT)

    pygame.draw.rect(screen, (200, 200, 200), restart_rect, border_radius=5)
    pygame.draw.rect(screen, (200, 200, 200), back_rect, border_radius=5)

    font = pygame.font.SysFont("arial", 18)
    restart_text = font.render("🔄 Restart", True, (0, 0, 0))
    back_text = font.render("🔙 Back", True, (0, 0, 0))

    screen.blit(restart_text, (restart_rect.x + 15, restart_rect.y + 5))
    screen.blit(back_text, (back_rect.x + 25, back_rect.y + 5))

    return restart_rect, back_rect

def draw_header_with_status(screen, font, move_count, elapsed_time, grid_size, tile_size):
    header_rect = pygame.Rect(0, BUTTON_AREA_HEIGHT, grid_size * tile_size, HEADER_HEIGHT)
    pygame.draw.rect(screen, (70, 130, 180), header_rect)

    title_text = font.render("🎉 Puzzle Game 🎉", True, (255, 255, 255))
    screen.blit(title_text, (10, BUTTON_AREA_HEIGHT + (HEADER_HEIGHT - title_text.get_height()) // 2))

    move_text = font.render(f"Moves: {move_count}", True, (255, 255, 255))
    move_pos_x = grid_size * tile_size - move_text.get_width() - 150
    screen.blit(move_text, (move_pos_x, BUTTON_AREA_HEIGHT + (HEADER_HEIGHT - move_text.get_height()) // 2))

    time_text = font.render(f"Time: {elapsed_time}s", True, (255, 255, 255))
    time_pos_x = grid_size * tile_size - time_text.get_width() - 20
    screen.blit(time_text, (time_pos_x, BUTTON_AREA_HEIGHT + (HEADER_HEIGHT - time_text.get_height()) // 2))

def main(image_path, grid_size):
    TILE_SIZE = 150
    WINDOW_WIDTH = grid_size * TILE_SIZE
    WINDOW_HEIGHT = grid_size * TILE_SIZE + HEADER_HEIGHT + BUTTON_AREA_HEIGHT

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Puzzle Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)

    pil_tiles = split_image(image_path, grid_size, TILE_SIZE)
    blank_index = len(pil_tiles) - 1
    pil_tiles[blank_index] = Image.new("RGB", (TILE_SIZE, TILE_SIZE), color=(0, 0, 0))
    pygame_tiles = [pil_to_pygame(tile) for tile in pil_tiles]

    full_img_pil = Image.open(image_path).resize((WINDOW_WIDTH, WINDOW_WIDTH))
    full_image_surface = pil_to_pygame(full_img_pil)

    positions = list(range(len(pil_tiles)))
    while True:
        random.shuffle(positions)
        if not is_solved(positions):
            break

    selected = []
    move_count = 0
    start_time = time.time()
    running = True

    while running:
        screen.fill((255, 255, 255))

        elapsed_time = int(time.time() - start_time)
        restart_rect, back_rect = draw_buttons(screen)
        draw_header_with_status(screen, font, move_count, elapsed_time, grid_size, TILE_SIZE)

        for idx, pos in enumerate(positions):
            tile = pygame_tiles[pos]
            x = (idx % grid_size) * TILE_SIZE
            y = (idx // grid_size) * TILE_SIZE + HEADER_HEIGHT + BUTTON_AREA_HEIGHT
            screen.blit(tile, (x, y))

            if idx in selected:
                pygame.draw.rect(screen, (0, 150, 255), (x, y, TILE_SIZE, TILE_SIZE), 5)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if restart_rect.collidepoint(mouse_pos):
                    # রিস্টার্ট গেম (main ফিরিয়ে কল)
                    return main(image_path, grid_size)

                elif back_rect.collidepoint(mouse_pos):
                    running = False
                    # pygame.quit() এখানে করবেনা! (home_page.py তেই হ্যান্ডেল হবে)
                    return 'back_to_home'

                else:
                    click_idx = get_tile_index(mouse_pos, grid_size, TILE_SIZE)
                    if click_idx is not None:
                        if click_idx in selected:
                            selected.remove(click_idx)
                        else:
                            selected.append(click_idx)

                        if len(selected) == 2:
                            positions[selected[0]], positions[selected[1]] = positions[selected[1]], positions[selected[0]]
                            selected = []
                            move_count += 1

                            if is_solved(positions):
                                show_win(screen, font, move_count, time.time() - start_time, full_image_surface, grid_size, TILE_SIZE)
                                # গেম শেষ, আবার শুরু করা যাবে
                                return 'back_to_home'

    #pygame.quit()
