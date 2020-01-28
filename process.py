import cv2


def add_fg(img_name):
    img1 = cv2.imread(img_name, cv2.IMREAD_COLOR)
    img2 = cv2.imread("foreground.jpg", cv2.IMREAD_COLOR)
    heigth = img1.shape[0]
    width = img1.shape[1]
    if heigth != 640 or width != 640:
        if width < heigth:
            new_width = 640
            new_height = int(heigth * 640 / width)
            img1 = cv2.resize(img1, (new_width, new_height))
            space = new_height - 640
            space1 = int(space/2)
            space2 = space - space1
            img1 = img1[space1:new_height - space2, 0:new_width]
        else:
            new_height = 640
            new_width = int(width * 640 / heigth)
            img1 = cv2.resize(img1, (new_width, new_height))
            print(img1.shape)
            space = new_width - 640
            space1 = int(space / 2)
            space2 = space - space1
            print(space1)
            print(space2)
            img1 = img1[0:new_height, space1:new_width-space2]
    img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 77, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    img1_bg = cv2.bitwise_and(img1, img1, mask=mask)
    img2_fg = cv2.bitwise_and(img2, img2, mask=mask_inv)
    img = cv2.add(img1_bg, img2_fg)
    cv2.imwrite("new" + img_name, img)
