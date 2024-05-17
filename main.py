# Importar Juegos
from pong import play_pong
from connect_four import play_connect_four

# Importar la clase Button para generar botones animados
from button import Button

# Marco de referencia
import pygame

# Constantes (Colores)
color1 = "#4E84A6"
color2 = "#60A4BF"
color3 = "#9AC7D9"
color4 = "#3F5259"
color5 = "#C2E0F2"

# Configuración de pygame y pantalla
width, height = 1280, 720
pygame.init()
font = pygame.font.Font('fonts/Montserrat-ExtraLight.ttf', 90)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Hall")
clock = pygame.time.Clock()
game_active = True

# Texto
game_hall_text_surf = font.render("GAME HALL", True, color4)
game_hall_text_rect = game_hall_text_surf.get_rect(midtop = (width / 2, 50))

# Botones para ejecutar los juegos
pong_button = Button(
	"PONG", 350, 100, (width // 2 - 175, height // 2 - 100), 3, color1, color2, color3, font, color4, play_pong
	)

connect_four_button = Button(
	"CONNECT4", 550, 100, (width // 2 - 275, height // 2 + 25), 3, color1, color2, color3, font, color4, play_connect_four
	)

def change_game_active():
	global game_active
	game_active = not game_active

exit_button = Button(
	"EXIT", 250, 100, (width - 275, height - 115), 3, color1, color2, color3, font, color4, change_game_active
	)

while game_active:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_active = False

	screen.fill(color5)
	screen.blit(game_hall_text_surf, game_hall_text_rect)
	pong_button.draw(screen)
	connect_four_button.draw(screen)
	exit_button.draw(screen)

	pygame.display.update()
	clock.tick(60)

pygame.quit()