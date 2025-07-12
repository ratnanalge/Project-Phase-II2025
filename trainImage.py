import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
from PIL import ImageTk, Image


def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message,text_to_speech):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(haarcasecade_path)
    faces, Id = getImagesAndLables(trainimage_path)
    recognizer.train(faces, np.array(Id))
    print("Id")
    print(trainimagelabel_path)
    recognizer.save(trainimagelabel_path)
    res = "Image Trained successfully" 
    message.configure(text=res)
    text_to_speech(res)

def getImagesAndLables(path):
    prn_mapping = {}
    current_label = 1
    faces = []
    labels = []

    newdir = [os.path.join(path, d) for d in os.listdir(path)]
    imagePaths = [
        os.path.join(newdir[i], f)
        for i in range(len(newdir))
        for f in os.listdir(newdir[i])
    ]

    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert("L")
        imageNp = np.array(pilImage, "uint8")
        prn = os.path.split(imagePath)[-1].split("_")[1]
        if prn not in prn_mapping:
            current_label += 1
            prn_mapping[prn] = current_label
        label = prn_mapping[prn]
        faces.append(imageNp)
        labels.append(label)

    with open("prn_mapping.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["label", "PRN"])
        for prn, label in prn_mapping.items():
            writer.writerow([label, prn])

    return faces, labels

