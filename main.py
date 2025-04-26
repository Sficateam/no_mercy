import pygame
import character
from world import World
import constants
from game import Game

pygame.init()

game = Game()
game.setup()

running = True
game_state = 'start-komix'

while running:
	events = pygame.event.get()

	for event in events:
		if event.type == pygame.QUIT:
			running = False

	if game_state == 'start-komix':
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					game_state = 'play'
		game.screen.blit(pygame.image.load(f'assets/bg/bg1.png').convert_alpha(), (0, 0))
	
	elif game_state == 'play':

		keys = pygame.key.get_pressed() 
		
		game.screen.fill((80,145,166))
		game.screen.blit(game.surface, (0, 0))
		game.surface.fill((110,190,66))

    
		screen_scroll = game.hero.update(keys, game.world.obstacles, events, game.npc_group)
		game.world.update(screen_scroll)
		#game.npc.update(game.world.obstacles, game.hero, screen_scroll)
		game.world.draw(game.surface)

		for npc in game.npc_group:
			npc.move(game.world.obstacles, screen_scroll)
			npc.get_animation()
			npc.draw(game.surface)
			


		game.hero.draw(game.surface)
		
		game.hero.attack(game.npc_group)

		# if game.hero.is_dead():
		# 	game_state = 'game_over'
		

	elif game_state == 'game_over':
		for event in events:
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					game_state = 'menu'
					game.setup()
		game.screen.blit(pygame.image.load(f'assets/bg/go.png').convert_alpha(), (0, 0))

	game.clock.tick(constants.FPS) 
	pygame.display.flip()

pygame.quit()