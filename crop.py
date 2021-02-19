import cv2, os
from tkinter import messagebox
from datetime import datetime

def crop(output_filename):
    log = ""

    try:
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

        log += "".join(["\n", str(datetime.now().time()).split(".")[0], " ", "Separating detected signature(s)."])
        
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

        log += "".join(["\n", str(datetime.now().time()).split(".")[0], " ", "Signature Extraction process completed."])

        log += "".join(["\n", str(datetime.now().time()).split(".")[0], " ", "Extracted signature(s) is/are stored in '", output_folder_name, "' folder."])

        messagebox.showinfo("Success", "".join(["Extracted signature(s) is/are stored in '", output_folder_name, "' folder."]))
    
    except Exception as e:
        messagebox.showerror("Error", "".join(["Error: ", str(e)]))
    
    finally:
        return log