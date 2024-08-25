import os
from PIL import Image, ImageDraw, ImageFilter

# Define paths
input_folder = '/storage/emulated/0/input'  # Input folder path
output_folder = '/storage/emulated/0/output'  # Output folder path

# Ensure output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def remove_watermark(image_path, output_path, watermark_area):
    try:
        # Open the image
        image = Image.open(image_path)
        width, height = image.size

        # Define the area of the watermark
        x1, y1, x2, y2 = watermark_area

        # Create a new image for watermark removal
        new_image = image.copy()
        draw = ImageDraw.Draw(new_image)

        # Define a patch size to cover the watermark
        patch_width = x2 - x1
        patch_height = y2 - y1

        # Create a patch by blending pixels from adjacent areas
        def get_patch_area(x1, y1, x2, y2):
            # Define areas around the watermark
            if x1 < patch_width:
                left_area = (x1 + patch_width, y1, x2 + patch_width, y2)
            else:
                left_area = (x1 - patch_width, y1, x2 - patch_width, y2)

            if x2 > width - patch_width:
                right_area = (x1 - patch_width, y1, x2 - patch_width, y2)
            else:
                right_area = (width - patch_width, y1, width, y2)

            return left_area, right_area

        left_patch_area, right_patch_area = get_patch_area(x1, y1, x2, y2)

        # Crop patches from adjacent areas
        left_patch = image.crop(left_patch_area)
        right_patch = image.crop(right_patch_area)

        # Resize patches to fit the watermark area
        left_patch = left_patch.resize((patch_width, patch_height))
        right_patch = right_patch.resize((patch_width, patch_height))

        # Blend patches over the watermark area
        new_image.paste(left_patch, (x1, y1))
        new_image.paste(right_patch, (x1 + patch_width, y1))

        # Optional: Apply Gaussian Blur to blend edges
        blur_radius = 3
        new_image = new_image.filter(ImageFilter.GaussianBlur(blur_radius))

        # Save the modified image
        new_image.save(output_path)
        print(f"Watermark removed and image saved as {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Define the size of the watermark area in pixels
    watermark_width = 200  # Adjust width for coverage
    watermark_height = 150  # Adjust height for better coverage

    # Check if the input folder contains images
    images_found = False

    # Process all images in the input folder
    for image_file in os.listdir(input_folder):
        if image_file.endswith(('jpg', 'jpeg', 'png')):
            images_found = True
            image_path = os.path.join(input_folder, image_file)

            # Open the image to determine its dimensions
            with Image.open(image_path) as img:
                width, height = img.size

            # Define the watermark area
            watermark_area = (0, int(height - watermark_height - 20), watermark_width, height)  # Adjust as needed

            # Define the output path
            output_path = os.path.join(output_folder, f"cleaned_{image_file}")

            # Remove the watermark from the image
            remove_watermark(image_path, output_path, watermark_area)

    if not images_found:
        print("No images found in the input folder.")

if __name__ == "__main__":
    main()
