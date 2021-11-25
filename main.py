import collections
import itertools
import math
import pygame
import time
import ray
from cells import Cells
from cell_objects import CellObjects

global num_cells_list
global num_cells_index
global num_cells
global cell_width
global cell_offset
global win_width
global win_height
global x_center
global y_center
global x_camera
global y_camera

time_between_steps = 0.125
delta = (0, 0)



def prime_factors(n):
    i = 2
    while i * i <= n:
        if n % i == 0:
            n /= i
            yield i
        else:
            i += 1
    if n > 1:
        yield n


def prod(iterable):
    result = 1
    for i in iterable:
        result *= i
    return result


def get_divisors(n):
    pf = prime_factors(n)
    pf_with_multiplicity = collections.Counter(pf)
    powers = [
        [factor ** i for i in range(count + 1)]
        for factor, count in pf_with_multiplicity.items()
    ]
    return sorted([prod(prime_power_combo) for prime_power_combo in itertools.product(*powers)])


def draw_play_menu(paused, selecting_object, moving_object):
    bools = [selecting_object, moving_object]
    draw_cells(cells.get())
    draw_lines()
    if moving_object:
        cell_object.update_position(mouse_to_cell_pos(pygame.mouse.get_pos()))
        draw_cells(cell_object.get())
    draw_pause_button(paused)
    draw_slow_down_button()
    draw_speed_up_button()
    draw_clear_button()
    draw_rotate_counter_clockwise_button()
    draw_rotate_clockwise_button()
    draw_add_button()

    if selecting_object:
        bools[0], bools[1] = selecting_object_menu()

    return bools


def draw_object():
    global cell_width
    global cell_offset
    global cell_object
    cell_width = int(win_width / num_cells)
    cell_offset = int(cell_width / 2)

    for cell in cell_object:
        x = cell[0]
        y = cell[1]

        pygame.draw.rect(win,
                         (64, 224, 208),
                         (int(x_center + x - cell_offset + (x * cell_width)),
                          int(y_center + y - cell_offset + (y * cell_width)),
                          cell_width, cell_width))


def draw_cells(cells):
    global cell_width
    global cell_offset
    cell_width = int(win_width / num_cells)
    cell_offset = int(cell_width / 2)

    for cell in cells:
        x = cell[0] + delta[0]
        y = cell[1] + delta[1]
        x_mod = 0
        y_mod = 0

        if x > 0:
            x_mod = 1 - x
        elif x <= 0:
            x_mod = -x
        if y > 0:
            y_mod = 1 - y
        elif y <= 0:
            y_mod = -y

        pygame.draw.rect(win,
                         (64, 224, 208),
                         (int(x_center + x - cell_offset + (x * cell_width) + x_mod),
                          int(y_center + y - cell_offset + (y * cell_width) + y_mod),
                          cell_width, cell_width))


def draw_lines():
    if num_cells != num_cells_list[-1]:
        c = (60 - int(num_cells_index / (len(num_cells_list) - 1) * 30))
        line_color = (c, c, c)
        for x in range(0, int(x_camera), cell_width):
            x_val_add = int(x_camera + (x + cell_offset))
            x_val_sub = int(x_camera - (x + cell_offset))
            pygame.draw.line(win, line_color, (x_val_add, 0), (x_val_add, win_height), 1)
            pygame.draw.line(win, line_color, (x_val_sub, 0), (x_val_sub, win_height), 1)

        for y in range(0, int(y_camera), cell_width):
            y_val_add = int(y_camera + (y + cell_offset))
            y_val_sub = int(y_camera - (y + cell_offset))
            pygame.draw.line(win, line_color, (0, y_val_add), (win_width, y_val_add), 1)
            pygame.draw.line(win, line_color, (0, y_val_sub), (win_width, y_val_sub), 1)


def draw_pause_button(paused):
    pygame.draw.rect(win, (0, 0, 0), pause_button)
    if paused:
        pygame.draw.polygon(win, (50, 50, 50), [(30, 30), (30, 60), (60, 45)])
    else:
        pygame.draw.rect(win, (50, 50, 50), (30, 30, 10, 30))
        pygame.draw.rect(win, (50, 50, 50), (50, 30, 10, 30))


def draw_slow_down_button():
    pygame.draw.rect(win, (0, 0, 0), slow_down_button)
    pygame.draw.polygon(win, (50, 50, 50), [(98, 45), (115, 30), (115, 60)])
    pygame.draw.polygon(win, (50, 50, 50), [(110, 45), (128, 30), (128, 60)])


def draw_speed_up_button():
    pygame.draw.rect(win, (0, 0, 0), speed_up_button)
    pygame.draw.polygon(win, (50, 50, 50), [(189, 45), (172, 30), (172, 60)])
    pygame.draw.polygon(win, (50, 50, 50), [(202, 45), (184, 30), (184, 60)])


def draw_clear_button():
    pygame.draw.rect(win, (0, 0, 0), clear_button)
    pygame.draw.line(win, (50, 50, 50), (240, 30), (270, 60), 10)
    pygame.draw.line(win, (50, 50, 50), (270, 30), (240, 60), 10)


