from PIL import Image
import os, sys

size = 150, 150

for infile in sys.argv[1:]:
    outfile = "thumbnails/" + os.path.splitext(infile)[0] + ".thumbnails"
    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail(size)
            im.save(outfile, "JPEG")
        except IOError:
            print("Could not create thumb", infile)
