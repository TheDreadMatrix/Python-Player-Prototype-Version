#version 330

layout(location = 0) in vec2 inPos;
layout(location = 1) in vec2 inUV;


layout(std140) uniform Projection{
    mat4 unProj;
};


uniform vec2 unPos;
uniform vec2 unScale;

uniform int unZayer;

out vec2 fUV;

void main(){

    vec2 finalPos = inPos * unScale + unPos;
    float finalZayer = float(unZayer) * 0.01;

    gl_Position = unProj * vec4(finalPos, finalZayer, 1.0);


    fUV = inUV;
}