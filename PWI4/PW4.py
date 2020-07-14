"""

Author: Hasse Straede Hansen 
Mail: hasse302@hotmail.com


"""
"""
This script is to communicate with PWI4, by PlaneWave Instruemnts using the python functions below.

Each function has a brief explanation.

Currently on version 0.0.1 as of 28/12/2019.

"""
import numpy as np
import requests
import time
from time import ctime
import numpy as np
from xml.etree import ElementTree as ET
import song_star_checker_AUTOTUNE as SSCA
import re
import datetime
import json
from RaConverter import *
from urllib.parse import urlencode


class Object(object): 
    """
    Simple object for collecting properties in PWI4Status
    """
    pass


class PWI4():   
    def __init__(self):
        """
        This function initializes the connection to PWI4. 
        It also defines names for the variables from PWI4, which are stored in self. 
        
        Returns: True
        """
        ##this is the IP address of PWI4
        self.link="http://10.22.88.145:8220/"
        status = requests.get(self.link+"status")
        
        print("The response is beneath")
        print(status.text)
        print("The response is above")
        
        data = status.text.split('\n')
        self.data = data

        #site parameters
        self.site_latitude = data[1].split('=')[1]
        self.site_longitude = data[2].split('=')[1]
        self.site_elevation = data[3].split('=')[1]
        self.site_lmst = data[4].split('=')[1]
        
        #Focuser
        self.FOC_connection = data[36].split('=')[1]
        self.FOC_pos = data[38].split('=')[1]
        self.FOC_moving = data[39].split('=')[1]


        #Rotator
        self.ROT_connection = data[40].split('=')[1]
        self.ROT_moving = data[44].split('=')[1]
        self.ROT_mechanial_pos = data[42].split('=')[1]
        self.ROT_pos = data[43].split('=')[1]
        self.ROT_derotate_enabled = data[41].split('=')[1]

        #Mount
        self.MNT_connection = data[5].split('=')[1] #true/false
        self.MNT_slewing = data[15].split('=')[1] #True/False
        self.MNT_Alt = data[14].split('=')[1] #in deg
        self.MNT_Azm = data[13].split('=')[1] #in deg
        self.MNT_Ra2000 = data[9].split('=')[1] #in hours
        self.MNT_Dec2000 = data[10].split('=')[1] #in degrees
        self.MNT_tracking = data[16].split('=')[1] #true/false
        self.MNT_AltMotor = data[27].split('=')[1] #enabled/disabled given by True/False
        self.MNT_AzmMotor = data[22].split('=')[1] #enabled/Disabled given by True/False
        self.MNT_PointingModel = data[32].split('=')[1] #filename of current pointing model
        self.MNT_PointingModelPoints = data[33].split('=')[1] #Number of points in pointing model
        self.MNT_PointingModelError = data[35].split('=')[1] #Error of pointing model in arcsec
        self.MNT_AltRMSErrorArcsec = data[23].split('=')[1]
        self.MNT_AzmRMSErrorArcsec = data[28].split('=')[1]
        



        #Setting the different values with a "human-readable" naming-scheme.

        #Status (times)
    #     self.STAT_utc = self.tree[0][0].text
    #     self.STAT_lst = self.tree[0][1].text
    #     self.STAT_jd  = self.tree[0][2].text

    #     #Focuser
    #     self.Foc_connection = self.tree[1][0].text
    #     self.Foc_pos = self.tree[1][1].text
    #     self.Foc_move = self.tree[1][3].text
    #     self.Foc_complete = self.tree[1][4].text
    #     self.Foc_homing = self.tree[1][5].text

    #     #Rotator
    #     self.ROT_connection = self.tree[4][0].text
    #     self.ROT_position = self.tree[4][1].text
    #     self.ROT_moving = self.tree[4][3].text 
    #     self.ROT_goToComplete = self.tree[4][4].text
    #     self.ROT_homing = self.tree[4][5].text
    #     self.ROT_AltAzDerotate = self.tree[4][6].text
        
    #     #Mount
    #     self.MNT_connection = self.tree[7][0].text
    #     self.MNT_on_target  = self.tree[7][1].text
    #     self.MNT_moving = self.tree[7][3].text
    #     self.MNT_tracking = self.tree[7][3].text
    #     self.MNT_Ra2000 = self.tree[7][8].text
    #     self.MNT_Dec2000 = self.tree[7][9].text
    #     self.MNT_Alt = self.tree[7][13].text
    #     self.MNT_Azm = self.tree[7][12].text
    #     self.MNT_AzmMotor = self.tree[7][20].text
    #     self.MNT_AltMotor = self.tree[7][21].text
    #     self.MNT_PointingModel = self.tree[7][22].text
    #     self.MNT_AzmMotorError = self.tree[7][16].text
    #     self.MNT_AltMotorError = self.tree[7][17].text
    #     self.MNT_AltRMSErrorArcsec = self.tree[7][15].text
    #     self.MNT_AzmRMSErrorArcsec = self.tree[7][14].text


        
    #    #Temperatures - NEEDS WORKING! DROPS OUT WHEN FOCUSER DISCONNECT
    #     if self.Foc_connection == "True":
    #        try:
    #            self.TEMP_pri = self.tree[9][0].text
    #            self.TEMP_amb = self.tree[9][1].text
    #            self.TEMP_sec = self.tree[9][2].text
    #            self.TEMP_backp = self.tree[9][3].text
    #            self.TEMP_m3 = self.tree[9][4].text
    #        except:
    #            print('There was an issue connecting the temperature sensors for the mirrors.')

    #     #Fans
    #     self.FANS_state = self.tree[10][0].text

    def update(self):
        """
        This function runs the __init__ function again to update the stored variables in self. 
        
        Returns: True
        
        """
        self.__init__()
        return True


    def getALL(self):
        """
        Prints all data from the XML.
        
        Per version 0.0.1: 
            The structure is not very human readable, but displays the whole
            XML-tree in one line. 
        
        Returns: 
            XML-tree in one line
        """
        
        ALL=self.data
        print(ALL)
        return ALL

    def getRA2000(self):
        """
        This function prints the current Right Ascension (RA) in the J2000 epoch of the mount/telescope.
        
        Returns:
            RA_J2000 in the format HH:MM:SS
        """
        self.update()
        RA = self.MNT_Ra2000

        RA_hour = RAconverter_DectoHH(float(RA))
        return RA_hour
    
    def getDEC2000(self):
        
        """
        Prints the current Declination (DEC) in the J2000 epoch of the mount/telescope.
        
        Returns:
            DEC_J2000 in the format DD:MM:SS
        """
        
        self.update()
        DEC = self.MNT_Dec2000
        DEC_hour = DecConverter_DecitoDD(float(DEC))
        return DEC_hour
    

    def getFocuserPos(self):
        """
        Prints the current position of the focuser in the telscope. 
        The units of the position is in microns.
        
        Returns:
            The position of the focuser in microns if the focuser is connected.
            Is the focuser not connected, a reply is sent about the focuser not being connected.
        """
        self.update()
        if self.FOC_connection == "true":
            print('The current position of the focuser is %s microns'%(self.FOC_pos))
            reply = "The current position of the focuser is %s microns"%(self.FOC_pos)
            return reply
        else:
            print('The focuser is not connected to PWI4. Please use .ConnectFOC() to connect the focuser to PWI2.')
            reply = 'The focuser is not connected to PWI4. Please use .ConnectFOC() to connect the focuser to PWI2.'
            return reply

    def getRotatorPos(self):
        """
        A function that prints the current position of the rotator.
        The units of the position of the rotator is in degrees. 
        
        Returns:
            The current position of the rotator in degrees.
        """
        self.update()
        if self.ROT_connection == "true":
            print('The current position of the rotator is %s degrees'%(self.ROT_pos))
            reply = 'The current position of the rotator is %s degrees'%(self.ROT_pos)
            return reply
        else:
            print("The rotator is not connected to PWI. Try the command: ConnectFOC()  ")
            reply = 'The rotator is not connected to PWI. Try the command: ConnectFOC() '
            return reply
    
    def getStatus(self):
        """
        Prints a status message with the current RA and DEC in J2000 epoch, the 
        current UTC time. The message also gives a message whehter the telescope 
        is moving and/or tracking. Finally it prints whether the mount, focuser and rotator is
        connected to the PWI. 
        
        Returns:
            The status message
        
        """
        self.update()
        RA = self.MNT_Ra2000
        DEC = self.MNT_Dec2000
        Alt = self.MNT_Alt
        Azm = self.MNT_Azm
        Moving = self.MNT_slewing #From the documentation, PWI recommends that I use on_target instead of moving!
        Mnt = self.MNT_connection
        Foc = self.FOC_connection
        tracking = self.MNT_tracking
        Rot = self.ROT_connection
        
        
        reply = "The telescope is pointed at RA: %s, DEC:%s (J2000) / Alt: %.4f, Azm: %.4f. \n" %(RA,DEC,float(Alt),float(Azm))
        
        
        print('The telescope is pointed at RA: %s, DEC:%s (J2000) / Alt: %.4f, Azm: %.4f.' %(RA,DEC,float(Alt),float(Azm)))

        if Moving == "False":
            print('The telescope is not moving.')
            reply += 'The telescope is not moving.\n'
        elif Moving == "True":
            print('The telescope is moving.')
            reply += 'The telescope is moving.\n'
            
        if tracking == "True":
            print('The telescope is tracking.')
            reply += 'The telescope is tracking \n'
        elif tracking == "False":
            print('The telescope is NOT tracking.')
            reply += 'The telescope is NOT tracking \n'
       
        
        print('Connections: \n')
        reply += 'Connections: \n'
        if Mnt == "true":
            print('The mount is connected to PWI')
            reply += 'The mount is connected to PWI \n'
        elif Mnt == "false":
            print('The mount is NOT connected to PWI')
            print('You should try connecting the mount with PWI using the command: .ConnectMNT()\n')
            reply += 'The mount is NOT connected to PWI \n' 
            reply += 'You should try connecting the mount with PWI using the command: .ConnectMNT() \n'
            
            
        if Foc == "true":
            print('The focuser is connected to PWI')
            reply += 'The focuser is connected to PWI \n'
        elif Foc == "false":
            print('The focuser is NOT connected to PWI')
            print('You should try connecting the focuser with the command: .ConnectFOC()\n')
            reply += 'The focuser is NOT connected to PWI\n'
            reply += 'You should try connecting the focuser with the command: .ConnectFOC() \n'
            
        if Rot == "true":
            print('The rotator is connected to PWI')
            reply += 'The rotator is connected to PWI\n'
        elif Rot == "false":
            print('The rotator is NOT connected to PWI')
            print('The rotator and focuser is linked in their connection.')
            print('You should maybe try to reconnect the focuser and theirby reconnect the rotator wit----h the functions: .DisconnectFOC() and .ConnectFOC()\n')
            reply += 'The rotator is NOT connected to PWI \n'
            reply += 'The rotator and focuser is linked in their connection. \n'
            reply += 'You should maybe try to reconnect the focuser and theirby reconnect the rotator with the functions: .DisconnectFOC() and .ConnectFOC() \n'
        
        return reply
    

    def getMNT_CONNECT(self):
        """
        Checks the connection between PWI and the mount of telescope.
        
        Returns:
            True/False for connection
        """
        self.update()
        if self.MNT_connection == "true":
            print("Mount is connected")
            return self.MNT_connection 
        else:
            print("ERROR: Mount NOT connected")
            return self.MNT_connection 


    def getFOC_CONNECT(self):
        """
        Checks the connection between PWI and the focuser
        
        Returns:
            True/False for connection between PWI and focuser
        """
        self.update()
        
        if self.FOC_connection == "true":
            print("Focuser is connected")
            return self.FOC_connection
        else:
            print("ERROR: Focuser NOT connected")
            return self.FOC_connection

    def getROT_CONNECT(self):
        """
        Checks the connection between PWI and the rotator. 
        Please note that the focuser and rotator are connected such that
        the focuser and rotator share the same connection to PWI. 
        So if the rotator is not connected, then the focuser won't bet connected either. 
        
        Returns:
            True/False for connection 
        """

        self.update()
        
        if self.ROT_connection == "true":
            print("Rotator is connected")
            return self.ROT_connection
        else:
            print("ERROR: Rotator not connected")
            return self.ROT_connection

    def getIsTrackingOn(self):
        """
        Checks if the telescope is tracking. 
        
        Returns:
            True/False for tracking 
        """
        self.update()
        IsTrackingOn = self.MNT_tracking
        if IsTrackingOn == "true":
            print("Tracking is ON.")
            return True #IsTrackingOn
        else:
            print("Tracking is OFF.")
            return False #IsTrackingOn
        
    def getTrackingRMSError(self):
        """
        """
        
        self.update()
        print('The RMS error on the Alt pointing is %.3f arcseconds'%(float(self.MNT_AltRMSErrorArcsec)))
        print('The RMS error on the Azm pointing is %.3f arcseconds'%(float(self.MNT_AzmRMSErrorArcsec)))

        reply = 'The RMS error on the Alt pointing is %.3f arcseconds \n'%(float(self.MNT_AltRMSErrorArcsec))
        reply += 'The RMS error on the Azm pointing is %.3f arcseconds'%(float(self.MNT_AzmRMSErrorArcsec))
        return reply

    def getTemps(self):
        """
        Prints the temperature of the primary mirror, the ambient temperature, 
        the secondary mirror, the backplate and the M3. 
        The unit of temperature is Celcius.
        
        Returns:
            Message with temperature of the primary mirror, the ambient temperature, 
        the secondary mirror, the backplate and the M3 (in this order)
        """
        
        
        self.update()
        Temp_PRI = self.TEMP_pri
        Temp_AMB = self.TEMP_amb
        Temp_SEC = self.TEMP_sec
        Temp_BPL = self.TEMP_backp
        Temp_M3 = self.TEMP_m3
        
        reply = ""
        
        #For the logging
        print("Temperature of primary:",Temp_PRI + " C") 
        print("Temperature of ambient:",Temp_AMB + " C") 
        print("Temperature of secondary:",Temp_SEC + " C") 
        print("Temperature of backplate:",Temp_BPL + " C")
        print("Temperature of M3:",Temp_M3 + " C") 
        
        #for the client
        reply += "Temperature of primary: %s C \n"%(Temp_PRI)
        reply += "Temperature of ambient: %s C\n"%(Temp_AMB)
        reply += "Temperature of secondary: %s C\n"%(Temp_SEC)
        reply += "Temperature of backplate: %s C\n"%(Temp_BPL)
        reply += "Temperature of M3: %s C\n"%(Temp_M3)
        
        return reply


    def MoveFocuserPos(self,position):
        """
        A function that moves the focuser position. The position is given 
        is units of microns. |
        Example: |
            MoveFocuserPos(10300) |
        Moves the focuser to 10300 microns
        
        Args: 
            The new position of the focuser given in microns.
            
            
        Returns:
            True when finished moving. 
            False if timeout occurs.
            False if the end position does not match the target position within 5 microns.
            
        """
        self.update()

        #Checks wheter the wanted position is already the current position. DOES NOT WORK FOR SOME REASON???
        if "position" == self.FOC_pos:
            print('The new requested position is already the current position of the focuser. Nothing will happen.')
            return True

        if "position" < "0":
            print('The position is less than 0 microns. The movement will NOT be executed')
            return False

        #Sends command to change position of focuser
        cmd=requests.get(self.link+"focuser/goto?target=%i"%(position))
        time.sleep(3)
        self.update()
        print('Starting to move focuser')
        timeout_sec = 30 #Number of seconds before a timeout
        timeout = time.time() + timeout_sec #setting timeout
        while self.FOC_moving == "false":
            print('Focuser moving, now at %s microns'%(self.FOC_pos))
            time.sleep(2)
            self.update()
            if time.time() > timeout:
                print('A timeout of %i seconds occured.'%(timeout_sec))
                return str("Error")
        self.update()
        if abs(self.FOC_pos - position) < 5:  #Checks if the new position is close enough to target. Set to 5 microns initially.
            print('The focuser has stopped at: %s microns'%(self.FOC_pos))
            return True
        else: 
            print('The focuser did not reach the target. The current position is %s microns'%(self.FOC_pos))
            return False
       
        
    def ConnectFOC(self):
        """
        A function to connect PWI to the focuser. 
        Please note that the rotator is also connected with the focuser
        since they share the same port to PWI. 
        
        Returns:
            True if connection is complete.
            False if timeout occurs.
        """
        FOC = requests.get(self.link+"focuser/enable")
        print('Trying to connect focuser - please wait')
        self.update()
        timeout_sec = 10 #Set the number of seconds before timeout.
        timeout = time.time() + timeout_sec
        while self.FOC_connection == "false":
            print('Waiting for focuser to connect')
            self.update()
            time.sleep(1)
            if time.time() > timeout:
                print('A timeout of %i sec has occured.'%(timeout_sec))
                return False #stop if the timeout is reached!
        return True

    def DisconnectFOC(self):
        """
        A function that disconnects the focuser from PWI. 
        Please note that the focuser and rotator are connected to PWI 
        via the same connection. A disconnect of the focuser would therefor
        also disconnect the rotator.
        
        Returns:
            True for finished disconnection
            False for timeout
        """
        self.update()
        if self.FOC_connection == "false":
            print('The focuser is already disconnected')
            return True

        cmd = requests.get(self.link+"?&device=focuser&cmd=disconnect")
        self.update()
        timeout_sec = 20
        timeout = time.time() + timeout_sec
        while self.FOC_connection == "true":
            print('Trying to disconnect focuser')
            self.update()
            time.sleep(1)
            if time.time() > timeout:
                print('A timeout of %i has occured.'%timeout_sec)
                print('There was error disconnecting the focuser')
                return False
        return True
    
    def MoveFocuserInc(self,increment):
        """
        A function that moves the focuser in increments of microns. 
        The increments work with addition, i.e. moving the focuser 100 microns and then 
        move it again 200 microns results in the focuser moving a total of 300 microns.
        
        Example:
            The current position is 10000 microns.
            You want to move the focuser a further away. 
            MoveFocuserInc(100) would then move the focuser 100 microns to 10100 microns.
            
        
        Args:
            Increment to move focuser in the units of microns
            
        Returns:
            True when done with moving
            False if there is a timeout
            False if new target position is less than 0 microns.
            False if the new position is more than 5 microns from the target position. 
        """
        self.update()
        
        self.FocInc_target = self.FOC_pos + increment

        if self.FocInc_target < 0:
            print('The new target is less than 0 microns. The movement will NOT be executed')
            return False
        cmd = requests.get(self.link+"?&device=focuser&cmd=move&increment=%i"%(increment))
        print('Offsetting the focuser by %i microns' %(increment))
        timeout_sec = 25 #number of seconds before timeout
        timeout = time.time() + timeout_sec
        time.sleep(3)
        self.update()
        while self.FOC_moving == "true" and self.FOC_complete == 'false':
            print('Focuser moving, now at %s microns'%(self.FOC_pos))
            time.sleep(2)
            self.update()
            if time.time() > timeout:
                print('A timeout of %i seconds occured.'%(timeout_sec))
                return False
        self.update()
        if abs(self.FOC_pos - self.FocInc_target) < 5: #checks that the new position is within 5 micron of the target. 
            print('Focuser set at position: %s'%(self.Foc_pos))
            return True
        else:
            print('The focuser did not reach STOPthe target position. The current position is %s microns'%(self.Foc_pos))
            return False
    
    
    
    def FocSTOP(self):
        """
        Stopping the focuser's movement. 
        This functions works, along with the other stop-functions, on a separate thread. 
        This ensures the function can always be called, by another terminal with the client running, even if another function is currently being executed. 
        
        Returns:
            True when focuser has been stopped
            False when a timeout occurs.
        """
        print('Stopping the focuser - please wait')
        cmd = requests.get(self.link+"focuser/stop")
        timeout_sec = 20 #number of seconds before timeout
        timeout = time.time() + timeout_sec
        time.sleep(3)
        self.update()
        while self.FOC_moving == "true":
            print('Focuser is still moving, now at %s microns, please wait'%(self.FOC_pos))
            time.sleep(2)
            self.update()
            if time.time() > timeout:
                print('A timeout of %i seconds occured.'%(timeout_sec))
                return False
        print("The focuser has now stopped, at %s microns"%(self.FOC_pos))
        return True
    
    
        
    def FocFindHome(self):
        """
        A function that homes the focuser. The homing-procedure moves the focuser from the current position to 0 microns, 
        then stops and then move the focuser to 1000 microns. This procedure takes on the order of 1-2 minutes
        depending on the initial starting position. 
        
        Returns:
            True when the homing procedure is finished
            False if there is a timeout. 
        """
        print('Homing - please wait')
        print('The position of the focuser before moving is %s microns'%(self.FOC_pos))
        cmd = requests.get(self.link+"?&device=focuser&cmd=findhome")
        timeout_sec = 120 #nuber of seconds before timeoutting
        timeout = time.time() + timeout_sec
        time.sleep(2)
        self.update()
        while self.FOC_homing == "true" and self.FOC_moving == "true":
            print('The focuser is homing, currently at %s microns - please wait' %(self.FOC_pos))
            self.update()
            time.sleep(2)
            if time.time() > timeout:
                print('There has been a timeout of %i seconds.'%(timeout_sec))
                return False
            
        print('The focuser has finished homing and is at %s microns' %(self.FOC_pos))
        print('\n The focuser will now move to 1000 microns. \n')
        time.sleep(2)
        self.update()
        while self.FOC_moving == "true":
            print('The focuser is moving and is currently at %s microns - please wait'%(self.FOC_pos))
            self.update()
            time.sleep(2)
            if time.time() > timeout+60:
                print('There has been a timeout of %i seconds'%(60+timeout_sec))
                return False
        print('The focuser has stopped moving and is positioned at %s'%(self.FOC_pos))
        return True
        
    
    
        #This function starts the focuser's auto-focusing function. 
        #However this does not work, since the function needs MAXIM-DL in PWI2
    def FocAutofocus(self):
        print('The focuser will start autofocusing - please wait')
        
        cmd = requests.get(self.link+"?&device=focuser&cmd=startautofocus")
    
        return
            
        

    def ConnectMNT(self):
        """
        A function that connects PWI to the mount of the telescope and energizes 
        the motors (effectively turning them on). 
        Once the motors are energized, they CANNOT be moved by hand.  
        
        Returns:
            True when connected and motors are energized
            False if there is a timeout
        """
        
        self.update()
        if self.MNT_connection == "true" and self.MNT_AzmMotor == "true" and self.MNT_AltMotor == "true":
            print('The mount is already connected and energized.')
            return True
        cmd = requests.get(self.link+"mount/connect")
        self.update()
        time.sleep(1)
        timeout_sec = 15 #Number of seconds before timeoutting
        timeout = time.time() + timeout_sec
        while self.MNT_connection == "false":
            print('Trying to connect mount. Please wait')
            self.update()
            time.sleep(1)
            if time.time() > timeout:
                print('The connection timed-out after %i seconds'%(timeout_sec))
                return False
        print('Mount is connected. Energizing motors now - please wait')
        time.sleep(1)
        enableAzm = requests.get(self.link+"mount/enable/axis=0")
        enableAlt = requests.get(self.link+"mount/enable/axis=1")
        time.sleep(2)
        self.update()
        #I dont know if I can use the same timeout method here since it is in the same function?
        while self.MNT_AzmMotor == "false" and self.MNT_AltMotor == "false":
            print('Energizing motors - please wait')
            time.sleep(1)
            self.update()
            if time.time() > timeout + 30:
                print('There was a timeout during the energizing of the motors')
                return False
        print('Motors are energized! You can proceed.')
        return True


    def DisconnectMNT(self):
        """
        A function that disconnects the mount from PWI. The functions start by 
        de-energizing the motors and then disconnect the mount. 
        
        Returns:
            True when disconnection is finished.
            False if there is a timeout before disconnecting.
        """
        self.update()
        if self.MNT_connection == "false":
            print('The mount is already disconnected')
            return True
        disableAzm = requests.get(self.link+"mount/disable?axis=0")
        disableAlt = requests.get(self.link+"mount/disable?axis=1")
        time.sleep(2)
        cmd = requests.get(self.link+"mount/disconnect")
        self.update()
        time.sleep(2)
        timeout_sec = 15 #set the number of seconds before timeout
        timeout = time.time()+timeout_sec
        while self.MNT_connection == "true":
            print('Trying to disconnect mount. Please wait')
            self.update()
            time.sleep(2)
            if time.time() > timeout:
                print('A timeout of %i sec has occured.'%(timeout_sec))
                return False #stop if the timeout is reached!
        print('Mount disconnected!')
        return True



        #Prints the error on the amz motor. Ideally it would print the error in words or "if error# then run command" to fix the error
    def AZM_motor_error(self):
        """
        The function prints the error code of the Azimuth motor. 
        
        Per version 0.0.1, this function does not work as inteded. 
        The idea is that the function, based on the error code, displays the 
        problem in a human-readable text and a suggestion on what could fix the issue.
        
        Returns:
            The error code from PWI
        
        """
        self.update()
        Err = self.MNT_AzmMotorError
        if Err == "29056":
            print('The motor pulse is too high. You should reset the motors using the function: MNTresetMotors')
            return Err
        if Err == '0':
            print('No error')
            return Err
        else:
            print(Err)
        return Err

    def ALT_motor_error(self):
        """
        The function prints the error code of the Altitude motor. 
        
        Per version 0.0.1, this function does not work as inteded. 
        The idea is that the function, based on the error code, displays the 
        problem in a human-readable text and a suggestion on what could fix the issue.
        
        Returns:
            The error code from PWI4
        """
        self.update()
        Err = self.MNT_AltMotorError
        if Err == "29056":
            print('The motor pulse is too high. You should reset the motors using the function: MNTresetMotors')
            return
        if Err == '0':
            print('No error')
        else:
            print(Err)
        return Err


     
    def MntResetMotors(self):
        """
        The function reset the motors. It calls two functions: Firstly the function
        MntMotorDisable and then MntMotorEnable. The first function one de-energizes the motors, 
        while the second function energizes the motors. The mount motors have then been reset.
        
        Returns:
            True when resetting the mount is finished.
            False if the resetting does not succed.
        
        """
        print('Starting to reset mount motors')
        
        try:
            self.MntMotorDisable()
        except Exception as e:
            print(e)
        
        try:
            self.MntMotorEnable()
        except Exception as e:
            print(e)
        self.update()
        
        if self.MNT_AltMotor != "true" and self.MNT_AzmMotor != "true":
            print('There was an error in the resetting of the motors')
            return False
        
        return True


    def checkFormatRaDec(self,RA,DEC):
        """
        A function that checks the format of the input which is Right Ascension (RA) 
        and Declination (DEC) of a target. 
        
        
        The correct format for RA will be:
            HH:MM:SS.SS
        
        The correct format for DEC will be:
            DD:MM:SS.SS
        
        It is possible to parse a negative DEC. A correct example would be:
            -15:50:06.50
            
        Args:
            Right Ascension of target, Declination of target
        
        Returns:
            The number of errors in the format.
        """
        
        #Split up the input into 3 parts, not sure if this is a good idea to manually set it to max 3 parts. We'll see. 
        RA_hr,RA_mm,RA_ss = RA.split(":",2) 
        DEC_deg,DEC_mm,DEC_ss = DEC.split(":",2)
        print(RA_hr,RA_mm,RA_ss)
        print(DEC_deg,DEC_mm,DEC_ss)
        format_error = 0
        if len(RA_ss) == 5:
            if (RA_ss)[2] == ":":
                print('Input error for RA. There is a ":" between the seconds input.')
                print('This should be a "."')
                format_error += 1
        if len(DEC_ss) == 4:
            if (DEC_ss)[2] == ":":
                print('Input error for DEC. There is a ":" between the seconds input.')
                print('This should be a "."')
                format_error += 1        
        return format_error
        


    def checkFormatAltAzm(self, Alt,Azm):
        """
        A function that checks the format of the inputs which is the Altitude (Alt) 
        and Azimuth (Azm) of a target. 
        
        The unit of the inputs are in degrees.
        
        The functions makes sure that the Alt is above 0 and below 90 degrees and
        the Azm is between 0 degrees and 360 degrees. 
        
        Args:
            Altitude in degrees, Azimuth in degrees
            
        Returns:
            Number of errors in format. If #errors > 0, then there is an issue with the format.
        
        """
        
        
        error = 0
        if Alt > 90:
            print('Error:')
            print('Altitude is in degrees and should be below 90 degrees')
            error += 1
        if Alt < 0: 
            print('Error:')
            print('Altitude is in degrees and should above 0 degrees')
            error += 1
        if Azm > 360:
            print('Error:')
            print('Azimuth is in degrees and should be below 360 degrees')
            error += 1
        if Azm < 0:
            print('Error:')
            print('Azimuth is in degrees and should be above 0 degrees')
            error += 1
        
        return error
    


    def MntMoveRaDecJ2000(self):
        """
        A function that starts the observation of a target. The target coordinates
        are passed through the function "setTargetRaDecJ2000(Ra,Dec)". This means
        that the coordinates are first set with "setTargetRaDecJ2000(Ra,Dec)" and then
        this function is used to move the mount.
        
        The target coordinates are then checked for the format. If there are no errors, 
        the target is then checked if it on the night sky with the Observer at Mount Kent, Queensland Australia .
        
        Per version 0.0.1:
        The minimum elevation, called horizon_limit, above the horizon is set to 15 deg.
        *PLEASE NOTE*: if the minimum elevation is to be changed, it needs to be changed both in here 
        and in PWI under the variable "LOWER TRACKING LIMIT". 
        
        If target is above the minimum elevation, the mount will move to the target and track the target.
        
        The mount will stay on target until otherwise told or until the target moves below the horizon limit.

        Returns:
            True when on target
            False if there is a error in the format of RA or DEC
            False if the target is below the minimum elevation above the horizon.
            False if there is a timeout
        """
        self.update()
        #Load in the RA and DEC (in epoch J2000) from self
        RA = self.RAJ2000
        DEC = self.DECJ2000
        

        #################################################################################
        #This piece checks the format of the input is correct. The following
        #formats are accepted: HH:MM:SS.SS         
        format_err = self.checkFormatRaDec(RA,DEC)        
        if format_err != 0:
            print("Errors in input format. Tracking will NOT be started")
            return False
        
        
        ##################################################################################
        
        ##################################################################################
        #Now that the format is checked, the RA and DEC is sent to song_star_checker_AUTOTUNE.py (SSCA)
        #The SSCA script uses the ephem package to where on the sky the star is. 
        #The script then checks whether the coordinates are then correct. 
        # If they are correct, RA and DEC are then sent to SSCA to get the alt,azm
        # If alt is above horizon-limit, then it will proceed to track that target
        
        check = SSCA.coordinates.coordinate_check(self,RA,DEC)
        horizon_limit = 15 #the alt-limit in degrees for the telescope to track
        ###### PLEASE NOTE THAT PWI WILL TRACK THE TARGET TO THE LIMIT SET IN PWI2 (LOWER TRACKING LIMIT) 
        #I have now set it to 15 deg both here and in PWI, but if we want to change it in the future, we need to change it both places.
        if check == 0:
            star_init = SSCA.star_pos.__init__(self,site=3) #sets the site for Mt. Kent
            star_alt = SSCA.star_pos.star_alt(self,RA,DEC) #uses the SSCA script to get alt
            star_azm = SSCA.star_pos.star_az(self,RA,DEC) #uses the SSCA script to get azm
            #print('Star alt, star azm')
            #print(star_alt,star_azm)
            if (str(star_alt)[1:2]) == ':': #The return value of the altitude of the star, when the Alt is below 10, is i.e. 8 and not 08. The code crashed beforehand due to "8:" not being an integer
                if int(str(star_alt)[0:1]) > horizon_limit:
                    RA_dec = RAconverter_HHtoDec(RA)
                    print('RA in decimal is:')
                    print(RA_dec)
                    print('The target is above the horizon-limit of %i deg. The tracking will begin momentarily.'%(horizon_limit))
                    track = requests.get(self.link+"mount/goto_ra_dec_j2000?ra_hours=%s&dec_degs=%s"%(RA.replace(":","%20"),DEC.replace(":","%20")))
                    timeout_sec = 60 #number of seconds before timeout
                    timeout = time.time() + timeout_sec
                    time.sleep(3)   
                    while self.MNT_slewing == "true":
                        print('Not on target yet, please wait') 
                        time.sleep(2)                   
                        self.update()
                        if time.time() > timeout:
                            print('A timeout of %i seconds has occured'%(timeout_sec))
                            return False
                    print('The telescope is on target')
                elif int(str(star_alt)[0:1]) < horizon_limit:
                    print('The target is below the horizon-limit of %i deg'%(horizon_limit))
                    print('The tracking will NOT be started.')
                    return False
                
                
            elif (str(star_alt)[2:3]) == ':':    
                if int(str(star_alt)[0:2]) > horizon_limit:
                    RA_dec = RAconverter_HHtoDec(RA)
                    print('RA in decimal is:')
                    print(RA_dec)
                    print('The target is above the horizon-limit of %i deg. The tracking will begin momentarily.'%(horizon_limit))
                    track = requests.get(self.link+"mount/goto_ra_dec_j2000?ra_hours=%s&dec_degs=%s"%(RA.replace(":","%20"),DEC.replace(':','%20')))
                    timeout_sec = 60 #number of seconds before timeout
                    timeout = time.time() + timeout_sec
                    time.sleep(3)   
                    while self.MNT_slewing == "true":
                        print('Not on target yet, please wait') 
                        time.sleep(2)                   
                        self.update()
                        if time.time() > timeout:
                            print('A timeout of %i seconds has occured'%(timeout_sec))
                            return False
                    print('The telescope is on target')
                elif int(str(star_alt)[0:2]) < horizon_limit:
                    print('The target is below the horizon-limit of %i deg'%(horizon_limit))
                    print('The tracking will NOT be started.')
                    return False
        return True
 


    def stopTracking(self):
        """
        A function that stops the tracking of a target. 
        
        Returns:
            True when tracking has stopped.
            True if the mount has already stopped. 
            False if there is a timeout
            False if there is an unknown error
            
        
        """
        #self.update()
        #if self.MNT_tracking == "false":
        #    print('The mount has already stopped tracking')
        #    return True


        stop = requests.get(self.link+"mount/tracking_off")
        print('Stopping tracking request sent - please wait')
        self.update()
        timeout_sec = 20 #number of seconds before timeout
        timeout = time.time()+timeout_sec
        while self.MNT_tracking == "true":
            print('Trying to stop tracking - please wait')
            time.sleep(1)
            self.update()
            if time.time() > timeout:
                print('This session has timed-out after %i seconds' %timeout_sec)
                return False
        if self.MNT_tracking == "false":
            print('The tracking is OFF and the mount has stoppped.')
            time.sleep(3)
            self.update()
            print('The current position of the telescope is %g\xb0 %g\xb0 (Alt,Azm)'%(float(self.MNT_Alt),float(self.MNT_Azm)))
        else: 
            print('Something went wrong trying to stop the tracking')
            return False
        return True

    def parkMount(self):
        """
        A function that parks the mount to a parking position. The mount moves to the 
        parking position, tracks the position of the parking position for a very short amount of time
        and then stops tracking the parking position, thereby stopping the mount at the parking position. 
        
        The function uses "stopTracking" for stopping the tracking once the mount is on target.
        
        Per version 0.0.1:
            The parking position has been chosen to be 20 degrees (Alt), 180 degrees (Azm)
            To change the parking position, the two variables, park_alt and park_azm, 
            needs to be changed in this source code function. 
            
        Returns:
            True when parking the mount is done. 
            False if there was a timeout 
        
        """
        park_alt = 25 # the altitude in deg where the telescope will be parked 
        park_azm = 180 # the azimuth in deg where the telescope will be parked
        print('The mount will be parked to the position %i\xb0, %i\xb0 (Alt,Azm)'%(park_alt,park_azm))
        park = requests.get(self.link+"mount/goto_alt_az?alt_degs=%s&az_degs=%s"%(park_alt,park_azm))
        timeout_sec = 60 #number of sec before timeout
        timeout = time.time() + timeout_sec
        time.sleep(3)
        self.update()
        while self.MNT_slewing == "true":
            print('Mount still moving - please wait')
            time.sleep(2)
            self.update()
            if time.time() > timeout:
                print('The session has timed out after %i seconds' %(timeout_sec))
                return False
        time.sleep(2)
        self.stopTracking() #Stops the tracking of the parking point
        
        return True
        
   
    def MountSTOP(self):
        """
        This function stops all mount movements when sent to PWI. 
        Please note that this function is called by the daemon on a different server (server2)
        to make sure this stop function can be called even if other functions are running.
        Example: The mount is moving to a new target, but needs to be stopped.
        The "MountSTOP" command is sent, uses server2, which only checks for stop-functions, 
        and stops the mount.
        
        Returns:
            True when the mount is stopped. 
            False if there is a timeout.
        """
        if self.MNT_tracking == 'false':
            print('Tracking is already off. The stop command will still be executed!')
            #A good idea? Otherwise, if there is something wrong and you can't stop the mount because of the if-statement.

        cmd = requests.get(self.link+'mount/stop')
        timeout_sec = 15 #Number of seconds before timeout
        timeout = time.time()+timeout_sec
        while self.MNT_slewing == "true" and self.MNT_tracking == "true":
            print('Waiting for mount to stop - please wait')
            time.sleep(2)
            self.update()
            if time.time() > timeout:
                print('The session has timed-out after %i seconds'%(timeout_sec))
                return False
        print('The mount has stopped')
        return True

    def MntMotorEnable(self):
        """
        A function that energizes the mount motors (Alt and Azm). 
        Essentially turning the motors on.
        Once the motors are energized, they CANNOT be moved by hand.
        
        Returns:
            True when the motors are energized
            False if there is a timeout
        """
        print("Sending command to energize motors - please wait")
        cmdAzm = requests.get(self.link+"mount/enable?axis=0")
        cmdAlt = requests.get(self.link+"mount/enable?axis=1")
        time.sleep(1)
        self.update()
        timeout_sec = 10 #number of seconds before timing out
        timeout = time.time() + timeout_sec
        while self.MNT_AltMotor == "false" and self.MNT_AzmMotor == "false":
            self.update()
            print('Waiting for motors to energize - please wait')
            time.sleep(2)
            if time.time() > timeout:
                print("The session has timed out after %i seconds"%(timeout_sec))
                return False
        print('The motors have energized.')
        return True
        
    def MntMotorDisable(self):
        """
        A function that de-energizes the mount motors (Alt and Azm).
        Essentially turning the motors off. 
        Once the motors are de-energized, you'll be able to move the mount by hand - but please be careful in doing so. 
        
        Returns: 
            True when the motors are disabled
            False if there is a timeout
        """
        print('Sending command to de-energize motors - please wait')
        cmdAzm = requests.get(self.link+"mount/disable?axis=0")
        cmdAlt = requests.get(self.link+"mount/disable?axis=1")
        time.sleep(1)
        self.update()
        timeout_sec = 10 #number of seconds before timeout
        timeout = time.time() + timeout_sec
        while self.MNT_AltMotor == "true" and self.MNT_AzmMotor == "true":
            print("Trying to energize motors - please wait")
            time.sleep(1)
            self.update()
            if time.time() > timeout:
                print('The session has timed out after %i seconds'%(timeout_sec))
                return False
        print('The motors have been disabled.')
        return True
        
    def MntMoveIncRaDec(self,RA,DEC):
        """
        A function that moves the mount in increments given by the user, for 
        the movement in the Right Ascension and Declination (RA, DEC). 
        
        The increments add i.e. an increment of (5,10) and afterwards a new increment
        of (10,10) would result in a total movement of (15,20) in RA/Dec respectively.
        
        *PLEASE NOTE*: The inputs for RA and DEC increments are in arcseconds. 
        
        Args: 
            Increments in arcseconds for Right Ascension and Declination
        Returns:
            True when movement is done and the mount is on target and tracking.
            False if there is a timeout.
        """
        
        
        print('Moving the mount %i arcsec, %i arcsec (Ra,Dec) - please wait'%(RA,DEC))
        cmd = requests.get(self.link+"?&device=mount&cmd=move&incrementra=%.8f&incrementdec=%.8f"%(RA,DEC))
        timeout_sec = 15 #number of seconds before timing out. 
        timeout = time.time() + timeout_sec
        time.sleep(2)
        self.update()
        while self.MNT_on_target == "False":
            print('Still moving mount - please wait')
            time.sleep(1)
            self.update()
            if time.time() > timeout:
                print('The session timed out after %i seconds'%(timeout_sec))
                return False
        print('The movement is done. The telescope is now tracking.')
        return True
        
    
    def MntMoveIncAltAzm(self,Alt,Azm):
        """
        A function that moves the mount in increments in Altitude and Azimuth (Alt,Azm).
        The increments are given by the user with the unit of *arcseconds*. 
        
        It should be noted that the increments add meaning if you add (50,20) and 
        then add another (10,10), the total movement will be (60,30) in Alt and Azm respectively.
        
        Args:
            Increments to move the mount in Altitude and Azimuth in the units of arcseconds
            
        Returns:
           True when movement in done and mount is on target and tracking
           False if there is a timeout.
        """
        
        print('Moving the mount - please wait')
        cmd = requests.get(self.link+"?&device=mount&cmd=move&incrementazm=%.4f&incrementalt=%.4f"%(Azm,Alt))
        time.sleep(2)
        timeout_sec = 15 #number of seconds before timing out
        timeout = time.time() + timeout_sec
        while self.MNT_on_target == "False":
            print('Mount still moving - please wait')
            time.sleep(1)
            self.update()
            if time.time() > timeout:
                print('The session has timed out after %i seconds'%(timeout_sec))
                return False
        print('The movement is done. The tracking is on.')
        return True
    
    

    def MntMoveRaDec(self):
        """
        A function that moves the mount to the Right Ascension and Declination (RA and DEC). 
        The input is loaded in from the function "setTargetRaDec(Ra,Dec)" where the target
        coordinates are set. This means you first set the target coordinates with 
        "setTargetRaDec(Ra,Dec)" and then move the mount with this function.
            
        Returns:
            True when the movement is finished and the mount is on target and tracking.
            False if there is a timeout.
            False if there is an error in the format of the input
            False if the target is below horizon limit - which is set to 15 degrees above horizon per version 0.0.1 
        """
        
        self.update()
        RA = self.RA
        DEC = self.DEC
        
        print('Moving mount - please wait')
        check = self.checkFormatRaDec(RA,DEC)
        if check != 0:
            print('Error')
            print('There is an error in the format of the RA/DEC. Tracking will NOT be started.')
            return False
        
        star_init = SSCA.star_pos.__init__(self,site=3)
        star_alt = SSCA.star_pos.star_alt(self,RA,DEC)
        star_azm = SSCA.star_pos.star_az(self,RA,DEC)
        horizon_limit = 15 #tracking limit. IF CHANGED HERE, THEN ALSO CHANGE IN PWI!!!!!
        alt_degree,_,_ = str(star_alt).split(":")
        
        if int(alt_degree) > horizon_limit:
            print('Target is above horizon limit of %i degrees'%(horizon_limit))
            print('The tracking will start momentarily - please wait')
            cmd = requests.get(self.link+"mount/goto_ra_dec_apparent?ra_hours=%s&dec_degs=%s"%(RA.replace(":","%20"),DEC.replace(":","%20")))
            timeout_sec = 60 #number of seconds before timing out
            timeout = time.time() + timeout_sec
            time.sleep(2)
            self.update()
            while self.MNT_slewing == "true":
                print('Mount is still moving to target - please wait')
                time.sleep(2)
                self.update()
                if time.time() > timeout: 
                    print('The session has timed out after %i seconds' %(timeout_sec))
                    return False
            print('The telescope is on target and is tracking')
        
        elif int(alt_degree) < horizon_limit: 
            print('The target is below the horizon limit of %i degrees'%(horizon_limit))
            print('Tracking will NOT be started!')
            return False

        return True

        
    def MntMoveAltAzm(self):
        """
        A function to move to the mount to an Altitude and Azimuth which is 
        first set with the function "setTargetAltAzm(Alt,Azm)". This means
        you have to first set the Alt/Azm coordinates with "setTargetAltAzm(Alt,Azm)"
        and then use this function to move the mount.
        
        The input is first checked for format errors and if there are no errors,
        and the target altitude is above the horizon limit - which is set to 15 degrees above horizon per version 0.0.1 -
        gives the commmand to move the mount to the given coordinates. 
        
        Returns:
            True when the mount has finished the movement and is on target and tracking.
            False if there is an error in the format of the input
            False if the target is below the horizon limit.
        """
        self.update()
        #Loading in the altitude and azimuth
        Alt = self.Alt
        Azm = self.Azm
        
        #check function for Alt/azm
        errors = self.checkFormatAltAzm(Alt,Azm)
        if errors != 0:
            print('There was an error with the Alt/Azm format')
            print('The movement will NOT begin')
            return False
        horizon_limit = 15 #degrees above the horizon where the telescope cannot track below. SHOULD BE CHANGE ALSO IN PWI2 and in MntMoveRaDec and MntMoveRaDecJ2000
