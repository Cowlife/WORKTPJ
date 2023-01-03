import pygame


class AnimationTransitionComponent:
    def __init__(self, sprite_group_list, list_of_sprites, map_rect, screen, keys, keys_damage, player):
        self.sprite_group_list = sprite_group_list
        self.list_of_sprites = list_of_sprites
        self.map_rect = map_rect
        self.screen = screen
        self.keys = keys
        self.keys_damage = keys_damage
        self.player = player

    def update_animation(self, lst_spr, i, idle_return=False):
        removal = self.list_of_sprites[0][i]
        addition = self.list_of_sprites[lst_spr][i]
        if idle_return:
            self.list_of_sprites[lst_spr][i].attack_animation = not self.list_of_sprites[lst_spr][i].attack_animation
            removal, addition = addition, removal
        self.sprite_group_list[0].remove(removal)
        self.sprite_group_list[0].add(addition)
        self.list_of_sprites[lst_spr][i].current_sprite = 0
        self.list_of_sprites[lst_spr][i].attack_stance = not self.list_of_sprites[lst_spr][i].attack_stance

    def enemy_spawner(self, rect, enemy):
        if rect.x < self.screen.get_size()[0]:
            pygame.draw.rect(self.screen, (200, 0, 0), rect)
            self.screen.blit(enemy.image, rect)
            enemy.text_printer(25, f"{int(enemy.target_health / 200) + 1}", (222, 109, 11), rect, self.screen)
            # counters to stronger enemies
            enemy.update()
        rect.x -= 5

    def enemy_collision(self, rect, enemy, is_attacked):
        removal_info = {
            True: [enemy, 200, 10, 1, "attack sound effect.wav"],
            False: [self.player, enemy.amount, 0, 0, "damage sound effect.wav"]
        }
        entity = removal_info.get(is_attacked)
        entity[0].get_damage(entity[1])
        self.player.score += entity[2]
        if is_attacked and entity[0].target_health > 0:
            rect.x += 100
        else:
            self.map_rect[0].remove(rect)
            self.map_rect[1].remove(enemy)
        self.player.chain = (self.player.chain * entity[3]) + entity[3]
        return pygame.mixer.Sound(f"assets/sound_effects/{entity[4]}")

    def animation_transitions(self):
        for i in range(-3, 0):
            for lst_spr in range(1, len(self.list_of_sprites)):
                if self.list_of_sprites[lst_spr][i].attack_animation:
                    self.update_animation(lst_spr, i, True)

        for rect, enemy in zip(self.map_rect[0], self.map_rect[1]):
            self.enemy_spawner(rect, enemy)
            for key in zip(self.keys, self.keys_damage):
                if key[0].rect.colliderect(rect) and not key[0].handled:  # not for actually skill

                    # Transition(self._menu, self._options)
                    sound_effecting = self.enemy_collision(rect, enemy, True)

                    for i in range(-3, 0):
                        if key[0].key == self.keys[i].key:
                            effects = {
                                'red': [3, 0],
                                'heal': [3, enemy.amount],
                            }
                            animation_update = effects.get(enemy.name, [1, 0])
                            self.player.get_health(animation_update[1])
                            self.update_animation(animation_update[0], i)

                    pygame.mixer.Sound.play(sound_effecting)
                    key[0].handled = True

                elif key[1].rect.colliderect(rect) and key[1].handled:

                    sound_effecting = self.enemy_collision(rect, enemy, False)

                    for i in range(-3, 0):
                        if key[1].key == self.keys_damage[i].key:
                            self.update_animation(2, i)

                    pygame.mixer.Sound.play(sound_effecting)

