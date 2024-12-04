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


# Class
class MouseMover: 
    # Variables
    key_color_hex = 0x010101 # Key color to make transparent
    key_color = (1, 1, 1, 0)
    initialTime = time.time()
    initialPosition = pyautogui.position()
    mouse_x, mouse_y = pyautogui.position()
    image = None
    displayingMenu = False
    icon = None
    running = False
    temporalOffset = 5
    runningAnimation = False


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
        self.show_window()
        self.displayingMenu = True
        self.displayMenu()    
    
    def displayMenu(self):
        if self.displayingMenu:
            info = pygame.display.Info()
            menu = pygame.image.load('GUI/GUI principale.png')
            self.screen.blit(menu, (info.current_w / 2 - 300, info.current_h / 2 - 200))
            temporalOffsetText = self.font.render(str(self.temporalOffset), True, (136,136,136))
            self.screen.blit(temporalOffsetText, (info.current_w / 2 + 110, info.current_h / 2 - 45))
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

    def handleInput(self, info, typing):
        input_text = ""
        active = True
        input_rect = pygame.Rect(info.current_w / 2 + 105, info.current_h / 2 - 52, 50, 30)
        while typing:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            self.temporalOffset = int(input_text)
                            typing = False
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]  # Remove the last character
                        elif len(input_text) < 2:
                            input_text += event.unicode  # Add the typed character to the input text
            if active:
                menu = pygame.image.load('GUI/GUI principaleInput.png')
                self.screen.blit(menu, (info.current_w / 2 - 300, info.current_h / 2 - 200))
            color = (123,141,147) if active else (207,216,220)
            pygame.draw.rect(self.screen, color, input_rect)
            text_surface = self.font.render(input_text, True, (0,0,0))
            self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
            pygame.display.flip()   


    # Hide/Show window
    def hide_window_icon(self):
        # Hides the window icon from the taskbar without hiding the window
        # Sets the window as "ToolWindow" (prevents the icon from appearing in the taskbar)
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TOOLWINDOW)
        
        # Sets the window as "topmost" to prevent it from going behind other windows
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    def show_window(self):
        """Shows the Pygame window (restores the window)."""
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)


    # Mouse
    def refreshMousePosition(self):
        self.mouse_x, self.mouse_y = pyautogui.position()

    def mouseController(self):
        if not self.displayingMenu:
            if self.initialPosition != pyautogui.position():
                self.initialPosition = pyautogui.position()
                self.initialTime = time.time()
            elif time.time() - self.initialTime > self.temporalOffset:
                self.runningAnimation = True
                self.moveMouseSquare()
                self.mouseMoveCircle()
                self.initialTime = time.time()


    # Image
    def scaleImage(self):
        dimensioneDesiderata = 100
        factor = dimensioneDesiderata / self.image.get_width()
        self.image = pygame.transform.smoothscale_by(self.image, factor)    

    def loadImage(self):
        # Load the image with transparency
        self.image = pygame.image.load('image.png').convert_alpha()
        self.scaleImage()

    def refreshImagePosition(self):
        self.screen.blit(self.image, (self.mouse_x, self.mouse_y))  # Position above the cursor


    # Time
    def loadTime(self):
        current_time = time.strftime("%H:%M:%S")
        time_surface = self.font.render(current_time, True, (255, 255, 255))  # Text color: white
        shadow_surface = self.font.render(current_time, True, (0, 0, 0))  # Shadow: black
        text_rect = time_surface.get_rect(center=(self.mouse_x + 50, self.mouse_y - 20))  # 20 pixels above the image
        self.screen.blit(shadow_surface, text_rect.move(2, 2))  # Slightly shifted shadow
        self.screen.blit(time_surface, text_rect)


    # Icon
    def on_quit(self, icon, item):
        self.icon.stop()
        self.running = False  # Sets the flag to stop the main loop

    # Function to create the icon image (you can use a .ico or .png file)
    def create_image(self):
        image = Image.open('favicon-32x32.png').convert('RGBA')  # Use the correct image file path
        return image

    # Function to start the icon in the system tray
    def start_tray(self):
        icon_image = self.create_image()  # Uses the icon created by the function
        self.icon = Icon("test_icon", icon_image, menu=Menu(MenuItem('Apri menu', self.loadMenu), MenuItem('Esci', self.on_quit)))
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
        self.loadImage()
        while self.running:
            clock = pygame.time.Clock()
            self.screen.fill(self.key_color)
            self.handleQuitEvent()
            self.mouseController()
            self.displayMenu()
            self.loadAll()
            clock.tick(60)

    def loadAll(self):
        if not self.displayingMenu:
            self.screen.fill(self.key_color)
            self.refreshImagePosition()
            self.loadTime()
            self.refreshMousePosition()
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
