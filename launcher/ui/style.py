from ..utils.configurator import Configurator

configurator = Configurator()
def set_style(window, name):
    try:
        with open(f"{configurator.theme_folder}\\{name}.css", "r", encoding="ansi") as file:
            style = file.read()
            window.setStyleSheet(style)
    except Exception as e:
        raise e