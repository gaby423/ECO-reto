from detection.run_detector_batch import load_and_run_detector_batch,write_results_to_file
from md_utils import path_utils
import os

# Pick a folder to run MD on recursively, and an output file
image_folder = os.path.expanduser('~/images/gxcevr.jpeg')
output_file = os.path.expanduser('~/images/megadetector_output_test.json')

# Recursively find images
image_file_names = path_utils.find_images(image_folder,recursive=True)

# This will automatically download MDv5a; you can also specify a filename.
results = load_and_run_detector_batch('MDV5A', image_file_names)

print(results)