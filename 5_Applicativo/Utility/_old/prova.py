import pygame
import tkinter as tk
from tkinter import filedialog
import os

# Inizializza Pygame
pygame.init()

# Crea la finestra
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Cambia cursore personalizzato")

# Funzione per caricare un file tramite una finestra di dialogo
def carica_file():
    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale di tkinter
    
    # Definisci un percorso relativo, ad esempio nella cartella 'cursors'
    percorso_relativo = os.path.join(os.getcwd(), 'Cursors')

    file_path = filedialog.askopenfilename(title="Seleziona un'immagine del cursore", initialdir=percorso_relativo, filetypes=[("Immagini PNG", "*.png")])
    
    return file_path

# Funzione per caricare il cursore da un file
def carica_cursore(file_path):
    # Carica l'immagine del cursore
    cursor_image = pygame.image.load(file_path)  # Carica l'immagine selezionata
    cursor_rect = cursor_image.get_rect()
    
    # Applica la dimensione desiderata
    dimensioneDesiderata = 50
    factor = dimensioneDesiderata / cursor_image.get_width()
    cursor_image = pygame.transform.smoothscale_by(cursor_image, factor)

    # Nascondi il cursore di sistema
    pygame.mouse.set_visible(False)

    # Restituisci l'immagine del cursore e il suo rettangolo di bounding
    return cursor_image, cursor_rect

# Ciclo del gioco
running = True
cursore_caricato = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Premi "C" per caricare il cursore
            if event.key == pygame.K_c and not cursore_caricato:
                file_path = carica_file()  # Fai scegliere un file all'utente
                if file_path:  # Se il percorso è valido
                    cursor_image, cursor_rect = carica_cursore(file_path)
                    cursore_caricato = True

    # Rendi lo schermo bianco
    screen.fill((255, 255, 255))

    # Disegna il cursore se è stato caricato
    if cursore_caricato:
        cursor_pos = pygame.mouse.get_pos()  # Ottieni la posizione del mouse
        cursor_rect.topleft = cursor_pos
        screen.blit(cursor_image, cursor_rect)  # Disegna l'immagine del cursore

    pygame.display.flip()

# Chiudi Pygame
pygame.quit()
