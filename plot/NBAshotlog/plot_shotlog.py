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


class data_linewidth_plot():
    def __init__(self,**kwargs):
        self.ax = kwargs.pop("ax", plt.gca())
        self.lw_data = kwargs.pop("linewidth", 1)
        self.lw = 1
        self.ax.figure.canvas.draw()
        self.ppd=72./fig.dpi
        self.trans = self.ax.transData.transform
        self._resize()

    def _resize(self):
        lw =  ((self.trans((1,self.lw_data))-self.trans((0,0)))*self.ppd)[1]
        self.lw = lw

def draw_half_court(ax=None, unit=1, lineColor='white', courtColor='#F7CEA2'):
    if ax is None:
        ax = plt.gca()

    lw = unit * 2 #line width
    color = 'k'

    # 精确line width
    court_lw = data_linewidth_plot(ax = ax,linewidth = 1).lw

    ## Create the basketball hoop
    #篮筐直径(内径)是18IN.,我们设置半径为9.2IN刨除line width 0.2IN,正好为篮筐半径
    hoop = Wedge((0, 0), unit * 9.2, 0, 360, width=unit * 0.2, color='#767676')
    hoop_neck = Rectangle((unit * -2, unit * -15 ), unit * 4, unit * 6, linewidth=None, color='#767676')
    
	## Create backboard
    #Rectangle, left lower at xy = (x, y) with specified width, height and rotation angle
    backboard = Rectangle((unit * -36, unit * -15 ), unit * 72, lw, linewidth=None, color='#767676')
    # List of the court elements to be plotted onto the axes

    ## Restricted Zone, it is an arc with 4ft radius from center of the hoop 
    #restricted = Wedge((0, 0), unit * 50, 0, 180, width=lw, color='#767676')
    restricted = Arc((0, 0), 96+lw, 96+lw, theta1=0, theta2=180,linewidth=court_lw, color='#767676', fill=False)
    #restricted_left = Rectangle((unit * -50, unit * -15 ), lw, unit * 15, linewidth=0, color='#767676')
    restricted_left = Rectangle((-48*unit-lw/2, unit * -15 ), 0, unit * 17, linewidth=court_lw, color='#767676')
    #restricted_right = Rectangle((unit * 48, unit * -15 ), lw, unit * 15, linewidth=0, color='#767676')
    restricted_right = Rectangle((unit*48+lw/2, unit * -15 ), 0, unit * 17, linewidth=court_lw, color='#767676')

    # Create free throw top arc  罚球线弧顶
    top_arc_diameter = 6 * 12 * 2 - lw
    top_free_throw = Arc((0, unit * 164), top_arc_diameter, top_arc_diameter, theta1=0, theta2=180,linewidth=court_lw, color=color, fill=False)
    # Create free throw bottom arc 罚球底弧
    bottom_free_throw = Arc((0, unit * 164), top_arc_diameter, top_arc_diameter, theta1=180, theta2=0,linewidth=court_lw, color=color, linestyle='dashed')

    # Create the outer box 0f the paint, width=16ft outside , height=18ft 10in
    outer_box = Rectangle((lw/2 - unit*96, -lw/2 - unit*63), 192-lw, 230-lw, linewidth=court_lw, color=color, fill=False)
    # Create the inner box of the paint, widt=12ft, height=height=18ft 10in
    inner_box = Rectangle((lw/2 - unit*72, -lw/2 - unit*63), 144-lw, 230-lw, linewidth=court_lw, color=color, fill=False)

    ## Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    #corner_three_left = Rectangle((-264*unit, -63*unit), lw, 168*unit, linewidth=0, color=color)
    corner_three_left = Rectangle((-264*unit+lw/2, -63*unit-lw/2), 0, 169*unit, linewidth=court_lw, color=color)
    corner_three_right = Rectangle((264*unit-lw/2, -63*unit-lw/2), 0, 169*unit, linewidth=court_lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the 
    # threes 
    three_diameter = (23 * 12 + 9) * 2 - lw
    three_arc = Arc((0, 0), three_diameter, three_diameter, theta1=22, theta2=158, linewidth=court_lw, color=color)

    # Center Court
    center_outer_arc = Arc((0, (94*12/2-63)*unit), 48*unit+lw, 48*unit+lw, theta1=180, theta2=0,linewidth=court_lw, color=color)
    center_inner_arc = Arc((0, (94*12/2-63)*unit), 144*unit-lw, 144*unit-lw, theta1=180, theta2=0,linewidth=court_lw, color=color)

    # Draw the half court line, baseline and side out bound lines
    outer_lines = Rectangle((-25*12*unit - lw/2, -63*unit-lw/2), 50*12*unit+lw, 94/2*12*unit + lw, linewidth=court_lw, color=color, fill=False)

    #2 IN. WIDE BY 3 FT. DEEP, 28 FT. INSIDE, 3FT. extenf onto court

    court_elements = [hoop, hoop_neck, backboard, restricted, restricted_left, restricted_right,
                        top_free_throw,bottom_free_throw,outer_box,inner_box,corner_three_left,corner_three_right,
                        three_arc,center_outer_arc,center_inner_arc,outer_lines]

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    #地板颜色'#F7CEA2'

fig = plt.figure(figsize=(10,10))
plt.axes().set_aspect('equal')

ax = fig.add_subplot(111)


ax.set_xlim(-330,330)
ax.set_ylim(-200,600)

draw_half_court(ax=ax)

#ax.plot([7.5, 7.5], [-7.5, 7.5], 'k-', lw=2)
#ax.plot([5.5, 5.5], [-7.5, 7.5], 'k-', lw=2)


'''
draw_court(ax=ax,outer_lines=False)
plt.xlim(-300,300)
plt.ylim(-100,500)
'''
plt.show()
