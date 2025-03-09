import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup the environment')

    parser.add_argument('--no_rasterizer', action='store_true', help='Skip installation of diff-gaussian-rasterizer')
    parser.add_argument('--no_simple_knn', action='store_true', help='Skip installation of simple-knn')
    parser.add_argument('--no_sam', action='store_true', help='Skip installation of SAM')
    parser.add_argument('--no_grounding_dino', action='store_true', help='Skip installation of GroundingDINO')
    parser.add_argument('--no_nvdiffrast', action='store_true', help='Skip installation of Nvdiffrast')
    # parser.add_argument('--no_deva', action='store_true', help='Skip installation of Tracking-Anything-with-DEVA')
    # parser.add_argument('--no_lama', action='store_true', help='Skip installation of LaMa')
    args = parser.parse_args()
    
    # Create a new conda environment
    print("[INFO] Creating the conda environment for Great3DGSForVR...")
    os.system("conda env create -f environment.yml")
    print("[INFO] Conda environment created.")

    # Install 3D Gaussian Splatting rasterizer
    if args.no_rasterizer:
        print("[INFO] Skipping installation of diff-gaussian-rasterization.")
    else:
        print("[INFO] Installing the 3D Gaussian Splatting rasterizer...")
        os.chdir("server/great3dgsforvr/submodules/")
        os.system("git clone --recursive https://github.com/YviKiwi00/diff-gaussian-rasterization.git")
        os.system("conda run -n Great3DGSForVR pip install -e ./diff-gaussian-rasterization")
        print("[INFO] 3D Gaussian Splatting rasterizer installed.")
        os.chdir("../../../")

    # Install simple-knn
    if args.no_simple_knn:
        print("[INFO] Skipping installation of simple-knn.")
    else:
        print("[INFO] Installing simple-knn...")
        os.chdir("server/great3dgsforvr/submodules/")
        os.system("conda run -n Great3DGSForVR pip install ./simple-knn")
        print("[INFO] simple-knn installed.")
        os.chdir("../../../")

    # Install SAM
    if args.no_sam:
        print("[INFO] Skipping installation of SAM.")
    else:
        os.chdir("server/great3dgsforvr/SAGS/gaussiansplatting/")
        print("[INFO] Installing SAM for SAGD...")
        os.makedirs("dependencies", exist_ok=True)
        os.chdir("dependencies/")
        os.makedirs("sam_ckpt", exist_ok=True)
        os.chdir("sam_ckpt/")
        os.system("wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth")
        os.system("git clone git@github.com:facebookresearch/segment-anything.git")
        os.chdir("segment-anything/")
        os.system("conda run -n Great3DGSForVR pip install -e .")
        print("[INFO] SAM for SAGD installed.")
        os.chdir("../../../../../../../")

    # Install GroundingDINO
    if args.no_grounding_dino:
        print("[INFO] Skipping installation of GroundingDINO.")
    else:
        os.chdir("server/great3dgsforvr/SAGS/gaussiansplatting/dependencies/sam_ckpt/segment-anything/")
        print("[INFO] Installing GroundingDINO for SAGD...")
        os.system("git clone https://github.com/IDEA-Research/GroundingDINO.git")
        os.chdir("GroundingDINO/")
        os.system("conda run -n Great3DGSForVR pip install -e .")
        os.makedirs("weights/")
        os.chdir("weights/")
        os.system("wget https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth")
        print("[INFO] GroundingDino for SAGD installed.")
        os.chdir("../../../../../../../../../")

    # Install Nvdiffrast
    if args.no_nvdiffrast:
        print("[INFO] Skipping installation of Nvdiffrast.")
    else:
        print("[INFO] Installing Nvdiffrast...")
        os.system("git clone https://github.com/NVlabs/nvdiffrast")
        os.chdir("nvdiffrast")
        os.system("conda run -n frosting pip install .")
        print("[INFO] Nvdiffrast installed.")
        print(
            "[INFO] Please note that Nvdiffrast will take a few seconds or minutes to build the first time it is used.")
        os.chdir("../")

    print("[INFO] Great3DGSForVR installation complete.")
