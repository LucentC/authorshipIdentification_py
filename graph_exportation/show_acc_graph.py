import numpy as np
import matplotlib.pyplot as plt

SHD = (0.45, 0.2, 0.2)
PHD = (0.6, 0.6, 0.6)
MHD = (0.6, 0.6, 0.65)

N = 3

ind = np.arange(N)    # the x locations for the groups
print ind
width = 0.2       # the width of the bars: can also be len(x) sequence

fig, ax = plt.subplots()
rects1 = ax.bar(ind + width * 0, SHD, width, color='r')
rects2 = ax.bar(ind + width * 1, PHD, width, color='y')
rects3 = ax.bar(ind + width * 2, MHD, width, color='g')

ax.set_xlabel('Paragraph classes')
ax.set_ylabel('Accuracy')
ax.set_title('Accuracy when k = 5')
ax.set_xticks(ind + (width * 3)/2.)
ax.set_xticklabels(('20-40', '40-60', '60-80'))
ax.set_yticks(np.arange(0, 1, 0.1))
ax.legend((rects1[0], rects2[0], rects3[0]), ('SHD', 'PHD', 'MHD'))

plt.show()
