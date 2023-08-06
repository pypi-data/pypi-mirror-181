import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def vector_plot(vector_df:pd.DataFrame(), title:str()):
    vector_df = vector_df.sort_index(ascending=False)
    
    explode = []
    for i in vector_df['element']:
        if i in 'backbone_element':
            explode.append(0)
        else:
            explode.append(0.1)
            
    
    labels = []
    for i in vector_df['element']:
        if i in 'backbone_element':
            labels.append('')
        else:
            labels.append(i)
    
    
    
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(aspect="equal"))
    
    
    wedges, texts = ax.pie(vector_df['length'],explode = explode, startangle=90)
    
    
    kw = dict(arrowprops=dict(arrowstyle="-"),
               zorder=0, va="center")
    n = 0
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        if len(labels[i]) > 0:
            n += 0.25
            ax.annotate(labels[i], xy=(x, y), xytext=(1.4*x+(n*x/4), y*1.1+(n*y/4)),
                        horizontalalignment=horizontalalignment, fontsize=20, weight="bold", **kw)
    
    circle1 = plt.Circle( (0,0), 1, color='black')
    circle2 = plt.Circle( (0,0), 0.95, color='white')
    
    ax.text(0.5, 0.5, str(title + '\n length: ' + str(sum(vector_df['length'])) + 'nc'), transform = ax.transAxes, va = 'center', ha = 'center', backgroundcolor = 'white', weight="bold", fontsize = 25)
    
    p=plt.gcf()
    p.gca().add_artist(circle1)
    p.gca().add_artist(circle2)
    
    plt.show()

    return fig

