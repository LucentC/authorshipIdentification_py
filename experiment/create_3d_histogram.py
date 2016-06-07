from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

thedata = np.genfromtxt(
                        'mydata.csv',       # file to read
                        skip_header=0,      # lines to skip at the top
                        skip_footer=0,      # lines to skip at the bottom
                        delimiter=',',      # column delimiter
                        dtype='float32'     # data type
                        )

x = thedata[:, 0]    # data from the first column
y = thedata[:, 1]    # data from the second column

hist, xedges, yedges = np.histogram2d(x, y, bins=4)

elements = (len(xedges) - 1) * (len(yedges) - 1)    # number of boxes
xpos, ypos = np.meshgrid(xedges[:-1]+0.25, yedges[:-1]+0.25)
xpos = xpos.flatten()           # x-coordinates of the bars
ypos = ypos.flatten()           # y-coordinates of the bars
zpos = np.zeros(elements)       # zero-array
dx = 0.5 * np.ones_like(zpos)   # length of the bars along the x-axis
dy = dx.copy()                  # length of the bars along the y-axis
dz = hist.flatten()             # height of the bars

fig = plt.figure()
ax = Axes3D(fig)

bar_colors = ['red', 'green', 'blue', 'aqua',
          'burlywood', 'cadetblue', 'chocolate', 'cornflowerblue',
          'crimson', 'darkcyan', 'darkgoldenrod', 'darkgreen',
          'purple', 'darkred', 'darkslateblue', 'darkviolet']


boxes = []
for thecolor in bar_colors:
    boxes.append(plt.Rectangle((0, 0), 1, 1, fc=thecolor)) # set legend colours

legends = ['label1', 'label2', 'label3', 'label4',
           'label5', 'label6', 'label7', 'label8',
           'label9', 'label10', 'label11', 'label12',
           'label12', 'label14', 'label15', 'label16']

ax.legend(boxes, legends)       # adds the legend labels

ax.bar3d(xpos, ypos, zpos,      # lower corner coordinates
         dx, dy, dz,            # width, depth and height
         color=bar_colors,      # bar colour
         alpha=0.6              # transparency of the bars
         )

ax.w_xaxis.set_ticklabels([])   # remove x-axis tick labels
ax.w_yaxis.set_ticklabels([])   # remove y-axis tick labels
ax.set_title('3D Histogram')    # title

ax.view_init(elev=28, azim=60)  # camera elevation and angle
ax.dist=12                      # camera distance

plt.show()                      # display the plot
