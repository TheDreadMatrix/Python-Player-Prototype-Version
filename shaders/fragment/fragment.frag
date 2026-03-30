#version 330 core


in vec2 GclUv;

out vec4 GclColor;

uniform sampler2D GclTexture;




void main(){
    GclColor = texture(GclTexture, GclUv);
}