#        if Alt > 90:
#            print('The altitude must be lower than 90 deg. The mount will NOT be moved')
#            return False
        if Alt < horizon_limit:
            print('The altitude must be higher than %i degrees. The mount will NOT be moved'%(horizon_limit))
            return False

        
        print('Starting movement in a moment - please wait')
        print('Starting position is at %.4f\xb0 %.4f\xb0 (Alt/Azm)'%(float(self.MNT_Alt),float(self.MNT_Azm)))
        cmd = requests.get(self.link+"mount/goto_alt_az?alt_degs=%s&az_degs=%s"%(Alt,Azm))
        timeout_sec = 60 #number of seconds before timing out.
        timeout = time.time() + timeout_sec
        time.sleep(2)
        self.update()
        while self.MNT_slewing == "true":
            print('Still moving the mount - please wait')
            self.update()
            time.sleep(2)
            if time.time() > timeout:
                print('This session has timedout after %i seconds'%(timeout_sec))
                print('The position at timeout was Alt: %s and Azm: %s'%(float(self.MNT_Alt),float(self.MNT_Azm)))
                return False
        print('The mount is on target and is tracking at %.3f\xb0,%.3f\xb0 (Alt/Azm)'%(float(self.MNT_Alt),float(self.MNT_Azm)))
        return True
        
    def startTracking(self):
        """
        A function that starts the tracking. The mount will track the current position on the sky. 
        
        Returns:
            True when tracking is on.
            False if there is a timeout.
        """
        print('Starting tracking - please wait')
        
        cmd = requests.get(self.link+"mount/tracking_on")
        
        timeout_sec = 15 # number of seconds before timing out
        timeout = time.time() + timeout_sec
        time.sleep(1)
        self.update()
        while self.MNT_tracking == "False":
            print('Not tracking yet - please wait')
            time.sleep(2)
            self.update()
            if time.time() > timeout: 
                print('The session has timed out after %i seconds'%(timeout_sec))
                return False
        print('Tracking is now on')
        return True
        
    
    def LoadPointingModel(self,filename):
        """
        This function loads in a pointing model from Documents/PlaneWave Instruments/PWI2/Mount/
        The filename has some restrictions:
            1. only alphanumeric characters, underscore and hyphen
            2. must end in ".pxp"
            3. Must be in the path "Documents/PlaneWave Instruments/PWI2/Mount" on the computer
        Example of command:
            LoadPointingModel('Model1.pxp')
            
        Args:
            Filename of pointing model you want to import
        Returns:
            True when pointing model is loaded.
            False if name of new pointing model does not correspond to the filename.            
        """
        
        
        name, filetype = filename.split('.')
        if filetype != "pxp":
            print('Error')
            print('The filetype must be .pxp!')
            return
        cmd = requests.get(self.link+"?&device=mount&cmd=setmodel&filename=%s"%(filename))
        time.sleep(2)
        self.update()
        if self.MNT_PointingModel == filename:
            print('The poiting model %s has been loaded successfully.'%(filename))
            return True
        else:
            print('There was an error loading in the pointing model.')
            return False



       
    def setTrackingRates(self,RArate,DECrate):
        """
        A function that sets the tracking rates, expressed as an offset to the standard sidereal rate. 
        If both inputs are 0, the tracking will be at the sidereal rate. 
        The units for the RArate and DECrate is arcseconds per sec.
        """
        
        cmd = requests.get(self.link+"?&device=mount&cmd=trackingrates&rarate=%.2f&decrate=%.2f"%(RArate,DECrate))
        
        return cmd
        

        #NOT DONE YET!


    def checkFormatArcsec(self,Arcsec):
        """
        A function that checks the format of arcseconds. 
        Per version 0.0.1, the function simply checks whether the input is above 
        60 or below 0. This may be changed in future versions.
        
        Args:
            Arcsecond
        Returns:
            Number of errors in the format.
        """
        
        print('Checking format - please wait')
        error = 0 #number of errors:
        if float(Arcsec) > 60.0:
            print('Error:')
            print('The number of arc seconds need to be below 60')
            error += 1
        if float(Arcsec) < 0.0:
            print('Error:')
            print('The number of arc seconds should be above 0')
            error +=1
        return error


        #Function that starts the homing procedure for the mount. 
        #At the moment (14/11/2019) DOES NOT WORK! Crashes the simulator, azm deg goes to 24000074 degs
    def startMntHoming(self):
        """
        A function that starts the homing procedure in PWI2 for the mount. 
        *PLEASE NOTE*: Per version 0.0.1 this function crashes the simulator and
        has not been tested on a real telescope. It is therefor suggested to be very careful when
        using this function
        
        Returns:
            Per version 0.0.1: Nothing.
        """
        print('Starting homing of the mount - please wait')
        cmd = requests.get(self.link+'mount/find_home')
        return cmd

    
        #a function that moves in the mount in alt/azi, like the arrow-keys in PWI. 
        #As of 14/11/2019, it does not work as intended. It moves way to fast and does not stop. 
        #So it eventually crashes the engines by hitting the alt/azm limits.
    def JogAltAzm(self,Alt,Azm):
        """
        A function that moves the mount of the telescope like the arrow-keys in PWI.
        *PLEASE NOTE*: Per version 0.0.1, this function is not working properly since
        it keeps moving instead of stopping after a short amount of time. 
        
        Args:
            The rate of change in Altitude and Azm 
        Returns:
            Per version 0.0.1: The http value of the sent command.
        """
        cmd = requests.get(self.link+"?&device=mount&cmd=jog&axis1rate=%.2f&axis2rate=%.2f"%(Azm,Alt))
        
        return cmd


        
    def SyncMountCoorJ2000(self,RA,DEC):
        """
        A function that synchronizes the mount coordinate system, so that the current telescope location corresponds
        to the given RA, DEC (in J2000 epoch). This should offset the entire telescope coordinate system to make the 
        reported coordinates at the current location match the provided coordinates
        Documentation says that this is typically done when starting to build a new pointing model.
        Per 14/11/2019 (version 0.0.1) it does not work. It happens to move the altitude of the telescope 
        to -78 (yes negative) degrees when using it with the simulator.
        Therefor I commented out the cmd, such that the function does not send out a command to synchronize the coordinate system.
        """
        errors = self.checkFormatRaDec(RA,DEC)
        if errors != 0:
            print('There was an error in the format of Ra/Dec.')
            print('The command will NOT be executed.')
            return
        #cmd = requests.get(self.link+"?&device=mount&cmd=sync&ra2000=%s&dec2000=%s"%(RA.replace(":"," "),DEC.replace(":"," ")))
        
        return



    def AddPointToModel(self,RA,DEC):
        """
        A function that adds a point/target to current pointing model. It assigns the current telescope position (RA,DEC) to the input provided by 
        the user - which is also a RA and DEC in J2000 epoch. The input is checked for format errors before adding point to pointing model.
        The telescope start tracking when this command is executed.
        
        Example of command:
            AddPointToModel("04:35:55.33","16:30:29.5") #Aldebaran's J2000.0 coordinates.

        Args:
            RA and DEC in J2000 epoch to add to the current pointing model
        Returns:
            True when point is added to the pointing model
            False if there is a format error in the input
            False if there is a timeout
        """
        
        
        print('Adding point to model - please wait')
        check = self.checkFormatRaDec(RA,DEC)
        if check != 0:
            print('There was an error in the format of RA/DEC')
            print('No point will be added to the pointing model')
            return False

        cmd = requests.get(self.link+"mount/model/add_point?ra_j2000_hours=%s&dec_j2000_degs=%s"%(RA.replace(":","%20"),DEC.replace(":","%20")))
        timeout_sec = 30 #number of seconds before timing out the session. 
        timeout = time.time() + timeout_sec
        time.sleep(1)
        self.update()
        while self.MNT_slewing == "true":
            print('Not on target yet - please wait')
            time.sleep(1)
            self.update()
            if time.time() > timeout:
                print('The session has timed out after %i seconds'%(timeout_sec))
                return False
        print('The point at %s, %s (RA,DEC) has been added to the current pointing model'%(RA,DEC))
        return True
    

    
      
    def SavePointingModel(self,filename):
        """
        The function saves the current pointing model, using the name provided by the user. 
        The pointing model is saved in "Docuements/PlaneWave Instruments/PWI2/Mount" on the local computer.
        The filename must be alphanumeric, but can also contain hyphen, "-", and underscore "_".
    
        Example of command: .SavePointingModel("Feb_model")
        
        Args:
            The filename under which the pointing model is saved.
        Returns:
            True when the pointing model is saved
            False if the filename is not alphanumeric.
        """
        copy = filename
        copy = copy.replace("-","")
        copy = copy.replace("_","")
        check = copy.isalnum()

        if check == False:
            print('Error:')
            print('The filename contains other characters than alphanumeric, "-" and "_".')
            print('The model will not be saved.')
            return False
        
        print('The pointing model will be saved as %s.pxp momentarily - please wait.' %(filename))
        cmd = requests.get(self.link+"?&device=mount&cmd=savemodel&filename=%s.pxp"%(filename))
        print('Model saved. Location: Documents/PlaneWave Instruments/PWI2/Mount')
        
        return True
    
    
    def ClearPointingModel(self):
        """
        This function deletes ALL the points in the current pointing model. 
        PLEASE BE CAREFUL WHEN USING THIS!

        Returns:
            True when points have been deleted
            False if the timeout session runs out. 
        """
        # while True:
        #     try:
        #         response = input("Do you want to delete all points of the current pointing model? [y/n]")
        #         if response == "y" or response == "Y" or response == "yes":
        #             pass
        #         if response == "n" or response =="N" or response == "no":
        #             break
        #         else:
        #             print("Invalid response")
        #             break
        #     except EOFError:
        #         return
        

        self.update()
        cmd = requests.get(self.link+"mount/model/clear_points")
        self.update()
        time.sleep(1)
        timeout_sec = 10
        timeout = time.time() + timeout_sec
        while self.MNT_PointingModelPoints != "0":
            print('Waiting for points to clear')
            time.sleep(2)
            self.update()
            if time.time() > timeout:
                print('This session has timed out after %i seconds'%(timeout_sec))
                return False
        print('The pointing model has been cleared')
        return True




    def FansON(self):
        """
        A function that turns the fans on in the telescope. 
        Firstly checks if the fans are already on. If not, then turns on fans.
        
        Returns: 
            True when fans are turned on.
            True if fans are already on.
            False if there is a timeout
        """
        self.update()
        if self.FANS_state == 'True':
            print('The fans are already on')
            return True
        else:
            cmd = requests.get(self.link+'?&device=fans&cmd=turnon')
            timeout_sec = 15 #number of seconds before timeout
            timeout = time.time() + timeout_sec
            while self.FANS_state == "False":
                print('Waiting for fans to turn on - please wait')
                time.sleep(3)
                self.update()
                if time.time() > timeout:
                    print('The session has timed out after %i seconds'%(timeout_sec))
                    return False
        print('The fans are turned on')
        return True

    def FansOFF(self):
        """
        A function that turns off the fans in the telescope. 
        If the fans are already off, then nothing happens. 
        Are the fans on, then a command is sent to turn the fans off.
        
        Returns: 
            True when fans are turned off.
            True if fans are already off
            False is there is a timeout
        
        """
        self.update()
        if self.FANS_state == 'False':
            print('The fans are already off.')
            return True
        else:
            cmd = requests.get(self.link+'?&device=fans&cmd=turnoff')
            timeout_sec = 15 #Number of seconds before timeout
            timeout = time.time() + timeout_sec
            while self.FANS_state == "True":
                print('Waiting for fans to turn off - please wait')
                time.sleep(2)
                self.update()
                if time.time() > timeout:
                    print('The session has timed out after %i seconds'%(timeout_sec))
                    return False
            print('The fans are turned off')
            return True
    

        #This function turns the rotator a number of degrees set by the input "position"
    def Rot_Move(self,position):
        """
        A function that moves the rotator. The user provides the new position 
        in degrees, between 360 degrees and 0 degrees. 
        
        Args:
            Position to run rotator to. Must be between 0 and 360 degrees.
            
        Returns: 
            True when the rotator has finished moving.
            False if the new position is above 360 degrees or below 0 degrees.
            False if there is a timeout
        """
        if position > 360:
            print('The new position needs to be below 360 degrees.')
            return False
        
        if position < 0: 
            print('The new position needs to be above 0 degrees.')
            return False
        
        print('The rotator will start moving momentarily - please wait')
        
        cmd = requests.get(self.link+"?&device=rotator&cmd=move&position=%i"%(position))
        time.sleep(2)
        self.update()
        timeout_sec = 180 #number of seconds before time-outting
        timeout = time.time() + timeout_sec
        while self.ROT_moving == "True":
            self.update()
            print('The rotator is moving, current position is %s deg - please wait'%(self.ROT_position))
            time.sleep(5)
            if time.time() > timeout:
                print('There has been a timeout of %s seconds'%(timeout_sec))
                print('The rotator position at timeout was %s deg'%(self.ROT_position))
                return False
        print('The rotator has stopped and is at %s deg'%(self.ROT_position))
        
        return True

        #A function to move the rotator in increments in units of degrees.
    def Rot_MoveInc(self,increment):
        """
        A function that moves the rotator in increment in units of degrees. The user provides the argument 
        of the increment. Example could be to move the rotator +15 degrees: Rot_MoveInc(15)
        The function then checks if the increment is larger than 360 degrees 
        or smaller than -360 degrees - if this is the case, the movement will not happen. 
        If the new increment + the current position is more than 360 degrees, then no movement
        will happen either. 
        
        The increments add up i.e. adding another 10 deg in increments after adding 10 deg results in the rotator
        moving 20 deg all in all.
        
        Args:
            Increment to move the rotator in degrees.
        
        Returns: 
            True when the movement is done 
            False if the increment is larger than 360 degrees
            False if the increment is smaller than -360 degrees
            False if the current position + the increment is more than 360 degrees.
            False if there is a timeout
        """
        self.update()


        if increment > 360:
            print('The increment is larger than 360 deg. The movement will NOT be executed.')
            return False
        
        if increment < 0:
            print('The increment is less than 0 deg. The movement will NOT be executed.')
            return False
        
        if increment + float(self.ROT_position) > 360:
            print('The rotator cannot move above 360 deg. The movement will NOT be executed')
            return False
        
        
        print('The rotator will start moving shortly - please wait')
        cmd = requests.get(self.link+"?&device=rotator&cmd=move&increment=%.2f"%(increment))
        
        time.sleep(1)
        timeout_sec = 60 #Number of seconds before time out
        timeout = time.time() + timeout_sec
        self.update()
        while self.ROT_moving == "True":
            print('The rotator is moving and is currently at %s deg - please wait'%(self.ROT_position))
            time.sleep(1.5)
            self.update()
            if time.time() > timeout:
                print('The session has timed out after %i seconds.'%(timeout_sec))
                print('The rotator position at timeout was %s degrees'%(self.ROT_position))
                return False
        self.update()
        print('The rotator has stopped moving and is at %s degrees'%(self.ROT_position))
        
        return True
        
        
    
    def RotSTOP(self):
        """
        A function that stops all rotator movement. 
        
        Returns:
            True when the rotator has stopped. 
            False if there is a timeout
        """
        print('Trying to stop the rotator - please wait')
        
        cmd = requests.get(self.link+"rotator/stop")
        time.sleep(1)
        self.update()
        timeout_sec = 15 #number of seconds before timeout
        timeout = time.time() + timeout_sec
        while self.ROT_moving == "true":
            print('The rotator is still moving - please wait')
            time.sleep(2)
            self.update()
            if time.time() > timeout:
                print('The session has timed out after %i seconds'%(timeout_sec))
                return False
        print('The rotator has stopped')
        return True
    
    
    def Rot_StartHoming(self):
        """
        A function that starts the rotator homing procedure. 
        
        Returns:
            True when the homing procedure is finished.
            False if there is a timeout.
        """
        print('The rotator will start homing - please wait')
        
        cmd = requests.get(self.link+"?&device=rotator&cmd=findhome")
        
        timeout_sec = 420 #number of seconds, 7 minutes
        timeout = time.time() + timeout_sec
        time.sleep(2)
        self.update()
        while self.ROT_homing == "True":
            self.update()
            print('Rotator is homing, currently at %s deg - please wait'%(self.ROT_position))
            time.sleep(2)
            if time.time() > timeout:
                print('The session has timed out after %i seconds.'%(timeout_sec))
                print('The rotator position at timeout was %s deg'%(self.ROT_position))
                return False
        time.sleep(5)
        self.update()
        print('The rotator has finished homing - current position is %s deg' %(self.ROT_position))
        
        return True
    
    def Rot_derotateStart(self):
        """
        A function that enables de-rotation on the Alt-Azm mount.
        
        Returns:
            True when the de-rotation is enabled.
            False if there is a timeout.
        """
        print('Enabling Alt-Azm field de-rotation - please wait')
        cmd = requests.get(self.link+"?&device=rotator&cmd=derotatestart")
        timeout_sec = 10 #number of seconds before time-out
        timeout = time.time()+ timeout_sec
        self.update()
        while self.ROT_AltAzDerotate == "False":
            self.update()
            print('Derotation not enabled yet - please wait')
            time.sleep(1)
            if time.time() > timeout:
                print("The session has timedout after %i seconds"%(timeout_sec))
                return False
        print('Alt-Azm field de-rotation has been enabled.')
        return True
    
    
    def Rot_derotateStop(self):
        """
        A function that disables de-rotation on the Alt-Azm mount.
        
        Returns:
            True when the de-rotation is disabled. 
            False if there is a timeout.
        """
        print('Disabling Alt-Azm field de-rotation - please wait')
        cmd = requests.get(self.link+"?&device=rotator&cmd=derotatestop")
        timeout_sec = 10 #number of seconds before timing out
        timeout = time.time() + timeout_sec
        self.update()
        while self.ROT_AltAzDerotate == "True":
            print('Trying to disable Alt-Azm field de-rotation - please wait')
            self.update()
            time.sleep(1)
            if time.time() > timeout:
                print('The session timed out after %i seconds'%(timeout_sec))
                return False
        print('The Alt-Azm de-rotation has been disabled')
        return True
    
    def getRotatorDerotate(self):
        """
        The function displays the current state of the derotate on the Alt/Azm mount.
        
        Returns:
            A message of whether the deratote is ON or OFF
            False is there was an error
        """
        
        self.update()
        if self.ROT_AltAzDerotate == "True":
            print('The Alt/Azm derotate is ON')
            reply = "The Alt/Azm derotate is ON"
            return reply
        
        if self.ROT_AltAzDerotate == "False":
            print('The Alt/Azm derotate is OFF')
            reply = "The Alt/Azm deratote is OFF"
            return reply
        else:
            print('There was an error')
            return False
            

    def setTargetRaDecJ2000(self,RA,DEC):#,RA_pm, DEC_pm):
        """
        A function to set coordinates for target in the J2000 Epoch. 
        The function MntMoveRaDecJ2000() can then take the values from self and 
        move the mount to the target. 
        
        Args:
            Right Ascension and Declination for target in J2000 Epoch in a string.
            Format should be:
                DD:MM:SS.SS
                HH:MM:SS.SS
            Proper motion for Right Ascension and Declication in milli arcsecond (mas) per year, each in a string.
        
        
        
        Example:
            setTargetRaDecJ2000("04:35:55.33","16:30:29.5",63.45, -188.94) #Aldebaran used for example
        
        Returns:
            True if the coordinates are set in self.
            True if the coordinates are already set in self.
            False if there was an error setting the coordinates.
        """
        #Check if the coordinates are already set
        try:
            if self.RAJ2000 == RA or self.DECJ2000 == DEC:
                print('The new coordinates are already set')
                return True
        except Exception as e:
            print(e)
    
        
        #save the new coordinates in self
        self.RAJ2000 = RA
        self.DECJ2000 = DEC

        ######################################################### proper motion stuff - can easily be commented out this way. 
        

        # #calculating the proper motion into RA and DEC. 
        # start_date = datetime.datetime(2000,1,1,0,0) #UTC time at the start of J2000.0 epoch
        # end_date = datetime.datetime.utcnow()
        # difference = end_date - start_date #The difference between now and J2000.0 start.
        # difference_yr = (difference.days + difference.seconds/86400.)/365.2425 #The difference in years between now and J2000.0 epoch.

        # #calculating the proper motion into Right Ascension and Declination
        # RA_pm * difference_yr *(1000) #now in arcseconds
        # DEC_pm * difference_yr *(1000) #now in arcseconds

        
        
        # #saves the proper motion in self
        # self.RAJ2000_pm = RA_pm
        # self.DECJ2000_pm = DEC_pm

        # if self.RAJ2000_pm !=RA_pm or self.DECJ2000_pm != DEC_pm:
        #     print('There was an error setting the proper motion')
        #     return False
        # ##############################################################

       
        #check if they are set correctly
        if self.RAJ2000 != RA or self.DECJ2000 != DEC:
            print('There was an error setting RA/DEC')
            return False
        

        print('The new coordinates have been set')
        return True
    
    def setTargetAltAzm(self,Alt,Azm):
        """
        A function that sets the target coordinates for the Alt/Azm target.
        This function is used together with MntMoveAltAzm(), where the user
        first sets the coordinates with this function and then moves the 
        telescope with MntMoveAltAzm().
        
        The coordinates are set in self.
        
        Args:
            Altitude and Azimuth of the target as integers.
            
        Returns:
            True if the target coordinates are set correctly
            True if the new coordinates match the coordinates already set in self.
            False if there was an issue setting the coordinates
            
        """
        self.update()
        #Check if coordinates are already set
        try:
            if self.Alt == Alt and self.Azm == Azm:
                print('The new coordinates is already set')
                return True
        except Exception as e:
            print(e)
        
        #Set coordinates in self
        self.Alt = Alt
        self.Azm = Azm
        
        #check if they are corretly set in self
        if self.Alt != Alt or self.Azm != Azm:
            print('There was an error setting the new coordinates')
            return False
        
        print('The new Alt/Azm coordinates have been set')
        return True
    
    def setTargetRaDec(self,Ra,Dec):
        """
        A function that set the coordinates for the target in topocentric 
        coordinates. 
        
        Args:
            Right Ascension and Declination in topocentric coordinates
            
            Format should be:
                DD:MM:SS.SS
                HH:MM:SS.SS
            Example:
                setTargetRaDec("11:32:59.79","-31:51:28.1")    
                
        Returns:
            True if the coordinates are set correctly.
            True if the new coordinates match the existing coordinates.
            False if there was an error setting the coordinates.
        
        """
        self.update()
        
        try:
            if self.RA == Ra or self.DEC == Dec:
                print('The new coordinates are already set')
                return True
        except Exception as e:
            print(e)
        
        self.RA = Ra
        self.DEC = Dec
        
        if self.RA != Ra or self.DEC != Dec:
            print('There was an error setting the new coordinates')
            return False
        print('The new coordinates have been set')
        return True
        

    
