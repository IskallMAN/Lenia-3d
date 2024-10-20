import numpy as np
import time as t
from pygame import *
from scipy.signal import fftconvolve
from pyautogui import size
from Len_creatures import *

# w,h = size().width,size().height #Full Window (= more lag)
w,h = 500,500
screen = display.set_mode((w,h))

display.set_caption("Lenia Artificial Life")

class grid():
    def __init__(self,width,height):
        self.kernel_size = 101
        self.period = 7
        self.width = width
        self.height = height
        self.grid = np.zeros(shape=(width,height), dtype=float)
        range_vals = np.linspace(-1, 1, self.kernel_size)
        x, y = np.meshgrid(range_vals, range_vals)
        r = np.sqrt(x**2 + y**2)
        kernel_function = lambda r: np.exp(4 - 1 / (r * (1 - r)))
        self.kernel = np.where((r > 0) & (r < 1), kernel_function(r), 0)
        self.kernel /= self.kernel.sum()

    def populate(self, creature : list = None):
        if creature != None:
            for e in creature:
                (x,y) = e.shape
                self.grid[self.width//2 - x//2 :self.width//2 - x//2 + x, self.height//2 - y//2 :self.height//2 - y//2 + y] = e
        else:
            self.grid = np.random.rand(self.width,self.height)

    def neighbors(self):
        return fftconvolve(self.grid, self.kernel, mode="same")

    def update(self):
        neighbors = self.neighbors()
        growth = growth_function(neighbors)
        self.grid += growth / self.period
        self.grid = np.clip(self.grid, 0, 1)

t_0 = t.time()

game_of_life = grid(w,h)
game_of_life.populate([np.array(Oscillator, dtype=float)])

def growth_function(U):
    return 0 + ((U>=0.12)&(U<=0.15)) - ((U<0.12)|(U>0.15))

while 1:
    for ev in event.get():
        if ev.type == QUIT:
            quit()
        if ev.type == KEYDOWN and ev.key == K_SPACE:
            game_of_life.populate()
        if ev.type == MOUSEBUTTONDOWN:
            nonzero_indices = np.argwhere(game_of_life.grid != 0)
            top_left = nonzero_indices.min(axis=0)
            bottom_right = nonzero_indices.max(axis=0) + 1
            cropped_arr = game_of_life.grid[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]]
            print([list(e) for e in list(cropped_arr)])
    render = surfarray.make_surface(game_of_life.grid*255)
    screen.blit(render, (0,0))
    # surfarray.blit_array(screen, game_of_life.grid*255)
    display.flip()
    # print("total time : ", t.time()-t_0)
    # t_0 = t.time()
    game_of_life.update()
    # print("update time : ", t.time()-t_0)