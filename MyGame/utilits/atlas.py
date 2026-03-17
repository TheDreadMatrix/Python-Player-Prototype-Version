from array import array




class FontAtlas:
    def __init__(self):
        self.char_dict = {}

        max_chars = 1024
        self.font_list = array("f", [0.0] * (max_chars * 4))
        self.instance_count = 0

        symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ.,x-!c*=:$#0123456789"
        x = 88
        for s in symbols:
            self.char_dict[s] = [x, 128]
            x += 8



    def generateTextListByte(self, text: str, *, start_x: float=0, start_y: float=0, space_x: float=100, space_y: float=120, new_line_x: float=0):
        x, y = start_x, start_y
        idx = 0
        for char in text:
            if char == "\n":
                y += space_y
                x = start_x + new_line_x
                continue
            if char not in self.char_dict:
                continue  

            self.font_list[idx] = x
            self.font_list[idx+1] = y
            self.font_list[idx+2] = self.char_dict[char][0]
            self.font_list[idx+3] = self.char_dict[char][1]

            idx += 4
            x += space_x

        self.instance_count = idx // 4
        return self.font_list[:idx] 