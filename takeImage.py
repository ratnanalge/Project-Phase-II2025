import os
import cv2
import numpy as np
import csv

def is_face_registered(new_face, registered_faces_folder, detector):
    new_resized = cv2.resize(new_face, (100, 100))

    for folder in os.listdir(registered_faces_folder):
        folder_path = os.path.join(registered_faces_folder, folder)
        if not os.path.isdir(folder_path):
            continue
        for file in os.listdir(folder_path):
            img_path = os.path.join(folder_path, file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            faces = detector.detectMultiScale(img, 1.3, 5)
            for (x, y, w, h) in faces:
                roi = img[y:y + h, x:x + w]
                roi_resized = cv2.resize(roi, (100, 100))

                hist1 = cv2.calcHist([roi_resized], [0], None, [256], [0, 256])
                hist2 = cv2.calcHist([new_resized], [0], None, [256], [0, 256])
                cv2.normalize(hist1, hist1)
                cv2.normalize(hist2, hist2)
                score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

                if score > 0.9:  
                    return True
    return False

def TakeImage(l1, l2, haar_path, train_folder, message, err_screen, text_to_speech):
    if not l1 and not l2:
        text_to_speech("Please enter your PRN number and Name.")
        return
    elif not l1:
        text_to_speech("Please enter your PRN number.")
        return
    elif not l2:
        text_to_speech("Please enter your Name.")
        return

    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            text_to_speech("Camera could not be opened.")
            return

        detector = cv2.CascadeClassifier(haar_path)
        PRN = l1
        Name = l2
        sampleNum = 0
        project_dir = os.path.dirname(os.path.abspath(__file__))
        train_folder = os.path.join(project_dir, "TrainingImage")

        folder_name = f"{PRN}_{Name}"
        save_path = os.path.join(train_folder, folder_name)

        print(f"[DEBUG] Attempting to create save path: {save_path}")
        os.makedirs(save_path, exist_ok=True)
        print(f"[DEBUG] Save path created successfully: {save_path}")


        os.makedirs(save_path, exist_ok=True)

        face_check_done = False
        face_registered = False

        while True:
            ret, img = cam.read()
            if not ret:
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face_crop = gray[y:y + h, x:x + w]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                if not face_check_done:
                    face_registered = is_face_registered(face_crop, train_folder, detector)
                    face_check_done = True
                    if face_registered:
                        text_to_speech("Face already registered.")
                        message.configure(text="Face already registered.")
                        cam.release()
                        cv2.destroyAllWindows()
                        return

                sampleNum += 1
                file_name = f"{Name}_{PRN}_{sampleNum}.jpg"
                cv2.imwrite(os.path.join(save_path, file_name), face_crop)

            cv2.imshow("Press 'q' to exit", img)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            elif sampleNum >= 50:
                break

        cam.release()
        cv2.destroyAllWindows()

        os.makedirs("StudentDetails", exist_ok=True)
        with open("StudentDetails/studentdetails.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([PRN, Name])

        res = f"Images saved for PRN No: {PRN}, Name: {Name}"
        message.configure(text=res)
        text_to_speech(res)

    except Exception as e:
        cam.release()
        cv2.destroyAllWindows()
        text_to_speech("Error occurred.")
        err_screen(str(e))
