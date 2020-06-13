#from consoleAP import console
import socket
from getpass import getpass
from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
from _thread import *
import bluetooth
from inputimeout import inputimeout, TimeoutOccurred
from pyzbar import pyzbar


HOST = "127.0.0.1" # The server's hostname or IP address.
PORT = 5007        # The port used by the server.
ADDRESS = (HOST, PORT)

MY_MAC = "6C:72:E7:CE:C1:EE"

class Menu:
    def printMenu():
        print("\nWelcome to Agent Pi Console View!")
        print("Console refreshes every 20 seconds")
        print("1. Login with Password")
        print("2. Login with Facial Recognition")
        print("3. Engineer Login with QR Code")
        print("4. Exit")

    def selectOptions():
        print("\nPlease select from these Options")
        print("1. Unlock Car")
        print("2. Return Car")
        print("3. Log Out")
    
    
    def engineerUI():
        print("\nWelcome to the EngineerUI!")
        print("What would you like to do?")
        print("1. Repair Car")
        print("2. Log Out")

class Functions:
    def login(s):
        """Logging in checks to see if it matches any user from our database

        :param s: socket
        :type s: socket
        :return: True if login successful, else False
        :rtype: boolean
        """
        username = "username:" + input("Please enter username: ")
        s.sendall(username.encode())
        outcome = False

        password = getpass('Password: ')
        passToSend = "password:" + password
        s.sendall(passToSend.encode())

        data = s.recv(2048)
        decodedData = data.decode()

        if not data:
            return

        if decodedData == "Login successful":
            print('\nLogin Successful')
            outcome = True

        else:
            print('\nLogin Failed')
            outcome = False

        return outcome

    def faceLogin(s, userID):
        """Function to login using face metrics

        :param s: socket
        :type s: socket
        :param userID: userID of the matching face from dataset
        :type userID: str
        :return: outcome, True if successful login, else false
        :rtype: boolean
        """
        message = 'userid:' + str(userID)
        s.sendall(message.encode())
        outcome = False

        data = s.recv(2048)
        decodedData = data.decode()

        if not data:
            return
        
        if decodedData == "Login successful":
            print('\nLogin Successful')
            outcome = True

        else:
            print('\nLogin Failed')
            outcome = False

        return outcome

    def unlockCar(s):
        """Function to unlock the car

        :param s: socket
        :type s: socket
        :return: True if unlocked, False otherwise
        :rtype: boolean
        """
        outcome = False
        bookingCode = "bookingcode:" + input("Unlock Code: ")
        s.sendall(bookingCode.encode())

        data = s.recv(2048)
        decodedData = data.decode()

        if not data:
            return False
    
        if decodedData == "Car Unlocked":
            print('\nCar Unlocked')
            outcome = True
    
        elif decodedData == 'Not your booking':
            print('\nError: Not your booking')

        elif decodedData == 'Already Unlocked':
            print('\nError: Car has already been unlocked')

        elif decodedData == 'Car already returned':
            print('\nError: Car has already been returned')
        
        elif decodedData == 'Wrong time':
            print('\nError: Your booking is not for the current time')

        else:
            print('\nError: Invalid booking code')

        return outcome

    def returnCar(s):
        """Return a car function that if user selects return car this method is called

        :param s: socket
        :type s: socket
        :return: True if returned, else False
        :rtype: boolean
        """
        outcome = False
        x = input('Are you sure you want to return the car? (Y/N): ')
        userInput = x.upper()
        msg = "returncar:" + userInput

        if userInput == 'Y' or userInput == 'N':
            s.sendall(msg.encode())
            data = s.recv(2048)
            decodedData = data.decode()

            if not data:
                return False

            if decodedData == 'Car Returned':
                print('\nCar Returned')
                outcome = True

            elif decodedData == 'Rejected':
                print('\nReturning car cancelled...')

            else:
                print('\nError while returning car')
                
        return outcome

    def bookingCode(s):
        """Function to check if booking code is valid

        :param s: socket
        :type s: socket
        :return: True if valid, else False
        :rtype: boolean
        """
        outcome = False
        msg = 'facebookingcode:' + input('Booking Code: ')
        s.sendall(msg.encode())
        data = s.recv(2048)
        decodedData = data.decode()

        if not data:
            return False
        
        if decodedData == 'Valid':
            outcome = True
        else:
            outcome = False
        
        return outcome


    def recogniseFace():
        """Function to check if any face matches the dataset

        :return: id of user if matches, else blank
        :rtype: String
        """
        foundUser = ''
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-e", "--encodings", default="encoding/encodings.pickle",
        help="path to serialized db of facial encodings")
        ap.add_argument("-r", "--resolution", type=int, default=240,
            help="Resolution of the video feed")
        ap.add_argument("-d", "--detection-method", type=str, default="hog",
            help="face detection model to use: either `hog` or `cnn`")
        args = vars(ap.parse_args())

        # load the known faces and embeddings
        print("[INFO] loading encodings...")
        data = pickle.loads(open(args["encodings"], "rb").read())

        # initialize the video stream and then allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        print('\nPlease look into the camera...')
        vs = VideoStream(src = 0).start()
        time.sleep(2.0)

        counter = 0

        # loop over frames from the video file stream
        while True:
            # grab the frame from the threaded video stream
            frame = vs.read()

            # convert the input frame from BGR to RGB then resize it to have
            # a width of 750px (to speedup processing)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb = imutils.resize(frame, width = args["resolution"])

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input frame, then compute
            # the facial embeddings for each face
            boxes = face_recognition.face_locations(rgb, model = args["detection_method"])
            encodings = face_recognition.face_encodings(rgb, boxes)
            name = ''
            
            counter += 1

            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"], encoding)

                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    name = max(counts, key = counts.get)
        

            if counter == 30:
                founderUser = ''
                print('\nFace Recognition Timeout: Exceeded time limit...')
                break
            if name != '':
                # print to console, identified person
                print("User id: {}".format(name))
                foundUser = name   
                break     

        # do a bit of cleanup
        vs.stop()
        
        return foundUser

    def searchBluetooth(s, found_devices):
        while True:
            nearby_devices = bluetooth.discover_devices()

            for x in nearby_devices:
                #Send message to master pi to check
                msg = 'bluetooth:' + x
                s.sendall(msg.encode())
                data = s.recv(2048)
                decodedData = data.decode()

                #If found in database
                if decodedData == 'True':
                    print("Engineer detected... logging in at next refresh")
                    found_devices.append(x)
                    return found_devices

    def detectQR(s):
        print("[INFO] starting video stream...")
        print("\nPlease show your QR code")

        vs = VideoStream(src = 0).start()
        found = False
        barcodeData = ''
        QR_Successful = False
        qr_counter = 0

        while found == False:
            qr_counter += 1
            

            # grab the frame from the threaded video stream and resize it to
	        # have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)

            # find the barcodes in the frame and decode each of the barcodes
            barcodes = pyzbar.decode(frame)

            # loop over the detected barcodes
            for barcode in barcodes:
                # the barcode data is a bytes object so we convert it to a string
                barcodeData = barcode.data.decode('utf-8')
                barcodeType = barcode.type
                found = True

            if qr_counter == 250:
                found = True
        
        if barcodeData != '':
            msg = 'mac:' + barcodeData
            s.sendall(msg.encode())

            data = s.recv(2048)
            decodedData = data.decode()

            if decodedData == 'True':
                print('\nQR Code Accepted!')
                QR_Successful = True
            else:
                print('\nInvalid QR Code')
                QR_Successful = False
        else:
            print('\nTimeout: No QR Code detected')
            QR_Successful = False

        return QR_Successful

