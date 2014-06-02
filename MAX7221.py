from Adafruit_BBIO.SPI import SPI
from ascii_font_8x8 import ascii_font_8x8
import Display


class MAX7221(Display.Display):

    def __init__(self, bus, device):
    	super(MAX7221, self).__init__(8, 8)
        SPI(bus, device).mode = 0
        self.spi_bus = SPI(bus, device)
        self.buf = [0, 0, 0, 0, 0, 0, 0, 0]

        self.OP_NOP = 0x0
        self.OP_DIG0 = 0x1
        self.OP_DIG1 = 0x2
        self.OP_DIG2 = 0x3
        self.OP_DIG3 = 0x4
        self.OP_DIG4 = 0x5
        self.OP_DIG5 = 0x6
        self.OP_DIG6 = 0x7
        self.OP_DIG7 = 0x8
        self.OP_DECODEMODE = 0x9
        self.OP_INTENSITY = 0xA
        self.OP_SCANLIMIT = 0xB
        self.OP_SHUTDOWN = 0xC
        self.OP_DISPLAYTEST = 0xF

        self.init()

    def rotate(self, x, n):
        return (x << n) | (x >> (8 - n))

    def init(self):
        self.write_command(self.OP_DISPLAYTEST, 0x0)
        self.write_command(self.OP_SCANLIMIT, 0x7)
        self.write_command(self.OP_DECODEMODE, 0x0)
        self.shutdown(False)
        self.update_display()

    def shutdown(self, off):
        if off:
            off = 0
        else:
            off = 1
        self.write_command(self.OP_SHUTDOWN, off)

    def write_spi(self, reg, data):
        self.spi_bus.writebytes([reg, data])

    def write_command(self, command, arg):
        self.write_spi(command, arg)

    def write_display(self, buffer):
        for col in range(0, len(buffer)):
            self.write_spi(col + 0x1, buffer[col])

    def update_display(self):
        self.write_display(self.buf)

    def draw_pixel(self, x, y, color):
        if color == 1:
            self.buf[y] = self.buf[y] | (1 << x)
        elif color == 0:
            self.buf[y] = self.buf[y] & ~(1 << x)
        self.update_display()

    def draw_fast_hline(self, x, y, w, color):
    	self.write_spi(0x1 + y, (0xFF >> (8 - w)) << x)
