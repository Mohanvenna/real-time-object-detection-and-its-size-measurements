
from django.shortcuts import render
from .models import dim,ptp
from django.http import HttpResponse
# Create your views here.
import sys
# import static

# adding Folder_2 to the system path

def home(request):

    return render(request,'ht.html')
def home2(request):
    from scipy.spatial.distance import euclidean
    from imutils import perspective
    from imutils import contours
    import numpy as np
    import imutils
    import cv2
    import json
    import os
    import csv
    import base64
    images = {}
    # field names
    '''def load_images_from_folder(folder):
    	for filename in os.listdir(folder):
    		img = cv2.imread(os.path.join(folder,filename))
    	if img is None:
    		return
    	images.append(img)'''

    import os
    from os import listdir

    # get the path or directory

    # print(images)
    # Function to show array of images (intermediate results)
    """def show_images(images):
        for i, img in enumerate(images):
            cv2.imshow("image_" + str(i), img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
"""
    from django.shortcuts import render
    from django.core.files.storage import FileSystemStorage
    import base64
    images={}
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
            # process the file data here
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        image = cv2.imread(filename)
        """
        _, buffer = cv2.imencode('.jpg', image)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        response_data = {'image': image_base64}"""
        #cv2.imshow('image',image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
                    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        edged = cv2.Canny(blur, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)

                    # show_images([blur, edged])

                    # Find contours
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

                    # Sort contours from left to right as leftmost contour is reference object
        (cnts, _) = contours.sort_contours(cnts)

                    # Remove contours which are not large enough
        cnts = [x for x in cnts if cv2.contourArea(x) > 150]

                    # cv2.drawContours(image, cnts, -1, (0, 255, 0), 3)

                    # show_images([image, edged])
                    # print(len(cnts))

                    # Reference object dimensions
                    # Here for reference I have used a 2cm x 2cm square
        ref_object = cnts[0]
        box = cv2.minAreaRect(ref_object)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)
        (tl, tr, br, bl) = box
        dist_in_pixel = euclidean(tl, tr)
        dist_in_cm = 2
        pixel_per_cm = dist_in_pixel / dist_in_cm
        wid: float
        ht: float
                    # Draw remaining contours
        for cnt in cnts:
            box = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            box = perspective.order_points(box)
            (tl, tr, br, bl) = box
            cv2.drawContours(image, [box.astype("int")], -1, (0, 0, 255), 2)
            mid_pt_horizontal = (tl[0] + int(abs(tr[0] - tl[0]) / 2), tl[1] + int(abs(tr[1] - tl[1]) / 2))
            mid_pt_verticle = (tr[0] + int(abs(tr[0] - br[0]) / 2), tr[1] + int(abs(tr[1] - br[1]) / 2))
            wid1 = euclidean(tl, tr) / pixel_per_cm
            ht1 = euclidean(tr, br) / pixel_per_cm
            wid = wid1 * 10
            ht = ht1 * 10
            cv2.putText(image, "{:.4f}mm".format(wid),
                        (int(mid_pt_horizontal[0] - 15), int(mid_pt_horizontal[1] - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            cv2.putText(image, "{:.4f}mm".format(ht), (int(mid_pt_verticle[0] + 10), int(mid_pt_verticle[1])),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        #show_images([image])
            obj=dim()
            obj.img=filename
            obj.wid=wid
            obj.ht=ht
            obj.save()
        for i, img in enumerate([image, edged]):
            _, buffer = cv2.imencode('.jpg', img)
            img_str = base64.b64encode(buffer).decode()
            images[f'image_{i}'] = f"data:image/jpg;base64,{img_str}"

            #return HttpResponse(json.dumps(response_data), content_type="application/json")
    # Read image and preprocess

    return render(request,'valve.html',{'images': images})
def home3(request):
    from scipy.spatial.distance import euclidean
    from imutils import perspective
    from imutils import contours
    import numpy as np
    import imutils
    import cv2
    import os

    # Function to show array of images (intermediate results)
    """def show_images(images):
        for i, img in enumerate(images):
            cv2.imshow("image_" + str(i), img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()"""

    import base64
    images = {}
    from django.shortcuts import render
    from django.core.files.storage import FileSystemStorage
    if request.method == 'POST' and request.FILES['file1']:
        file = request.FILES['file1']
        # process the file data here
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        # check if the image ends with png or jpg or jpeg

            # Read image and preprocess
        image = cv2.imread(filename)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply thresholding
        _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

            # Apply morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        eroded = cv2.erode(binary, kernel, iterations=3)
        dilated = cv2.dilate(eroded, kernel, iterations=3)

            # Apply image filtering
        filtered = cv2.medianBlur(gray, 21)

            # Subtract filtered image from binary image
        shadow_removed = cv2.subtract(filtered, dilated)

            # Display the original and shadow-free images
        #cv2.imshow('Original Image', image)
        #cv2.imshow('Shadow-Free Image', shadow_removed)
        cv2.waitKey(0)
        blur = cv2.GaussianBlur(shadow_removed, (9, 9), 0)
        edged = cv2.Canny(blur, 50, 100)
        #show_images([edged])
            # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        edged = cv2.dilate(edged, None, iterations=1)
            # show_images([edged])
        edged = cv2.erode(edged, None, iterations=1)

        #show_images([blur, edged])

            # Find contours
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

            # Sort contours from left to right as leftmost contour is reference object
        (cnts, _) = contours.sort_contours(cnts)

            # Remove contours which are not large enough
        cnts = [x for x in cnts if cv2.contourArea(x) > 100]

        cv2.drawContours(image, cnts, -1, (0, 255, 0), 4)

        #show_images([image, edged])
            # print(len(cnts))

            # Reference object dimensions
            # Here for reference I have used a 2cm x 2cm square
        ref_object = cnts[0]
        box = cv2.minAreaRect(ref_object)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)
        (tl, tr, br, bl) = box
        dist_in_pixel = euclidean(tl, tr)
        dist_in_cm = 2
        pixel_per_cm = dist_in_pixel / dist_in_cm

            # Draw remaining contours
        for cnt in cnts:
            box = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            box = perspective.order_points(box)
            (tl, tr, br, bl) = box
            cv2.drawContours(image, [box.astype("int")], -1, (0, 0, 255), 2)
            mid_pt_horizontal = (tl[0] + int(abs(tr[0] - tl[0]) / 2), tl[1] + int(abs(tr[1] - tl[1]) / 2))
            mid_pt_verticle = (tr[0] + int(abs(tr[0] - br[0]) / 2), tr[1] + int(abs(tr[1] - br[1]) / 2))
            wid1 = euclidean(tl, tr) / pixel_per_cm
            ht1 = euclidean(tr, br) / pixel_per_cm
            wid = wid1
            ht = ht1
            cv2.putText(image, "{:.2f}cm".format(wid),
                        (int(mid_pt_horizontal[0] - 15), int(mid_pt_horizontal[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 0), 2)
            cv2.putText(image, "{:.2f}cm".format(ht), (int(mid_pt_verticle[0] + 10), int(mid_pt_verticle[1])),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            obj = dim()
            obj.img = filename
            obj.wid = wid
            obj.ht = ht
            obj.save()
        #show_images([image])

        for i, img in enumerate([image, edged]):
            _, buffer = cv2.imencode('.jpg', img)
            img_str = base64.b64encode(buffer).decode()
            images[f'image_{i}'] = f"data:image/jpg;base64,{img_str}"
    return render(request, 'shadow.html',{'images': images})
def home1(request):
    from scipy.spatial.distance import euclidean
    from imutils import perspective
    from imutils import contours
    import numpy as np
    import imutils
    import cv2
    import base64
    import base64
    images = {}

    import datetime
    from django.conf import settings
    import os
    import csv

    # field names

    '''def load_images_from_folder(folder):
    	for filename in os.listdir(folder):
    		img = cv2.imread(os.path.join(folder,filename))
    	if img is None:
    		return
    	images.append(img)'''

    import os
    from os import listdir

    # get the path or directory

    # print(images)
    # Function to show array of images (intermediate results)
    """def show_images(images):
        for i, img in enumerate(images):
            cv2.imshow("image_" + str(i), img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()"""

    from django.core.files.storage import FileSystemStorage
    if request.method == 'POST' and request.FILES['file2']:
        file = request.FILES['file2']
            # process the file data here
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        image = cv2.imread(filename)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
            # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        edged = cv2.Canny(blur, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)

            # show_images([blur, edged])

            # Find contours
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

            # Sort contours from left to right as leftmost contour is reference object
        (cnts, _) = contours.sort_contours(cnts)

            # Remove contours which are not large enough
        cnts = [x for x in cnts if cv2.contourArea(x) > 100]

            # cv2.drawContours(image, cnts, -1, (0, 255, 0), 3)

            # show_images([image, edged])
            # print(len(cnts))

            # Reference object dimensions
            # Here for reference I have used a 2cm x 2cm square
        ref_object = cnts[0]
        box = cv2.minAreaRect(ref_object)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)
        (tl, tr, br, bl) = box
        dist_in_pixel = euclidean(tl, tr)
        dist_in_cm = 2
        pixel_per_cm = dist_in_pixel / dist_in_cm
        wid: float
        ht: float
            # Draw remaining contours
        for cnt in cnts:
            box = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            box = perspective.order_points(box)
            (tl, tr, br, bl) = box
            cv2.drawContours(image, [box.astype("int")], -1, (0, 0, 255), 2)
            mid_pt_horizontal = (tl[0] + int(abs(tr[0] - tl[0]) / 2), tl[1] + int(abs(tr[1] - tl[1]) / 2))
            mid_pt_verticle = (tr[0] + int(abs(tr[0] - br[0]) / 2), tr[1] + int(abs(tr[1] - br[1]) / 2))
            wid = euclidean(tl, tr) / pixel_per_cm
            ht = euclidean(tr, br) / pixel_per_cm
            cv2.putText(image, "{:.1f}cm".format(wid),
                            (int(mid_pt_horizontal[0] - 15), int(mid_pt_horizontal[1] - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            cv2.putText(image, "{:.1f}cm".format(ht), (int(mid_pt_verticle[0] + 10), int(mid_pt_verticle[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            obj = dim()
            obj.img = filename
            obj.wid = wid
            obj.ht = ht
            obj.save()
        #show_images([image])
        for i, img in enumerate([image, edged]):
            _, buffer = cv2.imencode('.jpg', img)
            img_str = base64.b64encode(buffer).decode()
            images[f'image_{i}'] = f"data:image/jpg;base64,{img_str}"


    return render(request, 'new.html',{'images': images})

def home4(request):
    import cv2
    from django.core.files.storage import FileSystemStorage
    if request.method == 'POST' and request.FILES['file3']:
        file = request.FILES['file3']
        # process the file data here
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        image = cv2.imread(filename)

        def get_coords(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                # Add the coordinates of the selected point to the list
                cv2.circle(image, (x, y), 5, (0, 0, 255), -1)
                point_list.append((x, y))

        # Create a window and bind the mouse callback function to it
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", get_coords)

        # Create an empty list to store the selected points
        point_list = []
        while True:
            # Display the image and wait for a key press
            cv2.imshow("image", image)
            key = cv2.waitKey(1) & 0xFF

            # If the 's' key is pressed, break from the loop
            if key == ord("s"):
                break

        # Print the list of selected points
        print(point_list)

        # Release the window and destroy all windows
        cv2.destroyAllWindows()
        from scipy.spatial.distance import euclidean
        dist = euclidean(point_list[0], point_list[1]) / 84.4
        print(dist)
        dist1=str(dist)
        obj=ptp()
        obj.dist=dist
        obj.img=filename
        obj.save()
        return render(request, 'poi.html',{'dist':dist1})
    return render(request, 'poi.html')