class Main:
    def run():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to {}...".format(ADDRESS))
            s.connect(ADDRESS)
            print("Connected.")

            isLoggedIn = False
            hasUnlocked = False
            isEngineer = False
            start_searching = True

            found_devices = []

            #endless loop for menu until exit 
            while True:
                if not isLoggedIn:

                    if len(found_devices) > 0:
                        response = "Engineer Detected"
                        start_searching = False

                    else:
                        if start_searching:
                            #New thread to work on searching mac address with bluetooth
                            start_new_thread(Functions.searchBluetooth,(s,found_devices,))
                        
                        Menu.printMenu()
                        try:
                            #Prompt for input with a certain time limit of 20 seconds
                            response = inputimeout(prompt='\nResponse: ', timeout=20)
                            start_searching = False
                        except TimeoutOccurred:
                            response = "Timeout"

                    #Checks to see which input 
                    if response == "1":
                        if Functions.login(s):
                            isLoggedIn = True
                        else:
                            isLoggedIn = False
                    elif response == "2":
                        userID = Functions.recogniseFace()
                        if userID != '':
                            if Functions.faceLogin(s, userID):
                                isLoggedIn = True
                            else:
                                print('\nFace unrecognised')
                                isLoggedIn = False
                    elif response == "3":
                        if Functions.detectQR(s):
                            isLoggedIn = True
                            isEngineer = True
                        else:
                            isLoggedIn = False
                            isEngineer = False
                            start_searching = True

                    elif response == "4":
                        print("\nShutting down...")
                        break

                    elif response == "Engineer Detected":
                        print("\nLogging in as Engineer")
                        found_devices.clear()
                        isLoggedIn = True
                        isEngineer = True
                    
                    elif response == "Timeout":
                        print("\nRefreshing console")
                        response = None

                    else:
                        print("\nError: Invalid Input")

                #If not an engineer (different user type than engineer)
                elif isLoggedIn and not isEngineer:
                    Menu.selectOptions()
                    response = input("\nResponse: ")

                    if response == "1":
                        if hasUnlocked:
                            print('You have already unlocked a car')

                        else:
                            if Functions.unlockCar(s):
                                hasUnlocked = True

                            else:
                                hasUnlocked = False

                    elif response == "2":
                        if hasUnlocked:

                            if Functions.returnCar(s):
                                hasUnlocked = False

                            else:
                                hasUnlocked = True

                        else:
                            print('\nYou have not unlocked a car to return')

                    elif response == "3":
                        msg = 'logout:random'
                        s.sendall(msg.encode())
                        print("\nLogging out...")
                        isLoggedIn = False
                        start_searching = True

                    else:
                        print("\nError: Invalid Input")

                else:
                    #User type of engineer which can only be unlocked with MAC address using bluetooth search
                    Menu.engineerUI()
                    response = input("\nResponse: ")

                    if response == "1":
                        carId = input("Confirm Car ID: ")

                        msg = 'repair:' + carId
                        s.sendall(msg.encode())
                        data = s.recv(2048)
                        decodedData = data.decode()

                        if decodedData == 'True':
                            #repair the car
                            print('car is now repaired')

                        elif decodedData == 'already repaired':
                            
                            #If car is already repaired
                            print("Car has already been repaired")

                        else:
                            #car is not found in issue list
                            print("No repair needed for this car")

                    elif response == "2":
                        msg = 'logout:random'
                        s.sendall(msg.encode())
                        print("\nLogging out...")
                        isLoggedIn = False
                        isEngineer = False
                        start_searching = True
                    else:
                        print("\nError: Invalid Input")


            print("Disconnecting from server.")
        print("Done.")


if __name__ == "__main__":
    Main.run()