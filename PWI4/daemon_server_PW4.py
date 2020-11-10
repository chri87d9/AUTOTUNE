"""
   Author: Mads Fredslund Andersen and Hasse Hansen.
   Mail: madsfa@phys.au.dk and hasse302@hotmail.com
"""


from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import time
import psycopg2
import os
import sys
from song_daemonize_AUTOTUNE import Daemon
import getopt
import xmlrpc.client  
import PW4 as PW
import _thread
import PWI4_config as conf



class RequestHandler(SimpleXMLRPCRequestHandler):
	"""Some XMLPRC-magic here. This is needed, and cannot be left out. Check the documentation?"""
	rpc_paths = ('/RPC2')

    #A function to stop the server
def stop_server():
	global RUNNING
	RUNNING = False
	return "Now stopping the daemon..."

class commander(Daemon):
    """
    This is the daemon that runs my script from PW_Class.py for operating the telescope.
    
    The first part is setting up the servers in which the daemon runs. 
    Please note that there are two server set up. The server named "server" takes operational functions, 
    while the server named "server2" takes only stop functions. The splitting up of the servers was done
    such that it was always possible to call a stop function. Some of the functions called by "server"
    run in a while-loop, resulting in the user not being able to use the stop functions. With the use 
    of 2 servers, this is now solved.
    
    After the setup, all the functions are defined and the registered to their respective servers. 
    When the functions are registered, then the threading is done to make sure the two servers run of
    their own thread. 
    
    At the bottom is the main function that starts the daemon and runs the server. 
    
    """

    def run(self):
        global RUNNING
        RUNNING = True
         
       ### server handling all other functions than stop functions.
        try:
            server = SimpleXMLRPCServer((conf.NOVO_daemon_host, conf.NOVO_daemon_port1), requestHandler=RequestHandler, logRequests=False,allow_none=True)
            server.allow_reuse_address = True
        except Exception as e:
            print('error: ',e)
            
            
        ### server handling the stop functions. This is to being able to send stop commands while the "while-loops" are running.
        try:
            server2 = SimpleXMLRPCServer((conf.NOVO_daemon_host, conf.NOVO_daemon_port2),requestHandler=RequestHandler,logRequests=False,allow_none=True)
            server2.allow_reuse_address = True
        except Exception as e:
            print('error:',e)

        ## Setup database connection
        try:
            #conn = psycopg2.connect("dbname=" + conf.dbname + " user=" + conf.dbuser)
            print("dbname=" + conf.dbname + " user=" + conf.dbuser)
        except Exception as e:
            print('error:',e)
            
        ###################################################
        #Setting a handle for the PWI2-class in PW_Class.py. 
        #This makes it possible for the server to call the correct functions in PWI2
        
        PWI=PW.PWI4()

        
        ###################################################
        # I define all the functions in PWI as a new function that the server can call them
        
        def Initialize():
            PWI.__init__()
            return
        
        def ConnectMNT():
            cmd = PWI.ConnectMNT()
            return cmd
        
        def ConnectFOC():
            cmd = PWI.ConnectFOC()
            return cmd
    
        def DisconnectFOC():
            cmd = PWI.DisconnectFOC()
            return cmd
        
        def DisconnectMNT():
            cmd = PWI.DisconnectMNT()
            return cmd
        
        def getStatus():
            cmd = PWI.getStatus()
            return cmd
       
        def setTargetRaDecJ2000(RA,DEC):
            cmd = PWI.setTargetRaDecJ2000(RA,DEC)
            return cmd
        
        def setTargetAltAzm(Alt,Azm):
            cmd = PWI.setTargetAltAzm(Alt,Azm)
            return cmd
        
        def setTargetRaDec(RA,DEC):
            cmd = PWI.setTargetRaDec(RA,DEC)
            return cmd
        
        def MntMoveRaDecJ2000():
            cmd = PWI.MntMoveRaDecJ2000()
            return cmd
        
        def update():
            reply = PWI.update()
            return reply
        
        def getALL():
            reply = PWI.getALL()
            return reply
        
        def getRA2000():
            reply = PWI.getRA2000()
            return reply
        
        def getDEC2000():
            reply = PWI.getDEC2000()
            return reply
    
        
        def getFocuserPos():
            reply = PWI.getFocuserPos()
            return reply
        
        def getMNT_CONNECT():
            reply = PWI.getMNT_CONNECT()
            return reply
        
        def getFOC_CONNECT():
            reply = PWI.getFOC_CONNECT()
            return reply
        
        def getROT_CONNECT():
            reply = PWI.getROT_CONNECT()
            return reply
        
        def getIsTrackingOn():
            reply = PWI.getIsTrackingOn()
            return reply
        
        def getTemps():
            reply = PWI.getTemps()
            return reply
        
        def getRotatorDerotate():
            reply = PWI.getRotatorDerotate()
            return reply
        
        def MoveFocuserPos(position):
            reply = PWI.MoveFocuserPos(position)
            return reply
        
        def FocSTOP():
            reply = PWI.FocSTOP()
            return reply
        
        def MntMotorReset():
            reply = PWI.MntMotorReset()
            return reply 
        
        def checkFormatRaDec(Ra,Dec):
            PWI.checkFormatRaDec(Ra,Dec)
            return
        
        def checkFormatAltAzm(Alt,Azm):
            PWI.checkFormatAltAzm(Alt,Azm)
            return
        
        def checkFormatArcsec(Arcsec):
            PWI.checkFormatArcsec(Arcsec)
            return
        
        def stopTracking():
            reply = PWI.stopTracking()
            return reply
        
        def parkMount():
            reply = PWI.parkMount()
            return reply
        
        def getRotatorPos():
            reply = PWI.getRotatorPos()
            return reply
        
        def MountSTOP():
            reply = PWI.MountSTOP()
            return reply
        
        def MntMotorEnable():
            reply = PWI.MntMotorEnable()
            return reply
        
        def MntMotorDisable():
            reply = PWI.MntMotorDisable()
            return reply
        
        def MntMoveRaDec():
            reply = PWI.MntMoveRaDec()
            return reply 
        
        def MntMoveAltAzm():
            reply = PWI.MntMoveAltAzm()
            return reply 
        
        def startTracking():
            reply = PWI.startTracking()
            return reply
        
        def LoadPointingModel(filename):
            reply = PWI.LoadPointingModel(filename)
            return reply
              
        def AddPointToModel(Ra,Dec):
            cmd = PWI.AddPointToModel(Ra,Dec)
            return cmd
        
        def SavePointingModel(filename):
            cmd = PWI.SavePointingModel(filename)
            return cmd
        
        def ClearPointingModel():
            reply = PWI.ClearPointingModel()
            return reply
        
        def FansON():
            reply = PWI.FansON()
            return reply
        
        def FansOFF():
            reply = PWI.FansOFF()
            return reply
        
        def Rot_Move(position):
            reply = PWI.Rot_Move(position)
            return reply
        
        def RotSTOP():
            reply = PWI.RotSTOP()
            return reply
        
        def Rot_derotateStart():
            reply = PWI.Rot_derotateStart()
            return reply
        
        def Rot_derotateStop():
            reply = PWI.Rot_derotateStop()
            return reply

        def getTrackingRMSError():
            reply = PWI.getTrackingRMSError()
            return reply
        
        def startMntHoming():
            reply = PWI.startMntHoming()
            return reply
        
        def updatedb():
        """Writes telescope status to postgresql database
        """
        cursor = conn.cursor()
        info=getALL() 
        #### NEDS CHECK #################
        for key in info.keys():
            cmd = "UPDATE %s SET value=%f WHERE info_id=%s" % (dbname, info[key],key)
            cursor.execute(cmd)

        ####################################
        
        ########################################################################## register functions for server2 - handling stop commands
        server2.register_function(FocSTOP)
        server2.register_function(MountSTOP)
        server2.register_function(RotSTOP)
        server2.register_function(stop_server)

        
        ##################################################################### register functions for server - operational commands
        server.register_function(DisconnectMNT)
        server.register_function(DisconnectFOC)
        server.register_function(ConnectFOC)
        server.register_function(ConnectMNT)
        server.register_function(Initialize)
        server.register_function(getStatus)
        server.register_function(MntMoveRaDecJ2000)
        server.register_function(update)
        server.register_function(getALL)
        server.register_function(getRA2000)
        server.register_function(getDEC2000)
        server.register_function(getFocuserPos)
        server.register_function(getMNT_CONNECT)
        server.register_function(getFOC_CONNECT)
        server.register_function(getROT_CONNECT)
        server.register_function(getIsTrackingOn)
        server.register_function(getTemps)
        server.register_function(MoveFocuserPos)
        server.register_function(MntMotorReset)
        server.register_function(checkFormatRaDec)
        server.register_function(checkFormatAltAzm)
        server.register_function(checkFormatArcsec)
        server.register_function(stopTracking)
        server.register_function(parkMount)
        server.register_function(MntMotorEnable)
        server.register_function(MntMotorDisable)
        server.register_function(MntMoveRaDec)
        server.register_function(MntMoveAltAzm)
        server.register_function(startTracking)
        server.register_function(LoadPointingModel)
        server.register_function(AddPointToModel)
        server.register_function(SavePointingModel)
        server.register_function(ClearPointingModel)
        server.register_function(FansON)
        server.register_function(FansOFF)
        server.register_function(Rot_Move)
        server.register_function(Rot_derotateStart)
        server.register_function(Rot_derotateStop)
        server.register_function(setTargetRaDecJ2000)
        server.register_function(setTargetAltAzm)
        server.register_function(setTargetRaDec)
        server.register_function(getRotatorPos)
        server.register_function(getRotatorDerotate)
        server.register_function(getTrackingRMSError)
        server.register_function(startMntHoming)

        
        server.register_function(stop_server)
        
        

        #####################################################################
        
        #Threading the two servers such that they run on their individual thread.
        def server2thread():
            while RUNNING:
                server2.handle_request()
        thread_value = _thread.start_new_thread(server2thread,())
        print('Thread successful')

        #Db thread. Updates sql db values
        def dbthread():
            while RUNNING:
                updatedb()

                
        thread_value = _thread.start_new_thread(dbthread,())
        print('Thread successful')
        #server2thread()
        
        #The server starts taking requests
        print("Starting handle_request loop...")
        while RUNNING:
            server.handle_request()

			
