#version 330 core


in vec2 fUV;

out vec4 fragColor;

uniform vec3 color_change;
uniform sampler2D tex;




void main(){
    vec4 texColor = texture(tex, fUV);

   
    if (texColor.a <= 0.0)
        discard;

    fragColor = texColor * vec4(color_change, 1.0);

}