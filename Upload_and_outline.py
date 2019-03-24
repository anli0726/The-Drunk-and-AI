from PIL import Image, ImageDraw
import face_recognition
import socket

s = socket.socket()             # Create a socket object
print('ocket created')
host = '10.104.149.38'	#!!! Important !!! This needs to be the LOCAL ip address
#of the mobile phone on the same wifi network as the PC that this code is running on

#'192.168.1.200'#socket.gethostname()     # Get local machine name
port = 60001                    # Reserve a port for your service.

s.connect((host, port))
#s.send("Hello server!")
print('Connected, attempting to download image')
with open('received_image.jpg', 'wb') as f:
    print('file opened')
    while True:
        #print('receiving data...')
        data = s.recv(1024)
        #print('data=%s', (data))
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('connection closed, going to try loading the image')
# Load the jpg file into a numpy array



image = face_recognition.load_image_file('/home/an/Downloads/received_image.jpg')
#image = face_recognition.load_image_file('/home/an/Pictures/ppl_faces.jpeg')




print('image should be loaded, now begining tracing')



# Find all the faces in the image using the default HOG-based model.
# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
# See also: find_faces_in_picture_cnn.py
face_locations = face_recognition.face_locations(image)
i = 0

#print("I found {} face(s) in this photograph.".format(len(face_locations)))

for face_location in face_locations:

    # Print the location of each face in this image
    top, right, bottom, left = face_location
    #print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

    # You can access the actual face itself like this:
    face_image = image[top:bottom, left:right]
    face_landmarks_list = face_recognition.face_landmarks(face_image)
    for face_landmarks in face_landmarks_list:
        pil_image = Image.fromarray(face_image)
        d = ImageDraw.Draw(pil_image, 'RGBA')

        # Eyebrows
        # d.polygon(face_landmarks['left_eyebrow'], fill=(150, 150, 150, 50))
        # d.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
        d.line(face_landmarks['left_eyebrow'], fill=(225, 0, 0, 225))
        d.line(face_landmarks['right_eyebrow'], fill=(225, 0, 0, 225))

        # Lips
        #d.polygon(face_landmarks['top_lip'], fill=(150, 150, 150, 150))
        #d.polygon(face_landmarks['bottom_lip'], fill=(150, 150, 150, 150))
        d.line(face_landmarks['top_lip'], fill=(225, 0, 0, 225))
        d.line(face_landmarks['bottom_lip'], fill=(225, 0, 0, 225))

        # Nose
        d.line(face_landmarks['nose_bridge'], fill=(225, 0, 0, 225))
        d.line(face_landmarks['nose_tip'], fill=(225, 0, 0, 225))


        # Eyeballs
        #d.polygon(face_landmarks['left_eye'], fill=(225, 0, 0, 225))
        #d.polygon(face_landmarks['right_eye'], fill=(225, 0, 0, 225))

        # Eyes profile
        d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(225, 0, 0, 225))
        d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(225, 0, 0, 225))

        d.line(face_landmarks['left_eye'], fill=(225, 0, 0, 225))
        d.line(face_landmarks['right_eye'], fill=(225, 0, 0, 225))

        pil_image.show()
    i +=1
    print(i)

"""
for face_landmarks in face_landmarks_list:
    pil_image = Image.fromarray(image)
    d = ImageDraw.Draw(pil_image, 'RGBA')

    # Make the eyebrows into a nightmare
    #d.polygon(face_landmarks['left_eyebrow'], fill=(150, 150, 150, 50))
    #d.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
    d.line(face_landmarks['left_eyebrow'], fill=(150, 150, 150, 50), width=5)
    d.line(face_landmarks['right_eyebrow'], fill=(150, 150, 150, 50), width=5)

    # Gloss the lips
    d.polygon(face_landmarks['top_lip'], fill=(150, 150, 150, 50))
    d.polygon(face_landmarks['bottom_lip'], fill=(150, 150, 150, 50))
    d.line(face_landmarks['top_lip'], fill=(150, 150, 150, 50))
    d.line(face_landmarks['bottom_lip'], fill=(150, 150, 150, 50), width=8)

    # Sparkle the eyes
    d.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
    d.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

    # Apply some eyeliner
    d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(150, 150, 150, 50), width=6)
    d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(150, 150, 150, 50), width=6)

    pil_image.show()
    """