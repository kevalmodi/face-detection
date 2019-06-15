import face_recognition
import cv2
import glob, os, time
import pymysql
from datetime import date,datetime
from flask import Flask,jsonify

app = Flask(__name__)


@app.route("/")
def fn1():

    result = fn2()

    print("result=",result)

    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin","*")

    return response

@app.route("/showResult")
def fn2():

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    list=[]
    count=0


    os.chdir(r'C:\Users\hp\Desktop\face')
    for file in glob.glob("*.jpg"):
        list.append(file)
        print("nikl gaya")


    index=0
    imagefiles=[]
    known_face_encodings=[]
    known_face_names=[]

    for imagefile in list:
        imagefiles.append(list[index].replace('.jpg',''))
        image = face_recognition.load_image_file(imagefile)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        index=index+1

    a=[[],[],[],[],[],[],[],[],[]]
    b=[]
    print(face_encoding)
    #
    known_face_names = imagefiles
    # for i in range(len(known_face_names)):
    #     a.append(b)
    # print(a[2])

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    all_time_faces_names = []
    Unknown_array = []
    process_this_frame = True


    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]


        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)


        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame,number_of_times_to_upsample=1)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            counter=0

            face_names = []
            if len(face_locations)>0:
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.50)

                    name = "Unknown"
                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches :
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]

                        a[first_match_index].append(name)

                    # Add all names to array for displaying on the screen
                    face_names.append(name)
                    # if person is unknown then add that to the unknow array for counting total number of unknown people
                    if name == "Unknown":
                        Unknown_array.append(name)
                        a[6].append(name)

                        # a[len(a)-1].append(name)
                    # else filter duplicate names and add those to the final array
                    for i in range(len(a)):
                        if len(a[i])==7 and "added" not in a[i]:
                            print("name ====================",a[i][0])

                            cv2.imwrite(r"E:\python\FaceRecognitonFinal\Unauthorized Images\{}.jpg".format(a[i][0]),frame)

                            a[i].append("added")



                    else:
                        if name not in all_time_faces_names:
                            all_time_faces_names.append(name)

        # process_this_frame = not process_this_frame
            else:
                a=[[],[],[],[],[],[],[]]

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left+20, top), (right+20, bottom), (0, 0, 255), 2)
            if(name=="Unknown"):
                if(counter==7):

                    count=count+1

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image

        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam


    video_capture.release()
    cv2.destroyAllWindows()

    userName = name
    enterDate = str(date.today())
    enterTime = str(datetime.time(datetime.now()))

    connection = pymysql.connect(

        host = "localhost",
        user = "root",
        password = "root",
        db = "misbehavedetection"
    )
    cursor1 = connection.cursor()
    cursor1.execute(
        "INSERT INTO teacher_authentication(userName,enterDate,enterTime) VALUES ('"+userName+"','"+enterDate+"','"+enterTime+"')"
    )
    connection.commit()
    cursor1.close()
    connection.close()

    infoDict = {"userName":userName}

    return infoDict

app.run(port=4040)