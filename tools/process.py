import cv2

FOREGROUND = cv2.imread("foreground.png", cv2.IMREAD_UNCHANGED)
# Normalize alpha channel from 0-255 to 0-1
ALPHA = FOREGROUND[:,:,3] / 255.0

def crop_and_resize_to_640X640(image):
    heigth = image.shape[0]
    width = image.shape[1]
    if heigth != 640 or width != 640:
        if width < heigth:
            new_width = 640
            new_height = int(heigth * 640 / width)
            image = cv2.resize(image, (new_width, new_height))
            space = new_height - 640
            space1 = int(space/2)
            space2 = space - space1
            image = image[space1:new_height - space2, 0:new_width]
        else:
            new_height = 640
            new_width = int(width * 640 / heigth)
            image = cv2.resize(image, (new_width, new_height))
            space = new_width - 640
            space1 = int(space / 2)
            space2 = space - space1
            image = image[0:new_height, space1:new_width-space2]
    return image

def add_fg(input_img_name, output_img_name):
    # Read image
    background = cv2.imread(input_img_name, cv2.IMREAD_COLOR)
    background = crop_and_resize_to_640X640(background)
    # set adjusted colors
    for color in range(0, 3):
        background[:,:,color] = ALPHA * FOREGROUND[:,:,color] + \
            background[:,:,color] * (1 - ALPHA)
    # Save image
    cv2.imwrite(output_img_name, background)
    # Return saved image name
