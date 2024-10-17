from matplotlib.pyplot import *


f = lambda n, m, s: np.exp( - (n-m)**2 / (2 * s**2) ) * 2 - 1
g = lambda n, m, s: np.maximum(0, 1 - (n-m)**2 / (9 * s**2) )**4 * 2 - 1
h = lambda n, m, s: (np.abs(n-m)<=s) * 2 - 1

a,b = 0.25 , 0.25

x = [i/1000 for i in range(1,1000)]
yf = [f(e,a,b) for e in x]
yg = [g(e,a,b) for e in x]
yh = [h(e,a,b) for e in x]


plot(x,yf,'blue')
plot(x,yg,'green')
plot(x,yh,'red')
show()

"""
Tout ça vient du Git

kernel_core = {
    0: lambda r: (4 * r * (1-r))**4,  # polynomial (quad4)
    1: lambda r: np.exp( 4 - 1 / (r * (1-r)) ),  # exponential / gaussian bump (bump4)
    2: lambda r, q=1/4: (r>=q)*(r<=1-q),  # step (stpz1/4)
    3: lambda r, q=1/4: (r>=q)*(r<=1-q) + (r<q)*0.5 # staircase (life)
}
growth_func = {
    0: lambda n, m, s: np.maximum(0, 1 - (n-m)**2 / (9 * s**2) )**4 * 2 - 1,  # polynomial (quad4)
    1: lambda n, m, s: np.exp( - (n-m)**2 / (2 * s**2) ) * 2 - 1,  # exponential / gaussian (gaus)
    2: lambda n, m, s: (np.abs(n-m)<=s) * 2 - 1  # step (stpz)
}

"""