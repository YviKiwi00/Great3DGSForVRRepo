import os
import argparse

parser = argparse.ArgumentParser(description='Setup the environment')
parser.add_argument("--dataset_name", "-d", required=True, type=str)
parser.add_argument("--image_scale", "-s", required=True, type=str, help="Can be 1, 2, 4 or 8")
args = parser.parse_args()

print(f"Preparing Labels for Dataset {args.dataset_name}...")
os.system(f"bash grouping/script/prepare_pseudo_label.sh {args.dataset_name} {args.image_scale}")
print("Labels for Gaussian Splatting training prepared.")