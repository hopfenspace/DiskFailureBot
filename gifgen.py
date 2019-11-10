import cv2, sys
from subprocess import call

template = "servers.png"
locations = [
	# HP
	(85, 27),
	(85, 55),
	(85, 84),
	(85, 109),
	(220, 27),
	(220, 55),
	(220, 84),
	(220, 109),

	# Dell
	(250, 270),
	(250, 305),
	(250, 342),
	(250, 385),
	(430, 270),
	(430, 305),
	(430, 342),
	(430, 385),
]
size = 7
color_working = (0, 255, 0) # BGR
color_broken = (0, 0, 255) # BGR

def genAnimation(broken):
	img = cv2.imread(template)

	for i in range(0, len(locations)):
		if (i + 1) in broken:
			continue
		cv2.circle(img, locations[i], size, color_working, -1)

	cv2.imwrite("tmp1.png", img)

	for i in range(0, len(locations)):
		if (i + 1) not in broken:
			continue
		cv2.circle(img, locations[i], size, color_broken, -1)

	cv2.imwrite("tmp2.png", img)

	call(["convert",
			"-delay", "60", "tmp1.png",
			"-delay", "60", "tmp2.png",
			"output.gif"])

	call("ffmpeg -y -i output.gif -pix_fmt yuv420p -r 25 -profile:v baseline output.mp4".split(" "))

	return "output.mp4"

if __name__ == "__main__":
	broken = []
	for i in range(1, len(sys.argv)):
		broken.append(int(sys.argv[i]))

	genAnimation(broken)
