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

#shot_df.LOC_Y = shot_df.LOC_Y * -1
'''
right_shot_df = shot_df[shot_df.SHOT_ZONE_AREA == "Right Side(R)"]
other_shot_df = shot_df[~(shot_df.SHOT_ZONE_AREA == "Right Side(R)")]

fig = plt.figure(figsize=(4.3,4))
ax = fig.add_subplot(111)
ax.scatter(right_shot_df.LOC_X, right_shot_df.LOC_Y, s=1, c='red', label='Right Side(R)')
ax.scatter(other_shot_df.LOC_X, other_shot_df.LOC_Y, s=1, c='blue', label='Other AREA')

ax.set_ylim(top=-50,bottom=580)
ax.legend()
'''

from matplotlib.patches import Circle, Rectangle, Arc, Wedge

def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint 油漆区
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc  罚球线弧顶
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc 罚球底弧
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the 
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

def draw_half_court(ax=None, unit=1, lineColor='white', courtColor='#F7CEA2'):
    if ax is None:
        ax = plt.gca()

    lw = unit * 2 #line width
    # Create the basketball hoop
    #篮筐直径(内径)是18IN.,我们设置半径为9.2IN刨除line width 0.2IN,正好为篮筐半径
    hoop = Wedge((0, 0), unit * 9.2, 0, 360, width=unit * 0.2, color='#767676')
    hoop_neck = Rectangle((unit * -48, unit * - ), unit * 6, unit * 6, linewidth=None, color='#767676')
    # Create backboard
    #Rectangle, lower left at xy = (x, y) with specified width, height and rotation angle
    backboard = Rectangle((unit * -36, unit * -15 ), unit * 72, lw, linewidth=None, color='#767676')
    # List of the court elements to be plotted onto the axes

    # Restricted Zone, it is an arc with 4ft radius from center of the hoop 
    restricted = Wedge((0, 0), unit * 50, 0, 180, width=lw, color='#767676')
    restricted_left = Rectangle((0, unit * -48 ), lw, unit * 15, linewidth=None, color='#767676')
    restricted_right = Rectangle((0, unit * 48 ), lw, unit * 15, linewidth=None, color='#767676')

    court_elements = [hoop, hoop_neck, backboard, restricted, restricted_left, restricted_right,
                        ]

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    #地板颜色'#F7CEA2'

fig = plt.figure(figsize=(7,7))
plt.axes().set_aspect('equal')

ax = fig.add_subplot(111)




draw_half_court(ax=ax)

#ax.plot([7.5, 7.5], [-7.5, 7.5], 'k-', lw=2)
#ax.plot([5.5, 5.5], [-7.5, 7.5], 'k-', lw=2)

ax.set_xlim(-300,300)
ax.set_ylim(-100,500)
'''
draw_court(ax=ax,outer_lines=False)
plt.xlim(-300,300)
plt.ylim(-100,500)
'''
plt.show()
