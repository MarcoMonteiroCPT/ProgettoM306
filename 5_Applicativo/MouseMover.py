import sys
import threading
import time
import math
import pygame
import win32gui
import win32con
import pyautogui
import mouse



# Variabili
screen = 0 
hwnd = 0 
tempoIniziale = 0
posizioneIniziale = 0
font = 0
image = None
hwnd = 0

# Classe
class MouseMover:
    key_color_hex = 0x010101    # Colore chiave da rendere trasparente
    key_color = (1, 1, 1, 0)

    # Imposta tempo e posizione iniziali
    tempoIniziale = time.time()
    posizioneIniziale = pyautogui.position()

    mouse_x, mouse_y = pyautogui.position()
    image = None
    
    
    

    def __init__(self):
        # Inizializza Pygame
        pygame.init()
        self.font = pygame.font.Font(None, 36)

        self.setup()

    # Setup
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
        # Riempi lo schermo con un colore trasparente
        




    def handleQuitEvent(self):
        # Gestisce la chiusura del programma
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def loadImage(self):
        # Carica l'immagine con trasparenza
        self.image = pygame.image.load('image.png').convert_alpha()
        self.scaleImage()
        # Disegna l'immagine sopra il cursore del mouse

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

        # Renderizza il testo dell'ora
        time_surface = self.font.render(current_time, True, (255, 255, 255))  # Colore del testo: bianco

        # Aggiungi un contorno nero per migliorare la visibilità
        shadow_surface = self.font.render(current_time, True, (0, 0, 0))  # Contorno: nero

        # Posiziona il testo sopra l'immagine
        text_rect = time_surface.get_rect(center=(self.mouse_x + 50, self.mouse_y -20))  # 20 pixel sopra l'immagine

        # Disegna il contorno
        self.screen.blit(shadow_surface, text_rect.move(2, 2))  # Contorno leggermente spostato
        # Disegna il testo principale
        self.screen.blit(time_surface, text_rect)

    def start(self):
        self.loadImage()
        while True:
            clock = pygame.time.Clock()
            self.screen.fill(self.key_color)
            self.handleQuitEvent()            
            self.mouseController()
            self.refreshImagePosition()
            self.loadTime()
            self.primoPiano()
            self.aggiornaPosizione()
            pygame.display.flip()
            clock.tick(60)



    def primoPiano(self):
        # Mantieni la finestra in primo piano
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    def mouseController(self):
        if self.posizioneIniziale != pyautogui.position():
            self.posizioneIniziale = pyautogui.position()
            self.tempoIniziale = time.time()
        elif time.time() - self.tempoIniziale > 5:
            self.moveMouseSquare()
            time.sleep(1)
            self.mouseMoveCircle()
            self.tempoIniziale = time.time()

    #Animazioni
    def moveMouseSquare(self):
        size = 200
        #Muove il mouse simulando un quadrato
        mouse.move(size, 0, absolute=False, duration=0.2)
        mouse.move(0, size, absolute=False, duration=0.2)
        mouse.move(-size, 0, absolute=False, duration=0.2)
        mouse.move(0, -size, absolute=False, duration=0.2)


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
            self.loadImage()
            self.loadTime()
            pygame.display.flip()



def run():
    mm = MouseMover()
    mm.setup()
    mm.start()


if __name__ == "__main__":
    run()