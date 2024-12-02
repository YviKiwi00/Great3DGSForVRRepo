import os
import numpy as np
from PIL import Image
import argparse
import random
import string


def generate_random_string(length=10):
    """Generates a random string of given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def process_images(masks_folder, images_folder, output_folder, background_color=(255, 255, 255, 255), random_folder_names=False, step=1):
    """
    Process binary masks and corresponding original images to extract objects based on color codes,
    excluding black as background. Saves output in separate folders per color code.

    Args:
        masks_folder (str): Path to the folder containing binary mask images.
        images_folder (str): Path to the folder containing original images.
        output_folder (str): Path to save the resulting images.
        background_color (tuple): RGB color for the background (default is white).
        random_folder_names (bool): Whether to use random names for output folders instead of color codes.
        step (int): Process only every n-th image (default is 1, i.e., process all images).
    """
    os.makedirs(output_folder, exist_ok=True)
    mask_files = sorted([f for f in os.listdir(masks_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    image_files = sorted([f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

    if len(mask_files) != len(image_files):
        raise ValueError("The number of masks and images should be the same.")

    mask_files = mask_files[::step]
    image_files = image_files[::step]

    for mask_file, image_file in zip(mask_files, image_files):
        mask_path = os.path.join(masks_folder, mask_file)
        image_path = os.path.join(images_folder, image_file)

        mask = np.array(Image.open(mask_path))
        image = np.array(Image.open(image_path))

        # Ensure the mask is in RGB format
        if mask.ndim == 2:  # If mask is grayscale, convert to RGB
            mask = np.stack([mask] * 3, axis=-1)

        unique_colors = np.unique(mask.reshape(-1, mask.shape[2]), axis=0)

        for color in unique_colors:
            if np.all(color == [0, 0, 0]):  # Skip black (background) color
                continue

            color_mask = (mask == color).all(axis=-1)
            if background_color[-1] < 255:  # Transparent background (RGBA)
                extracted_object = np.zeros((*image.shape[:2], 4), dtype=np.uint8)  # RGBA image
                extracted_object[color_mask, :3] = image[color_mask]  # Copy RGB
                extracted_object[color_mask, 3] = 255  # Set alpha to opaque for the object
                extracted_object[~color_mask] = background_color  # Set background to specified RGBA
            else:  # Opaque background (RGB)
                extracted_object = np.zeros_like(image)
                extracted_object[color_mask] = image[color_mask]
                extracted_object[~color_mask] = background_color[:3]  # Use only RGB values

            # Determine folder name
            color_code = "_".join(map(str, color))
            folder_name = generate_random_string() if random_folder_names else color_code
            color_folder = os.path.join(output_folder, folder_name)
            os.makedirs(color_folder, exist_ok=True)

            # Save the resulting image
            output_path = os.path.join(color_folder, f"{mask_file.split('.')[0]}.png")
            if background_color[-1] < 255:  # Transparent background
                Image.fromarray(extracted_object, mode="RGBA").save(output_path)
            else:  # Opaque background
                Image.fromarray(extracted_object).save(output_path)
            print(f"Saved: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract objects from masks with specific color coding.")
    parser.add_argument("--masks_folder", type=str, help="Path to the folder containing binary masks.")
    parser.add_argument("--images_folder", type=str, help="Path to the folder containing original images.")
    parser.add_argument("--output_folder", type=str, help="Path to save the resulting images.")
    parser.add_argument("--background_color", type=int, nargs='+', default=(255, 255, 255, 255),
                        help="Background color as RGBA values (default is white and opaque).")
    parser.add_argument("--random_folder_names", action="store_true",
                        help="Use random names for output folders instead of color codes.")
    parser.add_argument("--step", type=int, default=1,
                        help="Process only every n-th image (default is 1, i.e., process all images).")

    args = parser.parse_args()
    if len(args.background_color) not in {3, 4}:
        raise ValueError("Background color must have 3 (RGB) or 4 (RGBA) values.")
    if len(args.background_color) == 3:
        args.background_color = tuple(args.background_color) + (255,)  # Add alpha for full opacity if not provided


    process_images(
        masks_folder=args.masks_folder,
        images_folder=args.images_folder,
        output_folder=args.output_folder,
        background_color=tuple(args.background_color),
        random_folder_names=args.random_folder_names,
        step=args.step
    )
