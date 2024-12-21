import argparse
from PyPDF2 import PdfReader, PdfWriter

def crop_pdf(input_path, output_path, border_thickness):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        # Get the original page dimensions
        original_width = float(page.mediabox.width)
        original_height = float(page.mediabox.height)
        
        # Calculate the crop box
        left = border_thickness
        lower = border_thickness
        right = original_width - border_thickness
        upper = original_height - border_thickness

        # Apply the crop box
        page.cropbox.lower_left = (left, lower)
        page.cropbox.upper_right = (right, upper)
        writer.add_page(page)

    # Save the cropped PDF
    with open(output_path, "wb") as output_file:
        writer.write(output_file)

def main():
    parser = argparse.ArgumentParser(description="Crop black frames from PDF pages by specifying border thickness.")
    parser.add_argument("input", type=str, help="Path to the input PDF file.")
    parser.add_argument("output", type=str, help="Path to save the cropped PDF.")
    parser.add_argument("border_thickness", type=float, help="Thickness of the border to crop (applied equally to all sides).")

    args = parser.parse_args()

    crop_pdf(args.input, args.output, args.border_thickness)
    print(f"PDF cropped with border thickness {args.border_thickness} and saved to {args.output}")

if __name__ == "__main__":
    main()
