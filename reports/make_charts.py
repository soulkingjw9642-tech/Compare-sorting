"""Rebuild all figures from the committed benchmark CSV."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from matplotlib.font_manager import FontProperties

root = Path(__file__).resolve().parent
rows = list(csv.DictReader((root/'results.csv').open()))
algs = ['insertion','merge','gnome']
colors = ['#d88a42','#3977ad','#509477']
shapes = ['random','sorted','reverse','duplicates']
n_font = FontProperties(fname=str(root/'fonts/NanumGothic-Regular.ttf'))

def entry(shape,n,alg):
    return next(r for r in rows if r['shape']==shape and int(r['n'])==n and r['algorithm']==alg)

# Three grouped bar figures. Log panels omit zeros; their label explains this.
for field,label,filename in [('comparisons','Key comparisons','shape-compares-bars.png'),
                              ('time_ms','Mean time (ms)','shape-time-bars.png'),
                              ('moves','Item assignments','shape-moves-bars.png')]:
    fig, axes = plt.subplots(1,2,figsize=(10.2,4.15),layout='constrained')
    for ax in axes:
        for j,alg in enumerate(algs):
            vals=np.array([float(entry(sh,8000,alg)[field]) for sh in shapes])
            xs=np.arange(4)+(j-1)*.25
            ax.bar(xs, np.where(vals>0,vals,np.nan) if ax is axes[1] else vals,
                   width=.24,color=colors[j],label=alg)
        ax.set_xticks(np.arange(4),['random','sorted','reverse','duplicates'],rotation=20)
        ax.set_ylabel(label);ax.grid(axis='y',alpha=.23);ax.set_axisbelow(True)
    axes[0].set_title('Linear scale');axes[1].set_title('Log scale')
    axes[1].set_yscale('log');axes[1].legend(fontsize=8,loc='upper left')
    fig.suptitle(f'{label} by input shape  |  n = 8,000')
    fig.savefig(root/filename,dpi=175,bbox_inches='tight');plt.close(fig)

# Growth is shown as connected lines for each algorithm, at identical random inputs.
for field,label,filename in [('comparisons','Key comparisons','growth-compares.png'),
                              ('time_ms','Mean time (ms)','growth-time.png')]:
    fig,axes=plt.subplots(1,2,figsize=(10.2,4.1),layout='constrained')
    for ax in axes:
        for color,alg in zip(colors,algs):
            data=[r for r in rows if r['shape']=='random' and r['algorithm']==alg]
            ax.plot([int(r['n']) for r in data],[float(r[field]) for r in data],
                    'o-',color=color,label=alg,linewidth=2)
        ax.set_xlabel('Input size n (random)');ax.set_ylabel(label)
        ax.set_xticks([1000,2000,4000,8000]);ax.grid(True,which='both',alpha=.25)
    axes[0].set_title('Linear scale');axes[1].set_title('Log scale')
    axes[1].set_yscale('log');axes[1].legend(fontsize=8)
    fig.suptitle(f'{label} as n grows')
    fig.savefig(root/filename,dpi=175,bbox_inches='tight');plt.close(fig)

# Gnome sort: trace every swap of [4,2,3,1]. This matches src/sort.c's branch behavior.
a=[4,2,3,1];states=[(a.copy(),'시작',None)]
i=1
while i<len(a):
    if a[i-1]<=a[i]:i+=1
    else:
        pair=(i-1,i);a[i-1],a[i]=a[i],a[i-1]
        states.append((a.copy(),f'{len(states)}단계: 인접 원소 교환',pair))
        i=i-1 if i>1 else i+1
assert len(states)==6 and states[-1][0]==[1,2,3,4]
fig,ax=plt.subplots(figsize=(8.5,5.2));ax.set_xlim(0,9);ax.set_ylim(-.55,6.25);ax.axis('off')
for row,(vals,label,pair) in enumerate(states):
    y=5.3-row
    ax.text(.2,y+.18,label,fontsize=12,fontproperties=n_font,va='center')
    for col,v in enumerate(vals):
        x=3.4+col*1.18
        fc='#f7dbb9' if pair and col in pair else '#e6f0f7'
        ax.add_patch(FancyBboxPatch((x,y-.16),.94,.72,boxstyle='round,pad=.06',
                                    edgecolor='#44708e',facecolor=fc,linewidth=1.5))
        ax.text(x+.47,y+.2,str(v),ha='center',va='center',fontsize=16,weight='bold')
    if row<5:ax.annotate('',(5.65,y-.48),(5.65,y-.18),arrowprops={'arrowstyle':'->','color':'#888'})
ax.text(.2,-.1,'주황색 칸은 해당 단계에서 교환된 인접 원소',fontproperties=n_font,fontsize=9)
fig.savefig(root/'gnome-steps.png',dpi=170,bbox_inches='tight');plt.close(fig)
