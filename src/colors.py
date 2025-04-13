# PICO-8 Palette
P8_BLACK = (0, 0, 0)
P8_DARK_BLUE = (29, 43, 83)
P8_DARK_PURPLE = (126, 37, 83)
P8_DARK_GREEN = (0, 135, 81)
P8_BROWN = (171, 82, 54)
P8_DARK_GREY = (95, 87, 79)
P8_LIGHT_GREY = (194, 195, 199)
P8_WHITE = (255, 241, 232)
P8_RED = (255, 0, 77)
P8_ORANGE = (255, 163, 0)
P8_YELLOW = (255, 236, 39)
P8_GREEN = (0, 228, 54)
P8_BLUE = (41, 173, 255)
P8_LAVENDER = (131, 118, 156)
P8_PINK = (255, 119, 168)
P8_LIGHT_PEACH = (255, 204, 170)

# HTML 4.01 web colors
WEB_BLACK = (0, 0, 0)
WEB_SILVER = (192, 192, 192)
WEB_GRAY = (128, 128, 128)
WEB_WHITE = (255, 255, 255)
WEB_MAROON = (128, 0, 0)
WEB_RED = (255, 0, 0)
WEB_PURPLE = (128, 0, 128)
WEB_FUCHSIA = (255, 0, 255)
WEB_GREEN = (0, 128, 0)
WEB_LIME = (0, 255, 0)
WEB_OLIVE = (128, 128, 0)
WEB_YELLOW = (255, 255, 0)
WEB_NAVY = (0, 0, 128)
WEB_BLUE = (0, 0, 255)
WEB_TEAL = (0, 128, 128)
WEB_AQUA = (0, 255, 255)

BACKGROUND_COLOR = WEB_BLACK
TRANSPARENT_COLOR = WEB_BLACK
TIME_COLOR = P8_WHITE


def color_from_hex(hex_color):
    """
    Convert a hex color string to an RGB tuple.
    """
    hex_color = hex_color.replace("0x", "").replace("#", "")
    rgb = (
        (int(hex_color, 16) >> 16) & 255,
        (int(hex_color, 16) >> 8) & 255,
        int(hex_color, 16) & 255,
    )

    return rgb
