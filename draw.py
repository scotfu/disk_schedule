"""
Make a histogram of normally distributed random numbers and plot the
analytic PDF over it
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.patches as patches
import matplotlib.path as path
import json
from disk_schedule import ROUND,ALGORITHMS
from matplotlib.backends.backend_pdf import PdfPages

def draw_pic(data):
    pp = PdfPages('multipage.pdf',)
    a_pp=PdfPages('summary.pdf',)
    config={'dpi':200,'figsize':'58,116','bbox_inches':0}
    a_fig = plt.figure()
    for algorithm in ALGORITHMS:
        name=algorithm
        num=ALGORITHMS.index(algorithm)+1
        al_data=data[algorithm]
        mu, sigma = np.average(al_data),np.std(al_data)
        x = mu + sigma * np.random.randn(10000)
        fig = plt.figure()
        ax = fig.add_subplot(1,2,1)
        a_ax=a_fig.add_subplot(111)
        x=np.linspace(-5*sigma+mu,mu+5*sigma,100)

        y = mlab.normpdf(x,mu, sigma)
        l = ax.plot(x, y, 'r', linewidth=1)
        a_ax.plot(x, y, 'r', linewidth=1)
        ax.set_xlabel('Normal Distribution')
        ax.set_ylabel('Probability')
        ax.set_title(r'$\ %s: \mu=%s,\ \sigma=%s$'%(name,mu,sigma))
        ax.autoscale_view()
        ax.grid(True)



        ax = fig.add_subplot(1,2,2)
        ax.set_xlabel('Distribution')
        n, bins = np.histogram(al_data, 40)
        left = np.array(bins[:-1])
        right = np.array(bins[1:])
        bottom = np.zeros(len(left))
        top = bottom + n



        XY = np.array([[left,left,right,right], [bottom,top,top,bottom]]).T


        barpath = path.Path.make_compound_path_from_polys(XY)


        patch = patches.PathPatch(barpath, facecolor='blue', edgecolor='gray', alpha=0.8)
        ax.add_patch(patch)


        ax.set_xlim(left[0], right[-1])
        ax.set_ylim(bottom.min(), top.max())
        ax.autoscale_view()
        ax.grid(True)
        fig.set_size_inches(12,8)
        pp.savefig(fig)
    a_fig.set_size_inches(52,8)
    a_pp.savefig(a_fig)
#    plt.show()
    a_pp.close()
    pp.close()

def reform_data():
    reform={}
    with open('output.txt') as data:
        data=data.read()
    data= json.loads(data)
    for no in range(1,ROUND+1):
        for algorithm in range(len(ALGORITHMS)):
            name=data[str(no)]["results"][algorithm]["name"]
            path_cost=data[str(no)]["results"][algorithm]["path_cost"]
            try:
                reform[name].append(path_cost)
            except:    
                reform[name]=[path_cost]
    return reform


if __name__ =='__main__':
    data=reform_data()
    draw_pic(data)
        
