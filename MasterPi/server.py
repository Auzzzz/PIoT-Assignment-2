import socket
from passlib.hash import sha256_crypt
from _thread import *
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from datetime import datetime
from datetime import date

HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 5007 # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)


class Functions:

    def login(username, password, s):
        """Function to log in to the api which will the send back message to AP to signal whether it is a successful login or not. 
    
        :param username: username entered
        :param password: password entered  
        :param s: socket to send data
        :returns: userID or blank
    
        """
        loginUser = username
        loginPass = password
        msg = ''
        outcome = ''

        if loginUser is None or loginPass is None:
            msg = 'Username or Password is empty'
            s.sendAll(msg.encode())
        else:
            response = requests.get('http://127.0.0.1:5000/api/token', auth=(loginUser, loginPass))
        
            #Login failed
            if response.status_code == 401:
                msg = 'Unauthorized Access'

            #Login success
            else:
                data = json.loads(response.text)
                token = data['token']
                response = requests.get('http://127.0.0.1:5000/api/login', auth=(token, 'unused'))
                data = json.loads(response.text)
                userID = data['userid']
                msg = 'Login successful'
                outcome = str(userID)

        s.sendall(msg.encode())
        return outcome

    def loginWithFace(userID, s):
        """Function to log in to the api which will the send back message to AP to signal whether it is a successful login or not using facial recognition.
    
        :param userID: userID found from facial recognition entered
        :param s: socket to send data
        :returns: userID or blank
    
        """
        msg = ''
        response = requests.get('http://127.0.0.1:5000/api/person/' + str(userID))
        outcome = ''
        result = json.loads(response.text)
        blank = "{" + "}"
        
        if str(result) == blank:
            msg = 'Unauthorized Access'
        else:
            msg = 'Login successful'
            outcome = str(userID)
        
        s.sendall(msg.encode())
        return outcome


    def unlockCar(s, bookingCode, userID):
        """Function to unlock a car if the user successfully log in and entered the booking code.
    
        :param s: socket to send data
        :param bookingCode: booking code entered by user from AP
        :param userID: userID found from current user entered
        :returns: outcome. bookingID in string if success, blank otherwise
    
        """
        p = {'bookingcode':bookingCode}
        response = requests.post('http://127.0.0.1:5000/api/booking/code', json=p)
        msg = ''
        outcome = ''

        if response.ok:
            response_json = response.json()
            if str(response_json) != '[]':  
                bookingDetails = response_json[0]
                bookingUserID = bookingDetails['userid']
                bookingID = bookingDetails['bookingid']
                bookingStatus = bookingDetails['bookingstatus']
                startTime = bookingDetails['stime']
                endTime = bookingDetails['etime']
                bookingDate = bookingDetails['bdate']
                currentDate = date.today()
                now = datetime.now()
                timeNow = now.strftime("%H:%M:%S")
                
                if str(bookingUserID) == str(userID):
                    if bookingStatus == 1:
                        if str(startTime) <= str(timeNow) and str(timeNow) <= str(endTime) and str(bookingDate) == str(currentDate):
                            msg = 'Car Unlocked' 
                            j = {'bookingid':bookingID,'bookingstatus':str(2)}
                            response = requests.post('http://127.0.0.1:5000/api/booking/s', json=j)
                            outcome = str(bookingID)
                        
                        else:
                            msg = 'Wrong time'
                          
                    elif bookingStatus == 2:
                        msg = 'Already Unlocked'
                    
                    elif bookingStatus == 3:
                        msg = 'Car already returned'
                       
                    else:
                        msg = 'Error'
                 
                else:
                    msg = 'Not your booking' 
                    
            else:
                msg = 'Error'
        else:
            msg = 'Error'
    
        s.sendall(msg.encode())
        return outcome

    def returnCar(s, bookingID):
        """returnCar returns the car after the user selects return car in the console.

        :param s: socket
        :param bookingID: bookingID of current user being used
        :returns: outcome, True if success
        """
        p = {'bookingid':bookingID,'bookingstatus':str(3)}
        response = requests.post('http://127.0.0.1:5000/api/booking/s', json=p)
        msg = ''
        outcome = False

        if response.ok:
            msg = 'Car Returned'
            outcome = True
        else:
            msg = 'Error'
            outcome = False
        
        s.sendall(msg.encode())

        return outcome
    
    #To check for MAC address
    def checkMacAddress(s, mac_address, engineerUserID):

        #Get results from api
        response = requests.get('http://127.0.0.1:5000/api/users/engineer/check/{}'.format(mac_address))
        msg = ''
        result = json.loads(response.text)

        #if results are found
        if str(result) != '[]':
            engineerData = result[0]
            engineerUserID = engineerData['userid']
            msg = 'True'
        else:
            msg = 'False'
        
        s.sendall(msg.encode())
        
        return engineerUserID
    
    #Check if car needs repairs
    def checkCarIssues(s, carId, engineerId):

        #get information from carId
        response = requests.get('http://127.0.0.1:5000/api/car/issue/car/list/{}'.format(carId))
        result = json.loads(response.text)
        msg = 'False'

        #check if such car needs repair
        if str(result) != '[]':
            for r in result:
                
                assignedTo = r['assigned_to']
                issueStatus = r['issue_status']
                issueId = r['issueid']

                #if car targetted is found
                if str(assignedTo) == str(engineerId):
                    
                    #repair the car
                    if str(issueStatus) == '1':
                        msg = 'True'
                        p = {'issue_status':2}

                        #setting the issue status to 2 meaning already repaired
                        requests.post('http://127.0.0.1:5000/api/car/issue/web/status/{}'.format(str(issueId)), json = p)

                    #means car already repaired
                    elif str(issueStatus) == '2':
                        msg = 'already repaired'
        #send necessary information back to agent pi
        s.sendall(msg.encode())

