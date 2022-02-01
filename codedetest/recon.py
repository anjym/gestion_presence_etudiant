# import face_recognition
# import os
# import cv2
# import dlib
# import sys


# KNOW_FACES_DIR = "visageconnu"
# TOLERENCE = 0.5
# FRAME_THICKNESS = 3
# FRONT_THICKNESS = 2
# #MODEL = "cnn" #hog

# video = cv2.VideoCapture(2)

# print("loading known faces")

# known_faces = []
# known_names = []

# for name in os.listdir(KNOW_FACES_DIR):
# 	for filename in os.listdir(f"{KNOW_FACES_DIR}/{name}"):
# 		image = face_recognition.load_image_file(f"{KNOW_FACES_DIR}/{name}/{filename}",mode='RGB')
# 		print(image)
# 		encoding = face_recognition.face_encodings(image)[0]
# 		known_faces.append(encoding)
# 		known_names.append(name)

# while True:
# 	ret,image = video.read()
# 	locations = face_recognition.face_locations(image,model="hog")
# 	encodings = face_recognition.face_encodings(image,locations)

# 	for face_encoding,face_location in zip(encodings,locations):
# 		results = face_recognition.compare_faces(known_faces, face_encoding,TOLERENCE)
# 		match=None
# 		if True in results:
# 			match=known_names[results.index(True)]
# 			print(f"Match found:{match}")
# 			top_left = (face_location[3],face_location[0])
# 			bottom_right = (face_location[1],face_location[2])
# 			color = [0,255,0]
# 			cv2.Rectangle(image,top_left,bottom_right,color,FRAME_THICKNESS)

# 			top_left=(face_location[3], face_location[2])
# 			bottom_right = (face_location[1], face_location[2]+22)
# 			cv2.Rectangle(image,top_left, bottom_right,color, cv2.FILLED)
# 			cv2.putText(image, match, (face_location[3]+10,face_location[2]+15),cv2.FRONT_HERSEY_SIMPLEX, 0.5,(200,200,200), FRONT_THICKNESS)

# 	CV2.imshow(filename,image)
# 	if cv2.waitkey(1) & 0xFF == ord("q"):
# 		break

import face_recognition
import cv2
import numpy as np

# This is a super simple (but slow) example of running face recognition on live video from your webcam.
# There's a second example that's a little more complicated but runs faster.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

import math

def face_distance_to_conf(face_distancex, face_match_threshold=0.6):
    if face_distancex > face_match_threshold:
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distancex) / (range * 2.0)
        return linear_val
    else:
        range = face_match_threshold
        linear_val = 1.0 - (face_distancex / (range * 2.0))
        return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("michael.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "Michael.A",
    "Joe Biden"
]

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face enqcodings in the frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        #accur=face_distance_to_conf(face_distances, face_match_threshold=0.6)
        #print(face_distances)
        best_match_index = np.argmin(face_distances)
        best_match_index1 = np.argmin(face_distances)
        bb=np.argmin(face_distances)
        print(bb)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            dist=face_distances[bb]
            #print(matches[best_match_index])

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        msgk="[{:4.2f}] {}".format(dist, name)
        cv2.putText(frame, msgk, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()