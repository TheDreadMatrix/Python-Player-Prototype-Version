#include custom_fragment_texture

uniform vec2 textureSize;
uniform float pixelSize;

void main()
{
    vec2 uv = gluminary_Coordinate;

    vec2 pixelUV = pixelSize / textureSize;

    uv = floor(uv / pixelUV) * pixelUV;

    gluminary_FragColor = texture(gluminary_Texture, uv) * vec4(gluminary_r, gluminary_g, gluminary_b, gluminary_a);
}