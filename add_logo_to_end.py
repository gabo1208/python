from PIL import Image
import numpy as np

def clone_s_to_end(input_path, output_path):
    """
    Clone the 'S' letter from the beginning of the text and add it to the end.
    """
    # Open the image
    img = Image.open(input_path).convert('RGBA')
    data = np.array(img)
    
    width, height = img.size
    print(f"Original image size: {width}x{height}")
    
    # Find the bounding box of the first 'S'
    # The 'S' is at the beginning, let's look at roughly the first 12% of the image
    # to avoid capturing the 'T' as well
    search_width = width // 8  # Narrower search to get just the S
    s_section = data[:, :search_width]
    
    # Get alpha channel to find non-transparent pixels
    alpha = s_section[:, :, 3]
    
    # Find rows and columns with non-transparent pixels
    rows_with_content = np.any(alpha > 0, axis=1)
    cols_with_content = np.any(alpha > 0, axis=0)
    
    if not np.any(rows_with_content) or not np.any(cols_with_content):
        print("Error: Could not find 'S' content")
        return
    
    # Get bounding box of the 'S'
    row_start = np.where(rows_with_content)[0][0]
    row_end = np.where(rows_with_content)[0][-1] + 1
    col_start = np.where(cols_with_content)[0][0]
    col_end = np.where(cols_with_content)[0][-1] + 1
    
    # Extract the 'S' letter
    s_letter = data[row_start:row_end, col_start:col_end]
    s_height = row_end - row_start
    s_width = col_end - col_start
    
    print(f"'S' letter extracted: {s_width}x{s_height}")
    print(f"  Position: rows {row_start}-{row_end}, cols {col_start}-{col_end}")
    
    # Calculate new image width (original + spacing + S width)
    spacing = 10  # pixels between text and new S
    new_width = width + spacing + s_width
    
    # Create new image
    new_data = np.zeros((height, new_width, 4), dtype=np.uint8)
    
    # Copy original image to the left
    new_data[:, :width] = data
    
    # Place the cloned 'S' at the end, aligned vertically with the original
    s_x_offset = width + spacing
    new_data[row_start:row_end, s_x_offset:s_x_offset + s_width] = s_letter
    
    # Create and save the new image
    result = Image.fromarray(new_data, 'RGBA')
    result.save(output_path, 'PNG')
    print(f"✓ New image saved to: {output_path}")
    print(f"  - New size: {new_width}x{height}")
    print(f"  - Cloned 'S' added to the end")

if __name__ == "__main__":
    input_file = "dashboard/static/dashboard/img/vertical-logo-and-letters-transparent.png"
    output_file = "dashboard/static/dashboard/img/vertical-logo-with-ending-s.png"
    
    print("Cloning 'S' letter from beginning to end...")
    clone_s_to_end(input_file, output_file)
    print("\nDone! The new logo is ready.")

