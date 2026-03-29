#version 330 core
#pragma text.vert

in vec2 GclUv;
out vec4 GclColor;

uniform sampler2D GclTexture;
uniform float a;

void main(){
    GclColor = texture(GclTexture, GclUv) * vec4(a);

}