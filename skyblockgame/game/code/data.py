from utils import load_assets, load_levels, load_audio

# Adat osztály, a tároláshoz
class Data:

    def __init__(self):
        self.level_images = load_assets()
        self.audio = load_audio()
        self.levels = load_levels()
        self.current_level = 1
        self.map = self.levels[self.current_level]
