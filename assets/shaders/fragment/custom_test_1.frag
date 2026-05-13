#include vertex

uniform float time;

void main()
{
    vec2 uv = DM_Coord;

    // переливание
    float r = sin(time + uv.x * 6.0) * 0.5 + 0.5;
    float g = sin(time * 1.2 + uv.y * 6.0) * 0.5 + 0.5;
    float b = sin(time + uv.x * 3.0 + uv.y * 3.0) * 0.5 + 0.5;

    vec3 rainbow = vec3(r, g, b);

    vec4 tex = texture(DM_Texture, uv);

    OutColor = vec4(
        tex.rgb * rainbow * rgb,
        tex.a * alpha
    );
}