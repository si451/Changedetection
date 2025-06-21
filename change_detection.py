import cv2
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim


def main():
    input_folder = 'input-images'
    output_folder = 'output'


    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

   
    files = os.listdir(input_folder)
    image_pairs = []
    
    
    for file in files:
        if '~2' not in file and file.lower().endswith(('.png', '.jpg', '.jpeg')):
            base_name, ext = os.path.splitext(file)
            after_file_name = f"{base_name}~2{ext}"
            if after_file_name in files:
                image_pairs.append((file, after_file_name))

    print(f"Found {len(image_pairs)} image pairs to process.")

    
    for before_file, after_file in image_pairs:
        try:
            
            before_path = os.path.join(input_folder, before_file)
            after_path = os.path.join(input_folder, after_file)

            
            before_img = cv2.imread(before_path)
            after_img = cv2.imread(after_path)

            if before_img is None or after_img is None:
                print(f"Warning: Could not load one or both images for pair: {before_file}, {after_file}")
                continue

            
            if before_img.shape != after_img.shape:
                print(f"Warning: Image dimensions do not match for {before_file} and {after_file}. Skipping.")
                continue

            before_gray = cv2.cvtColor(before_img, cv2.COLOR_BGR2GRAY)
            after_gray = cv2.cvtColor(after_img, cv2.COLOR_BGR2GRAY)

            
            (score, diff) = ssim(before_gray, after_gray, full=True)
            diff = (diff * 255).astype("uint8")
            print(f"SSIM for {before_file}: {score}")

           
            thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            
            kernel = np.ones((5, 5), np.uint8)
            cleaned_thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            cleaned_thresh = cv2.morphologyEx(cleaned_thresh, cv2.MORPH_OPEN, kernel)

            
            contours, _ = cv2.findContours(cleaned_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            
            annotated_after = after_img.copy()
            changes_found = False

            for contour in contours:
                
                if cv2.contourArea(contour) > 100: 
                    changes_found = True
                    
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(annotated_after, (x, y), (x + w, y + h), (0, 0, 255), 2)

           
            if changes_found:
                
                comparison_image = np.hstack((before_img, annotated_after))

                output_filename = f"{os.path.splitext(before_file)[0]}_differences.jpg"
                output_path = os.path.join(output_folder, output_filename)
                cv2.imwrite(output_path, comparison_image)
                print(f"Saved differences for {before_file} to {output_path}")
            else:
                print(f"No significant changes found for {before_file}.")

        except Exception as e:
            print(f"An error occurred while processing {before_file}: {e}")

if __name__ == "__main__":
    main()