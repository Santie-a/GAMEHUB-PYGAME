# Referencia: Clear Code - https://github.com/clear-code-projects/elevatedButton/blob/main/button.py

import pygame

class Button:
	def __init__(self, text, width, height, pos, elevation, color1, color2, color_hover, font, font_color, function):
		# Atributos principales
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elecation = elevation
		self.original_x_pos = pos[0]
		self.original_y_pos = pos[1]
		self.function = function
		self.color_hover = color_hover
		self.color1 = color1

		# Rectángulo superior
		self.top_rect = pygame.Rect(pos, (width, height))
		self.top_color = color1

		# Rectángulo inferior 
		self.bottom_rect = pygame.Rect(pos, (width, height))
		self.bottom_color = color2

		# Texto
		self.text_surf = font.render(text, True, font_color)
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self, screen):
		# Logica de elevación
		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
		self.top_rect.x = self.original_x_pos - self.dynamic_elecation
		self.text_rect.center = self.top_rect.center

		# Mostrar el rectángulo
		pygame.draw.rect(screen, self.bottom_color, self.bottom_rect)
		pygame.draw.rect(screen, self.top_color, self.top_rect)
		screen.blit(self.text_surf, self.text_rect)
		self.check_click()

	def check_click(self):
		mouse_pos = pygame.mouse.get_pos()

		# Verificar si la posición del mouse esta sobre el botón
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = self.color_hover
			# Verificar si se está oprimiendo el click izquierdo y cambia el estado del atributo 'pressed'
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
			# Si se oprimió y soltó el botón mientras el mouse se encuentra en la caja, ejecuta la función pasada como parámetro 
			else:
				self.dynamic_elecation = self.elevation
				if self.pressed == True:
					self.function()
					self.pressed = False
		else:
			self.dynamic_elecation = self.elevation
			self.top_color = self.color1
			self.pressed = False