import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup the environment')
    
    parser.add_argument('--no_nvdiffrast', action='store_true', help='Skip installation of Nvdiffrast')
    parser.add_argument('--no_deva', action='store_true', help='Skip installation of Tracking-Anything-with-DEVA')
    parser.add_argument('--no_lama', action='store_true', help='Skip installation of LaMa')
    args = parser.parse_args()
    
    # Create a new conda environment
    print("[INFO] Creating the conda environment for Great3DGSForVR...")
    os.system("conda env create -f environment.yml")
    print("[INFO] Conda environment created.")
    
    # Install 3D Gaussian Splatting rasterizer
    print("[INFO] Installing the 3D Gaussian Splatting rasterizer...")
    os.chdir("frosting/gaussian_splatting/submodules/diff-gaussian-rasterization/")
    os.system("conda run -n Great3DGSForVR pip install -e .")
    print("[INFO] 3D Gaussian Splatting rasterizer installed.")
    
    # Install simple-knn
    print("[INFO] Installing simple-knn...")
    os.chdir("../simple-knn/")
    os.system("conda run -n Great3DGSForVR pip install -e .")
    print("[INFO] simple-knn installed.")
    os.chdir("../../../../")
    
    # Install Nvdiffrast
    if args.no_nvdiffrast:
        print("[INFO] Skipping installation of Nvdiffrast.")
    else:
        print("[INFO] Installing Nvdiffrast...")
        os.system("git clone https://github.com/NVlabs/nvdiffrast")
        os.chdir("nvdiffrast/")
        os.system("conda run -n Great3DGSForVR pip install .")
        print("[INFO] Nvdiffrast installed.")
        print("[INFO] Please note that Nvdiffrast will take a few seconds or minutes to build the first time it is used.")
        os.chdir("../")

    # Install Tracking-Anything-with-DEVA
    if args.no_deva:
        print("[INFO] Skipping installation of Tracking-Anything-with-DEVA.")
    else:
        print("[INFO] Installing Tracking-Anything-with-DEVA...")
        os.chdir("grouping/Tracking-Anything-with-DEVA/")
        os.system("conda run -n Great3DGSForVR pip install -e .")
        os.system("bash scripts/download_models.sh")
        os.system("git clone https://github.com/hkchengrex/Grounded-Segment-Anything.git")
        os.chdir("Grounded-Segment-Anything")
        os.system("export AM_I_DOCKER=False")
        os.system("export BUILD_WITH_CUDA=True")
        os.system("conda run -n Great3DGSForVR pip install -e segment_anything")
        os.system("conda run -n Great3DGSForVR pip install -e GroundingDINO")
        print("[INFO] Tracking-Anything-with-DEVA installed.")
        os.chdir("../../../")

    # Install LaMa
    if args.no_lama:
        print("[INFO] Skipping installation of LaMa.")
    else:
        print("[INFO] Installing LaMa...")
        os.chdir("grouping/lama/")
        os.system("conda run -n Great3DGSForVR pip install -r requirements.txt")
        print("[INFO] LaMa installed.")
        os.chdir("../../")

    print("[INFO] Great3DGSForVR installation complete.")
