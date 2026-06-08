#version 330 core

layout(location = 0) in vec2 inPos;
layout(location = 1) in vec2 inCoord;
layout(location = 2) in vec2 INSpos;
layout(location = 3) in vec2 INStexture_size;
layout(location = 4) in vec2 INStexture_pos;


layout(std140) uniform Projection{
    mat4 unProj;
};


uniform vec2 unPos;
uniform vec2 unSize;
uniform int unLayer;

uniform bool unFlipx;
uniform bool unFlipy;


out vec2 DM_Coord;

void main(){

    vec2 finalPos = inPos * unSize + unPos + INSpos;
    float finalZayer = float(unlayer) * 0.01;

    gl_Position = unProj * vec4(finalPos, finalZayer, 1.0);


    DM_Coord = inCoord;
}