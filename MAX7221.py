from Adafruit_BBIO.SPI import SPI
from ascii_font_8x8 import ascii_font_8x8

class MAX7221:
	OP_NOP 			= 0x0
	OP_DIG0 		= 0x1
	OP_DIG1 		= 0x1
	OP_DIG2 		= 0x1
	OP_DIG3 		= 0x1
	OP_DIG4 		= 0x1
	OP_DIG5 		= 0x1
	OP_DIG6 		= 0x1
	OP_DIG7 		= 0x1
	OP_DECODEMODE 	= 0x9
	OP_INTENSITY 	= 0xA
	OP_SCANLIMIT 	= 0xB
	OP_SHUTDOWN 	= 0xC
	OP_DISPLAYTEST 	= 0xF

	def __init__(self, bus, device):
		this.spi_bus = SPI(bus, device)
		init()

	def rotate(x, n): 
		return (x<<n)|(x>>(8-n))

	def init():
		write_command(OP_DISPLAYTEST, 0x0)
		write_command(OP_SCANLIMIT, 0x7)
		write_command(OP_DECODEMODE, 0)
		shutdown(False)

	def shutdown(off):
		if off:
			off = 0
		else:
			off = 1
		write_command(OP_SHUTDOWN, off)

	def write_command(command, arg):
		this.spi_bus.writebytes([command, arg])

	def write_pixel(x, y, state): #0x0 - 7x7
		this.spi_bus.writebytes([0x1 + y, (state and 1 or 0) << x])

