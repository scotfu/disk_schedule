"""
Make a histogram of normally distributed random numbers and plot the
analytic PDF over it
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import json
from disk_schedule import ROUND,ALGORITHMS

def draw_pic(mu,sigma):

    x = mu + sigma * np.random.randn(10000)
    fig = plt.figure()
    ax = fig.add_subplot(111)

# the histogram of the data
    n, bins, patches = ax.hist(x, 50, normed=1, facecolor='green', alpha=0.75)

# hist uses np.histogram under the hood to create 'n' and 'bins'.
# np.histogram returns the bin edges, so there will be 50 probability
# density values in n, 51 bin edges in bins and 50 patches.  To get
# everything lined up, we'll compute the bin centers
    bincenters = 0.5*(bins[1:]+bins[:-1])
# add a 'best fit' line for the normal PDF
    y = mlab.normpdf( bincenters, mu, sigma)
    l = ax.plot(bincenters, y, 'r--', linewidth=1)

    ax.set_xlabel('Smarts')
    ax.set_ylabel('Probability')
#ax.set_title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
    ax.set_xlim(1, 10240)
    ax.set_ylim(0, 0.03)
    ax.grid(True)

    plt.show()

if __name__ =='__main__':
    with open('output.txt') as data:
        data=data.read()
    data= json.loads(data)
    name=data["1"]["results"][0]["name"]
    path_cost=data["1"]["results"][0]["path_cost"]
#    draw_pic()
    print name,path_cost
