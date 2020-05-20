import socket
from passlib.hash import sha256_crypt
from _thread import *
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from getpass import getpass
import os, requests, json

HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 5004 # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)


def login(username, password, s):
    loginUser = username
    loginPass = password
    msg = ''

    if loginUser is None or loginPass is None:
        msg = 'Username or Password is empty'
        s.sendAll(msg.encode())
    else:
        response = requests.get('http://127.0.0.1:5000/api/token', auth=(loginUser, loginPass))
        print("Response from request is - " + str(response))
        print("Text from response is - " + str(response.text))
        
        #Login failed
        if str(response) == "<Response [401]>":
            msg = 'Unauthorized Access'
            s.sendall(msg.encode())
            print("<Response [401]> pathway")

        elif str(response.text) == "Unauthorized Access":
            msg = 'Unauthorized Access'
            s.sendall(msg.encode())
            print("Unauthorized Access pathway")
        #Login success
        else:
            data = json.loads(response.text)
            print(str(data))
            token = data['token']
            response = requests.get('http://127.0.0.1:5000/api/login', auth=(token, 'unused'))
            data = json.loads(response.text)
            msg = 'Login successful'
            s.sendall(msg.encode())
            print("login success")

def addClient(conn, addr):
    with conn:
        print("Connected to {}".format(addr))

        sessionUser = ''

        while True:
            data = conn.recv(2048)
            decodedData = data.decode()
            if(not data):
                break

            instruct, info = decodedData.split(":", 1)

            if instruct == "username":
                sessionUser = info
            elif instruct == "password":
                login(sessionUser, info, conn)

        print("Disconnecting from client " + str(addr) + "...")
        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind(ADDRESS)
    except socket.error as e:
        print(str(e))
     
    s.listen()

    while True:

        print("Listening on {}...".format(ADDRESS))
        conn, addr = s.accept()
        start_new_thread(addClient, (conn, addr,))

    print("Closing listening socket...")
print("Done!")
            