from pyautogui import *
import pyautogui
import time
import keyboard 
import random
import win32api, win32con

global GAME_REGION

# All images 
SKILL_ICONS = ['A', 'B']

# Area where skills are located at
SKILLS_AREA = region=(607, 901 , 250, 250)

found = False  
  
print("Finding game region...")
region = pyautogui.locateOnScreen("reference.png")
  
while region is None:
  print("Could not find game on screen. Is the game visible?")
  time.sleep(5)
  region = pyautogui.locateOnScreen("reference.png")

  # if region is none, keep going
  if (region is None):
    continue
  
    # calculate the region of the entire game
  bottomLeftX = region[0]  # left
  bottomLeftY = region[1] + region[3]  # bottom + width
  GAME_REGION = (bottomLeftX, bottomLeftY - 1080, 1200, 1200)
  print("Game region found: %s" % (GAME_REGION,))  
  found = True
  break
  
if found:    
  while 1:
    # Check if skils are on screen
    for skill in SKILL_ICONS:
      foundSkill = pyautogui.locateOnScreen('keys/'+skill+'.png', region=SKILLS_AREA)
      if foundSkill != None:
        print('Skill '+skill+' encontrada em: '+str(foundSkill))
    time.sleep(2)   
