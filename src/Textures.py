import arcade
from PIL import Image

class Textures:
    TILE_SIZE: int = 16
    ATLAS_SIZE: int = 256
    TILES_PER_SIDE: int = ATLAS_SIZE // TILE_SIZE
    
    def __init__(self, texture: str):
        self.image = Image.open(texture).convert('RGBA')
        
        self.textures: dict = {}
        
        for y in range(Textures.TILES_PER_SIDE):
            for x in range(Textures.TILES_PER_SIDE):
                left: int = x * Textures.TILE_SIZE
                top: int = y * Textures.TILE_SIZE
                right: int = left + Textures.TILE_SIZE
                bottom: int = top + Textures.TILE_SIZE
                
                region = self.image.crop((left, top, right, bottom))
                region = region.convert('RGBA')
                texture = arcade.Texture(region, hit_box_algorithm=None)
                self.textures[(x, y)] = texture
        
    def get_texture(self, x: int, y: int) -> arcade.Texture:
        return self.textures.get((x, y))
    
    def get_texture_wh(self, x: int, y: int, width: int, height: int, flipped: bool = False) -> arcade.Texture:
        """Получает текстуру из атласа с указанными размерами"""
        left: int = x
        top: int = y
        right: int = left + (width)
        bottom: int = top + (height)
        
        region = self.image.crop((left, top, right, bottom))
        region = region.convert('RGBA')
        tex = arcade.Texture(region, hit_box_algorithm=None)
        if (flipped): tex = tex.flip_horizontally()
        
        return tex