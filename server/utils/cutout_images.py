import os
import numpy as np
from PIL import Image
import argparse

def process_images(masks_folder, images_folder, output_folder, background_color=(255, 255, 255, 255)):
    """
    Process binary masks and corresponding original images to cutout rgb object,
    excluding black as background. Saves output in separate folder.

    Args:
        masks_folder (str): Path to the folder containing binary mask images.
        images_folder (str): Path to the folder containing original images.
        output_folder (str): Path to save the resulting images.
        background_color (tuple): RGB color for the background (default is white).
    """
    os.makedirs(output_folder, exist_ok=True)

    mask_files = sorted([f for f in os.listdir(masks_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    image_files = sorted([f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

    # if len(mask_files) != len(image_files):
    #     raise ValueError("The number of masks and images should be the same.")

    for mask_file, image_file in zip(mask_files, image_files):
        mask_base = os.path.splitext(mask_file)[0]
        image_base = os.path.splitext(image_file)[0]

        if image_base not in mask_base:
            continue

        mask_path = os.path.join(masks_folder, mask_file)
        image_path = os.path.join(images_folder, image_file)

        mask = np.array(Image.open(mask_path).convert("L"))
        image = np.array(Image.open(image_path).convert("RGBA"))

        mask = mask > 128

        if len(background_color) == 4:  # Transparent background (RGBA)
            extracted_object = np.zeros((*image.shape[:2], 4), dtype=np.uint8)  # RGBA image
            extracted_object[:, :, :3] = background_color[:3]  # Set background color
            extracted_object[:, :, 3] = background_color[3]  # Set background alpha
            extracted_object[mask] = image[mask]  # Copy RGB
        else:  # Opaque background (RGB)
            extracted_object = np.full_like(image[:, :, :3], background_color[:3], dtype=np.uint8)
            extracted_object[mask] = image[mask][:, :3]

        os.makedirs(output_folder, exist_ok=True)

        # Save the resulting image
        output_path = os.path.join(output_folder, f"{os.path.splitext(mask_file)[0]}.png")
        if len(background_color) == 4:  # Transparent background
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
    )