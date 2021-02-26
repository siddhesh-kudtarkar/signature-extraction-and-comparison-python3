import cv2, os
import opencv_wrapper as cvw
import numpy as np
from tkinter import messagebox
from datetime import datetime

def crop(output_filename, mode="gui"):
    if (mode == "gui"):
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

        if (mode == "gui"):
            log += "".join(["\n", str(datetime.now().time()).split(".")[0], " ", "Separating detected signature(s)."])
        else:
            print("".join(["\n", str(datetime.now().time()).split(".")[0], " ", "Separating detected signature(s)."]))
        
        padding = 30
        if len(contours) != 0:
            for c in contours:
                x,y,w,h = cv2.boundingRect(c)
                if(h>20):
                    cv2.rectangle(image,(x - padding,y - padding),(x + w + padding,y + h + padding),(255, 255, 255), 1)

        gray = cvw.bgr2gray(image)
        thresh = cvw.threshold_otsu(gray, inverse=True)

        # dilation
        img_dilation = cvw.dilate(thresh, 20)

        # Find contours
        contours = cvw.find_external_contours(img_dilation)
        # Map contours to bounding rectangles, using bounding_rect property
        rects = map(lambda c: c.bounding_rect, contours)
        # Sort rects by top-left x (rect.x == rect.tl.x)
        sorted_rects = sorted(rects, key=lambda r: r.x)

        # Distance threshold
        dt = 5

        # List of final, joined rectangles
        final_rects = [sorted_rects[0]]

        for rect in sorted_rects[1:]:
            prev_rect = final_rects[-1]

            # Shift rectangle `dt` back, to find out if they overlap
            shifted_rect = cvw.Rect(rect.tl.x - dt, rect.tl.y, rect.width, rect.height)
            intersection = cvw.rect_intersection(prev_rect, shifted_rect)
            if intersection is not None:
                # Join the two rectangles
                min_y = min((prev_rect.tl.y, rect.tl.y))
                max_y = max((prev_rect.bl.y, rect.bl.y))
                max_x = max((prev_rect.br.x, rect.br.x))
                width = max_x - prev_rect.tl.x
                height = max_y - min_y
                new_rect = cvw.Rect(prev_rect.tl.x, min_y, width, height)
                # Add new rectangle to final list, making it the new prev_rect
                # in the next iteration
                final_rects[-1] = new_rect
            else:
                # If no intersection, add the box
                final_rects.append(rect)

        counter, padding = 1, 20
        for rect in final_rects:
            rect.x = int(rect.x - (padding/2))
            rect.y = int(rect.y - (padding/2))
            rect.width = rect.width + padding
            rect.height = rect.height + padding
            if (rect.width >= 100 and rect.height >= 100):
                ROI = image[(rect.y):(rect.y + rect.height), (rect.x):(rect.x + rect.width)].copy()
                cv2.imwrite("".join([output_folder_name, "/output-", str(counter), ".jpg"]), ROI)
                counter += 1

        os.remove(output_filename)

        if (mode == "gui"):
            log += "".join(["\n", str(datetime.now().time()).split(".")[0], " ", "Signature Extraction process completed.", "\n", str(datetime.now().time()).split(".")[0], " ", "Extracted signature(s) is/are stored in '", output_folder_name, "' folder."])
            messagebox.showinfo("Success", "".join(["Extracted signature(s) is/are stored in '", output_folder_name, "' folder."]))
        else:
            print("".join(["\n", str(datetime.now().time()).split(".")[0], " ", "Signature Extraction process completed.", "\n", str(datetime.now().time()).split(".")[0], " ", "Extracted signature(s) is/are stored in '", output_folder_name, "' folder.", "\nSUCCESS: Extracted signature(s) is/are stored in '", output_folder_name, "' folder."]))
    
    except Exception as e:
        if (mode == "gui"):
            messagebox.showerror("Error", "".join(["Error: ", str(e)]))
        else:
            print("Error: {}".format(str(e)))
    
    finally:
        if (mode == "gui"):
            return log
