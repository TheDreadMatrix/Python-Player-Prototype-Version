


class Thunder:
    def __init__(self):
        self.flash = 0.0

    def strike(self):
        self.flash = 1.0

    def update(self, dt):
        self.flash = max(0.0, self.flash - 0.5 * dt)

    def apply(self, r, g, b):
        t = self.flash

        return (
            r + (1.0 - r) * t,
            g + (1.0 - g) * t,
            b + (1.0 - b) * t
        )