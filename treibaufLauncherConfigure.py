#!/usr/bin/python

# little script to use the treibauf rocket launcher

import os
import sys
import time
import pygame
import usb.core
from Tkinter import *
from PIL import Image, ImageTk

class launchControl(Frame):
   def __init__(self, target):
      self.target = target  
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

      Frame.__init__(self)

      print('Try to shoot: ', self.target)

      reset(self)

      readFile(self,target,"targets.dat")

      for i in range(0,len(self.xTargets)):
           moveTo(self,self.xTargets[i],self.yTargets[i])
           shoot(self)

      reset(self)

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

def shoot(self):
    self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x10,0x00,0x00,0x00,0x00,0x00,0x00]) # shoot
    time.sleep(3)

def reset(self):
    self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x04,0x00,0x00,0x00,0x00,0x00,0x00]) # move left
    time.sleep(6)
    self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00]) # move down
    time.sleep(3)
    self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x20,0x00,0x00,0x00,0x00,0x00,0x00]) # stop
    self.xPosition = 0
    self.yPosition = 0

def readFile(self,targetlist,filename="targets.dat" ):
    FILE = open(filename)
    for line in FILE:
        s = line.split()
        var = s[0]
        if var != '#':
            found = targetlist.find( var )
            print('try to find', var , 'Found', found)
            if found != -1:
               self.xTargets.append( s[1] )
               self.yTargets.append( s[2] )


if __name__ == '__main__':
   if not os.geteuid() == 0:
       sys.exit("Script must be run as root.")
   if len(sys.argv) < 2:
       print('Argument needed: ./treibaufLauncherConfigure <name>')
   else:
       launchControl(sys.argv[1])
