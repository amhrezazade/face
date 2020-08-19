

print("Loading...")

import shutil
import face_recognition
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import os



#DataSet path :
path = "dataset"

#Creating a list of files in dataset folder :
onlyfiles = []
try:
    print("Listing files...")
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
except:
    print("Error listing files")



#Loading Dataset (Images and Labels) :
known_face_names = []
known_face_encodings = []
for filename in onlyfiles:
    try:
        # Load a sample picture and learn how to recognize it.
        image = face_recognition.load_image_file(path + "/" + filename)
        encodedImage = face_recognition.face_encodings(image)[0]
        #and add it to known_face_encodings list :
        known_face_encodings.append(encodedImage)
        #Adding Label of the image to known_face_names list :
        Label = filename[0: filename.find('.')]
        known_face_names.append(Label)
        print(filename + "  -  OK  |  Label :" + Label)
    except:
        print(filename + "  -  Bad Image")


print(len(known_face_names), end='')

print(" Valid Image's found in dataset folder")



# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

def learn(ImageLabel):
    global known_face_names
    global known_face_encodings
    print("Trying to learn Label : " + ImageLabel)
    newfilename = path + "/" + ImageLabel + ".jpg"
    try:
        print("Copying file to dataset folder...")
        shutil.copyfile("temp.jpg",newfilename)
        # Load a sample picture and learn how to recognize it.
        print("Loading image file...")
        image = face_recognition.load_image_file(newfilename)
        print("processing first face in image...")
        encodedImage = face_recognition.face_encodings(image)[0]
        #and add it to known_face_encodings list :
        known_face_encodings.append(encodedImage)
        #Adding Label of the image to known_face_names list :
        known_face_names.append(ImageLabel)
        print(ImageLabel + "  -  OK  |  Label :" + Label)
        return 1
    except:
        try:
            os.remove(newfilename)
        except:
            print("Can not delete temp file from dataset")
        print(ImageLabel + "  -  Bad Image")
        return 0


def getNames():
    global known_face_names
    return known_face_names



def Check():
    global face_locations
    global face_encodings
    global face_names
    global known_face_names
    global known_face_encodings
    try:
        # Grab a single frame of video
        print("Loading temp file...")
        frame = face_recognition.load_image_file("temp.jpg")

        # Resize frame of video to 1/4 size for faster face recognition processing
        #small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        print("Resizing...")
        small_frame = frame


        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        print("Converting to rgb...")
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        print("finding face locations...")
        face_locations = face_recognition.face_locations(rgb_small_frame)
        print("encodeing face data...")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            print("processing face",end='')
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            # # If a match was found in known_face_encodings, just use the first one.
            if matches.count(True) == 1:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            else:
                if matches.count(True) > 1: #Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
            print(" - Label : " + name)
            face_names.append(name)
    
        return face_names
    except:
        return []
