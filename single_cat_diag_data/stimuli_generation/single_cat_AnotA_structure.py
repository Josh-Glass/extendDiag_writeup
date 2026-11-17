import numpy as np 
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.patches as patches


#################################################################################################################################################
###############################################################################################################################################
###################################################### MAKE STIM AND PLOT STRUCTURE ##############################################################
#################################################################################################################################################
#################################################################################################################################################


# # # # # # # # # # # # # # # # 
# 
#  Square Creator Function
# 
# # # # # # # # # # # # # # # # 

def generate_square(dim1, dim2, filename):
    lab_monitor = 1440/41 #<-- pixel info about lab monitor ensuring correct sizes
    res_w = lab_monitor

    # get correct dims
    dim2 = ( (dim2) * (230 - 25) ) + 25
    dim1 = ( (dim1) * (7.1 - 2.5) ) + 2.5


    d = dim1 * res_w
    s = int(np.round(dim2))

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



# ==========================================
# 1. VERIFICATION FUNCTION
# ==========================================
def verify_distances(target_A, cat_X, cat_Y):
    """Calculates and prints the minimum City-Block (L1) distance from A to X and Y."""
    dist_X = [round(abs(target_A[0] - x[0]) + abs(target_A[1] - x[1]), 4) for x in cat_X]
    dist_Y = [round(abs(target_A[0] - y[0]) + abs(target_A[1] - y[1]), 4) for y in cat_Y]
    
    min_X, min_Y = min(dist_X), min(dist_Y)
    
    print(f"--- DISTANCE VERIFICATION FOR LAST A AT {target_A} ---")
    print(f"Nearest Category X exemplar is at {cat_X[np.argmin(dist_X)]}")
    print(f"City-Block Distance to X: {min_X}")
    print(f"Nearest Category Y exemplar is at {cat_Y[np.argmin(dist_Y)]}")
    print(f"City-Block Distance to Y: {min_Y}")
    print("EQUIDISTANT?" , "YES!" if min_X == min_Y else "NO.")
    print("-" * 52)



# # # # # # # # # # # # # # # # 
# 
#  Create Images from Data
# 
# # # # # # # # # # # # # # # # 



# ==========================================
# 2. SETUP STRICT MATHEMATICAL COORDINATES
# ==========================================
# All coordinates shifted by +0.2 to move them to the top right

# X items (x > y): 3 diagonals
dataX = np.array([
    [.8, .7], [.9, .8], [1.0, .9],  # Diag 1 (closest to boundary, 3 items)
    [.9, .7], [1.0, .8],            # Diag 2 (2 items) 
    [1.0, .7]                       # Diag 3 (corner, 1 item)
])

# Y items (y > x): 3 diagonals
dataY = np.array([
    [.7, .8], [.8, .9], [.9, 1.0],  # Diag 1 (closest to boundary, 3 items)
    [.7, .9], [.8, 1.0],            # Diag 2 (2 items) 
    [.7, 1.0]                       # Diag 3 (corner, 1 item)
])

# Training items (A only, denser distribution)
dataA = np.array([
    [.250, .050], 
    [.325, .125], # New midpoint 1
    [.400, .200], 
    [.475, .275], # New midpoint 2
    [.550, .350], 
    [.625, .425], # New midpoint 3
    [.700, .500]
])


# Training items "Not A" (6 items, slope = -1, perpendicularly bisecting A at the midpoint)
# We skip the exact center [0.475, 0.275] so it doesn't print directly on top of the A item.
dataNotA = np.array([
    # Top-Left side (4 items)
    [.125, .625], 
    [.200, .550], 
    [.275, .475], 
    [.350, .400], 
    
    # --- WIDE BUFFER ZONE ---
    # Center A is at [0.475, 0.275]
    # --- WIDE BUFFER ZONE ---
    
    # Bottom-Right side (3 items)
    [.600, .150], 
    [.675, .075], 
    [.750, .000]  # Safely bottoms out exactly at y=0!
])



# Target item: The last A (closest to test items)
target_A = [.7, .5]

# Run verification
verify_distances(target_A, dataX, dataY)









import os
os.makedirs('single_cat_ANOTA', exist_ok=True)

for index, i in enumerate(dataA):
    generate_square(i[0], i[1], 'single_cat_ANOTA/' + 'A' + str(index+1) + '.png')


for index, i in enumerate(dataNotA):
    generate_square(i[0], i[1], 'single_cat_ANOTA/' + 'NotA' + str(index+1) + '.png')

for index, i in enumerate(dataX):
    generate_square(i[0], i[1], 'single_cat_ANOTA/' + 'X' + str(index+1) + '.png')


for index, i in enumerate(dataY):
    generate_square(i[0], i[1], 'single_cat_ANOTA/' + 'Y' + str(index+1) + '.png')



# ==========================================
# 3. PLOTTING
# ==========================================
fig, ax = plt.subplots(figsize=(8, 8))

# Yellow Shaded Region
rect = patches.Rectangle((.65, .65), .4, .4, linewidth=1.5, 
                         edgecolor='gray', facecolor='#fdfd96', alpha=0.9, zorder=0)
ax.add_patch(rect)

# The Decision Boundary (y = x)
ax.plot([-0.05, 1.1], [-0.05, 1.1], color='k', linestyle=(0, (5, 5)), linewidth=2, zorder=1)

# Plot Training Items (A only)
for coord in dataA:
    ax.text(coord[0], coord[1], 'A', color='red', fontsize=22, ha='center', va='center')


for coord in dataNotA:
    ax.text(coord[0], coord[1], '!A', color='Gray', fontsize=18, ha='center', va='center')

# Plot Test Items
for coord in dataX:
    ax.text(coord[0], coord[1], 'X', color='black', fontsize=16, ha='center', va='center')

for coord in dataY:
    ax.text(coord[0], coord[1], 'Y', color='black', fontsize=16, ha='center', va='center')


# ==========================================
# 4. ADD DISTANCE ANNOTATIONS
# ==========================================
# 1. A to Y (Target A is 0.7, 0.5. Nearest Y is 0.7, 0.8. Straight vertical line)
ax.plot([.7, .7], [.54, .77], color='gray', linewidth=1.5)
ax.text(.65, .6, '$D=0.3$', fontsize=14, ha='center')

# 2. A to X (Target A is 0.7, 0.5. Nearest X is 0.8, 0.7. L-Shape)
# Horizontal part: starts right of A, goes right to x=0.8
ax.plot([.73, .8], [.5, .5], color='gray', linewidth=1.5)      
# Vertical part: starts at corner y=0.5, goes up to below X at y=0.67
ax.plot([.8, .8], [.5, .67], color='gray', linewidth=1.5)      

# Text placement
ax.text(.82, .58, '$D=0.3$', fontsize=14)

# Formatting
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)
ax.set_aspect('equal')

plt.tight_layout()
plt.savefig('single_cat_diag_AnotA.png', dpi=300)
plt.show()

