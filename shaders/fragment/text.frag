#version 330 core


in vec2 GclUv;
out vec4 GclColor;

uniform sampler2D GclTexture;

bool isIgnoredColor(vec3 color) {
    vec3 c1 = vec3(0.4118, 0.5961, 0.0235); 
    vec3 c2 = vec3(1.0, 0.5020, 1.0);       

    float threshold = 0.01;

    bool matchC1 = distance(color, c1) < threshold;
    bool matchC2 = distance(color, c2) < threshold;

    return matchC1 || matchC2;
}

void main(){
    vec4 color = texture(GclTexture, GclUv);

    if (isIgnoredColor(color.rgb))
        discard;

    GclColor = color;

}