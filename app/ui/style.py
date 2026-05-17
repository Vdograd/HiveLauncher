from ..utils.build import build

def set_style(window, name: str):
    try:
        with open(f"{build.theme_folder}\\{name}.css", "r", encoding="ansi") as file:
            style = file.read()
            window.setStyleSheet(style)
    except Exception as e:
        raise e