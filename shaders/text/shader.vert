#version 330 core

#define ATLAS_SIZE vec2(512, 502)

layout(location = 0) in vec2 inPos;
layout(location = 1) in vec2 inUV;
layout(location = 2) in vec2 inTextPos;
layout(location = 3) in vec2 inTextOffset;

layout(std140) uniform Projection{
    mat4 unProj;
};



uniform vec2 unPos;
uniform vec2 unScale;
uniform vec2 unAtlas;


uniform int unZayer;

out vec2 fUV;

void main(){

    vec2 finalPos = inPos * unScale + unPos + inTextPos;
    float finalZayer = -float(unZayer) * 0.01;

    gl_Position = unProj * vec4(finalPos, finalZayer, 1.0);

    vec2 finalTextOffset = inTextOffset / ATLAS_SIZE;
    vec2 finalAtlasSize = unAtlas / ATLAS_SIZE;

    fUV = inUV * finalAtlasSize + finalTextOffset;
}