def main():
   """
      @brief: This is the main part of the code that starts up everything else. 
      The daemon is started in /tmp/ as "daemon.pid" and the output from the daemon is stored in the Dropbox account. 
      This is mostly relevant under my stay in Australia - THIS SHOULD BE CHANGED AFTER THE STAY. 
   """
   daemon = commander(conf.NOVO_daemon_pid, stdout=conf.NOVO_daemon_log, stderr=conf.NOVO_daemon_log)
   try:
      opts, list = getopt.getopt(sys.argv[1:], 'sth')
   except (getopt.GetoptError):
      print("Bad options provided!")
      sys.exit()
      
   for opt, a in opts:
      if opt == "-s":
         try:
            pid_number = open(conf.NOVO_daemon_pid,'r').readline()
            if pid_number:
               sys.exit('Daemon is already running!')
         except (Exception):
            pass
         print("Starting daemon...\n")
         daemon.start()
         print('This is after the daemon starting')
      elif opt == "-t":
          server = xmlrpc.client.ServerProxy('http://'+str(conf.NOVO_daemon_host)+':'+str(conf.NOVO_daemon_port1))
          print('Stopping Daemon...')
          server.stop_server()
	 # Hmm, calling stop_server() directly would properly work just fine. 
      elif opt == "-h":
         print("Options are:")
         print("python daemon_server.py -s	# This starts the daemon")
         print("python daemon_server.py -t	# This stops the daemon")
      else:
         print("Option %s not supported!" % (opt))


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(time.time(),e)
		print(time.time(), " The daemon has crashed")
