#version 330 core
layout(location = 0) in vec2 aPos;
layout(location = 1) in vec2 aTexCoords;

layout(std140) uniform Projection{
    mat4 proj;
};

uniform vec2 scale;


out vec2 TexCoords;

void main()
{
    TexCoords = vec2(aTexCoords.x, 1.0 - aTexCoords.y);
    gl_Position = proj * vec4(aPos * scale, 0.0, 1.0);
}