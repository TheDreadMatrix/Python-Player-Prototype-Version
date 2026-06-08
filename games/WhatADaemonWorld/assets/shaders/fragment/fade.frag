#version 330 core



uniform vec3 Color;
uniform float Alpha;

out vec4 GclColor;


void main(){



    GclColor = vec4(Color, Alpha);
}