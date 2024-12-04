import pygame

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Text Input Example")

# Set up fonts
font = pygame.font.Font(None, 36)

# Set up variables
input_text = ""
active = False
input_rect = pygame.Rect(150, 150, 300, 40)  # Position and size of the input box

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the input box was clicked to activate it
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
        
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    # Press Enter to finalize the input
                    print("Input text:", input_text)
                    input_text = ""  # Clear the text after pressing Enter
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Remove the last character
                else:
                    input_text += event.unicode  # Add the typed character to the input text
    
    # Draw the background
    screen.fill((255, 255, 255))
    
    # Draw the input box (changing color if active)
    color = (0, 0, 0) if active else (200, 200, 200)
    pygame.draw.rect(screen, color, input_rect, 2)

    # Render the text
    text_surface = font.render(input_text, True, (0, 0, 0))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
