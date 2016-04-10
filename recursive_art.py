""" TODO: Put your header comment here """

import random
import numpy
from PIL import Image
from math import *
from random import *
from colorsys import *
from pylab import*
from scipy.io import wavfile


def build_random_function(min_depth, max_depth, varis):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    if max_depth <= 0 or random() < -min_depth/5.0:    # it will simpy return a variable if it has hit the max depth or if it is past the min depth
        return choice(varis)
    else:    # return an actual function
        r = random()*10.0    # the variable that will decide which function to pick
        if r < 1.0:
            return ["prod", build_random_function(min_depth-1,max_depth-1,varis), build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 2.0:
            return ["avg", build_random_function(min_depth-1,max_depth-1,varis), build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 3.0:
            return ["sin_pi", build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 4.0:
            return ["cos_pi", build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 4.5:
            return ["cos_30", build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 5.0:
            return ["sin_30", build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 5.5:
            return ["tan_pi/4", build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 6.0:
            return ["neg", build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 6.5:
            return ["square", build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 7.0:
            return ["cube", build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 7.5:
            return ["square_root", build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 8.0:
            return ["lnabs", build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 8.5:
            return ["abs", build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 9.0:
            return ["hypot", build_random_function(min_depth-1,max_depth-1,varis), build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 9.5:
            return ["copysign", build_random_function(min_depth-1,max_depth-1,varis), build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 10.0:
            return ["pow", build_random_function(min_depth-1,max_depth-1,varis), build_random_function(min_depth-1,max_depth-1,varis)]


def evaluate(f, x, y):
    """
    evaluates a function over a set of points
    f = a list representing the function
    x, y = a numpy array of floats representing a coordinate system
    returns a numpy array of floats in range [-1.0,1.0]

    >>> evaluate(["avg", ["x"],["y"]], np.array([1.0, 0.0]), np.array([0.5, 0.5]))
    array([ 0.75,  0.25])
    """
    if f[0] == "x":
        ans = x
    elif f[0] == "y":
        ans = y
    elif f[0] == "prod":
        ans = evaluate(f[1],x,y) * evaluate(f[2],x,y)
    elif f[0] == "avg":
        ans = 0.5*(evaluate(f[1],x,y) + evaluate(f[2],x,y))
    elif f[0] == "cos_pi":
        ans = np.cos(pi * evaluate(f[1],x,y))
    elif f[0] == "sin_pi":
        ans = np.sin(pi * evaluate(f[1],x,y))
    elif f[0] == "cos_30":
        ans = np.cos(30 * evaluate(f[1],x,y))
    elif f[0] == "sin_30":
        ans = np.sin(30 * evaluate(f[1],x,y))
    elif f[0] == "tan_pi/4":
        ans = np.tan(pi/4.0 * evaluate(f[1],x,y))
    elif f[0] == "neg":
        ans = np.negative(evaluate(f[1],x,y))
    elif f[0] == "square":
        ans = np.square(evaluate(f[1],x,y))
    elif f[0] == "cube":
        ans = np.power(evaluate(f[1],x,y), 3)
    elif f[0] == "square_root":
        ans = evaluate(f[1],x,y)
        ans = np.copysign(np.sqrt(np.absolute(ans)), ans)
    elif f[0] == "lnabs":
        ans = np.log(np.absolute(evaluate(f[1],x,y))+1) / log(2)
    elif f[0] == "abs":
        ans = np.absolute(evaluate(f[1],x,y)) *2-1
    elif f[0] == "hypot":
        ans = np.hypot(evaluate(f[1],x,y), evaluate(f[2],x,y)) *sqrt(2)-1
    elif f[0] == "pow":
        ans = np.power(evaluate(f[1],x,y), np.floor(10*np.absolute(evaluate(f[2],x,y))))
    elif f[0] == "copysign":
        ans = np.copysign(evaluate(f[1],x,y), evaluate(f[2],x,y))
    else:
        raise TypeError(f[0]+" is not a supported function!")

    return np.around(ans, 5) # rounds to 5 digits to make it be in bounds


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


def build_x_coordinates(w,h):
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
    for y in range(h):
        row = []
        for x in range(w):
            row.append(x*2.0/(w-1)-1)
        basicArray.append(row)
    return np.array(basicArray)


def build_y_coordinates(w,h):
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
    for y in range(h):
        row = []
        for x in range(w):
            row.append(y*2.0/(h-1)-1)
        basicArray.append(row)
    return np.array(basicArray)


def generate_movie(filename, x_size=300, y_size=300, t_size=100):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(8,10,[["x"],["y"],["t"],["t"]])
    grn_function = build_random_function(8,10,[["x"],["y"],["t"],["t"]])
    blu_function = build_random_function(8,10,[["x"],["y"],["t"],["t"]])

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for k in range(t_size):
        print(int(100.0*k/t_size)), ("%") # displays percentages

        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                t = remap_interval(k, 0, t_size, -1, 1)
                pixels[i, j] = (
                        color_map(evaluate(red_function, x, y, t)),
                        color_map(evaluate(grn_function, x, y, t)),
                        color_map(evaluate(blu_function, x, y, t))
                        )

        tee = str(k+1)
        while len(tee) < 3:
            tee = "0"+tee
        im.save(filename+tee+".png")


def generate_parametric_art(filename, x_size=1000, y_size=1000):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for parametric, red, green, and blue channels - where the magic happens!
    para_function = build_random_function(3,5,[["x"],["y"]])
    red_function = build_random_function(4,6,[["x"],["y"],["t"]])
    grn_function = build_random_function(4,6,[["x"],["y"],["t"]])
    blu_function = build_random_function(4,6,[["x"],["y"],["t"]])

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            t = evaluate(para_function, x, y, 0)
            pixels[i, j] = (
                    color_map(evaluate(red_function, x, y, t)),
                    color_map(evaluate(grn_function, x, y, t)),
                    color_map(evaluate(blu_function, x, y, t))
                    )
    im.save(filename+".png")


def generate_art_HSV(filename, x_size=1000, y_size=1000):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for yrightness, iagenta, and qlue channels - where the magic happens!
    h_function = build_random_function(7,9,[["x"],["y"]])
    s_function = build_random_function(7,9,[["x"],["y"]])
    v_function = build_random_function(7,9,[["x"],["y"]])

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            rgb_vals = hsv_to_rgb(    # this assumes that y is positive, but i and q can be negative
                    (evaluate(h_function, x, y)+1)/2,
                    (evaluate(s_function, x, y)+1)/2,
                    (evaluate(v_function, x, y)+1)/2
                    )
            pixels[i, j] = (int(255*rgb_vals[0]), int(255*rgb_vals[1]), int(255*rgb_vals[2]))
    im.save(filename+".png")


def generate_art(filename, x_size=1000, y_size=1000):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7,9,[["x"],["y"]])
    grn_function = build_random_function(7,9,[["x"],["y"]])
    blu_function = build_random_function(7,9,[["x"],["y"]])
    # Input arrays
    x = build_x_coordinates(x_size, y_size)
    y = build_y_coordinates(x_size, y_size)
    # Evaluate the functions
    red_channel = evaluate(red_function, x, y)
    grn_channel = evaluate(grn_function, x, y)
    blu_channel = evaluate(blu_function, x, y)
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
    im.save(filename+".png")


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    i = 1
    while True:
        generate_art(str(i)+"myArt")
    	#generate_parametric_art(str(i)+"myArtPara")
    	#if i%5 == 0:
        #generate_movie("frame")
    	#generate_art_HSV(str(i)+"myArtHSV")
    	#if i%20 == 0:
    	#	generate_movie_from_sound(str(i)+"frame","ImperialMarch.wav")
    	i = i+1

print "Done!"
