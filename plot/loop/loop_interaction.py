import matplotlib
matplotlib.use('TkAgg')
import matplotlib.path as mpath

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

Path = mpath.Path

fig, ax = plt.subplots()

verts = [
   (0., 0.),   # P0
   (0.5, 0.4),  # P1
   (1., 0),  # P2
]

codes = [
    Path.MOVETO,
    Path.CURVE3, #我们看到CURVE4占了3个点
    Path.CURVE3,
]

path = Path(verts, codes)


pp1 = mpatches.PathPatch(
    path,
    fc="none", transform=ax.transData)

ax.add_patch(pp1)
ax.plot([0.5], [0.2], "ro")
ax.set_title('The red point should be on the path')

ax.set_ylim([0,1])

plt.show()