def draw_rotate_counter_clockwise_button():
    pygame.draw.rect(win, (0, 0, 0), rotate_counter_clockwise_button)
    pygame.draw.circle(win, (50, 50, 50), (win_width - 185, 45), 15)
    pygame.draw.circle(win, (0, 0, 0), (win_width - 185, 45), 8)
    pygame.draw.rect(win, (0, 0, 0), (win_width - 210, 20, 25, 25))
    pygame.draw.polygon(win, (50, 50, 50), [(win_width - 185, 25), (win_width - 185, 41), (win_width - 197, 33)])


def draw_rotate_clockwise_button():
    pygame.draw.rect(win, (0, 0, 0), rotate_clockwise_button)
    (win_width - 140, 20, 50, 50)
    pygame.draw.circle(win, (50, 50, 50), (win_width - 115, 45), 15)
    pygame.draw.circle(win, (0, 0, 0), (win_width - 115, 45), 8)
    pygame.draw.rect(win, (0, 0, 0), (win_width - 115, 20, 25, 25))
    pygame.draw.polygon(win, (50, 50, 50), [(win_width - 115, 25), (win_width - 115, 41), (win_width - 103, 33)])


def draw_add_button():
    pygame.draw.rect(win, (0, 0, 0), add_object_button)
    pygame.draw.line(win, (50, 50, 50), (win_width - 60, 45), (win_width - 30, 45), 10)
    pygame.draw.line(win, (50, 50, 50), (win_width - 45, 30), (win_width - 45, 60), 10)


def selecting_object_menu():
    menu_width = 400
    menu_height = 600
    menu_color = (0, 0, 0)
    num_buttons = 4
    button_color = (30, 30, 30)
    x = int(x_center - menu_width/2)
    y = int(y_center - menu_height/2)
    pygame.draw.rect(win, menu_color, (x, y, menu_width, menu_height))
    buffer = 20
    total_button_height = menu_height-2*buffer
    button_height = int((total_button_height-(num_buttons-1)*buffer)/num_buttons)
    button_width = menu_width-2*buffer
    button_x = x+buffer
    button_y = y+buffer
    add_glider_button = pygame.Rect(button_x, button_y, button_width, button_height)
    add_light_weight_spaceship_button = pygame.Rect(button_x, button_y+button_height+buffer, button_width, button_height)
    add_gosper_glider_gun_button = pygame.Rect(button_x, button_y+(button_height+buffer)*2, button_width, button_height)
    add_acorn_button = pygame.Rect(button_x, button_y+(button_height+buffer)*3, button_width, button_height)
    select_object_buttons = [add_glider_button, add_light_weight_spaceship_button, add_gosper_glider_gun_button, add_acorn_button]
    for button in select_object_buttons:
        pygame.draw.rect(win, button_color, button)

    font = pygame.font.SysFont('Comic Sans MS', 30)

    glider_text = font.render('Glider', False, (0, 0, 0))
    light_weight_spaceship_text = font.render('Light-weight Spaceship', False, (0, 0, 0))
    gosper_glider_gun_text = font.render('Gosper Glider Gun', False, (0, 0, 0))
    acorn_text = font.render('Acorn', False, (0, 0, 0))

    win.blit(glider_text, (button_x + button_width / 2 - 42, button_y + button_height / 2 - 20))
    win.blit(light_weight_spaceship_text, (button_x + button_width / 2 - 160, button_y+button_height+buffer + button_height / 2 - 20))
    win.blit(gosper_glider_gun_text, (button_x + button_width / 2 - 128, button_y+(button_height+buffer)*2 + button_height / 2 - 20))
    win.blit(acorn_text, (button_x + button_width / 2 - 39, button_y+(button_height+buffer)*3 + button_height / 2 - 20))

    pygame.display.update()

    selecting_object = False
    moving_object = False
    run_object_menu = True
    while run_object_menu:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run_object_menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if add_glider_button.collidepoint(mouse_pos):
                        cell_object.make_glider(mouse_to_cell_pos(mouse_pos))
                        moving_object = True
                    elif add_light_weight_spaceship_button.collidepoint(mouse_pos):
                        cell_object.make_light_weight_spaceship(mouse_to_cell_pos(mouse_pos))
                        moving_object = True
                    elif add_gosper_glider_gun_button.collidepoint(mouse_pos):
                        cell_object.make_gosper_glider_gun(mouse_to_cell_pos(mouse_pos))
                        moving_object = True
                    elif add_acorn_button.collidepoint(mouse_pos):
                        cell_object.make_acorn(mouse_to_cell_pos(mouse_pos))
                        moving_object = True
                    run_object_menu = not moving_object

    return selecting_object, moving_object


