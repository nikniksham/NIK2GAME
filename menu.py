from Framework import Application, Widget, load_image, Button, scale_to


def run_menu():
    REPOSITORY = 'sprite/User_Interface/'
    spase = 10
    size_screen = [1920, 1080]
    app = Application(size_screen, fill_color=(255, 255, 255), full_screen=True)
    fon = scale_to(load_image(REPOSITORY + 'fon 1.png'), size_screen)
    button_off_image = load_image(REPOSITORY + 'Game.png', -1)
    button_on_image = load_image(REPOSITORY + 'Game_active.png', -1)
    button_exit_image = load_image(REPOSITORY + 'Out_active.png', -1)
    button_exit_off_image = load_image(REPOSITORY + 'Out.png', -1)

    def play_funk(then):
        then.app.running = False
        print(then.app.running)

    def exit_funk(then):
        quit()

    fon = Widget(fon, (0, 0))
    button_play = Button([button_off_image, button_on_image], (spase, spase * 10), play_funk)
    button_exit = Button([button_exit_off_image, button_exit_image], (spase, spase * 11 + button_on_image.get_size()[0]), exit_funk)

    app.add_widget(fon, 0)
    app.add_widget(button_exit)
    app.add_widget(button_play)

    app.run()