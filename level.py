import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height
from tiles import Tile, StaticTile, Crate, Coin, Palm
from enemy import Enemy
from decorations import Sky, Water, Clouds


class Level:
    def __init__(self, level_data, surface):
        # general set up
        self.display_surface = surface
        self.world_shift = -3

        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crates setup
        crates_layout = import_csv_layout(level_data['crates'])
        self.crates_sprites = self.create_tile_group(crates_layout, 'crates')

        # coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coin_layout, 'coins')

        # foreground palms
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg palms')

        # background palms
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg palms')

        # enemies
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')

        # decorations
        self.sky = Sky(7)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 40, level_width)
        self.cloud = Clouds(300, level_width, 20)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('./graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('./graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    if type == 'coins':
                        if val == '0':
                            sprite = Coin(tile_size, x, y, './graphics/coins/gold')
                        if val == '1':
                            sprite = Coin(tile_size, x, y, './graphics/coins/silver')

                    if type == 'fg palms':
                        if val == '0':
                            sprite = Palm(tile_size, x, y, './graphics/terrain/palm_small')
                        if val == '1':
                            sprite = Palm(tile_size, x, y, './graphics/terrain/palm_large')

                    if type == 'bg palms':
                        sprite = Palm(tile_size, x, y, './graphics/terrain/palm_bg')

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if val != '0':
                        pass
                    if val == '1':
                        hat_surface = pygame.image.load('./graphics/character/hat.png')
                        sprite = StaticTile(tile_size, x, y, hat_surface)
                        self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def run(self):
        # decoration
        self.sky.draw(self.display_surface)

        # Clouds
        self.cloud.draw(self.display_surface, self.world_shift)

        # background palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # crate
        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # foreground palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        # coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        # player sprites
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface, self.world_shift)













