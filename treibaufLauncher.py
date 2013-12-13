#!/usr/bin/python

# little script to use the treibauf rocket launcher
# send an email to rocketlauncher@treibauf.ch and all the targets (e.g. hummel@treibauf.ch)
# mission will shortly be accomplished

import os
import sys
import time
import pygame
import usb.core
import RPi.GPIO as GPIO

#imports for email
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.parser import HeaderParser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.Utils import COMMASPACE, formatdate
from email import Encoders

MAILSERVER = "imap.gmail.com"                     # mail server
PORT = 993                                        # mail server port
USERNAME = "**********************@gmail.com"     # mail adress
PASSWORD = "*************" 			              # mail password	

# initialize the GPIO
GPIO.setmode(GPIO.BOARD)

#################################################
# class launchControl with all needed variables 
class launchControl():
   def __init__(self):  
      self.xPosition = 0
      self.yPosition = 0
      self.xTargets = list()
      self.yTargets = list()
      self.dev = usb.core.find(idVendor=0x2123, idProduct=0x1010)
      if self.dev is None:
         raise ValueError('Launcher not found.')
      if self.dev.is_kernel_driver_active(0) is True:
         self.dev.detach_kernel_driver(0)
      self.dev.set_configuration()

      GPIO.setup(7,GPIO.OUT)

#################################################
#################################################
# while loop 
      print( 'Waiting for targets...' )
      
      while( 1 ):
          targetList = checkEmailAndGetTargets()

          if targetList :

              reset(self)

              readFileAndGetCoordinates(self,targetList,"targets.dat")

              GPIO.output(7,True)

              for i in range(0,len(self.xTargets)):
                  moveTo(self,self.xTargets[i],self.yTargets[i])
                  shoot(self)

              GPIO.output(7,False)

              reset(self)

              print( 'Waiting for targets...' )

          time.sleep(20)
#
#################################################
#################################################

#################################################
# move to function
def moveTo(self,xTarget,yTarget):
    xDiff = float(xTarget)-float(self.xPosition)
    if xDiff < 0:
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x04,0x00,0x00,0x00,0x00,0x00,0x00]) # move left
      time.sleep(-xDiff)
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x20,0x00,0x00,0x00,0x00,0x00,0x00]) # stop
    else:
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x08,0x00,0x00,0x00,0x00,0x00,0x00]) # move right
      time.sleep(xDiff)
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x20,0x00,0x00,0x00,0x00,0x00,0x00]) # stop

    yDiff = float(yTarget)-float(self.yPosition)
    if yDiff < 0:
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00]) # move down
      time.sleep(-yDiff)
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x20,0x00,0x00,0x00,0x00,0x00,0x00]) # stop
    else:
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x00]) # move up
      time.sleep(yDiff)
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x20,0x00,0x00,0x00,0x00,0x00,0x00]) # stop

    self.xPosition = xTarget
    self.yPosition = yTarget
# end move to function
#################################################

#################################################
# shoot function, triggers the rocket launcher
def shoot(self):
    self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x10,0x00,0x00,0x00,0x00,0x00,0x00]) # shoot
    time.sleep(4)
# end shoot function
#################################################

#################################################
# reset function, resets the rocket launcher to position 0,0 ( all to the left and down )
def reset(self):
    self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x04,0x00,0x00,0x00,0x00,0x00,0x00]) # move left
    time.sleep(6)
    self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00]) # move down
    time.sleep(3)
    self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x20,0x00,0x00,0x00,0x00,0x00,0x00]) # stop
    self.xPosition = 0
    self.yPosition = 0
    self.xTargets = list()
    self.yTargets = list()
# end reset function
#################################################

#################################################
# readFileAndGetCoordinates function, read the target file and get the coordinates for the targets
def readFileAndGetCoordinates(self,targetlist,filename="targets.dat" ):
    FILE = open(filename)
    targetliststring = ''.join(targetlist)
    for line in FILE:
        s = line.split()
        var = s[0]
        if var != '#':
            found = targetliststring.find( var )
            if found != -1:
               print('Target: ', var , 'Executing now!')
               self.xTargets.append( s[1] )
               self.yTargets.append( s[2] )
# end readFileAndGetCoordinates function
#################################################

#################################################
# checkEmailAndGetTargets function, check on the mail server if a new target list has arrived, get the targets
def checkEmailAndGetTargets():
    targets_list = []
    imap_server = imaplib.IMAP4_SSL(MAILSERVER,PORT)
    imap_server.login(USERNAME, PASSWORD)
    imap_server.select('INBOX')
    status, email_ids = imap_server.search(None, '(UNSEEN)')
    if email_ids != ['']:
        for e_id in email_ids[0].split():   		      
          resp, data = imap_server.fetch(e_id, '(RFC822)')   
          perf = HeaderParser().parsestr(data[0][1])	      
    	  targets_list.append(perf['To'])		          

    imap_server.close()
    return targets_list
# end checkEmailAndGetTargets function
#################################################

#################################################
#################################################
# main loop 
if __name__ == '__main__':
   if not os.geteuid() == 0:
       sys.exit("Script must be run as root.")
   launchControl()
