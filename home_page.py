import pygame
import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import sys
import puzzle_game

pygame.init()
pygame.font.init()

# BackGround Music
pygame.mixer.init()
pygame.mixer.music.load("click.mp3")  # Ensure this file is in the same folder
pygame.mixer.music.play(-1)  # Loop indefinitely

# Screen Setting
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puzzle Game - Home")

# Fonts
font = pygame.font.SysFont("Arial", 32)
small_font = pygame.font.SysFont("Arial", 24)

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (70, 130, 180)

COLOR_TOP = (255, 200, 200)
COLOR_BOTTOM = (200, 180, 255)

clock = pygame.time.Clock()

# Tkinter root for file dialog
root = tk.Tk()
root.withdraw()

# Button scales for smooth hover
button_scales = {
    "browse": 1.0,
    "Easy": 1.0,
    "Medium": 1.0,
    "Hard": 1.0,
    "start": 1.0,
    "back": 1.0,
}

def draw_gradient_background(surface, top_color, bottom_color):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

def animate_scale(name, hover, selected=False):
    speed = 0.1
    target = 1.1 if hover or selected else 1.0
    current = button_scales[name]
    if abs(current - target) > 0.01:
        if current < target:
            button_scales[name] += speed
        else:
            button_scales[name] -= speed
    else:
        button_scales[name] = target

def draw_text_center(surface, text, y, font, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    x = (WIDTH - text_surface.get_width()) // 2
    surface.blit(text_surface, (x, y))

def draw_button(surface, rect, text, scale=1.0, is_selected=False):
    center = rect.center
    w, h = rect.size
    new_w, new_h = int(w * scale), int(h * scale)
    new_rect = pygame.Rect(0, 0, new_w, new_h)
    new_rect.center = center

    color = BLUE if is_selected else GRAY
    pygame.draw.rect(surface, color, new_rect, border_radius=6)
    pygame.draw.rect(surface, DARK_GRAY, new_rect, 2, border_radius=6)

    text_surface = small_font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=new_rect.center)
    surface.blit(text_surface, text_rect)

def draw_file_name_box(surface, filename):
    box_width = 350
    box_height = 40
    x = (WIDTH - box_width) // 2
    y = 135

    pygame.draw.rect(surface, (240, 240, 240), (x, y, box_width, box_height), border_radius=6)
    pygame.draw.rect(surface, (200, 200, 200), (x, y, box_width, box_height), 2, border_radius=6)

    if len(filename) > 40:
        display_name = "..." + filename[-37:]
    else:
        display_name = filename

    text_surface = small_font.render(display_name, True, (0, 0, 0))
    surface.blit(text_surface, (x + 10, y + (box_height - text_surface.get_height()) // 2))

def draw_image_box(surface, image_path):
    box_width = 300
    box_height = 220
    x = (WIDTH - box_width) // 2
    y = 190

    pygame.draw.rect(surface, (230, 230, 230), (x, y, box_width, box_height), border_radius=10)
    pygame.draw.rect(surface, (180, 180, 180), (x, y, box_width, box_height), 2, border_radius=10)

    try:
        img = pygame.image.load(image_path)
        img_w, img_h = img.get_size()
        scale = min(box_width / img_w, box_height / img_h)
        new_w, new_h = int(img_w * scale), int(img_h * scale)
        img = pygame.transform.scale(img, (new_w, new_h))

        img_x = x + (box_width - new_w) // 2
        img_y = y + (box_height - new_h) // 2
        surface.blit(img, (img_x, img_y))
    except Exception:
        error_text = small_font.render("Image load error", True, (255, 0, 0))
        surface.blit(error_text, (x + 10, y + 10))

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    return file_path

def main_home_page():
    running = True
    image_path = None
    level = "Easy"

    # Buttons
    browse_button = pygame.Rect(WIDTH//2 - 100, 80, 200, 40)
    level_buttons = {
        "Easy": pygame.Rect(250, 445, 100, 40),
        "Medium": pygame.Rect(370, 445, 100, 40),
        "Hard": pygame.Rect(490, 445, 100, 40),
    }
    start_button = pygame.Rect(WIDTH//2 - 100, 510, 200, 50)

    # Back button (top-left corner)
    back_button = pygame.Rect(20, 20, 70, 40)  # আকার সামঞ্জস্য করতে পারেন

    while running:
        draw_gradient_background(screen, COLOR_TOP, COLOR_BOTTOM)

        draw_text_center(screen, "🧩 Image Puzzle Game 🧩", 20, font, color=(50, 20, 60))

        mouse_pos = pygame.mouse.get_pos()

        # Animate buttons hover & selected scale
        animate_scale("browse", browse_button.collidepoint(mouse_pos))
        for lvl in level_buttons:
            animate_scale(lvl, level_buttons[lvl].collidepoint(mouse_pos), selected=(lvl == level))
        animate_scale("start", start_button.collidepoint(mouse_pos))
        animate_scale("back", back_button.collidepoint(mouse_pos))

        # Draw buttons with scale and selected effect
        draw_button(screen, browse_button, "📂 Browse Image", scale=button_scales["browse"])

        if image_path:
            filename = os.path.basename(image_path)
            draw_file_name_box(screen, filename)
            draw_image_box(screen, image_path)

        draw_text_center(screen, "Select Difficulty:", 410, small_font, color=(80, 40, 70))

        for lvl, rect in level_buttons.items():
            draw_button(screen, rect, lvl, scale=button_scales[lvl], is_selected=(lvl == level))

        draw_button(screen, start_button, "▶️ Start Game", scale=button_scales["start"])

        # Draw Back button with a symbol or text (e.g., "< Back")
        back_text_surface = small_font.render("< Back", True, (0, 0, 0))
        back_rect = back_text_surface.get_rect(center=back_button.center)
        pygame.draw.rect(screen, GRAY, back_button, border_radius=6)
        pygame.draw.rect(screen, DARK_GRAY, back_button, 2, border_radius=6)
        screen.blit(back_text_surface, back_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if browse_button.collidepoint(event.pos):
                    selected = select_image()
                    if selected:
                        image_path = selected

                for lvl, rect in level_buttons.items():
                    if rect.collidepoint(event.pos):
                        level = lvl

                if start_button.collidepoint(event.pos):
                    if image_path:
                        grid_size = {"Easy": 3, "Medium": 4, "Hard": 5}[level]
                        puzzle_game.main(image_path, grid_size)

                if back_button.collidepoint(event.pos):
                    pygame.quit()
                    # subprocess দিয়ে game_menu.py চালানো
                    try:
                        subprocess.Popen([sys.executable, "game_menu.py"])
                    except Exception as e:
                        print("Back button error:", e)
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main_home_page()




