""" A file to generate random art with various algorithms """

import random
import numpy as np
from PIL import Image
import math
import colorsys
import os


def build_random_function(min_depth, max_depth, numVaris=2, time=False):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        numVaris: the number of variables this function may incorporate
        time: True if t represents time, False if it represents a parametric component or does not exist
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    if max_depth <= 0 or random.random() < -min_depth/5.0:    # it will simpy return a variable if it has hit the max depth or if it is past the min depth
        n = random.randint(1,numVaris)

        if time and n == 3:  # if there is a t
            func = random.choice([np.sin,np.cos])
            coef = random.choice([3, 5, 7, 10, 23])
            return lambda x,y,t=0: func(t*coef)
        else:
            if n == 1:
                return lambda x,y,t=0: x
            if n == 2:
                return lambda x,y,t=0: y
            if n == 3:
                return lambda x,y,t=0: t

    else:                                                     # otherwise it will return an actual function
        r = random.random()    # the variable that will decide which function to pick
        arg1 = build_random_function(min_depth-1,max_depth-1,numVaris,time)
        if r < .33:
            arg2 = build_random_function(min_depth-1,max_depth-1,numVaris,time)

        if r < .10:
            return lambda x,y,t=0: arg1(x,y,t) * arg2(x,y,t)
        if r < .20:
            return lambda x,y,t=0: (arg1(x,y,t) + arg2(x,y,t))/2.0
        if r < .27:
            return lambda x,y,t=0: np.hypot(arg1(x,y,t), arg2(x,y,t)) *math.sqrt(2)-1
        if r < .30:
            return lambda x,y,t=0: np.copysign(arg1(x,y,t), arg2(x,y,t))
        if r < .33:
            return lambda x,y,t=0: np.power(arg1(x,y,t), np.floor(10*np.absolute(arg2(x,y,t))))
        if r < .49:
            return lambda x,y,t=0: np.sin(arg1(x,y,t) * random.choice([math.pi, 3, 4, 5, 30]))
        if r < .65:
            return lambda x,y,t=0: np.cos(arg1(x,y,t) * random.choice([math.pi, 3, 4, 5, 30]))
        if r < .70:
            return lambda x,y,t=0: np.tan(arg1(x,y,t) * math.pi/4)
        if r < .75:
            return lambda x,y,t=0: np.negative(arg1(x,y,t))
        if r < .80:
            return lambda x,y,t=0: np.power(arg1(x,y,t), 3)
        if r < .85:
            return lambda x,y,t=0: ((lambda value: np.copysign(np.sqrt(np.absolute(value)), value))(arg1(x,y,t)))
        if r < .90:
            return lambda x,y,t=0: np.log(np.absolute(arg1(x,y,t))+1) /math.log(4)-1
        if r < .95:
            return lambda x,y,t=0: np.absolute(arg1(x,y,t)) *2-1
        if r < 1.0:
            return lambda x,y,t=0: np.square(arg1(x,y,t)) *2-1


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    maped_to_01 = (float)(val-input_interval_start)/(input_interval_end-input_interval_start)
    return maped_to_01*(output_interval_end-output_interval_start) + output_interval_start


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def build_x_coordinates(w,h,d=1):
    """
    bulids a numpy array representing a coordinate system
    w,h = integers representing the dimensions of the array
    returns a numpy array with dimensions w and h and values from -1.0 to 1.0

    >>> build_x_coordinates(3,3)
    array([[-1.,  0.,  1.],
           [-1.,  0.,  1.],
           [-1.,  0.,  1.]])

    """
    basicArray = []
    for z in range(d):
        level = []
        for y in range(h):
            row = []
            for x in range(w):
                row.append(x*2.0/(w-1)-1)
            level.append(row)
        basicArray.append(level)
    if d > 1:
        return np.array(basicArray)
    else:
        return np.array(basicArray[0])


def build_y_coordinates(w,h,d=1):
    """
    bulids a numpy array representing a coordinate system
    w,h = integers representing the dimensions of the array
    returns a numpy array with dimensions w and h and values from -1.0 to 1.0

    >>> build_y_coordinates(3,3)
    array([[-1., -1., -1.],
           [ 0.,  0.,  0.],
           [ 1.,  1.,  1.]])
    """
    basicArray = []
    for z in range(d):
        level = []
        for y in range(h):
            row = []
            for x in range(w):
                row.append(y*2.0/(h-1)-1)
            level.append(row)
        basicArray.append(level)
    if d > 1:
        return np.array(basicArray)
    else:
        return np.array(basicArray[0])


