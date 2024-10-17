import numpy as np
import time as t
from pygame import *
import imageio
from scipy import signal
from pyautogui import size

w,h = size().width,size().height
# w,h = 500,500
screen = display.set_mode((w,h))
fps_cap = 0
recording = 1

display.set_caption("Conway's Game Of Life")
clock = time.Clock()
DEEP_BLUE, WHITE = (12, 0, 106), (255,255,255)
convolution = np.array([[1,1,1],[1,0,1],[1,1,1]])
font.init()
Arial = font.SysFont('Arial', 35)

class grid():
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.frames = []
        self.board = np.zeros(shape=(width,height), dtype=bool)
        
    def populate(self, creature_1 = None, creature_2 : np.ndarray = None):
        if type(creature_1) == np.ndarray:
            (x1,y1) = creature_1.shape
            (x2,y2) = creature_2.shape
            self.board[self.width//2- x1//2:self.width//2 - x1//2 + x1, self.height//2 - y1//2 :self.height//2 - y1//2 + y1] = creature_1
            # self.board[self.width//2- x2//2:self.width//2 - x2//2 + x2, self.height//2 :self.height//2 + y2] = creature_2
        else:
            self.board = np.random.choice([0, 1], size=(self.width, self.height))
    
    def neighbors(self):
        return signal.convolve(self.board, convolution, mode="same")
    
    def update(self):
        neighbors = self.neighbors()
        survive = np.logical_and(self.board, np.logical_or(neighbors == 2, neighbors == 3))
        born = np.logical_and(~self.board, neighbors == 3)
        self.board = np.logical_or(survive, born)

    def show_board(self):
        scaled_board = np.kron(self.board, np.ones((w//self.width, h//self.height)))
        view = np.zeros((*scaled_board.shape, 3), dtype=np.uint8)
        view[scaled_board == 0] = DEEP_BLUE
        view[scaled_board == 1] = WHITE
        if recording:
            self.frames.append(np.rot90(np.flip(view, axis=1)))
        return view

game_of_life = grid(w//2,h//2)

def rle_to_numpy(rle_string, width, height):
    rows = rle_string.split('$')
    result = np.zeros((height, width), dtype=int)
    row, col = 0, 0
    count = ''
    for part in rows:
        for char in part:
            if char.isdigit():
                count += char
            elif char == 'b':
                col += int(count) if count else 1
                count = ''
            elif char == 'o':
                live_count = int(count) if count else 1
                result[row, col:col + live_count] = 1
                col += live_count
                count = ''
        row += 1
        col = 0
    
    return result

# Text_surf_1 = Arial.render("Lenia 3D :", False, 3*[255])
Text_surf_1 = transform.scale(image.load("creatures/image.jpg"), (475,475))
Text_surf_2 = Arial.render("Automate cellulaire", False, 3*[255])
Text_surf_array_1 = surfarray.array3d(Text_surf_1)[:,:,0]//128 * np.random.choice([0, 1], size=(475,475))
Text_surf_array_2 = surfarray.array3d(Text_surf_2)[:,:,0]//128

# Find patterns at : https://conwaylife.com/wiki/Category:Patterns  
# glider_gun = rle_to_numpy("23b2o24b2o$23b2o24b2o$41b2o$40bo2bo$41b2o2$36b3o$36bobo$9b2o25b3o$9b2o25b2o$8bo2bo23b3o$8bo2bob2o20bobo$8bo4b2o20b3o$10b2ob2o$31b2o$21b2o7bo2bo$21b2o8b2o$49b2o$49b2o2$4b2o18bo$2o4b4o10b2o2b2ob3o$2o2b2ob3o10b2o4b4o$4bo19b2o!", 51, 24)
game_of_life.populate(Text_surf_array_1, Text_surf_array_2)

while 1:
    for ev in event.get():
        if ev.type == QUIT:
            if recording:
                full_blue = np.zeros((h, w, 3), dtype=int)
                full_blue[:, :] = DEEP_BLUE

                first_frame = game_of_life.frames[0].astype(float)
                last_frame = game_of_life.frames[-1].astype(float)

                # Transition from last frame to blue
                for i in range(1, 16):
                    alpha = i / 15  # Gradually increase weight for full_blue
                    blended_frame = ((1 - alpha) * last_frame + alpha * full_blue).astype(np.uint8)
                    game_of_life.frames.append(blended_frame)

                # Transition from blue to first frame
                for i in range(1, 31):
                    alpha = i / 30  # Gradually increase weight for first_frame
                    blended_frame = ((1 - alpha) * full_blue + alpha * first_frame).astype(np.uint8)
                    game_of_life.frames.append(blended_frame)
                # imageio.mimwrite(f"video_2.mp4", game_of_life.frames, codec='libx264')
                imageio.mimsave(f"CPBx_1.gif", game_of_life.frames, fps=15, quality = 8, bitrate = "5000k", loop=0)
            quit()
        if ev.type == KEYDOWN and ev.key == K_SPACE:
            game_of_life.populate()
    # screen.blit(surfarray.make_surface(game_of_life.board*255), (0,0))
    # screen.blit(Text_surf,(0,0))
    # screen.blit(surfarray.make_surface(game_of_life.show_board()),(0,0))
    surfarray.blit_array(screen, game_of_life.show_board())
    display.flip()
    clock.tick(fps_cap)
    game_of_life.update()