import cv2
import numpy as np

def bilinear_interpolation(x, y, img):
    x1, y1 = int(x), int(y)
    x2, y2 = min(x1 + 1, img.shape[1]-1), min(y1 + 1, img.shape[0]-1)
    
    q11 = img[y1, x1]
    q21 = img[y1, x2]
    q12 = img[y2, x1]
    q22 = img[y2, x2]
    
    return q11 * (x2 - x) * (y2 - y) + q21 * (x - x1) * (y2 - y) + q12 * (x2 - x) * (y - y1) + q22 * (x - x1) * (y - y1)

def rotate_image(image, angle):
    angle_rad = np.radians(angle)
    h, w = image.shape[:2]
    
    # Compute the new image dimensions
    new_w = int(abs(np.sin(angle_rad) * h) + abs(np.cos(angle_rad) * w))
    new_h = int(abs(np.sin(angle_rad) * w) + abs(np.cos(angle_rad) * h))
    
    # Allocate memory for the new image
    rotated_image = np.zeros((new_h, new_w), dtype=image.dtype)
    
    # Compute the center of rotation
    cx, cy = w // 2, h // 2
    new_cx, new_cy = new_w // 2, new_h // 2
    
    # Perform rotation with inverse mapping
    for i in range(new_w):
        for j in range(new_h):
            x = (i - new_cx) * np.cos(angle_rad) + (j - new_cy) * np.sin(angle_rad) + cx
            y = -(i - new_cx) * np.sin(angle_rad) + (j - new_cy) * np.cos(angle_rad) + cy
            
            if 0 <= x < w and 0 <= y < h:
                rotated_image[j, i] = bilinear_interpolation(x, y, image)
                
    return rotated_image

def image_rotate():
    image_path = input("Please enter the path to your image: ")

    # Converting the image to grayscale 
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("Error: Unable to open the image file.")
        return
    
    # Display original image
    cv2.imshow('Original Image', image)
    
    # Asking the user for the angle to rotate
    while True:
        try:
            angle = int(input("Please enter the angle to rotate (0 ≤ angle ≤ 360): "))
            if 0 <= angle <= 360:
                break
            else:
                print("Invalid input. Please enter an integer between 0 and 360.")
        except ValueError:
            print("Invalid input. Please enter an integer.")
    
    # Asking the user for the direction to rotate
    while True:
        direction = input("Please enter the direction to rotate (clockwise/counterclockwise): ").lower()
        if direction in ['clockwise', 'counterclockwise']:
            break
        else:
            print("Invalid input. Please enter 'clockwise' or 'counterclockwise'.")
    
    # Deciding the rotation angle based on direction
    if direction == 'clockwise':
        angle = -angle  # Rotate clockwise
    
    # Rotate the image using the custom function
    rotated_image = rotate_image(image, angle)
    
    # Display and save the rotated image
    cv2.imshow('Rotated Image', rotated_image)
    
    # Save the rotated image
    new_image_path = "rotated_" + image_path.split("/")[-1]
    cv2.imwrite(new_image_path, rotated_image)
    print(f"Rotated image saved as {new_image_path}")

    cv2.waitKey(0)  # Wait until a key is pressed
    cv2.destroyAllWindows()  # Close all windows


# Run the function
image_rotate()