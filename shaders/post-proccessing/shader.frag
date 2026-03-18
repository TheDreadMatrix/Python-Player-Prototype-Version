#version 330 core
out vec4 FragColor;
in vec2 TexCoords;
uniform sampler2D tex;
uniform float time;

const float curvature = 0.09;
const float scanlineIntensity = 0.08;
const float noiseIntensity = 0.008;
const float chromaOffset = 0.0015;

float rand(vec2 co){
    return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453);
}

void main()
{
    vec2 uv = TexCoords * 2.0 - 1.0;
    uv += uv * (uv.x*uv.x + uv.y*uv.y) * curvature;
    uv = uv * 0.5 + 0.5;

    if(uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0){
        FragColor = vec4(0.0);
        return;
    }

    vec3 color;
    color.r = texture(tex, uv + vec2(chromaOffset, 0.0)).r;
    color.g = texture(tex, uv).g;
    color.b = texture(tex, uv - vec2(chromaOffset, 0.0)).b;

    float scanline = sin(uv.y * 1080.0) * scanlineIntensity;
    float noise = (rand(uv + time) - 0.5) * noiseIntensity;

    color -= scanline;
    color += noise;
    color *= 0.8;

    FragColor = vec4(color * vec3(1, 0.9, 0.8), 1.0);
}