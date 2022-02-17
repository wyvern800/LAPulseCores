from pyautogui import *
import tkinter as tk
from PIL import Image, ImageTk
import pyautogui
import time
import keyboard
import random
import win32api
import win32con
import threading
from utils import *

global GAME_REGION
inCooldown = {}
shown = {}
found = False
callStack = []
TICKS = 0.50

# All images
SKILL_ICONS = ['1', '2', '3', '4', '5', '6', '7', '8']

# Area where skills are located at (left, top, width, height)
SKILLS_AREA = (607, 901, 250, 250)


class App(threading.Thread):  
    '''
        Draws the skill that went out of cooldown on screen
    '''
    def draw_skill(self, file):
        # Load the image
        skillIcon = Image.open(file)

        # Resize the Image using resize method
        resized_image = skillIcon.resize((50, 50), Image.ANTIALIAS)
        global new_image
        new_image = ImageTk.PhotoImage(resized_image)
        
        # Update the icon on screen
        self.root.call('wm', 'attributes', '.', '-topmost', True)
        self.root.after(2000, lambda: self.root.call('wm', 'attributes', '.', '-topmost', False))
        self.root.canvas.itemconfig(self.image_on_canvas, image=new_image)
        
        
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()

        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        self.root.config(cursor="none")
        self.root.overrideredirect(True)

        self.root.canvas = tk.Canvas(self.root, bg="blue", bd=0,
                                     highlightthickness=0, width=50, height=50)
    
        self.root.canvas.pack()
        
        self.image_on_canvas = self.root.canvas.create_image(0, 0, anchor="nw", image=None)

        self.root.attributes("-transparentcolor", "blue")

        self.root.eval('tk::PlaceWindow . center')

        self.root.wm_attributes('-alpha', 0.6)
        
        print('Created canvas '+ str(self.root.canvas))
        self.root.mainloop()


app = App()

'''
    The main application
'''
def main():
  print('App is running...')
  
  try:
      print("Finding game region...")
      region = pyautogui.locateOnScreen("reference.png")

      while region is None:
          print("Could not find game on screen. It is whether closed or minimized")
          time.sleep(2)
          region = pyautogui.locateOnScreen("reference.png")
          
          # Check if game is running within the process
          if (checkIfProcessRunning('lostark.exe') == False):
              print("Could not find game on screen. Is it minimized?")
              continue

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
          # To avoid skill to be shown on app start
          lastSkillDrawn = None

          while 1:
              if checkIfProcessRunning('lostark.exe') == False:
                  print('Could not find game on screen. It is whether closed or minimized')
                  continue
              
              # Check if skils are on screen
              for skill in SKILL_ICONS:
                  file = 'keys/'+skill+'.png'

                  foundSkill = pyautogui.locateOnScreen(
                      file, region=SKILLS_AREA)

                  # If we found the skill
                  if foundSkill != None:
                      if (shown.get(skill) == True):
                          continue
                      print('Skill '+skill+' saiu do cooldown '+str(foundSkill))
                      inCooldown[skill] = False
                      shown[skill] = True

                      # If skill wasn't drawn, then do it LOL
                      if (lastSkillDrawn is not None):
                          app.draw_skill(file)

                  # If it is rechargind, trigger the still on cooldown
                  elif pyautogui.locateOnScreen(file, region=SKILLS_AREA, grayscale=True, confidence=0.5) and inCooldown.get(skill) == False:
                      print('Skill '+str(skill)+' cooldown')
                      inCooldown[skill] = True
                      shown[skill] = False
                      lastSkillDrawn = skill

              # Ticks to wait
              time.sleep(TICKS)
  except KeyboardInterrupt:
      # Close program if subthread issues KeyboardInterrupt
      os._exit(0)
      
main()