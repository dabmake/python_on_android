from __future__ import division
import serial
import time


class Roomba(object):

  def __init__(self):
     self.ser=serial.Serial('/dev/ttyACM0',115200,)
 #   self.ser=serial.Serial('/dev/ttyUSB0',115200,)
#    self.ser.open()
   
  def wake(self):   
    self.ser.write('\x80') 
    self.ser.write('\x82') 
   
   
  def Sleep(self): 
    self.ser.write('\x85')  # POWER (back to passive Mode)


  def findCharger(self): 
    self.ser.write('\x8f') # Roomba tries to find its dock


  def brushesON(self): 
    self.ser.write('\x8a') # Roomba's MOTOR
    self.ser.write('\xff') # Velocity high byte, HEX 00


  def brushesOFF(self): 
    self.ser.write('\x8a') # Roomba's MOTOR command
    self.ser.write('\xc0') # Velocity high byte, HEX 00


  

   
  def goForward(self):
    self.ser.write('\x89') # Roomba's DRIVE command
    self.ser.write('\x00') # Velocity high byte, HEX 00
    self.ser.write('\xc8') # Velocity low byte,  HEX C8 (00C8=200mm/sec)
    self.ser.write('\x80') # Radius high byte,   HEX 80
    self.ser.write('\x00') # Radius low byte,    HEX 00 (8000=straight)


  def goBackward(self): 
    self.ser.write('\x89') # Roomba's DRIVE command
    self.ser.write('\xff')
    self.ser.write('\x38') # Velocity FF38 = -200 mm/sec (backwards)
    self.ser.write('\x80')
    self.ser.write('\x00') # Radius 8000 = go straight


  def spinLeft(self): 
    self.ser.write('\x89') # Roomba's DRIVE command
    self.ser.write('\x00')   
    self.ser.write('\xc8') # Velocity of spin 00C8 = 200 mm/sec
    self.ser.write('\x00')
    self.ser.write('\x01') # Radius 0001 = spin left


  def spinRight(self):
    self.ser.write('\x89') # Roomba's DRIVE command
    self.ser.write('\x00')
    self.ser.write('\xc8') # Velocity of spin 00C8 = 200 mm/sec
    self.ser.write('\xff')
    self.ser.write('\xff') # Radius FFFF = spin right


  def stopMoving(self): 
    self.ser.write('\x89') # Roomba's DRIVE command
    self.ser.write('\x00')
    self.ser.write('\x00') # Velocity 0000 = stopped
    self.ser.write('\x00')
    self.ser.write('\x00') # Radius 0000 = nothing
#    self.ser.write('\x80')

  def goDistance(self, mm):   # Distance in mm, >0 foreward move, <0 backward move

	  
    drivetime = abs(0.01*mm)      #time in ms 
    if mm > 0: 
      self.goForward()
    else:
      self.goBackward()
    time.sleep(drivetime)
    self.stopMoving()


  def turnLeft(self, degrees):
	  
    ftime = degrees/360*4      #time in ms 
    drivetime = ftime
    self.spinLeft()
    time.sleep(drivetime)
    self.stopMoving()
  

  def turnRight(self, degrees): 
	  
    ftime = degrees/360*4  #time in ms 
    drivetime = ftime
    print drivetime
    self.spinRight()

    time.sleep(drivetime)
    self.stopMoving()

