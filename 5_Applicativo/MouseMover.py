import sys
import time
import math
import pygame
import win32gui
import win32con
import pyautogui
import mouse
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading
import tkinter as tk
from tkinter import filedialog
import os


# Class
class MouseMover: 
    # Variables
    key_color_hex = 0x010101 # Key color to make transparent
    key_color = (1, 1, 1, 0)
    initialTime = time.time()
    initialPosition = pyautogui.position()
    mouse_x, mouse_y = pyautogui.position()
    displayingMenu = False
    icon = None
    running = False
    temporalOffset = 5
    runningAnimation = False
    cursor = None
    cursorPath = "image.png"
    showingCursorSelector = False

    # Constructor
    def __init__(self):     
        pygame.init() # Initialize Pygame
        self.font = pygame.font.Font(None, 36)
        self.setup()


    # Setup
    def setup(self):   
        info = pygame.display.Info() # Get the primary screen dimensions
        width, height = info.current_w, info.current_h
  
        self.screen = pygame.display.set_mode((width, height), pygame.NOFRAME | pygame.SRCALPHA) # Create a borderless window with alpha support

        self.hwnd = pygame.display.get_wm_info()['window'] # Get the window handle
        
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED) # Set the window as "layered"
        win32gui.SetLayeredWindowAttributes(self.hwnd, self.key_color_hex, 0, win32con.LWA_COLORKEY) # Set the background transparency

        self.hide_window_icon()
        self.running = True

    def setToForeground(self):
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    

    # Events
    def handleQuitEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


    # Menu
    def loadMenu(self):
        self.displayingMenu = True
        self.displayMenu()    
    
    def displayMenu(self):
        if self.displayingMenu:
            info = pygame.display.Info()
            menu = pygame.image.load('GUI/GUI principale.png')
            self.screen.blit(menu, (info.current_w / 2 - 300, info.current_h / 2 - 200))
            temporalOffsetText = self.font.render(str(self.temporalOffset), True, (136,136,136))
            if self.temporalOffset < 10:
                self.screen.blit(temporalOffsetText, (info.current_w / 2 + 115, info.current_h / 2 - 45))
            else:
                self.screen.blit(temporalOffsetText, (info.current_w / 2 + 109, info.current_h / 2 - 45))
            self.setToForeground()
            self.menuController(info)

    def menuController(self, info):
        self.refreshMousePosition()
        if pygame.mouse.get_pressed()[0]:
            # Resume
            if (self.mouse_x > info.current_w / 2 - 151 and self.mouse_x < info.current_w / 2 - 24) and (self.mouse_y > info.current_h / 2 + 95 and self.mouse_y < info.current_h / 2 + 143):
                self.displayingMenu = False
                self.hide_window_icon()
            # Quit
            elif (self.mouse_x > info.current_w / 2 + 29 and self.mouse_x < info.current_w / 2 + 156) and (self.mouse_y > info.current_h / 2 + 95 and self.mouse_y < info.current_h / 2 + 143):
                self.on_quit()
            # Temporal offset
            elif (self.mouse_x > info.current_w / 2 + 86 and self.mouse_x < info.current_w / 2 + 160) and (self.mouse_y > info.current_h / 2 -53 and self.mouse_y < info.current_h / 2 - 19):
                self.handleInput(info, True)
            # Cursor
            elif (self.mouse_x > info.current_w / 2 - 142 and self.mouse_x < info.current_w / 2 - 33) and (self.mouse_y > info.current_h / 2 + 23 and self.mouse_y < info.current_h / 2 + 54):
                self.hide_window_icon()
                self.displayingMenu = False
                self.showingCursorSelector = True

    def handleInput(self, info, typing):
        input_text = ""
        input_rect = pygame.Rect(info.current_w / 2 + 105, info.current_h / 2 - 52, 50, 30)
        while typing:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if input_text != "":
                            self.temporalOffset = int(input_text)
                        typing = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]  # Remove the last character
                    elif len(input_text) < 2 and '0' <= event.unicode <= '9':  # Limita i numeri a 1-9 e due cifre
                        input_text += event.unicode  # Add the typed character to the input text
            menu = pygame.image.load('GUI/GUI principaleInput.png')
            self.screen.blit(menu, (info.current_w / 2 - 300, info.current_h / 2 - 200))
            color = (123,141,147)
            pygame.draw.rect(self.screen, color, input_rect)
            text_surface = self.font.render(input_text, True, (0,0,0))
            if len(input_text) == 1:
                self.screen.blit(text_surface, (input_rect.x + 11, input_rect.y + 6))
            else:
                self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 6))
            pygame.display.flip()   


    # Hide/Show window
    def hide_window_icon(self):
        # Hides the window icon from the taskbar without hiding the window
        # Sets the window as "ToolWindow" (prevents the icon from appearing in the taskbar)
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TOOLWINDOW)


    # Mouse
    def refreshMousePosition(self):
        self.mouse_x, self.mouse_y = pyautogui.position()

    def mouseController(self):
        if not self.displayingMenu:
            if self.initialPosition != pyautogui.position():
                self.initialPosition = pyautogui.position()
                self.initialTime = time.time()
            elif time.time() - self.initialTime > self.temporalOffset*60:# Togliere *60 per i secondi
                self.runningAnimation = True
                self.moveMouseSquare()
                self.mouseMoveCircle()
                self.initialTime = time.time()


    # Cursor
    def findCursor(self):
        root = tk.Tk()
        root.withdraw()  # Nasconde la finestra principale di tkinter
        
        # Definisci un percorso relativo, ad esempio nella cartella 'cursors'
        percorso_relativo = os.path.join(os.getcwd(), 'Cursors')

        self.cursorPath = filedialog.askopenfilename(title="Seleziona un'immagine del cursore", initialdir=percorso_relativo, filetypes=[("Immagini PNG", "*.png")])
        self.showingCursorSelector = False
        return self.cursorPath

    def loadCursor(self):
         # Carica l'immagine del cursore
        self.cursor= pygame.image.load(self.cursorPath).convert_alpha()  # Carica l'immagine selezionata
        self.scaleCursor()

    def displayCursor(self):
        self.screen.blit(self.cursor, (self.mouse_x+10, self.mouse_y))  # Disegna l'immagine del cursore

    def scaleCursor(self):
        dimensioneDesiderata = 100
        factor = dimensioneDesiderata / self.cursor.get_width()
        self.cursor = pygame.transform.smoothscale_by(self.cursor, factor)


    # Time
    def loadTime(self):
        current_time = time.strftime("%H:%M:%S")
        time_surface = self.font.render(current_time, True, (255, 255, 255))  # Text color: white
        shadow_surface = self.font.render(current_time, True, (0, 0, 0))  # Shadow: black
        text_rect = time_surface.get_rect(center=(self.mouse_x + 60, self.mouse_y - 20))  # 20 pixels above the image
        self.screen.blit(shadow_surface, text_rect.move(2, 2))  # Slightly shifted shadow
        self.screen.blit(time_surface, text_rect)


    # Icon
    def on_quit(self, icon, item):
        self.icon.stop()
        self.running = False  # Sets the flag to stop the main loop

    def create_image(self):
        image = Image.open('Utility/favicon-32x32.png').convert('RGBA')  # Use the correct image file path
        return image

    def start_tray(self):
        icon_image = self.create_image()  # Uses the icon created by the function
        self.icon = Icon("test_icon", icon_image, menu=Menu(MenuItem('Apri menu', self.loadMenu), MenuItem('Chiudi', self.on_quit)))
        self.icon.run()


    # Animations
    def moveMouseSquare(self):
        size = 200
        # Moves the mouse simulating a square
        for i in range(0, size, 1):
            if not self.runningAnimation:
                break
            mouse.move(1, 0, absolute=False, duration=0.001)
            self.loadAll()
            self.isInterrupted(self.mouse_x, self.mouse_y)
            
        for i in range(0, size, 1):
            if not self.runningAnimation:
                break
            mouse.move(0, 1, absolute=False, duration=0.001)
            self.loadAll()
            self.isInterrupted(self.mouse_x, self.mouse_y)
            
        for i in range(0, size, 1):
            if not self.runningAnimation:
                break
            mouse.move(-1, 0, absolute=False, duration=0.001)
            self.loadAll()
            self.isInterrupted(self.mouse_x, self.mouse_y)
            
        for i in range(0, size, 1):
            if not self.runningAnimation:
                break
            mouse.move(0, -1, absolute=False, duration=0.001)
            self.loadAll()
            self.isInterrupted(self.mouse_x, self.mouse_y)

    def mouseMoveCircle(self):
        radius = 10
        # Moves the mouse simulating a circle
        for i in range(0, 360, 5):
            if not self.runningAnimation:
                break
            angle = math.radians(i)
            # calculates the x and y coordinates
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            # moves the mouse to the calculated position
            mouse.move(x, y, absolute=False, duration=0.01)
            self.loadAll()
            self.isInterrupted(self.mouse_x, self.mouse_y)  

    def isInterrupted(self, lastX, lastY):
        self.refreshMousePosition()
        if self.mouse_x != lastX or self.mouse_y != lastY:
            self.runningAnimation = False


    # Running
    def start(self):
        self.loadCursor()
        while self.running:
            if self.showingCursorSelector:
                self.refreshScreen()
                self.cursorPath = self.findCursor()  # Fai scegliere un file all'utente
                if self.cursorPath:  # Se il percorso è valido
                    self.loadCursor()
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                clock = pygame.time.Clock()
                self.screen.fill(self.key_color)
                self.handleQuitEvent()
                self.mouseController()
                self.displayMenu()
                self.loadAll()
                clock.tick(60)

    def refreshScreen(self):
        self.screen.fill(self.key_color)
        pygame.display.flip()

    def loadAll(self):
        if not self.displayingMenu:
            self.screen.fill(self.key_color)
            self.refreshMousePosition()
            self.displayCursor()
            self.loadTime()         
        self.setToForeground()
        pygame.display.flip()

    
# Run
def run(mm):
    mm.setup()
    mm.start()


# Main
if __name__ == "__main__":
    mm = MouseMover()

    # Run the pystray code in the main thread
    tray_thread = threading.Thread(target=mm.start_tray, daemon=True)  # Set as daemon to terminate automatically

    # Start the threads
    tray_thread.start()

    run(mm)

    # Wait for Pygame to finish
    tray_thread.join()
