from swampy.TurtleWorld import *



def snow_flake_side(ttl, length, level):
	if level == 0:
		fd(ttl, length)
	else:
		snow_flake_side(ttl, length/3.0, level-1)
		lt(ttl, 60)
		snow_flake_side(ttl, length/3.0, level-1)
		rt(ttl, 120)
		snow_flake_side(ttl, length/3.0, level-1)
		lt(ttl, 60)
		snow_flake_side(ttl, length/3.0, level-1)


def dragon_curve(ttl, length, level):
	draw_dragon(ttl, length, level, True)


def draw_dragon(ttl, length, level, direc):
	if level == 0:
		fd(ttl, length)
	else:
		if direc:	# direction alternates
			draw_dragon(ttl,length*.7071,level-1, direc)
			rt(ttl)
			draw_dragon(ttl,length*.7071,level-1, not direc)
		else:
			draw_dragon(ttl,length*.7071,level-1, not direc)
			lt(ttl)
			draw_dragon(ttl,length*.7071,level-1, direc)


def levy_C_curve(ttl, length, level):
	if level == 0:
		fd(ttl, length)
	else:
		lt(ttl, 45)
		levy_C_curve(ttl, length*.7071, level-1)
		rt(ttl)
		levy_C_curve(ttl, length*.7071, level-1)
		lt(ttl, 45)


def recursive_tree(ttl, length, level):
	if level == 0:
		fd(ttl, length)
	else:
		fd(ttl, length)
		tts = clone(ttl)
		lt(tts, 30)
		recursive_tree(tts, length*0.6, level-1)
		tts.undraw()
		ttl.bk(length/3.0)
		lzd = clone(ttl)
		rt(lzd, 40)
		recursive_tree(lzd, length*0.64, level-1)
		lzd.undraw()


def clone(ttl):
	tts = Turtle()
	tts.x = ttl.x
	tts.y = ttl.y
	tts.heading = ttl.heading
	return tts


tmnt = TurtleWorld()
raphael = Turtle()
raphael.delay = 0
levy_C_curve(raphael, 100, 14)
wait_for_user()