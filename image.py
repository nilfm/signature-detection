from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

path_to_file = './'

im_frame = Image.open(path_to_file + 'test.png')
np_frame = np.array(im_frame.getdata()).reshape(470, 600)

np_frame[np_frame > 1] = 1

plt.imshow(np_frame, cmap = 'gray')
plt.show()
# plt.scatter([2,3],[4,5])
