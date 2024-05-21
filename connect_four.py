import pygame.mouse


def play_connect_four(Local = False):
	# Framework
	import pygame

	# Librería para manejos de tiempo
	from time import sleep

	# Constantes (Colores y separación para el tablero)
	color1 = "#1B4001"
	color2 = "#9BBF65"
	color3 = "#E9F2A7"
	x_sep = 165
	y_sep = 90

	# Configuración de pygame y pantalla
	width, height = 1280, 720
	pygame.init()
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption("CONNECT4")
	clock = pygame.time.Clock()
	game_active = True

	# Fuentes
	font = pygame.font.Font('fonts/Montserrat-ExtraLight.ttf', 100)
	font_small = pygame.font.Font('fonts/Montserrat-ExtraLight.ttf', 40)

	# Graficos de la pantalla inicial
	main_start_text_surf = font.render("CONNECT4", True, color1)
	main_start_text_rect = main_start_text_surf.get_rect(midtop = (width / 2, height / 2 - 120))

	start_text1_surf = font_small.render("Press SPACE to play", True, color1)
	start_text1_rect = start_text1_surf.get_rect(midtop = (width / 2, height / 2 + 25))

	start_text2_surf = font_small.render("Press ESC to return to the main hub", True, color1)
	start_text2_rect = start_text2_surf.get_rect(midtop = (width / 2, height / 2 + 75))

	# Graficos de la pantalla pricipal
	board_rect = pygame.Rect((60, 30), (width - 2 * 60, 580))

	dot1_surf = pygame.image.load('images/connect4/dot1.png').convert_alpha()

	dot2_surf = pygame.image.load('images/connect4/dot2.png').convert_alpha()

	dot3_surf = pygame.image.load('images/connect4/dot3.png').convert_alpha()

	turn_text_surf = font_small.render("It's Player 1 turn!", True, color1)
	turn_text_rect = turn_text_surf.get_rect(midbottom = (width / 2, height - 25))
 
	play_again_text_surf = font_small.render("SPACE to play again", True, color1)
	play_again_text_rect = play_again_text_surf.get_rect(bottomright = (width - 10, height - 25))

	full_row_text_surf = font_small.render("Row is full", True, color1)
	full_row_text_rect = full_row_text_surf.get_rect(bottomleft = (20, height - 25))

	# Funciones de lógica y mostrar elementos en pantalla.

	# Función que crea un tablero vacío con espacios que representan la ausencia de un token.
	def create_board():
		return [[" " for i in range(7)] for i in range(6)]

	# Función para añadir un token al tablero. Si la columna está llena, levanta un error que es atrapado por la estructura try-except que altera una variable para mostrar en pantalla que el movimiento no es válido
	def add_token(token, board, pos):
		i = -1
		
		if board[0][pos].strip():
			raise ValueError
		
		while True:
			if not board[i][pos].strip():
				board[i][pos] = token
				break
			else:
				i -= 1
			
		return board
	
	# Función que verifica las diferentes formas de ganar en Connect4
	def check_winner(board):
		# Check for rows
		for row in board:
			for i in range(4):
				if row[i] == "0" and row[i+1] == "0" and row[i+2] == "0" and row[i+3] == "0":
					return True
				elif row[i] == "1" and row[i+1] == "1" and row[i+2] == "1" and row[i+3] == "1":
					return True
			
		# Check for columns
		for i in range(3):
			for j in range(7):
				if board[i][j] == "0" and board[i+1][j] == "0" and board[i+2][j] == "0" and board[i+3][j] == "0":
					return True
				elif board[i][j] == "1" and board[i+1][j] == "1" and board[i+2][j] == "1" and board[i+3][j] == "1":
					return True
				
		# Check for diagonals (\)
		for i in range(3):
			for j in range(4):
				if board[i][j] == "0" and board[i+1][j+1] == "0" and board[i+2][j+2] == "0" and board[i+3][j+3] == "0":
					return True
				if board[i][j] == "1" and board[i+1][j+1] == "1" and board[i+2][j+2] == "1" and board[i+3][j+3] == "1":
					return True
				
		# Check for diagonals (/)
		for i in range(3):
			for j in range(3, 7):
				if board[i][j] == "0" and board[i+1][j-1] == "0" and board[i+2][j-2] == "0" and board[i+3][j-3] == "0":
					return True
				if board[i][j] == "1" and board[i+1][j-1] == "1" and board[i+2][j-2] == "1" and board[i+3][j-3] == "1":
					return True

		else:
			return False
	
	# Mostrar los elementos de la pantalla inicial
	def render_start():
		screen.blit(main_start_text_surf, main_start_text_rect)
		screen.blit(start_text1_surf, start_text1_rect)
		screen.blit(start_text2_surf, start_text2_rect)

	# Mostrar los elementos de la pantalla principal
	def render_board(board):
		pygame.draw.rect(screen, color3, board_rect, border_radius = 10)
		for i in range(len(board)):
			for j in range(len(board[i])):
				if board[i][j] == "0": 
					screen.blit(dot1_surf, (x_sep * j + 100, y_sep * i + 50))
				elif board[i][j] == "1":
					screen.blit(dot2_surf, (x_sep * j + 100, y_sep * i + 50))
				elif board[i][j] == " ":
					screen.blit(dot3_surf, (x_sep * j + 100, y_sep * i + 50))

	# Variables para el juego
	scene = "start"
	board = create_board()
	turn = 0
	is_valid = True
	winner = False

	# Bucle principal
	while game_active:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_active = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					game_active = False
					

		# Verificar las teclas.
		keys = pygame.key.get_pressed()
		mouse_pos = pygame.mouse.get_pos()
		mouse_pressed = pygame.mouse.get_pressed()

		# Color solido de fondo
		screen.fill(color2)

		# Mostrar elementos teniendo en cuenta la escena
		if scene == "start":
			render_start()
			if keys[pygame.K_SPACE]: scene = 'main'

		if scene == "main":
			render_board(board)
			screen.blit(turn_text_surf, turn_text_rect)

			# Si en el tablero no hay ganador, espera a un input del usuario. Cuando haya uno, verifica si hay ganador
			if not winner:
				if mouse_pressed[0] and board_rect.collidepoint(mouse_pos):
					col = ((mouse_pos[0] - 40)  // 7 // 25) % 7 # Encontrar la columna adecuada basado en la posición del mouse
					if turn == 0:
						try:
							board = add_token("0", board, col)
							turn_text_surf = font_small.render("It's Player 2 turn!", True, color1)
							turn = 1
							is_valid = True
							winner = check_winner(board)
							sleep(0.5)
						except:
							is_valid = False
					else:
						try:
							board = add_token("1", board, col)
							turn_text_surf = font_small.render("It's Player 1 turn!", True, color1)
							turn = 0
							is_valid = True
							winner = check_winner(board)
							sleep(0.5)
						except:
							is_valid = False
				
				if not is_valid:
					screen.blit(full_row_text_surf, full_row_text_rect)
			
			# Si hay ganador, esperar si los jugadores quieren jugar de nuevo
			else:
				screen.blit(play_again_text_surf, play_again_text_rect)

				if turn:
					turn_text_surf = font_small.render("Player 1 wins!", True, color1)
				else:
					turn_text_surf = font_small.render("Player 2 wins!", True, color1)

				if keys[pygame.K_SPACE]:
					board = create_board()
					turn = 0
					turn_text_surf = font_small.render("It's Player 1 turn!", True, color1)
					winner = False
					
						
		pygame.display.update()
		clock.tick(60)

	if Local: pygame.quit()

if __name__ == '__main__':
	play_connect_four(True)