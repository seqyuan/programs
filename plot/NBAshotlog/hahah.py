import matplotlib.pyplot as plt

from matplotlib.patches import Circle, Rectangle, Arc, Wedge

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




def draw_half_court(ax=None, lineColor='white', unit = 1,courtColor='#F7CEA2'):
    if ax is None:
        ax = plt.gca()

    lw = unit * 2 #line width
    color = 'k'

    court_lw = data_linewidth_plot(ax = ax,linewidth = lw).lw

    ## Create the basketball hoop
    #篮筐直径(内径)是18IN.,我们设置半径为9.2IN刨除line width 0.2IN,正好为篮筐半径

    # Create free throw top arc  罚球线弧顶
    #top_free_throw = Arc((0, 0), 12, 6, theta1=0, theta2=180,linewidth=10, color=color, fill=False)
    top_free_throw = Wedge((0, 0), unit * 10, 0, 360, width=unit * 2, color='y')
    top_free_throw_2 = Wedge((0, 0), unit * 10, 0, 360, width=unit * 1,joinstyle='bevel', color='r',alpha = 0.3)
    
    # Create free throw bottom arc 罚球底弧
    bottom_free_throw = Arc((0, 0), 18, 18, theta1=0, theta2=360,linewidth=court_lw, color='b', alpha = 0.3,linestyle='dashed')


    court_elements = [top_free_throw,bottom_free_throw]

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    #地板颜色'#F7CEA2'



fig = plt.figure(figsize=(6,6))

ax = fig.add_subplot(111,aspect='equal')
#ax.set_aspect('equal')
ax.set_xlim(-12,12)
ax.set_ylim(-12,12)

draw_half_court(ax=ax)



plt.show()
