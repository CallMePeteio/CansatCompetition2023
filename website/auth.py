from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, login_manager
from datetime import datetime

from .models import User, Flightmaster, GPSdata, Telemdata
from . import db, pathToDB, selectFromDB, timeToMinutes

import sqlite3
import random
import time


auth = Blueprint('auth', __name__)


loginEmails = ["admin@gmail.com", "petter@gmail.com", "teodor@gmail.com", "nikolai@gmail.com"] # ALLE DE FORKJELLIGE BRUKERNAVNENE PÅ NETTSIDENM
loginPaswds = ["Passord1"] # ALLE DE FORKJELLIGE PASSORDENE TIL NETTSIDENE



@auth.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST": # IF THE REQUEST METHOD IS POST
        email = request.form.get("email") # GETS THE EMAIL INPUTTED IN THE EMAIL FEILD
        password = request.form.get("password")  # GETS THE PASSWORD INPUTTED IN THE PASSWORD FEILD

        if email in loginEmails: # IF THE EMAIL IS IN THE LOGINEMAIL LIST
            if password in loginPaswds: # IF THE PASSWORD IS IN THE PASSWORD LIST

                user = User.query.filter_by(email=email).first() # FINDS THE USER
                if user: # IF THE USER EXISTS
                    if check_password_hash(user.password, password): # CHECKS IF THE PASSWORD IS CORRECT 

                        login_user(user, remember=True) # LOGINS THE NEW USER
                        flash("Logged in", category="sucsess") # FLASHES THE LOGIN MESSAGE 
                        return redirect(url_for("home.renderHome")) # REDIRECTS TO HOME

                    else:
                        flash("Wrong Password", category="error") # FLASHES THE MESSAGE IF YOU ENTERED THE WRONG PASSWORD
                else:
                    flash("Wrong Email", category="error") # FLASHES THE MESSAGE IF YOU ENTERED THE WRONG EMAIL

            else:
                flash("Incorecct password", category="error") # FLASHES THE MESSAGE IF YOU ENTERED THE WRONG PASSWORD
        else:
            flash("Incorrect email", category="error") # FLASHES THE MESSAGE IF YOU ENTERED THE WRONG EMAIL
          
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout(): # LOGSOUT THE USER
    logout_user() # LOGS OUT THE USER 
    return redirect(url_for('auth.login')) # REDIRECTS THE USER TO THE LOGIN PAGE









@auth.route("/secretuser", methods=["POST", "GET"])
def secretUser():

    for userEmail in loginEmails: 
        userMake = User(email=userEmail, password=generate_password_hash(loginPaswds[0], method="sha256"))
        db.session.add(userMake)
        db.session.commit()

    return render_template("base.html")





@auth.route("/secret", methods=["POST", "GET"])
@login_required
def secret():
    print()

    now = datetime.now()
    currentTime = now.strftime("%Y-%m-%d %H:%M:%S")

    flightMake = Flightmaster(loginId=current_user.id,  startTime=currentTime)
    db.session.add(flightMake)
    db.session.commit()


    flightData = selectFromDB(pathToDB, "flightmaster", ["WHERE"], ["loginId"], [current_user.id]) # SELECS ALL OF THE DATA FROM FLIGHTMASTER WHERE LOGINID IS CURRENT USER.ID
    latestFlightID = flightData[len(flightData) -1][0] # GETS THE LATEST FLIGHT ID

    latestFlightStartTime = flightData[len(flightData) -1][2] # FINDS THE LATEST FLIGHT STARTTIME, RETURNS YEAR:MONTH HR:MIN:SEC
    latestFlightStartTime = latestFlightStartTime.split(" ")[1] # CONVERTS THE latestFlightStartTime TO HR:MIN:SEC
    flightStartMin = timeToMinutes(latestFlightStartTime) # CONVERTS THE LATEST FLIGHTSTARTTIME TO MINUTES

    dataSize = 4
    for i in range(dataSize): 


        gpsData = GPSdata(flightId=latestFlightID, lat=random.uniform(67.206842, 67.208182), lon=random.uniform(15.117254, 15.157934))

        currentFlightMin = timeToMinutes("_", currentTime=True) # GETS THE CURRENT FLIGHT TIME IN MINUTES
        estimatedFlightTime=currentFlightMin-flightStartMin # CALCULATES THE ESTMATED FLIGHT TIME

        telemData = Telemdata(flightId=latestFlightID, atmoPressure=random.uniform(10, 15), temperature=random.uniform(10, 30), flightTime=estimatedFlightTime)
        db.session.add(gpsData)
        db.session.add(telemData)
        db.session.commit()
        time.sleep(2)


    return render_template("base.html")

@auth.route("/generatedata", methods=["POST", "GET"])
@login_required
def generateData():
    print()

    flightData = selectFromDB(pathToDB, "flightmaster", ["WHERE"], ["loginId"], [current_user.id]) # SELECS ALL OF THE DATA FROM FLIGHTMASTER WHERE LOGINID IS CURRENT USER.ID

    latestFlightID = flightData[len(flightData) -1][0]

    latestFlightStartTime = flightData[len(flightData) -1][2] # FINDS THE LATEST FLIGHT STARTTIME, RETURNS YEAR:MONTH HR:MIN:SEC
    latestFlightStartTime = latestFlightStartTime.split(" ")[1] # CONVERTS THE latestFlightStartTime TO HR:MIN:SEC
    flightStartMin = timeToMinutes(latestFlightStartTime) # CONVERTS THE LATEST FLIGHTSTARTTIME TO MINUTES
 
    dataSize = 100
    for i in range(dataSize): 
        gpsData = GPSdata(flightId=latestFlightID, lat=random.uniform(67.206842, 67.208182), lon=random.uniform(15.117254, 15.157934))
        #gpsData = GPSdata(flightId=latestFlightID, lat=random.randint(0, 50), lon=random.randint(0, 50))

        currentFlightMin = timeToMinutes("_", currentTime=True) # GETS THE CURRENT FLIGHT TIME IN MINUTES
        estimatedFlightTime=currentFlightMin-flightStartMin # CALCULATES THE ESTMATED FLIGHT TIME

        telemData = Telemdata(flightId=latestFlightID, atmoPressure=random.uniform(10, 15), temperature=random.uniform(10, 30), flightTime=estimatedFlightTime)
        db.session.add(gpsData)
        db.session.add(telemData)
        db.session.commit()
        time.sleep(2)


    return render_template("base.html")