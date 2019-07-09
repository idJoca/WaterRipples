import pygame
from pygame import surfarray
import numpy as np


class main():
    _continue_flag = True

    def __init__(self, width, height, dampening=0.95):
        pygame.init()
        if (width == 0 or height == 0):
            self.canvas = pygame.display \
                                .set_mode(
                                         (width, height),
                                          pygame.NOFRAME |
                                          pygame.FULLSCREEN)
        else:
            self.canvas = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Water ripple")
        self.canvas.fill((0, 0, 0))
        # Sets the width and height
        screen_details = pygame.display.Info()
        self.width = screen_details.current_w
        self.height = screen_details.current_h

        self.buffer_1 = np.zeros((self.width, self.height), dtype=np.float32)
        self.buffer_2 = np.zeros((self.width, self.height), dtype=np.float32)
        self.sums = np.zeros((self.width, self.height), dtype=np.float32)
        self.dampening = dampening        
        self.mouse_down = False
        
    def start(self):
        self.clock = pygame.time.Clock()
        rows = []
        cols = []
        for x in range(0, self.width - 1):
            for y in range(0, self.height - 1):
                rows.append([x - 1, x, x, x + 1])
                cols.append([y, y - 1, y + 1, y])
        self.rows = np.array(rows)
        self.cols = np.array(cols)
        center_x = self.width // 2
        center_y = self.height // 2
        x_slice = slice(center_x - 2, center_x + 2)
        y_slice = slice(center_y - 2, center_y + 2)
        self.buffer_2[x_slice, y_slice] = 500
        self.buffer_1[x_slice, y_slice] = 500

    def swap_buffers(self):
        temp = self.buffer_1
        self.buffer_1 = self.buffer_2
        self.buffer_2 = temp

    def loop(self):
        cornerless_x = slice(0, self.width - 1)
        cornerless_y = slice(0, self.height - 1)
        while self._continue_flag is True:
            if (self.buffer_2.min() > -0.2 and self.buffer_2.max() < 0.2):
                self.buffer_1.fill(0)
                self.buffer_2.fill(0)
            self.sums[cornerless_x, cornerless_y] = self.buffer_1[self.rows, self.cols] \
                                                    .sum(axis=1, keepdims=True) \
                                                    .reshape((self.width - 1,
                                                              self.height - 1))            
            self.buffer_2 = (self.sums / 2 - self.buffer_2) * self.dampening
            surfarray.blit_array(self.canvas, self.buffer_2)
            self.swap_buffers()              
            pygame.display.flip()
            # print(self.clock.get_fps())
            self.clock.tick(30)
            for event in pygame.event.get():
                # Quit the program if the use close the windows
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    self._continue_flag = False
                # Or press ESCAPE
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        self._continue_flag = False 

                if (event.type == pygame.MOUSEBUTTONDOWN):
                    self.mouse_down = True
                    mouse_x = event.pos[0]
                    mouse_y = event.pos[1]                    
                    x_slice = slice(mouse_x - 4, mouse_x + 4)
                    y_slice = slice(mouse_y - 4, mouse_y + 4)
                    self.buffer_1[mouse_x, mouse_y] = 500
                    self.buffer_2[x_slice, y_slice] = 500

                elif (event.type == pygame.MOUSEMOTION and
                        self.mouse_down is True):
                    mouse_x = event.pos[0]
                    mouse_y = event.pos[1]
                    x_slice = slice(mouse_x - 4, mouse_x + 4)
                    y_slice = slice(mouse_y - 4, mouse_y + 4)
                    self.buffer_2[x_slice, y_slice] = 500

                elif (event.type == pygame.MOUSEBUTTONUP):
                    self.mouse_down = False

program = main(400, 400)
program.start()
program.loop()