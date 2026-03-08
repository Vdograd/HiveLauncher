from PIL import Image
import os
from ..utils.configurator import Configurator

class TextureSize64:
    def __init__(self):
        self.configurator = Configurator()

    def resize_pixel_art(self, img, target_size, method='NEAREST'):
        resample_method = Image.Resampling.LANCZOS
        if method == 'NEAREST' and target_size[0] % img.size[0] == 0:
            return img.resize(target_size, resample_method)
        img_resized = img.resize(target_size, resample_method)
        return img_resized

    def resize_with_grid(self, img, target_size):
        if img.mode == 'RGBA':
            result = Image.new('RGBA', target_size, (255, 255, 255, 0))
        else:
            result = Image.new('RGB', target_size, (255, 255, 255))

        for x in range(img.width):
            for y in range(img.height):
                pixel = img.getpixel((x, y))
                scale_x = target_size[0] // img.width
                scale_y = target_size[1] // img.height
                for dx in range(scale_x):
                    for dy in range(scale_y):
                        result.putpixel((x * scale_x + dx, y * scale_y + dy), pixel)
        return result

    def save_texture(self, nickname):
        input_path = f"{self.configurator.static_folder}\\head_skins_response\\{nickname}\\{nickname}.png"
        output_dir = f"{self.configurator.static_folder}\\head_skins_response\\{nickname}"
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            return e

        img = Image.open(input_path)

        square_size = 8
        square_number = 10
        row = (square_number - 1) // 8
        col = (square_number - 1) % 8

        left = col * square_size
        top = row * square_size
        square_8x8 = img.crop((left, top, left + square_size, top + square_size))


        multipliers = [6, 18]
        for i, multiplier in enumerate(multipliers):
            target_size = (8 * multiplier, 8 * multiplier)
            resized = square_8x8.resize(target_size, Image.Resampling.NEAREST)
            
            if i == 0: 
                final_size = (50, 50)
                resized = resized.resize(final_size, Image.Resampling.NEAREST)
            else:
                final_size = (150, 150)
                resized = resized.resize(final_size, Image.Resampling.NEAREST)
            
            filename = os.path.join(output_dir, f"{nickname}_{final_size[0]}x{final_size[1]}.png")
            resized.save(filename)

class TextureSize1024:
    def __init__(self):
        self.configurator = Configurator()
    def resize_image(self, img, target_size):
        original_mode = img.mode
        
        if original_mode == 'RGBA':
            new_img = Image.new('RGBA', target_size, (255, 255, 255, 0))
            img_resized = img.copy()
        else:
            new_img = Image.new('RGB', target_size, (255, 255, 255))
            img_resized = img.convert('RGB')
        
        original_width, original_height = img.size
        target_width, target_height = target_size
        
        ratio = min(target_width / original_width, target_height / original_height)
        new_size = (int(original_width * ratio), int(original_height * ratio))
        
        img_resized = img_resized.resize(new_size, Image.Resampling.LANCZOS)
        
        position = (
            (target_width - new_size[0]) // 2,
            (target_height - new_size[1]) // 2
        )
        
        if original_mode == 'RGBA':
            new_img.paste(img_resized, position, img_resized)
        else:
            new_img.paste(img_resized, position)
        
        return new_img

    def save_texture(self, nickname):
        input_path = f"{self.configurator.static_folder}\\head_skins_response\\{nickname}\\{nickname}.png"
        output_dir = f"{self.configurator.static_folder}\\head_skins_response\\{nickname}"
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            return e

        img = Image.open(input_path)
        square_10 = img.crop((128, 128, 256, 256))

        sizes = [(50, 50), (150, 150)]
        for size in sizes:
            resized = self.resize_image(square_10, size)
            output_path = os.path.join(output_dir, f"{nickname}_{size[0]}x{size[1]}.png")
            resized.save(output_path)