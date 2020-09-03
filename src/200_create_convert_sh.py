import os
import argparse
import sys
import glob

input_dir = "../docs/files/original/**/*.jpg"

files = glob.glob(input_dir, recursive=True)

f = open("c.sh", 'w')

for file in files:
    new_file_path = file.replace("/original/", "/tile/").replace(".jpg", ".tif")
    new_output_dir = os.path.dirname(new_file_path)

    f.write("mkdir -p " + new_output_dir + "\n")
    f.write("if [ ! -e \""+ new_file_path + "\" ]; then\n")
    f.write(
        "   convert " + file + " -define tiff:tile-geometry=256x256 -compress jpeg 'ptif:" + new_file_path + "'\n")
    f.write("fi\n")

f.close()
