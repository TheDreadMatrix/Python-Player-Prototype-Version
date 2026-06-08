#version 330 core

layout(location = 0) in vec2 inPos;

layout(std140) uniform Projection{
    mat4 unProj;
};

uniform vec2 unPos;
uniform vec2 unScale;
uniform int unZayer;

void main(){
    vec2 finalPos = inPos * unScale + unPos;
    float finalZayer = float(unZayer) * 0.01;

    gl_Position = unProj * vec4(finalPos, finalZayer, 1.0);
}
