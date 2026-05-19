


Single drawing -> Atlas modrawing -> Animation ([CutOut])




self.RESOURCES.registerAtlas("my-atlas", path, filter, anisotropy)
self.RESOURCES.registerTexture("key-texture", path, filter, anisotropy)
self.RESOURCES.registerCutOutTexture("cut-out", path, xywh, filter, anisotropy)

self.RESOURCES._registerRawTexture("raw", mgl.Texture)

self.RESOURCES.registerShader("my-custom", path)


self.MAIN.forget()

self.MAIN.submitAtlas("my-atlas", )
self.MAIN.submit("key-texture", size, position, rgba, layer, flipx, flipy, shader="my-custom")


self.MAIN.render()