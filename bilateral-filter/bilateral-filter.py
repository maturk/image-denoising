'''
Bilateral filter
by: Matias
'''

import math
import os
import argparse
import numpy as np
from PIL import Image


parser = argparse.ArgumentParser()
parser.add_argument('--save', type=bool, default=True, help='whether or not to save output files')
parser.add_argument('--show', type=bool, default=True, help='whether to show input/output image or not')
parser.add_argument('--file', type=str, default='/assets/cbox.png', help='input image file')
parser.add_argument('--save_name', type=str, default='out', help='input image file')
parser.add_argument('--size', type=int, default=10, help='kernel size')
parser.add_argument('--sigma_color', type=int, default=30, help='standard deviation for gaussian kernel')
parser.add_argument('--sigma_space', type=int, default=30, help='standard deviation for gaussian kernel')


# Gaussian function
def gaussian(x, sigma):
    return (1.0/(2*np.pi*(sigma**2)))*np.exp(-(x**2)/(2*(sigma**2))) 

def distance(x1,y1,x2,y2):
    return np.sqrt(np.abs((x1-x2)**2-(y1-y2)**2))

# bilateral filter
def bilateral_filter(src, size = 5, sigma_color = 1, sigma_space = 1):
    if len(src.shape) == 2:
        channels = 1
    elif src.shape[2]==3:
        channels = 3
    else:
        print('Invalid source image')
        exit
    
    r = math.floor(size / 2) # diameter of kernel
    out_image = np.zeros(src.shape)
    
    # iterate over pixels in src image
    for row in range(src.shape[0]): # x
        for col in range(src.shape[1]): # y
            total_weight = 0 
            pixel = 0
            
            # kernel range
            for kernel_x in range(-r, r):
                for kernel_y in range(-r,r):
                    x = row - kernel_x
                    y = col - kernel_y
                    # skip out of bounds kernels 
                    if x >= src.shape[0]:
                        continue
                    if y >= src.shape[1]:
                        continue
                    # color and distane weights
                    intensity_weight = gaussian(src[x][y] - src[row][col], sigma_color) # gaussian on pixel intensities
                    distance_weight = gaussian(math.sqrt((x - row)**2 +(y - col)**2), sigma_space) # gaussian on pixel distances
                    weight = intensity_weight * distance_weight
                    total_weight += weight
                    pixel += weight*src[x][y]
                    
            # normalize pixel by total accumulated weight
            pixel = pixel // total_weight
            out_image[row,col] = pixel
    return out_image


def main():
    args = parser.parse_args()
    img = np.array(Image.open(f'{os.getcwd()}{args.file}'))
    out_image = bilateral_filter(img, args.size, args.sigma_color, args.sigma_space).astype(np.uint8)
    
    if args.show:
        Image.open(f'{os.getcwd()}{args.file}').show()
        Image.fromarray(out_image).show()
    
    if args.save:
        out_image = Image.fromarray(out_image)
        save_path = f'{os.getcwd()}/results/bilateral'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        out_image.save(f'{save_path}/{args.save_name}_{args.size}_{args.sigma_color}_{args.sigma_space}.png')
    

if __name__ == "__main__":
    main()