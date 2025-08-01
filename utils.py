# utils.py

import cv2
import easyocr
from openpyxl import Workbook, load_workbook
from datetime import datetime
import os

reader = easyocr.Reader(['en'])

def preview_and_crop(img_path):
    image = cv2.imread(img_path)

    # Resize image to 50% of assumed 1920x1080 resolution
    screen_width = int(0.5 * 1920)
    screen_height = int(0.5 * 1080)
    resized = cv2.resize(image, (screen_width, screen_height))

    roi = cv2.selectROI("Crop IPC Image (50% screen)", resized, showCrosshair=True)
    cv2.destroyAllWindows()

    if sum(roi) == 0:
        return image  # No selection; return full image

    x, y, w, h = roi

    # Map ROI from resized to original coordinates
    x_orig = int(x * image.shape[1] / screen_width)
    y_orig = int(y * image.shape[0] / screen_height)
    w_orig = int(w * image.shape[1] / screen_width)
    h_orig = int(h * image.shape[0] / screen_height)

    cropped_img = image[y_orig:y_orig+h_orig, x_orig:x_orig+w_orig]

    # Preview cropped image
    cv2.imshow("Cropped Preview", cropped_img)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()

    return cropped_img

def extract_text_from_cropped(image):
    result = reader.readtext(image)
    extracted_text = [text[1] for text in result]
    return " | ".join(extracted_text)



def save_to_excel(image_data, filename):
    if os.path.exists(filename):
        wb = load_workbook(filename)
        ws = wb.active
    else:
        wb = Workbook()
        ws = wb.active
        ws.title = "IPC Alerts"
        ws.append(["Image Name", "Extracted Text", "Timestamp"])

    for image_name, text in image_data:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append([image_name, text, timestamp])

    wb.save(filename)
