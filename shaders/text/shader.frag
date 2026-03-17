#version 330 core

#define IGNORE_COLOR_1 vec3(6.0/255.0, 152.0/255.0, 6.0/255.0)
#define IGNORE_COLOR_2 vec3(255.0/255.0, 128.0/255.0, 255.0/255.0)

in vec2 fUV;

out vec4 fragColor;

uniform vec3 color_change;
uniform sampler2D tex;


bool defineColor(vec3 color, vec3 target){
    float threshold = 0.03; 
    return all(lessThan(abs(color - target), vec3(threshold)));
}


void main(){
    vec4 OutColor = texture(tex, fUV);

    if (defineColor(OutColor.rgb, IGNORE_COLOR_1) || defineColor(OutColor.rgb, IGNORE_COLOR_2))
        discard;

   
    if (defineColor(OutColor.rgb, vec3(1.0, 1.0, 1.0)))
        OutColor.rgb = color_change;

    fragColor = OutColor;

}