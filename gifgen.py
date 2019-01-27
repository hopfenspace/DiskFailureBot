import cv2, sys
from subprocess import call

template = "HP-Proliant-DL380-G6.jpg"
locations = [
	(85, 150),
	(85, 178),
	(85, 207),
	(85, 232),
	(220, 150),
	(220, 178),
	(220, 207),
	(220, 232),
]
size = 7
color_working = (0, 255, 0) # BGR
color_broken = (0, 0, 255) # BGR

def genAnimation(broken):
	img = cv2.imread(template)

	if len(broken) == 0:
		cv2.putText(img, "ALL DISKS OPERATIONAL", (5, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 1, color_working, 3)
	else:
		broken_list = sorted(broken)
		broken_list = map(str, broken_list)
		broken_list = ", ".join(broken_list)

		cv2.putText(img, "PLEASE REPLACE DISK(S) " + broken_list, (5, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 1, color_broken, 3)

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
