import pygame
from pygame import mixer
import character
from world import World
import constants
from game import Game

mixer.init()
pygame.init()

game = Game()
game.setup()

pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
hit_fx = pygame.mixer.Sound("assets/audio/hit.mp3")
hit_fx.set_volume(0.5)


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
			npc.update()
			

		game.hero.draw(game.surface)
		
		game.hero.attack(game.npc_group, hit_fx)

		if game.npc_count(game.num_of_infected)[0] == 1:
			game_state = 'loose'

		if game.npc_count(game.num_of_infected)[1]:
			game_state = 'win'
		# if game.hero.is_dead():
		# 	game_state = 'game_over'
		

	elif game_state == 'win' or game_state == 'loose':
		for event in events:
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if event.button == 1:
						game_state = 'menu'
						game.setup()
		if game_state == 'win':
			game.screen.blit(pygame.image.load(f'assets/bg/win.png').convert_alpha(), (0, 0))
		if game_state == 'loose':
			game.screen.blit(pygame.image.load(f'assets/bg/go.png').convert_alpha(), (0, 0))

	game.clock.tick(constants.FPS) 
	pygame.display.flip()

pygame.quit()