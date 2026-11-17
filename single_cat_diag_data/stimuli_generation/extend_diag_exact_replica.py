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
def verify_distances(target, cat_A, cat_B):
    """Calculates and prints the minimum City-Block (L1) distance to categories."""
    # Added round() to handle Python's floating-point math quirks with decimals
    dist_A = [round(abs(target[0] - a[0]) + abs(target[1] - a[1]), 4) for a in cat_A]
    dist_B = [round(abs(target[0] - b[0]) + abs(target[1] - b[1]), 4) for b in cat_B]
    
    min_A, min_B = min(dist_A), min(dist_B)
    
    print(f"--- DISTANCE VERIFICATION FOR TARGET {target} ---")
    print(f"Nearest Category A exemplar is at {cat_A[np.argmin(dist_A)]}")
    print(f"City-Block Distance to A: {min_A}")
    print(f"Nearest Category B exemplar is at {cat_B[np.argmin(dist_B)]}")
    print(f"City-Block Distance to B: {min_B}")
    print("EQUIDISTANT?" , "YES!" if min_A == min_B else "NO.")
    print("-" * 47)



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

# Training items (4 items each)
# STRETCHED: Spacing increased to 0.15. Top-most items remain locked.
dataB = np.array([[.05, .25], [.20, .40], [.35, .55], [.5, .7]])
dataA = np.array([[.25, .05], [.40, .20], [.55, .35], [.7, .5]])

# Target item for the D=0.3 demonstration
target_X = [.8, .7]

# Run verification
verify_distances(target_X, dataA, dataB)











for index, i in enumerate(dataA):
    generate_square(i[0], i[1], 'single_cat_obs/' + 'A' + str(index+1) + '.png')


for index, i in enumerate(dataX):
    generate_square(i[0], i[1], 'single_cat_obs/' + 'X' + str(index+1) + '.png')


for index, i in enumerate(dataY):
    generate_square(i[0], i[1], 'single_cat_obs/' + 'Y' + str(index+1) + '.png')



# ==========================================
# 3. PLOTTING
# ==========================================
fig, ax = plt.subplots(figsize=(8, 8))

# Yellow Shaded Region (Shifted to match new data)
rect = patches.Rectangle((.65, .65), .4, .4, linewidth=1.5, 
                         edgecolor='gray', facecolor='#fdfd96', alpha=0.9, zorder=0)
ax.add_patch(rect)

# The Decision Boundary (y = x)
ax.plot([-0.05, 1.1], [-0.05, 1.1], color='k', linestyle=(0, (5, 5)), linewidth=2, zorder=1)

# Plot Training Items
for coord in dataB:
    ax.text(coord[0], coord[1], 'B', color='blue', fontsize=22, ha='center', va='center')

for coord in dataA:
    ax.text(coord[0], coord[1], 'A', color='red', fontsize=22, ha='center', va='center')

# Plot Test Items
for coord in dataX:
    ax.text(coord[0], coord[1], 'X', color='black', fontsize=16, ha='center', va='center')

for coord in dataY:
    ax.text(coord[0], coord[1], 'Y', color='black', fontsize=16, ha='center', va='center')

# ==========================================
# 4. ADD DISTANCE ANNOTATIONS
# ==========================================
# B to target (Target X is at 0.8, 0.7. Nearest B is 0.5, 0.7. Horizontal line)
ax.plot([.53, .77], [.7, .7], color='gray', linewidth=1.5)
ax.text(.65, .72, '$D=0.3$', fontsize=14, ha='center') # Left the text as D=3 to match original figure conceptually

# A to target (Target X is at 0.8, 0.7. Nearest A is 0.7, 0.5.)
# 1. Horizontal part: starts slightly right of A, goes right to x=0.8
ax.plot([.73, .8], [.5, .5], color='gray', linewidth=1.5)      
# 2. Vertical part: starts at corner y=0.5, goes up to slightly below X
ax.plot([.8, .8], [.5, .67], color='gray', linewidth=1.5)      

# Text placement
ax.text(.82, .58, '$D=0.3$', fontsize=14)

# Formatting
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)
# ax.set_xticks([]) 
# ax.set_yticks([])
ax.set_aspect('equal')

plt.tight_layout()
plt.savefig('exact_replica_diag.png', dpi=300)
plt.show()

# #Graph all the A's
# plt.scatter(dataA[0,0], dataA[0,1], c = 'r', s=450, marker= (r'$A1$'))
# plt.scatter(dataA[1,0], dataA[1,1], c = 'r', s=450, marker= (r'$A2$'))
# plt.scatter(dataA[2,0], dataA[2,1], c = 'r', s=450, marker= (r'$A3$'))
# plt.scatter(dataA[3,0], dataA[3,1], c = 'r', s=450, marker= (r'$A4$'))
# plt.scatter(dataA[4,0], dataA[4,1], c = 'r', s=450, marker= (r'$A5$'))
# plt.scatter(dataA[5,0], dataA[5,1], c = 'r', s=450, marker= (r'$A6$'))
# plt.scatter(dataA[6,0], dataA[6,1], c = 'r', s=450, marker= (r'$A7$'))
# plt.scatter(dataA[7,0], dataA[7,1], c = 'r', s=450, marker= (r'$A8$'))
# plt.scatter(dataA[8,0], dataA[8,1], c = 'r', s=450, marker= (r'$A9$'))






# #Graph all the T's
# plt.scatter(dataT[0,0], dataT[0,1], c = 'k', s=450, marker= (r'$T1$'))
# plt.scatter(dataT[1,0], dataT[1,1], c = 'k', s=450, marker= (r'$T2$'))
# plt.scatter(dataT[2,0], dataT[2,1], c = 'k', s=450, marker= (r'$T3$'))
# plt.scatter(dataT[3,0], dataT[3,1], c = 'k', s=450, marker= (r'$T4$'))
# plt.scatter(dataT[4,0], dataT[4,1], c = 'k', s=450, marker= (r'$T5$'))
# plt.scatter(dataT[5,0], dataT[5,1], c = 'k', s=450, marker= (r'$T6$'))
# plt.scatter(dataT[6,0], dataT[6,1], c = 'k', s=450, marker= (r'$T7$'))
# plt.scatter(dataT[7,0], dataT[7,1], c = 'k', s=450, marker= (r'$T8$'))
# plt.scatter(dataT[8,0], dataT[8,1], c = 'k', s=450, marker= (r'$T9$'))




# plt.axvline(x=0.5, ymin=0, ymax=1, color='k', linestyle='dotted', linewidth=2)
# plt.axhline(y=0.5, xmin=0, xmax=1, color='k', linestyle='dotted', linewidth=2)
# plt.xlim(-0.05,1.05)
# plt.ylim(-0.05,1.05)
# plt.xlabel("Size")
# plt.ylabel("lightness")

# plt.savefig('single_cat_obs.png')

print("DONE!")