import pygame
import sys
import win32gui
import win32con
import pyautogui
import time
import mouse
import math


# Inizializza Pygame
pygame.init()

# Ottieni le dimensioni dello schermo primario
info = pygame.display.Info()
width, height = info.current_w, info.current_h

# Crea la finestra senza bordi e con supporto alpha
screen = pygame.display.set_mode((width, height), pygame.NOFRAME | pygame.SRCALPHA)

# Ottieni l'handle della finestra
hwnd = pygame.display.get_wm_info()['window']

# Colore chiave da rendere trasparente (bianco)
key_color = 0xFFFFFF  # Bianco in formato RGB esadecimale

# Imposta la finestra come "layered"
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

# Imposta la trasparenza dello sfondo
win32gui.SetLayeredWindowAttributes(hwnd, key_color, 0, win32con.LWA_COLORKEY)

# Carica l'immagine con trasparenza
image = pygame.image.load('image.png').convert_alpha()

# Imposta il font per l'orologio
font = pygame.font.Font(None, 36)  # Font predefinito, dimensione 36



#Metodi animazione
def draw_square(size):
    mouse.move(size, 0, absolute=False, duration=0.2)
    mouse.move(0, size, absolute=False, duration=0.2)
    mouse.move(-size, 0, absolute=False, duration=0.2)
    mouse.move(0, -size, absolute=False, duration=0.2)


def draw_circle(radius):
    # move the mouse in a circle
    for i in range(0, 360, 5):
        # convert degrees to radians
        angle = math.radians(i)
        # calculate the x and y coordinates
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        # move the mouse to the calculated position
        mouse.move(x, y, absolute=False, duration=0.01)

# Ciclo principale
if __name__ == "__main__":
    tempoIniziale = time.time()
    posizioneIniziale = pyautogui.position()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if posizioneIniziale != pyautogui.position():
            posizioneIniziale = pyautogui.position()
            tempoIniziale = time.time()
        elif time.time() - tempoIniziale > 5:
            draw_square(200)
            time.sleep(1)
            draw_circle(10)
            tempoIniziale = time.time()

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