class Main:
    def addClient(conn, addr):
        with conn:
            print("Connected to {}".format(addr))
        
            sessionUser = ''
            sessionBookingID = ''
            sessionUserID = ''
            sessionBookingDetails = ''

            while True:
                try:
                    data = conn.recv(2048)
                    decodedData = data.decode()
                except ConnectionResetError:
                    print('Disconnected from ' + str(addr))

                if(not data):
                    break

                instruct, info = decodedData.split(":", 1)

                if instruct == "username":
                    sessionUser = info
                elif instruct == "password":
                    sessionUserID = Functions.login(sessionUser, info, conn)
                elif instruct == 'userid':
                    sessionUserID = Functions.loginWithFace(info, conn)
                elif instruct == "bookingcode":
                    sessionBookingID = Functions.unlockCar(conn, info, sessionUserID)
                elif instruct == "returncar":
                    if info == 'Y':
                        Functions.returnCar(conn, sessionBookingID)
                    else:
                        msg = 'Rejected'
                        conn.sendall(msg.encode())
                elif instruct == 'logout':
                    sessionUser = ''
                    sessionBookingID = ''
                    sessionBookingDetails = ''
                    sessionUserID = ''
                elif instruct == 'bluetooth':
                    #search for MAC adress with input
                    sessionUserID = Functions.checkMacAddress(conn, info, sessionUserID)

                elif instruct == 'repair':
                    Functions.checkCarIssues(conn, info, sessionUserID)

            print("Disconnecting from client " + str(addr) + "...")
            conn.close()

    def run():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(ADDRESS)
                print('Server Running...')
                print("\n( -- Press CTRL+C to Quit -- )\n")
            except socket.error as e:
                print(str(e))
     
            s.listen()

            while True:
                try:
                    print("Listening on {}...".format(ADDRESS))
                    conn, addr = s.accept()
                    start_new_thread(Main.addClient, (conn, addr,))
                except KeyboardInterrupt:
                    break

            s.shutdown(socket.SHUT_RDWR)
            s.close()
            print("\nClosing listening socket...")
        print("Done!")

if __name__ == "__main__":
    Main.run()