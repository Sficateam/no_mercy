import pygame
import pytmx


class World():
    def __init__(self, map):
        self.map_tmx = pytmx.load_pygame(f'assets/world/{map}.tmx')
        self.tile_images = []        
        self.obstacles = []
        self.positions = []
        
    def process_data(self):
        for layer in self.map_tmx.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_image = self.map_tmx.get_tile_image_by_gid(gid)
                    if tile_image:
                        tile = [tile_image, x * self.map_tmx.tilewidth, y * self.map_tmx.tileheight]
                        self.tile_images.append(tile)

            if layer.name == "collision":
                for x, y, gid in layer:
                    data = self.map_tmx.get_tile_properties_by_gid(gid)
                    if data:
                        rect = pygame.Rect(
                        x * self.map_tmx.tilewidth,
                        y * self.map_tmx.tileheight,
                        self.map_tmx.tilewidth,
                        self.map_tmx.tileheight
                    
                    )
                        self.obstacles.append(rect)

        positions =  self.map_tmx.get_layer_by_name("positions")
        for x, y, gid in positions:
            data = self.map_tmx.get_tile_properties_by_gid(gid)
            if data:
                rect = pygame.Rect(
                    x * self.map_tmx.tilewidth,
                    y * self.map_tmx.tileheight,
                    self.map_tmx.tilewidth,
                    self.map_tmx.tileheight
                )
                self.positions.append(rect)


    def draw(self, surface):
        for tile_image in self.tile_images:
            surface.blit(tile_image[0], (tile_image[1],tile_image[2]))


    def update(self, screen_scroll):
        for tile_image in self.tile_images:
            tile_image[1] += screen_scroll[0]
            tile_image[2] += screen_scroll[1]

        for obstacle in self.obstacles:
            obstacle.x += screen_scroll[0]
            obstacle.y += screen_scroll[1]
