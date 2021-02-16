import cv2, os, crop
import matplotlib.pyplot as plt
from skimage import measure, morphology
from skimage.color import label2rgb
from skimage.measure import regionprops

def extract(src_img_path):
    try:
        print("\nSignature Extraction process started...")
        #Read the input image
        img = cv2.imread(src_img_path, 0)
        img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  #Ensure binary

        #Connected component analysis by scikit-learn framework
        blobs = img > img.mean()
        blobs_labels = measure.label(blobs, background=1)
        image_label_overlay = label2rgb(blobs_labels, image=img, bg_label=0)

        fig, ax = plt.subplots(figsize=(10, 6))

        the_biggest_component, total_area, counter, average = 0, 0, 0, 0.0

        for region in regionprops(blobs_labels):
            if (region.area > 10):
                total_area = total_area + region.area
                counter = counter + 1
            # print region.area # (for debugging)
            # take regions with large enough areas
            if (region.area >= 250):
                if (region.area > the_biggest_component):
                    the_biggest_component = region.area

        average = (total_area/counter)

        #Experimental-based ratio calculation, modify it for cases, a4_constant is used as a threshold value to remove connected pixels are smaller than a4_constant for A4 size scanned documents
        a4_constant = ((average/84.0)*250.0)+100

        #Remove the connected pixels are smaller than a4_constant
        b = morphology.remove_small_objects(blobs_labels, a4_constant)
        
        #Save the the pre-version which is the image is labelled with colors as considering connected components
        plt.imsave('pre_version.png', b)

        #Read the pre-version
        img = cv2.imread('pre_version.png', 0)
        
        #Ensure binary
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        os.remove("pre_version.png")
        
        #Save the the result
        output_filename = "".join([os.path.basename(src_img_path).split(".")[0], "-output.jpg"])
        cv2.imwrite(output_filename, img)
        crop.crop(output_filename)
    except Exception as e:
        print("Error: {}".format(e))