class Display(object):

    def __init__(self, w, h):
        self.width = w
        self.height = h

    def draw_pixel(self, x, y, color):
        pass

    def draw_circle(self, x0, y0, r, color):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x, y = 0, r

        self.draw_pixel(x0, y0 + r, color)
        self.draw_pixel(x0, y0 - r, color)
        self.draw_pixel(x0 + r, y0, color)
        self.draw_pixel(x0 - r, y0, color)

        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y

            x += 1
            ddF_x += 2
            f += ddF_x

            self.draw_pixel(x0 + x, y0 + y, color)
            self.draw_pixel(x0 + y, y0 + x, color)
            self.draw_pixel(x0 + x, y0 - y, color)
            self.draw_pixel(x0 + y, y0 - x, color)
            self.draw_pixel(x0 - x, y0 + y, color)
            self.draw_pixel(x0 - y, y0 + x, color)
            self.draw_pixel(x0 - x, y0 - y, color)
            self.draw_pixel(x0 - y, y0 - x, color)

    def draw_circle_helper(self, x0, y0, r, corner, color):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x, y = 0, r

        while x < y:
            if f > 0:
                y -= 1
                ddF_y += 2
                f += ddF_y

            x += 1
            ddF_x += 2
            f += ddF_x

            if corner & 0x4:
                self.draw_pixel(x0 + x, y0 + y, color)
                self.draw_pixel(x0 + y, y0 + x, color)
            if corner & 0x2:
                self.draw_pixel(x0 + x, y0 - y, color)
                self.draw_pixel(x0 + y, y0 - x, color)
            if corner & 0x8:
                self.draw_pixel(x0 - x, y0 + y, color)
                self.draw_pixel(x0 - y, y0 + x, color)
            if corner & 0x1:
                self.draw_pixel(x0 - x, y0 - y, color)
                self.draw_pixel(x0 - y, y0 - x, color)

    def fill_circle(self, x0, y0, r, color):
        self.draw_fast_vline(x0, y0 - r, 2 * r - 1, color)
        self.fill_circle_helper(x0, y0, r, 3, 0, color)

    def fill_circle_helper(self, x0, y0, r, corner, delta, color):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x, y = 0, r

        while x < y:
            if f > 0:
                y -= 1
                ddF_y += 2
                f += ddF_y

            x += 1
            ddF_x += 2
            f += ddF_x

            if corner & 0x1:
                self.drawFastVLine(x0 + x, y0 - y, 2 * y + 1 + delta, color)
                self.drawFastVLine(x0 + y, y0 - x, 2 * x + 1 + delta, color)

            if corner & 0x1:
                self.drawFastVLine(x0 - x, y0 + y, 2 * y + 1 + delta, color)
                self.drawFastVLine(x0 - y, y0 + x, 2 * x + 1 + delta, color)

    def draw_line(self, x0, y0, x1, y1, color):
        steep = abs(y1 - y0) > abs(x1 - x0)

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 - y1, y0

        dx, dy = x1 - x0, abs(y1 - y0)

        err = dx // 2
        ystep = -1

        if y0 < y1:
            ystep = 1

        while x0 <= x1:
            if steep:
                self.draw_pixel(y0, x0, color)
            else:
                self.draw_pixel(x0, y0, color)

            err -= dy
            if err < 0:
                y0 += ystep
                err += dx
            x0 += 1

    def draw_rect(self, x, y, w, h, color):
        self.draw_fast_hline(x, y, w, color)
        self.draw_fast_hline(x, y + h - 1, w, color)
        self.draw_fast_vline(x, y, h, color)
        self.draw_fast_vline(x + w - 1, y, h, color)

    def draw_fast_vline(self, x, y, h, color):
        self.draw_line(x, y, x, y + h - 1, color)

    def draw_fast_hline(self, x, y, w, color):
        self.draw_line(x, y, x + w - 1, y, color)

    def fill_rect(self, x, y, w, h, color):
        for i in range(x, x + w):
            self.draw_fast_vline(i, y, h, color)

    def fill_screen(self, color):
        self.fill_rect(0, 0, self.width, self.height, color)

    def draw_round_rect(self, x, y, w, h, r, color):
        self.draw_fast_hline(x + r, y, w - 2 * r, color)
        self.draw_fast_hline(x + r, y + h - 1, w - 2 * r, color)
        self.draw_fast_vline(x, y + r, h - 2 * r, color)
        self.draw_fast_vline(x + w - 1, y + r, h - 2 * r, color)

        self.draw_circle_helper(x + r, y + r, r, 1, color)
        self.draw_circle_helper(x + w - r - 1, y + r, r, 2, color)
        self.draw_circle_helper(x + w - r - 1, y + h - r - 1, r, 4, color)
        self.draw_circle_helper(x + r, y + h - r - 1, r, 8, color)

    def fill_round_rect(self, x, y, w, h, r, color):
        self.fill_rect(x + r, y, w - 2 * r, h, color)

        self.fill_circle_helper(
            x + w - r - 1, y + r, r, 1, h - 2 * r - 1, color)
        self.fill_circle_helper(
            x + r, y + r, r, 2, h - 2 * r - 1, color)

    def draw_triangle(self, x0, y0, x1, y1, x2, y2, color):
        self.draw_line(x0, y0, x1, y1, color)
        self.draw_line(x1, y1, x2, y2, color)
        self.draw_line(x2, y2, x0, y0, color)
