import os
import argparse


def delete_every_nth_image(folder, step):
    """
    Deletes every n-th image in the specified folder.

    Args:
        folder (str): Path to the folder containing images.
        step (int): Delete every n-th image (1-based indexing).
    """
    # Get all files in the folder and sort them
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

    if step <= 0:
        raise ValueError("Step (n) must be greater than 0.")

    # Iterate through files and delete every n-th file
    for index, file in enumerate(files, start=1):
        if index % step == 0:  # Check if the file is the n-th file
            file_path = os.path.join(folder, file)
            os.remove(file_path)
            print(f"Deleted: {file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete every n-th image from a folder.")
    parser.add_argument("--image_path", type=str, help="Path to the folder containing images.")
    parser.add_argument("--image_number", type=int, help="Delete every n-th image (e.g., n=3 means delete 3rd, 6th, 9th, etc.).")

    args = parser.parse_args()

    delete_every_nth_image(folder=args.image_path, step=args.image_number)
