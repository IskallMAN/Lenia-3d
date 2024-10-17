import numpy as np
from pygame import *
import imageio
from scipy import signal
from pyautogui import size

# w,h = size().width,size().height #Full Window (= more lag)
w,h = 500,500
screen = display.set_mode((w,h))
fps_cap = 0 # 0 = unlimited framerate, 10 = max 10 fps
recording = False
video_output_name = "Video"

display.set_caption("Lenia Artificial Life")
clock = time.Clock()

class grid():
    def __init__(self,width,height):
        #Tweakable parameters
        self.kernel_size = 21
        self.spread = 0.25
        self.target_mean = 0.25
        #Don't touch the rest
        self.width = width
        self.height = height
        self.grid = np.zeros(shape=(width,height), dtype=bool)
        range_vals = np.linspace(-1, 1, self.kernel_size)
        x, y = np.meshgrid(range_vals, range_vals)
        r = np.sqrt(x**2 + y**2)
        kernel_function = lambda r: np.exp(4 - 1 / (r * (1 - r)))
        self.kernel = np.where((r > 0) & (r < 1), kernel_function(r), 0)
        self.kernel /= self.kernel.sum()
        # self.growth_function = lambda n: 0.5* (np.exp(-((n - 0.5)**2) / (2 * 0.1**2)) - 0.5)
        self.growth_function = lambda n, m, s: np.exp( - (n-m)**2 / (2 * s**2) ) * 2 - 1
        
    def populate(self, creature : np.ndarray = None):
        if type(creature) == np.ndarray:
            (x,y) = creature.shape
            self.grid[self.width//2:self.width//2 + x, self.height//2:self.height//2 + y] = creature
        else:
            self.grid = np.random.rand(self.width,self.height)
    
    def neighbors(self):
        return signal.convolve2d(self.grid, self.kernel, mode="same")
    
    def update(self):
        neighbors = self.neighbors()
        growth = self.growth_function(neighbors, self.target_mean, self.spread)
        self.grid += growth
        self.grid = np.clip(self.grid, 0, 1)


game_of_life = grid(w,h)
game_of_life.populate()
frames = []

while 1:
    for ev in event.get():
        if ev.type == QUIT:
            if recording:
                imageio.mimwrite(f"{video_output_name}.mp4", frames, codec='libx264')
            quit()
        if ev.type == KEYDOWN and ev.key == K_SPACE:
            game_of_life.populate()
    # render = surfarray.make_surface(game_of_life.grid*255)
    # screen.blit(render, (0,0))
    surfarray.blit_array(screen, game_of_life.grid*255)
    # if recording:
    #     frames.append(surfarray.array3d(render))
    display.flip()
    clock.tick(fps_cap)
    game_of_life.update()