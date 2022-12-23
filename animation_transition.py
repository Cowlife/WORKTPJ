class AnimationTransitionComponent:
    def __init__(self, sprite_group_list, list_of_sprites):
        self.sprite_group_list = sprite_group_list
        self.list_of_sprites = list_of_sprites

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
