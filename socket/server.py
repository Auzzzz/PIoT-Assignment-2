import socket
from passlib.hash import sha256_crypt
from _thread import *
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from getpass import getpass
import os, requests, json
from datetime import datetime
from datetime import date

HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 5002 # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)


class Functions:
    def login(username, password, s):
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
            if str(response) == "<Response [401]>":
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
        msg = ''
        response = requests.get('http://127.0.0.1:5000/api/person/' + str(userID))
        outcome = ''

        if str(response) == '<Response [401]>':
            msg = 'Unauthorized Access'
        else:
            msg = 'Login successful'
            outcome = str(userID)
        
        s.sendall(msg.encode())
        return outcome


    def unlockCar(s, bookingCode, userID):
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
                            response = requests.post('http://127.0.0.1:5000/api/booking', json=j)
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
        p = {'bookingid':bookingID,'bookingstatus':str(3)}
        response = requests.post('http://127.0.0.1:5000/api/booking', json=p)
        msg = ''

        if response.ok:
            msg = 'Car Returned'
        else:
            msg = 'Error'
        
        s.sendall(msg.encode())


class Main:
    def addClient(conn, addr):
        with conn:
            print("Connected to {}".format(addr))
            print("( -- Press CTRL+C to Quit -- )")
        
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
                
            print("Disconnecting from client " + str(addr) + "...")
            conn.close()

    def run():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(ADDRESS)
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