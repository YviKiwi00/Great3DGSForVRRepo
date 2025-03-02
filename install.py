import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup the environment')
    
    # parser.add_argument('--no_nvdiffrast', action='store_true', help='Skip installation of Nvdiffrast')
    # parser.add_argument('--no_deva', action='store_true', help='Skip installation of Tracking-Anything-with-DEVA')
    # parser.add_argument('--no_lama', action='store_true', help='Skip installation of LaMa')
    # args = parser.parse_args()
    
    # Create a new conda environment
    print("[INFO] Creating the conda environment for Great3DGSForVR...")
    os.system("conda env create -f environment.yml")
    print("[INFO] Conda environment created.")


    print("[INFO] Great3DGSForVR installation complete.")
