from MainClasss import Build, ImageButton
from random import choice


class DialogPerson(Build):
    def __init__(self, image, coord, missions, scena, dialog_funktion, texts=[]):
        super().__init__(image_out=image, coord=coord, scena=scena, layer_open=2, layer_close=2)
        self.mission = missions
        self.texts = texts
        self.end_dialog = False
        self.end_dialog_texts = [['Ну иди уже!'], ['Чего ждешь?'], ['Время не ждет, БЕГИ!']]
        self.button = ImageButton(self.image, self.get_coord(), self.start_dialog)
        self.alarm = False

    def start_dialog(self):
        if not self.end_dialog:
            self.mission.set_text(self.texts)
            self.end_dialog = True
        else:
            self.mission.set_text(choice(self.end_dialog_texts))

    def update(self, objects, main_chunk, camera):
        for object in objects:
            if object.is_type('MainHero') and not self.alarm and self.rect.colliderect(object.get_rect()):
                self.scena.add_button(self.button)
                self.alarm = True
            if object.is_type('MainHero') and self.alarm and not self.rect.colliderect(object.get_rect()):
                self.scena.remove_button(self.button)
                self.alarm = False