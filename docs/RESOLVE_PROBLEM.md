



onRender:

    self.renderer.render("base:tex", pos, size, r, g, b, a, layer, mode, shader)
    self.renderer.draw_rect(r, g, b, a, pos, size, layer, mode, shader)

    self.renderer.renderInstance()