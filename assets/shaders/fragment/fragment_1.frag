#include custom_fragment

in vec3 color_frag;
uniform float time;

void main(){

    gluminary_FragColor = texture(gluminary_Texture, gluminary_Coordinate) * vec4(color_frag, 1);

}