def mouse_to_cell_pos(pos):
    x, y = pos
    if x > 0:
        x = (x - x_center + cell_offset - 1) / cell_width
    elif x < 0:
        x = (x - x_center + cell_offset) / cell_width
    if y > 0:
        y = (y - y_center + cell_offset - 1) / cell_width
    elif y < 0:
        y = (y - y_center + cell_offset) / cell_width
    return math.floor(x - delta[0]), math.floor(y - delta[1])


def makeTestCells(num):
    cells.add((0, 0))
    for i in range(1, num):
        cells.add((i, 0))
        cells.add((0, i))
        cells.add((i, i))
        cells.add((-i, 0))
        cells.add((0, i))
        cells.add((-i, i))
        cells.add((i, 0))
        cells.add((0, -i))
        cells.add((i, -i))
        cells.add((-i, 0))
        cells.add((0, -i))
        cells.add((-i, -i))


def play_menu():
    global time_between_steps
    global num_cells_index
    global num_cells
    global delta

    makeTestCells(250)

    run = True
    paused = True
    screen_dragging = False
    selecting_object = False
    moving_object = False
    clearing_live_cells = False
    multi_processing = False
    rcd_x = 0
    rcd_y = 0
    old_time = time.time()
    start_time = time.time()

    while run:

        if cells.size() >= 50:
            multi_processing = True
        else:
            multi_processing = False

        if multi_processing:
            if clearing_live_cells:
                tik = time.time()
                while time.time() - tik < 0.1:
                    wait = True
                cells.clear()
                clearing_live_cells = False
            cells.start_step()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if moving_object:
                        moving_object = False
                    else:
                        run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if pause_button.collidepoint(pos):
                        paused = not paused
                    elif clear_button.collidepoint(pos):
                        if multi_processing:
                            clearing_live_cells = True
                        else:
                            cells.clear()
                    elif slow_down_button.collidepoint(pos):
                        time_between_steps *= 2
                    elif speed_up_button.collidepoint(pos):
                        if time_between_steps > 0.01:
                            time_between_steps *= 0.50
                    elif add_object_button.collidepoint(pos):
                        selecting_object = True
                    elif rotate_counter_clockwise_button.collidepoint(pos):
                        cell_object.rotate(False)
                    elif rotate_clockwise_button.collidepoint(pos):
                        cell_object.rotate(True)
                    elif moving_object:
                        cell_object.add(cells)
                    else:
                        x, y = mouse_to_cell_pos(pos)
                        if (x, y) in cells.get():
                            cells.remove((x, y))
                        else:
                            cells.add((x, y))
                elif event.button == 3:
                    screen_dragging = True
                    mouse_pos = pygame.mouse.get_pos()
                    rcd_x = mouse_pos[0]
                    rcd_y = mouse_pos[1]
                elif event.button == 4 and num_cells_index != 0:
                    num_cells_index -= 1
                    num_cells = num_cells_list[num_cells_index]
                elif event.button == 5 and num_cells_index != len(num_cells_list) - 1:
                    num_cells_index += 1
                    num_cells = num_cells_list[num_cells_index]
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    screen_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if screen_dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    delta_x = mouse_pos[0] - rcd_x
                    delta_y = mouse_pos[1] - rcd_y
                    if abs(delta_x) > cell_width:
                        delta = (int(delta[0] + delta_x / cell_width), delta[1])
                        rcd_x = pygame.mouse.get_pos()[0]
                    if abs(delta_y) > cell_width:
                        delta = (delta[0], int(delta[1] + delta_y / cell_width))
                        rcd_y = pygame.mouse.get_pos()[1]

        new_time = time.time()
        if new_time - old_time > time_between_steps:
            old_time = new_time
            win.fill((30, 30, 30))
            bools = draw_play_menu(paused, selecting_object, moving_object)
            selecting_object = bools[0]
            moving_object = bools[1]
            pygame.display.update()
            if not paused:
                if multi_processing:
                    cells.finish_step()
                else:
                    cells.step()

if __name__ == '__main__':

    pygame.init()
    pygame.font.init()
    ray.init()
    cells = Cells()
    cell_object = CellObjects()

    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    win_width, win_height = win.get_size()

    x_center = win_width / 2
    y_center = win_height / 2
    x_camera = win_width / 2
    y_camera = win_height / 2

    num_cells_list = get_divisors(win_width)
    num_cells_index = math.floor(len(num_cells_list) / 2)
    num_cells = num_cells_list[num_cells_index]
    cell_width = int(win_width / num_cells)
    cell_offset = int(cell_width / 2)

    pygame.display.set_caption("Game of Life")
    pause_button = pygame.Rect(20, 20, 50, 50)
    slow_down_button = pygame.Rect(90, 20, 50, 50)
    speed_up_button = pygame.Rect(160, 20, 50, 50)
    clear_button = pygame.Rect(230, 20, 50, 50)
    add_object_button = pygame.Rect(win_width - 70, 20, 50, 50)
    rotate_clockwise_button = pygame.Rect(win_width - 140, 20, 50, 50)
    rotate_counter_clockwise_button = pygame.Rect(win_width-210, 20, 50, 50)

    play_menu()
