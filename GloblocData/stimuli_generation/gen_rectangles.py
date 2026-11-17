import numpy as np 
from PIL import Image, ImageDraw




# # # # # # # # # # # # # # # # 
# 
#  Square Creator Function
# 
# # # # # # # # # # # # # # # # 

def generate_square(dim1, dim2, filename):
    lab_monitor = 1440/41 #<-- pixel info about lab monitor ensuring correct sizes
    res_w = lab_monitor

    # get correct dims
    dim1 = ( (dim1) * (230 - 25) ) + 25
    dim2 = ( (dim2) * (7.1 - 2.5) ) + 2.5


    d = dim2 * res_w
    s = int(np.round(dim1))

    # size of image
    v=250
    canvas = (v,v)

    # something for saving it (idk i didn't write these next parts)
    thumb = canvas[0], canvas[1]

    # init canvas
    im = Image.new('RGBA', canvas, (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)

    # draw rectangles
    x1 = canvas[0]/2 - d/2
    y1 = canvas[0]/2 + d/2
    x2 = canvas[0]/2 + d/2
    y2 = canvas[0]/2 - d/2

    draw.rectangle([x1, y1, x2, y2],
        outline = (0, 0, 0, 255), 
        fill = (s,s,s,255),
    )

    # make thumbnail
    im.thumbnail(thumb)

    # save image
    im.save(filename)







# # # # # # # # # # # # # # # # 
# 
#  Create Images from Data
# 
# # # # # # # # # # # # # # # # 

data = np.array([
    [.02,.02], # A
    [.08,.08], # A
    [.14,.14], # A

    [.2,.2], # A
    [.26,.26], # A
    [.32,.32], # A

    [.04,.98], # B
    [.12,.74], # B
    [.24,.88], # B

    [.36,.04], # B
    [.56,.1], # B
    [.7,.52], # B

    [.6, .6],  # generalzation test items
    [.8, .6],  # generalzation test items
    [.28, .12],  # generalzation test items
    [.48, .48],  # generalization test item
    [.12, .28],  # generalization test item

    [.78,.14], # C
    [.9,.06], # C
    [.94,.18], # C

    [.04,.44], # C
    [.06,.62], # C
    [.18,.58], # C

    [.26, 1], # D
    [.34, 1], # D
    [.42, 1], # D

    [.5, 1], # D
    [.58, 1], # D
    [.66, 1], # D


])

for index, i in enumerate(data):
    generate_square(i[0], i[1], 'images/' + str(index) + '.png')





# plot if you want

import matplotlib.pyplot as plt

#labels = [0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4]
labels = ['r','r','r','r','r','r','b','b','b','b','b','b','y','y','y','y','y','k','k','k','k','k','k','g','g','g','g','g','g']
plt.scatter(
        data[:,0],
        data[:,1],
        c = labels,
)
plt.savefig('structure.png')
