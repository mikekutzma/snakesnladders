import snl
import numpy as np
from scipy.special import factorial
from scipy.optimize import curve_fit
from scipy.stats import gamma, poisson
import matplotlib.pyplot as plt

func = poisson.pdf

game = snl.Game()

game.play(10000)

gamelens = [len(x)-1 for x in game.log]
y,x,patches = plt.hist(gamelens,bins=range(max(gamelens)+1),normed=True)
popt, pcov = curve_fit(func, x[:-1], y)

plt.plot(x,func(x,popt))
plt.show()

