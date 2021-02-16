from skimage.measure import compare_ssim
import cv2
import numpy as np

def compare(src_img_path, ref_img_path):

    print("\nSignature Comparison process started...")
    src = cv2.imread(src_img_path)
    ref = cv2.imread(ref_img_path)

    h1, w1, c1 = src.shape
    h2, w2, c2 = ref.shape

    if ((h1 > h2) or (w1 > w2)):
        src = cv2.resize(src, (w2, h2))
    elif ((h2 > h1)  (w2 > w1)):
        ref = cv2.resize(ref, (w1, h1))

    # Convert images to grayscale
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    ref_gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)

    #Compute SSIM between two images
    (score, diff) = compare_ssim(src_gray, ref_gray, full=True)
    print("\nImage similarity: {0}%".format(round(score * 100, 2)))

    # The diff image contains the actual image differences between the two images and is represented as a floating point data type in the range [0,1] so we must convert the array to 8-bit unsigned integers in the range [0,255] src we can use it with OpenCV
    diff = (diff * 255).astype("uint8")

    #Threshold the difference image, followed by finding contours to obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(src.shape, dtype='uint8')
    filled_ref = ref.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 40:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(src, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.rectangle(ref, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.drawContours(mask, [c], 0, (0,255,0), -1)
            cv2.drawContours(filled_ref, [c], 0, (0,255,0), -1)

    print("\nSignature Comparison process completed.")