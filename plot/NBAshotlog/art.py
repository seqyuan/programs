#import pandas as pd
#shot_df = pd.read_excel('outfile.xlsx', sheetname=0, header=0, index_col=0)


'''

print (shot_df.head())
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#plt.style.use('ggplot')
'''

import matplotlib.pyplot as plt

from matplotlib.patches import Circle, Rectangle, Arc, Wedge



def draw_half_court(ax=None):
    if ax is None:
        ax = plt.gca()

    restricted = Arc((0, 0), 10, 10, theta1=0, theta2=180, linewidth=4, color='#767676')
    ax.add_patch(restricted)

    aa = Wedge((0, 0), 6, 0, 180, width=3, color='#767676')
    ax.add_patch(aa)


fig = plt.figure(figsize=(6,6))
plt.axes().set_aspect('equal')

ax = fig.add_subplot(111)




draw_half_court(ax=ax)

#ax.plot([7.5, 7.5], [-7.5, 7.5], 'k-', lw=2)
#ax.plot([5.5, 5.5], [-7.5, 7.5], 'k-', lw=2)

ax.set_xlim(-16,16)
ax.set_ylim(-16,16)
'''
draw_court(ax=ax,outer_lines=False)
plt.xlim(-300,300)
plt.ylim(-100,500)
'''
plt.show()
