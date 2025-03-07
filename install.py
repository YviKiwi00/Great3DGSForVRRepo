import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup the environment')
    
    parser.add_argument('--no_nvdiffrast', action='store_true', help='Skip installation of Nvdiffrast')
    # parser.add_argument('--no_deva', action='store_true', help='Skip installation of Tracking-Anything-with-DEVA')
    # parser.add_argument('--no_lama', action='store_true', help='Skip installation of LaMa')
    args = parser.parse_args()
    
    # Create a new conda environment
    print("[INFO] Creating the conda environment for Great3DGSForVR...")
    os.system("conda env create -f environment.yml")
    print("[INFO] Conda environment created.")

    # Install 3D Gaussian Splatting rasterizer and simple-knn for MCMC
    print("[INFO] Installing the 3D Gaussian Splatting rasterizer for MCMC...")
    os.chdir("server/great3dgsforvr/3dgs-mcmc/submodules/")
    os.system("git clone --recursive https://github.com/YviKiwi00/diff-gaussian-rasterization.git")
    os.system("conda run -n Great3DGSForVR pip install ./diff-gaussian-rasterization")
    print("[INFO] 3D Gaussian Splatting rasterizer for MCMC installed.")

    print("[INFO] Installing simple-knn for MCMC...")
    os.system("conda run -n Great3DGSForVR pip install ./simple-knn")
    print("[INFO] simple-knn for MCMC installed.")
    os.chdir("../../../../")

    # Install 3D Gaussian Splatting rasterizer, simple-knn, SAM and GroundingDINO for SAGD
    print("[INFO] Installing the 3D Gaussian Splatting rasterizer for SAGD...")
    os.chdir("server/great3dgsforvr/SAGS/gaussiansplatting/submodules/")
    os.system("git clone --recursive https://github.com/YviKiwi00/diff-gaussian-rasterization.git")
    os.system("conda run -n Great3DGSForVR pip install ./diff-gaussian-rasterization")
    print("[INFO] 3D Gaussian Splatting rasterizer for SAGD installed.")

    print("[INFO] Installing simple-knn for SAGD...")
    os.system("conda run -n Great3DGSForVR pip install ./simple-knn")
    print("[INFO] simple-knn for SAGD installed.")
    os.chdir("../")

    print("[INFO] Installing SAM for SAGD...")
    os.makedirs("dependencies", exist_ok=True)
    os.chdir("dependencies/")
    os.system("wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth")
    os.system("git clone git@github.com:facebookresearch/segment-anything.git")
    os.chdir("segment-anything/")
    os.system("conda run -n Great3DGSForVR pip install -e .")
    print("[INFO] SAM for SAGD installed.")

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
