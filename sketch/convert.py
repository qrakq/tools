import cv2
import numpy as np
import os
import argparse

def process_image_for_ink_saving(input_path, output_path):
    """
    Process an image to create a black-and-white contour pencil drawing.
    If the image is predominantly dark, it negates the image to save ink.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the processed image file.
    """
    # Load the image
    image = cv2.imread(input_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   
#    adaptive_thresh = cv2.adaptiveThreshold(
#        gray,
#        maxValue=255,
#        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # Mean of the neighborhood
#        thresholdType=cv2.THRESH_BINARY,
#        blockSize=31,  # Size of neighborhood area (odd number)
#        C=2           # Subtract 2 to fine-tune
#    )
    # Apply GaussianBlur to smooth the image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Detect edges using the Canny edge detector
    edges = cv2.Canny(blurred, 30, 100)
    
    # Optional: Dilate edges to make them bolder
#   kernel = np.ones((2, 2), np.uint8)
#   edges = cv2.dilate(edges, kernel, iterations=1)
    # Calculate the mean brightness of the grayscale image
    mean_brightness = np.mean(gray)
    # If the image is predominantly dark, invert the edge-detected image
    if mean_brightness < 128:  # Threshold for "dark" image
        edges = cv2.bitwise_not(edges)
    
    # Save the result
    cv2.imwrite(output_path, edges)

def batch_process_images(input_dir, output_dir):
    """
    Process all images in a directory and save the results in another directory.

    Args:
        input_dir (str): Path to the input directory containing images.
        output_dir (str): Path to the output directory for saving processed images.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        
        # Check if the file is an image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            output_path = os.path.join(output_dir, filename)
            print(f"Processing {input_path} -> {output_path}")
            process_image_for_ink_saving(input_path, output_path)
        else:
            print(f"Skipping non-image file: {filename}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Batch process images for ink-saving sketches.")
    parser.add_argument("input_dir", type=str, help="Path to the input directory containing images.")
    parser.add_argument("output_dir", type=str, help="Path to the output directory for saving processed images.")
    args = parser.parse_args()

    # Batch process images
    batch_process_images(args.input_dir, args.output_dir)


