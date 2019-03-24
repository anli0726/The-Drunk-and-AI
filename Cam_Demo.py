import face_recognition
import cv2

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load sample pictures and learn how to recognize them.
obama_image = face_recognition.load_image_file('/home/an/Pictures/Obama.jpg')
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

an_image = face_recognition.load_image_file('/home/an/Pictures/An Li.jpg')
an_face_encoding = face_recognition.face_encodings(an_image)[0]

bruce_image = face_recognition.load_image_file('/home/an/Pictures/Bruce Lee.jpg')
bruce_face_encoding = face_recognition.face_encodings(bruce_image)[0]

jack_image = face_recognition.load_image_file('/home/an/Pictures/Jack Black.jpg')
jack_face_encoding = face_recognition.face_encodings(jack_image)[0]

# Create arrays of known face encodings and their names
known_face_encoding = an_face_encoding
known_face_name = "An Li"

old_center = [0,0]
font = cv2.FONT_HERSHEY_DUPLEX
_a = 0
while True:
    # Grab a single frame of video
    _, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses)
    # to RGB color (which face_recognition uses)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face enqcodings in the frame of video
    face_location = face_recognition.face_locations(rgb_frame)

    system_box = [(64,400),(192,380)]


    if 0 < len(face_location) < 2:
        [(top, right, bottom, left)] = face_location
        face_encoding = face_recognition.face_encodings(rgb_frame, face_location)


        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(known_face_encoding, face_encoding)
        name = "Unknown"
        if match[0]:
            name = known_face_name
        # If a match was found in known_face_encodings, just use the first one.
        center = [(top + bottom) / 2, (left + right) / 2]

        # Draw a box around the face
        [box_left, box_top, box_right, box_bottom] = [left - 5, top - 10, right + 5, bottom + 10]
        cv2.rectangle(frame, (box_left, box_top), (box_right, box_bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (box_left, box_bottom - 35), (box_right, box_bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, name, (box_left + 6, box_bottom - 6), font, 1.0, (255, 255, 255), 1)
        if _a == 0:
            if center[0] - old_center[0] > 20 or center[1] - old_center[1] > 20:
                steady_time = 0
                #cv2.rectangle(frame, system_box[0], system_box[1], (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, "Please Maintain Your Face", (75, 65), font, 1.0,
                            (0, 0, 255), 2)
                cv2.putText(frame, "Steadily to Camera", (75, 100), font, 1.0,
                            (0, 0, 255), 2)
                x = 0
            else:
                if steady_time < 5:
                    #cv2.rectangle(frame, system_box[0], system_box[1], (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, "Recording... Please Use Your ", (65, 65), font, 1.0, (255, 0, 0), 2)
                    cv2.putText(frame, "Eyes to Track the Blue Block", (65, 100), font, 1.0, (255, 0, 0), 2)
                    if x==0:
                        flip = 1
                    if x==600:
                        flip = -1
                    if flip>0:
                        cv2.rectangle(frame, (x, 130), (x + 30, 160), (255, 0, 0), cv2.FILLED)
                        x += 120
                    else:
                        cv2.rectangle(frame, (x, 130), (x + 30, 160), (255, 0, 0), cv2.FILLED)
                        x -= 120
                    steady_time += 1
                else:
                    _a = 1
        else:
            if steady_time <= 10:
                cv2.putText(frame, "Analyzing...", (150, 65), font, 1.0, (255, 0, 0), 2)
                steady_time += 1
            else:
                cv2.putText(frame, "You Are Sober! Great!", (130, 65), font, 1.0, (0, 255, 0), 2)

        old_center = center
        # Display the resulting image
        cv2.imshow('Video', frame)
    else:
        # Display the resulting image
        #cv2.rectangle(frame, system_box[0], system_box[1], (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, "Unable to Recognize User's Face", (70, 65), font, 1.0, (255, 255, 255), 2)
        cv2.putText(frame, "or Recognize Multiple Faces", (70, 100), font, 1.0, (255, 255, 255), 2)
        cv2.imshow('Video', frame)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
