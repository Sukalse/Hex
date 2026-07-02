import pygame
import math

from graphics.utils import *
from graphics.settings import *

class GraphicsGame:

    def __init__(self, game, screen):
        self.game = game

        self.clock = pygame.time.Clock()

        self.screen = screen
        self.running = True
        self.dragging = False
        self.click = False

        self.camera_x = WIDTH/2
        self.camera_y = HEIGHT/2

        self.player = False
        self.player_count = 0

        self.HEX_SIZE = 40

        self.bigfont = pygame.font.Font(None, 33)
        self.smallfont = pygame.font.Font(None, 24)

        self.text_rect = pygame.Rect(920, 380, 250, 390)
        self.turn_rect = pygame.Rect(WIDTH/2-200, 40, 400, 100)

        self.update_camera_info()

    def render_text(self):
        pygame.draw.rect(self.screen, INFO_BACKGROUND_COLOR, self.text_rect, border_radius=10)
        pygame.draw.rect(self.screen, INFO_BACKGROUND_COLOR, self.turn_rect, border_radius=10)

        title = self.bigfont.render("Lorem Ipsum", True, (255,255,255))
        title_rect = title.get_rect(topleft=(self.text_rect.left+10, self.text_rect.top+10))

        mouse_pos_text = self.smallfont.render("(q, r) : ("+str(self.q_mouse)+", "+str(self.r_mouse)+")", True, (150, 150, 150))
        mouse_pos_rect = mouse_pos_text.get_rect(topleft=(self.text_rect.left+10, self.text_rect.top+50))

        turn = self.bigfont.render("Player "+str(int(self.player)+1)+" to play", True, PIECE_COLOR[self.player])
        turn_rect  = turn.get_rect(midtop=(self.turn_rect.left + self.turn_rect.width/2, self.turn_rect.top+10))


        self.screen.blit(title, title_rect)
        self.screen.blit(mouse_pos_text, mouse_pos_rect)
        self.screen.blit(turn, turn_rect)

    def mainloop(self):
        while self.running:
            self.handle_events(pygame.event.get())
            self.update_camera_info()

            self.screen.fill(BACKGROUND_COLOR)

            self.draw_hover_hex()
            self.draw_map()

            self.render_text()

            pygame.display.flip()
            self.clock.tick(60)

    def update_camera_info(self):
        self.hex_width = math.sqrt(3) * self.HEX_SIZE
        self.hex_height = 2 * self.HEX_SIZE
        self.row_spacing = 1.5 * self.HEX_SIZE

    def draw_hover_hex(self):
        world_x, world_y = hex_to_pixel(self.q_mouse, self.r_mouse, self.HEX_SIZE)

        pygame.draw.polygon(
            self.screen,
            HOVER_HEX_COLOR,
            hex_points(world_x + self.camera_x, world_y + self.camera_y, self.HEX_SIZE*0.8)
        )

    def handle_events(self, events):
        mx, my = pygame.mouse.get_pos()

        world_x = (mx - self.camera_x)
        world_y = (my - self.camera_y)

        self.q_mouse, self.r_mouse = hex_round(*pixel_to_hex(world_x, world_y, self.HEX_SIZE))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.dragging=True
                    self.click=True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
                if self.click:
                    if self.game.get_tile(self.q_mouse, self.r_mouse) is None:
                        self.game.add_tile(self.q_mouse, self.r_mouse, self.player)
                        self.player_count += 1
                        if self.player_count >= 2:
                            self.player_count = 0
                            self.player = not self.player

                    self.click = False
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                dx, dy = event.rel
                self.click = False
                self.camera_x += dx
                self.camera_y += dy
            elif event.type == pygame.MOUSEWHEEL:
                self.HEX_SIZE -= event.y
            elif event.type == pygame.QUIT:
                self.running = False
        self.HEX_SIZE = min(max(self.HEX_SIZE, MIN_HEX_SIZE), MAX_HEX_SIZE)

    def draw_map(self):
        min_r = int(-self.camera_y / self.row_spacing) - 2
        max_r = int((HEIGHT-self.camera_y) / self.row_spacing) + 2

        for r in range(min_r, max_r + 1):

            offset = r / 2

            min_q = int((-self.camera_x / self.hex_width) - offset) - 2
            max_q = int(((-self.camera_x + WIDTH) / self.hex_width) - offset) + 2

            for q in range(min_q, max_q + 1):
                world_x, world_y = hex_to_pixel(q, r, self.HEX_SIZE)

                screen_x = world_x + self.camera_x
                screen_y = world_y + self.camera_y

                pygame.draw.polygon(
                    self.screen,
                    HEX_BORDER_COLOR,
                    hex_points(screen_x, screen_y, self.HEX_SIZE*.93),
                    width=1,
                )

                tile = self.game.get_tile(q, r)
                if tile is not None:
                    pygame.draw.polygon(
                        self.screen,
                        PIECE_COLOR[tile.color],
                        hex_points(screen_x, screen_y, self.HEX_SIZE*0.8)
                    )

