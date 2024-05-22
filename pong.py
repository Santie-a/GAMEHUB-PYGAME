def play_pong(local = False):
	# Librería de tiempo para generar pausas.
	from time import sleep

	# Librería de python que permite crear juegos con gráficos.
	import pygame

	# Librería random para que el inicio sea aleactorio.
	from random import randint

	# Variables de inicio.
	ball_direction = -1 if randint(0, 1) == 0 else 1
	multiplier = 1
	x_vel, y_vel = 5, randint(-2, 2)
	score_a, score_b = 0, 0

	# Configuración de pygame y ventana.
	width, height = 1280, 720
	pygame.init()
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption("PONG")
	clock = pygame.time.Clock()
	game_active = True

	# Fuentes.
	font = pygame.font.Font('fonts/Montserrat-ExtraLight.ttf', 100)
	font_small = pygame.font.Font('fonts/Montserrat-ExtraLight.ttf', 40)

	# Gráficos de la pantalla inicial.
	start_image = pygame.image.load('images/pong/start.png').convert()

	start_text_surf = font_small.render("Press SPACE to play", True, 'white')
	start_text_rect = start_text_surf.get_rect(midtop = (width / 2, height / 2 + 50))

	start_text2_surf = font_small.render("Press ESC to return to the main hub", True, 'white')
	start_text2_rect = start_text2_surf.get_rect(midtop = (width / 2, height / 2 + 100))

	# Gráficos del programa principal: Surf (Surface) para la imágen en si misma; Rect (Rectangle) para manejo de posición y colisiones.
	background = pygame.image.load('images/pong/background.png').convert()

	paddle1_surf = pygame.image.load('images/pong/paddle.png').convert_alpha()
	paddle1_rect = paddle1_surf.get_rect(center = (100, height / 2))

	paddle2_surf = pygame.image.load('images/pong/paddle.png').convert_alpha()
	paddle2_rect = paddle1_surf.get_rect(center = (width - 100, height / 2))

	ball_surf = pygame.image.load('images/pong/ball.png').convert_alpha()
	ball_rect = ball_surf.get_rect(center = (width / 2, height / 2))

	score_a_text_surf = font.render(str(score_a), True, 'white')
	score_a_text_rect = score_a_text_surf.get_rect(midtop = (width / 2 - 80, 30))

	score_b_text_surf = font.render(str(score_b), True, 'white')
	score_b_text_rect = score_b_text_surf.get_rect(midtop = (width / 2 + 80, 30))

	# Gráficos para mostar el ganador.
	winner_text_surf = font.render("WINNER", True, 'white')
	winner_text_rect = winner_text_surf.get_rect(center = (width / 2, height / 2 - 40))

	play_again_text_surf = font_small.render("SPACE to play again", True, 'white')
	play_again_text_rect = play_again_text_surf.get_rect(center = (width / 2, height / 2 + 55))

	# Variable para manejar la escena que se muestra en pantalla.
	scene = 'start'

	# Funciones para organizar el bucle principal.

	# Renderizar la página de inicio.
	def render_start():
		screen.blit(start_image, (0, 0))
		screen.blit(start_text_surf, start_text_rect)
		screen.blit(start_text2_surf, start_text2_rect)

	# Renderizar el programa principal (Actualiza la imágen que contiene los puntajes).
	def render_main():
		screen.blit(background, (0, 0))
		screen.blit(paddle1_surf, paddle1_rect)
		screen.blit(paddle2_surf, paddle2_rect)
		screen.blit(ball_surf, ball_rect)
		score_a_text_surf = font.render(str(score_a), True, 'white')
		score_b_text_surf = font.render(str(score_b), True, 'white')
		screen.blit(score_a_text_surf, score_a_text_rect)
		screen.blit(score_b_text_surf, score_b_text_rect)

	# Mover las raquetas (Evita que se salgan del marco ilustrado por el fondo).
	def move_paddles(keys):
		if keys[pygame.K_w] and paddle1_rect.top >= 35: paddle1_rect.top -= 10
		if keys[pygame.K_s] and paddle1_rect.bottom <= height - 35: paddle1_rect.bottom += 10
		if keys[pygame.K_UP] and paddle2_rect.top >= 35: paddle2_rect.top -= 10
		if keys[pygame.K_DOWN] and paddle2_rect.bottom <= height - 35: paddle2_rect.bottom += 10

	# Mueve la pelota vertical y horizontalmente teniendo en cuenta el multiplicador.
	def move_ball(direction, x_vel, y_vel, multiplier):
		if direction == -1:
			ball_rect.left -= x_vel * multiplier
			ball_rect.top += y_vel
		else:
			ball_rect.right += x_vel * multiplier
			ball_rect.top += y_vel

	# Evita que se salga por los bordes superiores (Si se mantiene dentro del marco retorna la misma velocidad en y, de lo contrario invierte la velocidad para que cambie la dirección y la retorna).
	def ball_pos(y_vel):
		if ball_rect.centery < 40:
			ball_rect.centery = 40
			y_vel *= -1
		elif ball_rect.centery > height - 40:
			ball_rect.centery = height - 40
			y_vel *= -1
		return y_vel

	# Verifica las colisiones con las raquetas
	def paddle_collide():
		if paddle1_rect.colliderect(ball_rect):
			ball_rect.centerx = 120
			return "paddle1"
		elif paddle2_rect.colliderect(ball_rect):
			ball_rect.centerx = width - 120
			return "paddle2"
		else:
			return None

	# Verifica si la pelota ha pasado algún límite (izquierda o derecha) y retorna identificadores según la posición. Si se mantiene dentro del marco regresa None.
	def check_scorer():
		if ball_rect.centerx < - 100:
			return "b"
		elif ball_rect.centerx > width + 100:
			return "a"
		else:
			return None

	# Establecer valores por defecto para empezar una nueva ronda o partida.
	def set_default():
		multiplier = 1
		x_vel, y_vel = 5, randint(-2, 2)
		ball_pos = (width / 2, height / 2)
		return multiplier, x_vel, y_vel, ball_pos

	# Bucle del programa principal.
	while game_active:
		# Revisar si hay algún evento (Salir del juego).
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_active = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					game_active = False

		# Verificar las teclas.
		keys = pygame.key.get_pressed()

		# Mostrar elementos en pantalla teniendo en cuenta la escena.
		if scene == 'start':
			render_start()
			if keys[pygame.K_SPACE]: scene = 'main'

		elif scene == 'main':
			render_main()

			# Verifica si hay algún ganador.
			if score_a < 3 and score_b < 3:
				# Mueve las raquetas si algúna tecla se está presionando.
				move_paddles(keys)

				# Verifica la posición de la pelota.
				y_vel = ball_pos(y_vel)

				# Verifica si alguna raqueta hace contacto con la pelota. Si hay contacto invierte la dirección en x y añade velocidad a la pelota.
				p_collide = paddle_collide()
				if p_collide == "paddle1":
					ball_direction *= -1
					multiplier += 0.2
					y_vel = (ball_rect.centery - paddle1_rect.centery) * 0.15 + randint(-3, 3) * (multiplier * 0.1)
				elif p_collide == "paddle2":
					ball_direction *= -1
					multiplier += 0.2
					y_vel = (ball_rect.centery - paddle2_rect.centery) * 0.15 + randint(-3, 3) * (multiplier * 0.1)

				# Mueve la pelota en función de todos los cambios hechos anteriormente.
				move_ball(ball_direction, x_vel, y_vel, multiplier)
			
				# Verifica si algún jugador hizo punto. Si es así establece valores por defecto e introduce un sleep.
				scorer = check_scorer()
				if scorer:
					if scorer == 'a': score_a += 1
					elif scorer == 'b': score_b += 1
					multiplier, x_vel, y_vel, ball_rect.center = set_default()
					sleep(1)
			
			# De lo contrario algún jugador supero el puntaje definido.
			else:
				# Ubica el texto de ganador en su lado.
				if score_a > score_b:
					winner_text_rect.centerx = width / 4 + 40
					play_again_text_rect.centerx = width / 4 + 75
				else:
					winner_text_rect.centerx = width * (3/4) - 40
					play_again_text_rect.centerx = width * (3/4) - 15

				# Muestra el texto
				screen.blit(winner_text_surf, winner_text_rect)
				screen.blit(play_again_text_surf, play_again_text_rect)

				# Si está en esta pantalla y se pulsa el espacio, se reinicia el juego.
				if keys[pygame.K_SPACE]:
					score_a, score_b = 0, 0
					multiplier, x_vel, y_vel, ball_rect.center = set_default()

		# Actualizar la pantalla (60FPS).
		pygame.display.update()
		clock.tick(60)

	# Finalizar el proceso.
	if local: pygame.quit()

if __name__ == '__main__':
	play_pong(True)