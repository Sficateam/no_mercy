import pygame
from pygame import mixer
import character
from character import Npc
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
				if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
					game_state = 'play'
					game.reset_time()
		game.intro_animation()
	
	elif game_state == 'play':

		game.sounds.play_anouc() 
		
		game.screen.fill((128,128,128))
		game.screen.blit(game.surface, (0, 0))
		game.surface.fill((128,128,128)) 

    
		screen_scroll = game.hero.update(game.world1.obstacles, events, game.npc_group)
		game.world1.update(screen_scroll)
		game.world1.draw(game.surface)

		for npc in game.npc_group:
			npc.update(game.world1.obstacles, screen_scroll, game.sounds.dying)
			npc.draw(game.surface)

		game.hero.draw(game.surface)
		
		game.hero.attack(game.npc_group, game.sounds.attack)

		game.sounds.play_cough_sounds()
		game.sounds.play_eat_sound()

		elapsed_time = (pygame.time.get_ticks() - game.game_time)
		elapsed_time_seconds = elapsed_time // 1000

		font = pygame.font.Font(None, 36)
		time_display_text = font.render(f'Time: {abs(elapsed_time_seconds - constants.TIME_LIMIT_SECONDS)} s', True, (255, 255, 255))
		game.screen.blit(time_display_text, (0, 0))

		eliminated_text = font.render(f'Eliminated: {character.Npc.count_infected} / {constants.NUMBER_OF_INFECTED_NPC * 2}', True, (255, 255, 255))
		game.screen.blit(eliminated_text, (constants.SCREEN_WIDTH - 200, 0))

		if game.npc_count(constants.NUMBER_OF_INFECTED_NPC)[0] == 1:
			now = pygame.time.get_ticks()
			if now - game.hero.last_attack > constants.LAST_DEATH_IN_GAME:
				game.hero.last_attack = now	
				game_state = 'loose'

		if game.npc_count(constants.NUMBER_OF_INFECTED_NPC)[1]:
			now = pygame.time.get_ticks()
			if now - game.hero.last_attack > constants.LAST_DEATH_IN_GAME:
				game.hero.last_attack = now	
				game_state = 'win'

		if elapsed_time > constants.TIME_LIMIT:
			game_state = 'time-up'

		
	elif game_state == 'win' or game_state == 'loose' or game_state == 'time-up':
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
					game_state = 'start-komix'
					game.sounds.stop_music()					
					game.setup()
					game.sounds.unplayed = True
		
										
		if game_state == 'win':
			game.screen.blit(pygame.image.load(f'assets/bg/Ending-win.png').convert_alpha(), (0, 0))
			game.sounds.play_final_sound(game.sounds.win)
		if game_state == 'loose':
			game.screen.blit(pygame.image.load(f'assets/bg/Kill-innocent.png').convert_alpha(), (0, 0))
			game.draw_subtitles('GAME OVER')
			game.sounds.play_final_sound(game.sounds.loose)
		if game_state == 'time-up':
			game.screen.blit(pygame.image.load(f'assets/bg/Time-over.png').convert_alpha(), (0, 0))
			game.draw_subtitles('GAME OVER')
			game.sounds.play_final_sound(game.sounds.escape)
	game.clock.tick(constants.FPS) 
	pygame.display.flip()

pygame.quit()