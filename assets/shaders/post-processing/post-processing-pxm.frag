#include custom_fragment


uniform vec2 textureSize;
uniform float pixelSize;

void main()
{
    if (pixelSize == 1){
        gluminary_FragColor = texture(gluminary_Texture, gluminary_Coordinate);
        return;
    }

    vec2 uv = gluminary_Coordinate;

    vec2 pixelUV = pixelSize / textureSize;

    uv = floor(uv / pixelUV) * pixelUV;

    gluminary_FragColor = texture(gluminary_Texture, uv);
}