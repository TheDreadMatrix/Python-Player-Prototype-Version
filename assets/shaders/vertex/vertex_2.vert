#include custom_instance_vertex

void main(){
    gl_Position = getPosition();

    gotoFragment();

}