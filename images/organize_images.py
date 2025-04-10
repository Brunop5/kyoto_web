import os
from PIL import Image
import math

def calculate_ratio_difference(width, height):
    target_ratio = 960/640  # 1.5
    current_ratio = width/height
    return abs(current_ratio - target_ratio)

def resize_and_crop(image, target_width, target_height):
    # Calculate target aspect ratio
    target_ratio = target_width / target_height
    
    # Get current dimensions
    width, height = image.size
    current_ratio = width / height
    
    if current_ratio > target_ratio:
        # Image is wider than target ratio
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        image = image.crop((left, 0, left + new_width, height))
    else:
        # Image is taller than target ratio
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        image = image.crop((0, top, width, top + new_height))
    
    # Resize to target dimensions
    return image.resize((target_width, target_height), Image.Resampling.LANCZOS)

def process_images():
    # Create the target directory if it doesn't exist
    target_dir = "960w"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Get all files in the current directory
    files = os.listdir('.')
    print(files)
    
    # Store image information for ratio comparison
    image_info = []
    
    # First pass: collect information about all images
    for filename in files:
        # Skip directories, non-image files, and main.jpg
        if (os.path.isdir(filename) or 
            filename.lower() == 'main.jpg' or
            not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))):
            continue
            
        try:
            with Image.open(filename) as img:
                width, height = img.size
                ratio_diff = calculate_ratio_difference(width, height)
                image_info.append({
                    'filename': filename,
                    'ratio_diff': ratio_diff,
                    'img': img.copy()  # Keep a copy of the image
                })
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
    # Sort images by ratio difference and take the best 16
    image_info.sort(key=lambda x: x['ratio_diff'])
    selected_images = image_info[:16]
    
    # Process the selected images
    for info in selected_images:
        try:
            # Resize and crop the image
            processed_img = resize_and_crop(info['img'], 960, 640)
            
            # Save the processed image with the original filename
            new_path = os.path.join(target_dir, info['filename'])
            processed_img.save(new_path, 'JPEG', quality=95)
            print(f"Processed: {info['filename']}")
            
        except Exception as e:
            print(f"Error processing {info['filename']}: {str(e)}")
    
    print(f"\nTotal images processed: {len(selected_images)}")
    print(f"Images have been resized and saved to the '{target_dir}' directory")

if __name__ == "__main__":
    process_images()