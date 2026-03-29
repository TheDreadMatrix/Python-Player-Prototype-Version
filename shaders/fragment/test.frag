#include vertex
#pragma text.vert

//#version 330 core
//
//in vec2 GclUv;
//out vec4 GclColor;
//
//
//uniform sampler2D GclTexture;
//
//

uniform float num;

void main(){
    GclColor = texture(GclTexture, GclUv) * vec4(num);
}

