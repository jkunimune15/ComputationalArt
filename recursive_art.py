""" Header Comment """

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
            return ["cube_root", build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 8.0:
            return ["pow", build_random_function(min_depth-1,max_depth-1,varis), build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 8.5:
            return ["lnabs", build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 9.0:
            return ["abs", build_random_function(min_depth-1,max_depth-1,varis)]
        if r < 10.0:
            return ["hypot", build_random_function(min_depth-1,max_depth-1,varis), build_random_function(min_depth-1,max_depth-1,varis)]


def evaluate_function(f, x, y, t=0, a=0):
    """ Evaluate the random function f with inputs x,y,t,a
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_function(["x"],-0.5, 0.75,0)
        -0.5
        >>> evaluate_function(["y"],0.1,0.02,0)
        0.02
        >>> evaluate_function(["prod",["x"],["y"]], 2.0,3.0,0)
        6.0
        >>> evaluate_function(["avg",["x"],["y"]], 0.0,1.0,0)
        0.5
        >>> evaluate_function(["sin_pi",["x"]], -0.5,0,0)
        -1.0
        >>> evaluate_function(["cos_pi",["x"]], -0.5,0,0)
        0.0
        >>> evaluate_function(["sin_30",["x"]], 0.0,0,0)
        0.0
        >>> evaluate_function(["cos_30",["x"]], 0.0,0,0)
        1.0
        >>> evaluate_function(["tan_pi/4",["x"]], 1.0,0,0)
        1.0
        >>> evaluate_function(["neg",["x"]], 0.28319,0,0)
        -0.28319
        >>> evaluate_function(["square",["x"]], 0.5,0,0)
        -0.5
        >>> evaluate_function(["cube",["x"]], 0.5,0,0)
        0.125
        >>> evaluate_function(["cube_root",["x"]], 0.125,0,0)
        0.5
        >>> evaluate_function(["pow",["x"],["y"]], -0.25,-0.5,0)
        0.0
        >>> evaluate_function(["lnabs",["x"]], -1.0,0,0)
        1.0
        >>> evaluate_function(["abs",["x"]], -0.0,0,0)
        -1.0
        >>> evaluate_function(["hypot",["x"],["y"]], -1.0,1.0,0)
        1.0
        >>> evaluate_function(["prod", ["sin_pi", ["x"]], ["y"]], 1/6.0, 0.4,0)
        0.2
    """
    ans = 0
    if f[0] == "x":
        ans = x
    elif f[0] == "y":
        ans = y
    elif f[0] == "t":
        ans = t
    elif f[0] == "a":
        ans = a
    elif f[0] == "prod":
        ans = evaluate_function(f[1],x,y,t) * evaluate_function(f[2],x,y,t)
    elif f[0] == "avg":
        ans = 0.5*(evaluate_function(f[1],x,y,t) + evaluate_function(f[2],x,y,t))
    elif f[0] == "cos_pi":
        ans = cos(pi * evaluate_function(f[1],x,y,t))
    elif f[0] == "sin_pi":
        ans = sin(pi * evaluate_function(f[1],x,y,t))
    elif f[0] == "cos_30":
        ans = cos(30 * evaluate_function(f[1],x,y,t))
    elif f[0] == "sin_30":
        ans = sin(30 * evaluate_function(f[1],x,y,t))
    elif f[0] == "tan_pi/4":
        ans = tan(pi/4.0 * evaluate_function(f[1],x,y,t))
    elif f[0] == "neg":
        ans = -1.0* evaluate_function(f[1],x,y,t)
    elif f[0] == "square":
        ans = evaluate_function(f[1],x,y,t)**2 *2-1
    elif f[0] == "cube":
        ans = evaluate_function(f[1],x,y,t)**3
    elif f[0] == "cube_root":
        ans = evaluate_function(f[1],x,y,t)
        ans = copysign(pow(abs(ans),1/3.0), ans) # extra step needed to cube root negative numbers
    elif f[0] == "pow":
        ans = abs(evaluate_function(f[1],x,y,t))**abs(evaluate_function(f[2],x,y,t)) *2-1
    elif f[0] == "lnabs":
        ans = log(abs(evaluate_function(f[1],x,y,t))+1) / log(2)
    elif f[0] == "abs":
        ans = abs(evaluate_function(f[1],x,y,t)) *2-1
    elif f[0] == "hypot":
        ans = sqrt(evaluate_function(f[1],x,y,t)**2 + evaluate_function(f[2],x,y,t)**2) *sqrt(2)-1
    else:
        raise Exception("That's not a function I recognize!")

    return round(ans, 5) # rounds to 5 digits to make it be in bounds


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


def processAudio(music_filename):
    """
    Processes the sound and creates three lists of amplitudes for high, low, and middle ranges
    input: the filename of the wav file as a string
    output: a list of lists of ints
    """
    sampFreq, snd = wavfile.read(music_filename)
    duration = snd.shape[0]/sampFreq # I don't really know what this line does.
    s1 = snd[:,0]
    frameRate = 12#fps
    t_size = duration*frameRate
    t_step = sampFreq/frameRate    # the number of samples in each frame

    ALo = []
    AMd = []
    AHi = []
    maxLo = 0
    maxMd = 0
    maxHi = 0
    print "Processing audio..."
    for k in range(t_size):
        if k%10 == 0:
            print(int(100.0*k/t_size)), ("%") # displays percentages

        p = fft(s1[k*t_step:(k+1)*t_step])    # looks at one piece of the audio
        n = t_step
        nUniquePts = ceil((n+1)/2.0)
        p = p[0:nUniquePts]
        p = abs(p)
        p = p/float(t_step)
        p = p**2

        ALo.append(numpy.sum(p[0:30]))
        AMd.append(numpy.sum(p[30:50]))
        AHi.append(numpy.sum(p[50:1000]))
        if ALo[k] > maxLo:
            maxLo = ALo[k] # figures out how to scale volumes
        if AMd[k] > maxMd:
            maxMd = AMd[k]
        if AHi[k] > maxHi:
            maxHi = AHi[k]

    for k in range(t_size):    # scales all volumes to be in range [-1,1]
        ALo[k] = remap_interval(ALo[k], 0,maxLo, -1,1)
        AMd[k] = remap_interval(AMd[k], 0,maxMd, -1,1)
        AHi[k] = remap_interval(AHi[k], 0,maxHi, -1,1)

    return [ALo, AMd, AHi]


def generate_movie_from_sound(filename, music_filename, x_size=300, y_size=300):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(4,6,[["x"],["y"],["a"],["a"]])
    green_function = build_random_function(4,6,[["x"],["y"],["a"],["a"]])
    blue_function = build_random_function(4,6,[["x"],["y"],["a"],["a"]])
    # this is the musical part
    listOfLists = processAudio(music_filename)
    ALo = listOfLists[0]
    AMd = listOfLists[1]
    AHi = listOfLists[2]
    t_size = len(ALo)
    # Create image and loop over all pixels
    print "Generating image..."
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
                        color_map(evaluate_function(red_function, x, y, t, ALo[k])),
                        color_map(evaluate_function(green_function, x, y, t, AMd[k])),
                        color_map(evaluate_function(blue_function, x, y, t, AHi[k]))
                        )

        tee = str(2*k+1)
        while len(tee) < 3:    # this halves the framerate
            tee = "0"+tee
        im.save(filename+tee+".png")
        tee = str(2*k+2)
        while len(tee) < 3:
            tee = "0"+tee
        im.save(filename+tee+".png")


def generate_movie(filename, x_size=300, y_size=300, t_size=100):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(8,10,[["x"],["y"],["t"]])
    green_function = build_random_function(8,10,[["x"],["y"],["t"]])
    blue_function = build_random_function(8,10,[["x"],["y"],["t"]])

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
                        color_map(evaluate_function(red_function, x, y, t)),
                        color_map(evaluate_function(green_function, x, y, t)),
                        color_map(evaluate_function(blue_function, x, y, t))
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
    green_function = build_random_function(4,6,[["x"],["y"],["t"]])
    blue_function = build_random_function(4,6,[["x"],["y"],["t"]])

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        if i%10 == 0:
            print(int(100.0*i/x_size)), ("%") # displays percentages
        
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            t = evaluate_function(para_function, x, y, 0)
            pixels[i, j] = (
                    color_map(evaluate_function(red_function, x, y, t)),
                    color_map(evaluate_function(green_function, x, y, t)),
                    color_map(evaluate_function(blue_function, x, y, t))
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
        if i%10 == 0:
            print(int(100.0*i/x_size)), ("%") # displays percentages

        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            rgb_vals = hsv_to_rgb(    # this assumes that y is positive, but i and q can be negative
                    (evaluate_function(h_function, x, y)+1)/2,
                    (evaluate_function(s_function, x, y)+1)/2,
                    (evaluate_function(v_function, x, y)+1)/2
                    )
            pixels[i, j] = (int(255*rgb_vals[0]), int(255*rgb_vals[1]), int(255*rgb_vals[2]))
    im.save(filename+".png")


def generate_art(filename, x_size=1000, y_size=1000):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for parametric, red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7,9,[["x"],["y"]])
    green_function = build_random_function(7,9,[["x"],["y"]])
    blue_function = build_random_function(7,9,[["x"],["y"]])

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        if i%10 == 0:
            print(int(100.0*i/x_size)), ("%") # displays percentages

        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_function(red_function, x, y)),
                    color_map(evaluate_function(green_function, x, y)),
                    color_map(evaluate_function(blue_function, x, y))
                    )
    im.save(filename+".png")


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    #i = 1
    #while True:
    	#generate_art(str(i)+"myArt")
    	#generate_parametric_art(str(i)+"myArtPara")
    	#if i%5 == 0:
   	generate_movie("frame")
    	#generate_art_HSV(str(i)+"myArtHSV")
    	#if i%20 == 0:
    	#	generate_movie_from_sound(str(i)+"frame","ImperialMarch.wav")
    	#i = i+1

    #generate_art("myArt")
    print "Done!"
