#include vertex




uniform vec3 setColor;

void main(){
    vec4 color = texture(GclTexture, GclUv) * vec4(setColor, 1);

    if (color.a <= 0.0)
        discard;

    GclColor = color;

}