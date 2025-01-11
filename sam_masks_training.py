import os
import argparse
from datetime import datetime

startTime = datetime.now()

parser = argparse.ArgumentParser(description='Setup the environment')
parser.add_argument("--dataset_name", "-d", required=True, type=str)
parser.add_argument("--image_scale", "-s", required=True, type=str, help="Can be 1, 2, 4 or 8")
parser.add_argument("--prompt", "-p", required=False, type=str, default="", help="Prompt for text guided segmentation. If empty, segmentation will be automatic.")
args = parser.parse_args()

print(f"Preparing Labels for Dataset {args.dataset_name}...")
if args.prompt:
    os.system(f"bash grouping/script/prepare_pseudo_label_with_prompt.sh {args.dataset_name} {args.image_scale} {args.prompt}")
else:
    os.system(f"bash grouping/script/prepare_pseudo_label.sh {args.dataset_name} {args.image_scale}")
print("Labels for Gaussian Splatting training prepared.")

print(f"Training 3D Gaussian Grouping Model for Dataset {args.dataset_name}...")
os.system(f"bash grouping/script/train.sh {args.dataset_name} {args.image_scale}")
print("Training of 3D Gaussian Grouping model finished.")

print(f"Done. Took {print(datetime.now() - startTime)}.")