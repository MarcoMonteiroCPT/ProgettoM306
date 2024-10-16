import pygame
import sys
import time
import math
import win32gui
import win32con
import pyautogui
import mouse


# Variabili
screen = 0 
hwnd = 0 
tempoIniziale = 0
posizioneIniziale = 0
image = 0
font = 0

# Classe
class MouseMover:
    key_color = 0x010101    # Colore chiave da rendere trasparente
    # Imposta tempo e posizione iniziali
    tempoIniziale = time.time()
    posizioneIniziale = pyautogui.position()

    font = pygame.font.Font(None, 36)  # Font predefinito, dimensione 36

    def __init__(self):
        # Inizializza Pygame
        pygame.init()
        self.setup()

    # Setup
    def setup(self):
        
        # Ottieni le dimensioni dello schermo primario
        info = pygame.display.Info()
        width, height = info.current_w, info.current_h

        # Crea la finestra senza bordi e con supporto alpha
        self.screen = pygame.display.set_mode((width, height), pygame.NOFRAME | pygame.SRCALPHA)

        # Ottieni l'handle della finestra
        hwnd = pygame.display.get_wm_info()['window']

        # Imposta la finestra come "layered"
        win32gui.SetWindowLong(hwnd, 
                               win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

        # Imposta la trasparenza dello sfondo
        win32gui.SetLayeredWindowAttributes(hwnd, self.key_color, 0, win32con.LWA_COLORKEY)

    def handleQuitEvent(self):
        # Gestisce la chiusura del programma
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def start(self):
        while True:
            self.handleQuitEvent()
            
            # TODO dedicare una funzione apposita

            if self.posizioneIniziale != pyautogui.position():
                self.posizioneIniziale = pyautogui.position()
                self.tempoIniziale = time.time()
            elif time.time() - self.tempoIniziale > 5:
                moveMouseSquare(200)
                time.sleep(1)
                mouseMoveCircle(10)
                self.tempoIniziale = time.time()

            # Ottieni la posizione del mouse usando pyautogui
            mouse_x, mouse_y = pyautogui.position()

            # Riempi lo schermo con un colore trasparente
            screen.fill((255, 255, 255, 0))  # Colore bianco trasparente

            # Disegna l'immagine sopra il cursore del mouse
            screen.blit(image, (mouse_x, mouse_y))  # Posiziona sopra il cursore

            # Ottieni l'ora corrente
            current_time = time.strftime("%H:%M:%S")

            # Renderizza il testo dell'ora
            time_surface = font.render(current_time, True, (255, 255, 254))  # Colore del testo: bianco

            # Aggiungi un contorno nero per migliorare la visibilità
            shadow_surface = font.render(current_time, True, (0, 0, 0))  # Contorno: nero

            # Posiziona il testo sopra l'immagine
            text_rect = time_surface.get_rect(center=(mouse_x + image.get_width() // 2, mouse_y - 20))  # 20 pixel sopra l'immagine

            # Disegna il contorno
            screen.blit(shadow_surface, text_rect.move(2, 2))  # Contorno leggermente spostato
            # Disegna il testo principale
            screen.blit(time_surface, text_rect)

            # Aggiorna lo schermo
            pygame.display.flip()

            # Mantieni la finestra in primo piano
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def loadImage():
    # Global
    global image
    # Carica l'immagine con trasparenza
    image = pygame.image.load('image.png').convert_alpha()

#Animazioni
def moveMouseSquare(size):
    #Muove il mouse simulando un quadrato
    mouse.move(size, 0, absolute=False, duration=0.2)
    mouse.move(0, size, absolute=False, duration=0.2)
    mouse.move(-size, 0, absolute=False, duration=0.2)
    mouse.move(0, -size, absolute=False, duration=0.2)
    mouse.move(size/2, 0, absolute=False, duration=0.2)


def mouseMoveCircle(radius):
    # Muove il mouse simulando un cerchio
    for i in range(0, 360, 5):
        # Converte in gradi in radianti
        angle = math.radians(i)
        # calcola le coordinate x e y
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        # muove il mouse alla posizione calcolata
        mouse.move(x, y, absolute=False, duration=0.01)



def run():
    mm = MouseMover()
    # setup()
    # loadImage()
    # setFont()
    # start()


if __name__ == "__main__":
    run()