import os
import shutil
import ctypes
import win32con
from screeninfo import get_monitors
from PIL import Image, ImageDraw, ImageFont


def get_wallpaper():
    ubuf = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER, len(ubuf), ubuf, 0)
    return ubuf.value


def set_wallpaper(path):
    changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
    ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, path, changed)


def hex2rgba(color):
    if color[0] == "#":
        color = color[1:]

    if len(color) == 3:
        return int(color[0] + color[0], 16), int(color[1] + color[1], 16), int(color[2] + color[2], 16), 255
    elif len(color) == 6:
        return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16), 255
    elif len(color) == 8:
        return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16), int(color[6:8], 16)
    else:
        raise Exception("Invalid hex-color: " + color)


class Panel:
    def __init__(self, outer=30, gutter=20):
        self.boundaries = get_monitors()[0].width, get_monitors()[0].height

        self.padding = 10
        self.main_axis = "left"
        self.cross_axis = "top"
        self.text = "<blank panel>"
        self.color = "#000"
        self.background = "#ffffff80"
        self.font = None

        self.outer = outer
        self.gutter = gutter
        self.column_width = (self.boundaries[0] - 2 * self.outer - 2 * self.gutter) // 3
        self.row_height = (self.boundaries[1] - 2 * self.outer - 2 * self.gutter) // 3

    @staticmethod
    def render(panels, saved_wallpaper=None):
        modified_wallpaper = None
        for index, panel in enumerate(panels):
            prefer_saved = index == 0 and saved_wallpaper is not None
            saved_wallpaper, modified_wallpaper = panel.draw_wallpaper(saved_wallpaper, modified_wallpaper, prefer_saved)

        set_wallpaper(os.path.abspath(modified_wallpaper))
        return saved_wallpaper

    def set_padding(self, padding):
        self.padding = padding

    def set_position(self, main_axis, cross_axis):
        if main_axis not in ["left", "middle", "right"] or cross_axis not in ["top", "middle", "bottom"]:
            raise Exception("Invalid value for one of the axises!")

        self.main_axis = main_axis
        self.cross_axis = cross_axis

    def set_font(self, font_family, font_size):
        self.font = ImageFont.truetype(font_family, font_size)

    def set_text(self, text, color="#000"):
        self.text = text.strip()
        self.color = hex2rgba(color)

    def set_background(self, background="#fff"):
        self.background = hex2rgba(background)

    def fit_image(self, image):
        ratio = image.width / image.height

        if ratio > self.boundaries[0] / self.boundaries[1]:
            image = image.resize((int(self.boundaries[1] * ratio), self.boundaries[1]))
            left = int((image.width - self.boundaries[0]) / 2)
            right = image.width - left
            image = image.crop((left, 0, right, image.height))
        else:
            image = image.resize((self.boundaries[0], int(self.boundaries[0] / ratio)))
            top = int((image.height - self.boundaries[1]) / 2)
            bottom = image.height - top
            image = image.crop((0, top, image.width, bottom))

        return image

    def convert_text_into_multiline(self, draw):
        collapsed_text = ""
        for line in self.text.split("\n"):
            collapsed_line = ""

            for word in line.split(" "):
                line_length = draw.textlength(collapsed_line + word, font=self.font)
                if line_length <= self.column_width - 2 * self.padding:
                    collapsed_line += word + " "
                else:
                    collapsed_text += collapsed_line + "\n"
                    collapsed_line = ""

            collapsed_text += "\n"

        return collapsed_text.replace("\n\n", "\n")

    def calculate_background_layout(self, draw, multiline_text):
        if self.main_axis == "left":
            x = self.outer
        elif self.main_axis == "middle":
            x = self.outer + self.column_width + self.gutter
        else:
            x = self.boundaries[0] - self.outer - self.column_width

        if self.cross_axis == "top":
            y = self.outer
        elif self.cross_axis == "middle":
            y = self.outer + self.row_height + self.gutter
        else:
            y = self.boundaries[1] - self.outer - self.row_height

        (left, top, right, bottom) = draw.multiline_textbbox((x, y), multiline_text, font=self.font)
        right += 2 * self.padding
        bottom += 2 * self.padding
        height = bottom - top

        if bottom > self.boundaries[1]:
            if self.cross_axis == "middle":
                bottom = self.boundaries[1] // 2 + height // 2
                top = bottom - height
            if self.cross_axis == "bottom":
                bottom = self.boundaries[1] - self.outer
                top = bottom - height

        return left, top, right, bottom

    def calculate_text_layout(self, background_layout):
        return background_layout[0] + self.padding, background_layout[1] + self.padding

    def draw_wallpaper(self, saved_wallpaper=None, modified_wallpaper=None, prefer_saved=False):
        if not self.font:
            raise Exception("Please set a valid font!")

        if not os.path.exists("../wallpaper/"):
            os.mkdir("../wallpaper/")

        if saved_wallpaper and prefer_saved:
            wallpaper = saved_wallpaper
        elif modified_wallpaper:
            wallpaper = modified_wallpaper
        else:
            wallpaper = get_wallpaper()
            if not os.path.exists("../wallpaper/saved/"):
                os.mkdir("../wallpaper/saved/")
            saved_wallpaper = "wallpaper/saved/" + os.path.basename(wallpaper)
            shutil.copyfile(wallpaper, saved_wallpaper)

        if not os.path.exists("../wallpaper/modified/"):
            os.mkdir("../wallpaper/modified/")

        modified_wallpaper = "wallpaper/modified/" + os.path.basename(wallpaper)

        image = self.fit_image(Image.open(wallpaper))
        draw = ImageDraw.Draw(image, "RGBA")

        multiline_text = self.convert_text_into_multiline(draw)
        background_layout = self.calculate_background_layout(draw, multiline_text)
        text_layout = self.calculate_text_layout(background_layout)

        draw.rounded_rectangle(background_layout, fill=self.background, radius=5)
        draw.multiline_text(text_layout, multiline_text, font=self.font, fill=self.color)

        image.save(modified_wallpaper)

        return saved_wallpaper, modified_wallpaper


def __test_locally():
    import lorem

    panels = []
    for main_axis in ["left", "middle", "right"]:
        for cross_axis in ["top", "middle", "bottom"]:
            panel = Panel()
            panel.set_position(main_axis, cross_axis)
            panel.set_padding(20)
            panel.set_background("#000000c0")
            panel.set_font("fonts/Poppins-Regular.ttf", 24)
            panel.set_text(lorem.paragraph(), color="#fff")

            panels.append(panel)

    Panel.render(panels, "wallpaper/saved/pexels-deden-dicky-ramdhani-5755160.jpg")


# if __name__ == "__main__":
#     test_locally()