################################################################################

PW = PWI4()
####################### WORKS ##########

#### Functions that are for information

#PW.getALL()
#PW.getRA2000()
#PW.getDEC2000()
#PW.getJD()
#PW.getUTC()
#PW.getMNT_CONNECT()
#PW.getStatus()
#PW.getFocuser_CONNECT()
#PW.getROT_CONNECT()
#PW.getIsTrackingOn()
#PW.getTemps()



##### Function that are for setting a new value or doing something actively

#PW.ConnectMNT()
#PW.DisconnectMNT()
#PW.MountSTOP()
#PW.parkMount()
#PW.MntResetMotors()
#PW.MntMotorEnable()
#PW.MntMotorDisable()



#PW.ConnectFOC()
#PW.DisconnectFOC()
#PW.MoveFocuserPos(10000) #Try-except in update!
#PW.MoveFocInc(50)
#PW.FocFindHome()
#PW.FocSTOP() 



#PW.Rot_Move(170)
#PW.Rot_derotateStart()
#PW.Rot_derotateStop()
#PW.Rot_StartHoming()
#PW.Rot_stop()

#PW.FansON()
#PW.FansOFF()

#PW.stopTracking()
#PW.startTracking()

#PW.setTargetAltAzm(30,30) 
#PW.setTargetRaDec("","")
#PW.setTargetRaDecJ2000("","")