def build_t_coordinates(w,h,d=1):
    """
    bulids a numpy array representing a coordinate system
    w,h = integers representing the dimensions of the array
    returns a numpy array with dimensions w and h and values from -1.0 to 1.0

    >>> build_t_coordinates(2,2,d=2)
    array([[[-1., -1.],
            [-1., -1.]],
    <BLANKLINE>
           [[ 1.,  1.],
            [ 1.,  1.]]])
    """
    basicArray = []
    for z in range(d):
        level = []
        for y in range(h):
            row = []
            for x in range(w):
                row.append(z*2.0/(d-1)-1)
            level.append(row)
        basicArray.append(level)
    return np.array(basicArray)


def generate_movie(filename, x_size=500, y_size=500, t_size=300):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(9,11, 3,True)
    grn_function = build_random_function(9,11, 3,True)
    blu_function = build_random_function(9,11, 3,True)
    # Input arrays
    x = build_x_coordinates(x_size, y_size, t_size)
    y = build_y_coordinates(x_size, y_size, t_size)
    t = build_t_coordinates(x_size, y_size, t_size)
    # Evaluate the functions
    red_channel = red_function(x, y, t)
    grn_channel = grn_function(x, y, t)
    blu_channel = blu_function(x, y, t)
    # Creates a folder for these frames
    if not os.path.exists("New_Art/"+filename+"/"):
        os.makedirs("New_Art/"+filename+"/")

    for k in range(t_size):
        print(int(100.0*k/t_size))+1, ("%") # displays percentages
        # Create image and loop over all pixels
        im = Image.new("RGB", (x_size, y_size))
        pixels = im.load()
        for i in range(x_size):
            for j in range(y_size):
                pixels[i, j] = (
                    color_map(red_channel[k,i,j]),
                    color_map(grn_channel[k,i,j]),
                    color_map(blu_channel[k,i,j])
                    )
        im.save("New_Art/"+filename+"/frame{:03d}.png".format(k))


def generate_parametric_art(filename, x_size=1000, y_size=1000):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(4,6, numVaris=3)
    grn_function = build_random_function(4,6, numVaris=3)
    blu_function = build_random_function(4,6, numVaris=3)
    par_function = build_random_function(4,6, numVaris=2)
    # Input arrays
    x = build_x_coordinates(x_size, y_size)
    y = build_y_coordinates(x_size, y_size)
    # Evaluate the functions
    par_channel = par_function(x, y)
    red_channel = red_function(x, y, par_channel)
    grn_channel = grn_function(x, y, par_channel)
    blu_channel = blu_function(x, y, par_channel)
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    im2 = Image.new("L", (x_size, y_size))
    pixels = im.load()
    pixel2 = im2.load()
    for i in range(x_size):
        for j in range(y_size):
            pixels[i, j] = (
                    color_map(red_channel[i,j]),
                    color_map(grn_channel[i,j]),
                    color_map(blu_channel[i,j])
                    )
            pixel2[i, j] = color_map(par_channel[i,j])
    im.save("New_Art/"+filename+".png")
    im2.save("New_Art/"+filename+"_.png")


def generate_art_HSV(filename, x_size=1000, y_size=1000):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for yrightness, iagenta, and qlue channels - where the magic happens!
    h_function = build_random_function(7,9)
    s_function = build_random_function(7,9)
    v_function = build_random_function(7,9)
    # Input arrays
    x = build_x_coordinates(x_size, y_size)
    y = build_y_coordinates(x_size, y_size)
    # Evaluate the functions
    h_channel = h_function(x, y)
    s_channel = s_function(x, y)
    v_channel = v_function(x, y)
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            rgb_vals = colorsys.hsv_to_rgb(
                (h_channel[i,j]+1)/2,
                (s_channel[i,j]+1)/2,
                (v_channel[i,j]+1)/2
                )
            pixels[i, j] = (int(255*rgb_vals[0]), int(255*rgb_vals[1]), int(255*rgb_vals[2]))
    im.save("New_Art/"+filename+".png")


def generate_art(filename, x_size=1000, y_size=1000):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7,9)
    grn_function = build_random_function(7,9)
    blu_function = build_random_function(7,9)
    # Input arrays
    x = build_x_coordinates(x_size, y_size)
    y = build_y_coordinates(x_size, y_size)
    # Evaluate the functions
    red_channel = red_function(x, y)
    grn_channel = grn_function(x, y)
    blu_channel = blu_function(x, y)
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            pixels[i, j] = (
                    color_map(red_channel[i,j]),
                    color_map(grn_channel[i,j]),
                    color_map(blu_channel[i,j])
                    )
    im.save("New_Art/"+filename+".png")


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    i = 0
    while True:
        generate_art(str(i)+"myArt")
        generate_art_HSV(str(i)+"myArtHSV")
    	generate_parametric_art(str(i)+"myArtPara")
        #if i%5 == 0:
    	#   generate_movie(str(i)+"myFrames")
    	i += 1

print "Done!"