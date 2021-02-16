import cv2, os

def crop(output_filename):

    image = cv2.imread(output_filename, 1)
    img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU,img)
    cv2.bitwise_not(img,img)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, rect_kernel)
    contours, hier = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    output_folder_name = output_filename.split(".")[0]
    if (os.path.exists(output_folder_name) == False):
        os.mkdir(output_folder_name)
    
    counter = 1
    if len(contours) != 0:
        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            if(h>20):
                cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),1)
                ROI = image[y:y+h, x:x+w].copy()
                cv2.imwrite("".join([output_folder_name, "/output-", str(counter), ".jpg"]), ROI)
                counter += 1
    os.remove(output_filename)
    print("Signature Extraction process completed.")
    print("Extracted signatures are saved in '{}' folder.".format(output_folder_name))