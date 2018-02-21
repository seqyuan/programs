
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc,Wedge


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
    restricted = Arc((0, 0), 96+lw, 96+lw, theta1=0, theta2=180,linewidth=court_lw, color='#767676', fill=False)
    restricted_left = Rectangle((-48*unit-lw/2, unit * -15 ), 0, unit * 17, linewidth=court_lw, color='#767676')
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


fig = plt.figure(figsize=(12,11))
ax = fig.add_subplot(111,aspect='equal')
ax.set_xlim(-330,330)
ax.set_ylim(800,-100)


draw_half_court(ax=ax)

'''
import pandas as pd
shot_df = pd.read_excel('outfile.xlsx', sheetname=0, header=0, index_col=0)

df_made = shot_df[shot_df.EVENT_TYPE=='Made Shot'][['LOC_X','LOC_Y']]
ax.scatter(df_made.LOC_X, df_made.LOC_Y,s=1,color='b',label = 'Made Shot')
df_missed = shot_df[shot_df.EVENT_TYPE=='Missed Shot'][['LOC_X','LOC_Y']]
ax.scatter(df_missed.LOC_X, df_missed.LOC_Y,s=1,color='r',label = 'Missed Shot')

ax.legend()
ax.set_xlabel('')
ax.set_ylabel('')
#ax.tick_params(labelbottom='off', labelleft='off')
plt.axis('off')
ax.set_title('James Harden FGA \n2017-18 Reg. Season', y=1.2, fontsize=18)

'''

plt.show()
