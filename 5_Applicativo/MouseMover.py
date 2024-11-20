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

# Variabili
screen = 0 
hwnd = 0 
tempoIniziale = 0
posizioneIniziale = 0
font = 0
image = None
hwnd = 0
displayingMenu = False

# Classe
class MouseMover:
    key_color_hex = 0x010101    # Colore chiave da rendere trasparente
    key_color = (1, 1, 1, 0)

    # Imposta tempo e posizione iniziali
    tempoIniziale = time.time()
    posizioneIniziale = pyautogui.position()

    mouse_x, mouse_y = pyautogui.position()
    image = None
    displayingMenu = False
    
    def __init__(self):
        # Inizializza Pygame
        pygame.init()
        self.font = pygame.font.Font(None, 36)

        self.setup()

    def setup(self):
        # Ottieni le dimensioni dello schermo primario
        info = pygame.display.Info()
        width, height = info.current_w, info.current_h  

        # Crea la finestra senza bordi e con supporto alpha
        self.screen = pygame.display.set_mode((width, height), pygame.NOFRAME | pygame.SRCALPHA)

        # Ottieni l'handle della finestra
        self.hwnd = pygame.display.get_wm_info()['window']

        # Imposta la finestra come "layered"
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

        # Imposta la trasparenza dello sfondo
        win32gui.SetLayeredWindowAttributes(self.hwnd, self.key_color_hex, 0, win32con.LWA_COLORKEY)

    def handleEvents(self):
        for event in pygame.event.get():
            self.handleQuitEvent(event)
            self.handleKeydownEvent(event)
    
    def handleQuitEvent(self, event):
        # Gestisce la chiusura del programma
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    def handleKeydownEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.displayingMenu = not self.displayingMenu
                self.tempoIniziale = time.time()
    
    def displayMenu(self):      
        if self.displayingMenu:
            info = pygame.display.Info()
            menu = pygame.image.load('GUI/GUI principale.png')
            self.screen.blit(menu, (info.current_w/2-300, info.current_h/2-200))
            self.primoPiano()
            self.menuController(info)

    def menuController(self, info):
        self.aggiornaPosizione()
        if pygame.mouse.get_pressed()[0]:
            if (self.mouse_x > info.current_w/2-151 and self.mouse_x < info.current_w/2-24) and (self.mouse_y > info.current_h/2+95 and self.mouse_y < info.current_h/2+143):
                self.displayingMenu = False

    def loadImage(self):
        # Carica l'immagine con trasparenza
        self.image = pygame.image.load('image.png').convert_alpha()
        self.scaleImage()

    def refreshImagePosition(self):
        self.screen.blit(self.image, (self.mouse_x, self.mouse_y))  # Posiziona sopra il cursore
    
    def scaleImage(self):
        dimensioneDesiderata = 100
        factor = dimensioneDesiderata/self.image.get_width()
        self.image = pygame.transform.smoothscale_by(self.image, factor)
            
    def aggiornaPosizione(self):
        self.mouse_x, self.mouse_y = pyautogui.position()

    def loadTime(self):
        current_time = time.strftime("%H:%M:%S")
        time_surface = self.font.render(current_time, True, (255, 255, 255))  # Colore del testo: bianco
        shadow_surface = self.font.render(current_time, True, (0, 0, 0))  # Contorno: nero
        text_rect = time_surface.get_rect(center=(self.mouse_x + 50, self.mouse_y -20))  # 20 pixel sopra l'immagine
        self.screen.blit(shadow_surface, text_rect.move(2, 2))  # Contorno leggermente spostato
        self.screen.blit(time_surface, text_rect)

    def start(self):
        self.loadImage()
        while True:
            clock = pygame.time.Clock()
            self.screen.fill(self.key_color)
            self.handleEvents()          
            self.mouseController() 
            self.displayMenu()
            self.loadAll()
            clock.tick(60)

    def loadAll(self):
        if not self.displayingMenu:
            self.screen.fill(self.key_color)
            self.refreshImagePosition()
            self.loadTime()
            self.aggiornaPosizione()
        self.primoPiano()
        pygame.display.flip()

    def primoPiano(self):
        # Mantieni la finestra in primo piano
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    def mouseController(self):
        if not self.displayingMenu:
            if self.posizioneIniziale != pyautogui.position():
                self.posizioneIniziale = pyautogui.position()
                self.tempoIniziale = time.time()
            elif time.time() - self.tempoIniziale > 5:
                self.moveMouseSquare()
                self.mouseMoveCircle()
                self.tempoIniziale = time.time()

    def moveMouseSquare(self):
        size = 200
        #Muove il mouse simulando un quadrato
        for i in range(0, size, 1):
            mouse.move(1, 0, absolute=False, duration=0.001)
            self.loadAll()
        for i in range(0, size, 1):
            mouse.move(0, 1, absolute=False, duration=0.001)
            self.loadAll()
        for i in range(0, size, 1):
            mouse.move(-1, 0, absolute=False, duration=0.001)
            self.loadAll()
        for i in range(0, size, 1):
            mouse.move(0, -1, absolute=False, duration=0.001)
            self.loadAll()

    def mouseMoveCircle(self):
        radius = 10
        # Muove il mouse simulando un cerchio
        for i in range(0, 360, 5):
            angle = math.radians(i)
            # calcola le coordinate x e y
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            # muove il mouse alla posizione calcolata
            mouse.move(x, y, absolute=False, duration=0.01)
            self.loadAll()


# Funzione per il menu della system tray (opzione "Esci")
def on_quit(icon, item):
    print("Chiusura dell'icona tray")
    icon.stop()

# Funzione per creare l'immagine dell'icona (puoi usare un file .ico o .png)
def create_image():
    # Crea una nuova immagine per l'icona (32x32 px)
    image = Image.new('RGBA', (32, 32), (255, 255, 255, 0))  # Immagine trasparente 32x32 px
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 32, 32), fill="blue")  # Disegna un quadrato blu
    return image

# Funzione per avviare l'icona nella system tray
def start_tray():
    icon_image = create_image()  # Usa l'icona creata dalla funzione
    icon = Icon("test_icon", icon_image, menu=Menu(MenuItem('Esci', on_quit), MenuItem('Apri menu', self.displayMenu)))
    icon.run()

# Funzione principale di Pygame
def pygame_loop():
    mm = MouseMover()
    mm.setup()
    mm.start()

def run():
    mm = MouseMover()
    mm.setup()
    mm.start()

if __name__ == "__main__":
    # Esegui il codice pystray nel thread principale
    tray_thread = threading.Thread(target=start_tray, daemon=True)  # Impostato come daemon per terminare automaticamente
    pygame_thread = threading.Thread(target=pygame_loop)

    # Avvia i thread
    tray_thread.start()
    pygame_thread.start()

    # Attendi che Pygame termini
    pygame_thread.join()
    tray_thread.join()
