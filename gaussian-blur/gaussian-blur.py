import math
import os
import argparse
import numpy as np
from PIL import Image


parser = argparse.ArgumentParser()
parser.add_argument('--save', type=bool, default=True, help='whether or not to save output files')
parser.add_argument('--show', type=bool, default=False, help='whether to show input/output image or not')
parser.add_argument('--file', type=str, default='/assets/cbox.png', help='input image file')
parser.add_argument('--save_name', type=str, default='out.png', help='input image file')


# Gaussian Kernel 
def gaussian_kernel(size = 3, sigma = 1):
    ax = np.linspace(-(size - 1) / 2 , (size  - 1) / 2 , size) # evenly distributed over interval (start, end) 
    gaussian = np.exp(-0.5 * np.square(ax) / np.square(sigma)) # gaussian function
    kernel = np.outer(gaussian, gaussian) # gaussian matrix
    return kernel / np.sum(kernel) # normalize
    

# Convolution operation
def convolve2D(image, kernel, padding=0, strides=1):
    # Cross Correlation
    kernel = np.flipud(np.fliplr(kernel))

    # Gather Shapes of Kernel + Image + Padding
    xKernShape = kernel.shape[0]
    yKernShape = kernel.shape[1]
    xImgShape = image.shape[0]
    yImgShape = image.shape[1]

    # Shape of Output Convolution
    xOutput = int(((xImgShape - xKernShape + 2 * padding) / strides) + 1)
    yOutput = int(((yImgShape - yKernShape + 2 * padding) / strides) + 1)
    output = np.zeros((xOutput, yOutput, image.shape[2]))

    # Apply Equal Padding to All Sides
    if padding != 0:
        imagePadded = np.zeros((image.shape[0] + padding*2, image.shape[1] + padding*2))
        imagePadded[int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = image
        print(imagePadded)
    else:
        imagePadded = image
    
    # Iterate through image
    for y in range(image.shape[1]):
        # Exit Convolution
        if y > image.shape[1] - yKernShape:
            break
        # Only Convolve if y has gone down by the specified Strides
        if y % strides == 0:
            for x in range(image.shape[0]):
                # Go to next row once kernel is out of bounds
                if x > image.shape[0] - xKernShape:
                    break
                try:
                    # Only Convolve if x has moved by the specified Strides
                    if x % strides == 0:
                        for channel in range(image.shape[2]):
                            output[x, y, channel] = (kernel[:,:,channel] * imagePadded[x: x + xKernShape, y: y + yKernShape, channel]).sum()
                except:
                    break
    return output

def main():
    args = parser.parse_args()
    img = np.array(Image.open(f'{os.getcwd()}{args.file}'))
    kernel = gaussian_kernel(size=10, sigma = 2)
    kernel = np.repeat(kernel[:, :, np.newaxis], 3, axis = 2)
    img_out = convolve2D(img , kernel = kernel).astype(np.uint8)
    if args.show:
        Image.open(f'{os.getcwd()}{args.file}').show()
        Image.fromarray(img_out).show()
    
    if args.save:
        img_out = Image.fromarray(img_out)
        save_path = f'{os.getcwd()}/results/gaussian-blur'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        img_out.save(f'{save_path}/{args.save_name}')


if __name__ == "__main__":
    main()