#PW.MntMoveRaDecJ2000()) 
#PW.MntMoveRaDEC() 
#PW.MntMoveAltAzm() 
#PW.MntMoveIncRaDec(10,10) 
#PW.MntMoveIncAltAzm(5,5) 

#PW.checkFormatRaDec("20:25:38.99","-56:44:07.7")
#PW.checkFormatAltAzm(90.0,340)

#PW.LoadPointingModel("test.pxp")
#PW.AddPointToModel("03:47:14.86","-74:14:18.9") #Works but not quite sure what to do with it




################# TESTING AREA / DOESNT WORK (at least the way I want it to work) ########################


#PW.AZM_motor_error() #Needs to give the correct error in words (and number) to the user
#PW.ALT_motor_error() #Needs to give the correct error in words and numbers to the end user

#PW.FocAutofocus()

#PW.MntMoveRaDec("19:11:00","-22:19:05") #A lot of work needed for this to work, compared to the usage of the function. See entry 8/11/2019 in logbook for more on this.

#PW.LoadPointingModel("stupid.pxp") #Needs to be tested with a pointing model file with a while/if loop to check that the pointingmodel has changed.

#PW.setTrackingRates(3,3) #Needs a lot of work, not done at all.
#PW.checkFormatArcsec() #Need some work, not done at all.



#PW.startMntHoming() #Crashes the simulator at search 7 in Azm. Not sure why, but the Azm value in the simulator goes to 240000074 (deg) so something is clearly wrong.

#PW.JogAltAzm(0.001,0) #Crashes the motor by moving very fast. The lowest value that produces a response in PWI is 0.01 deg/s and that crashes the motors (sends the telescope moving very fast
                        #I can't give it a lower value, or no response from PWI in those cases. So I am not sure what to do with this function. Giving a velocity also seems weird, given 
                        # I don't give an end-time. So do the function just give it a constant velocity and it will move at that speed until crash? 
                        # That is not how the arrows in PWI work. 
                        
                        
                        
#PW.SyncMountCoorJ2000("02:50:28.24","-75:04:00.9") #Does not work, crashes with an altitude of -78 deg. 
                        
#PW.SavePointingModel("Test_hyphen-underscore") #Not fully working yet, check for alphanumeric (with hyphen and underscore) but does not currently save the pointing model


