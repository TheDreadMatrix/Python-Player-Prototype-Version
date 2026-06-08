#include vertex_atlas_extension //instancing atlas INSpos INStexture_size INTtexture_position
#include vertex_texture_array_extension // using samplerArray2D
#include vertex_texture_array_instansing_extension // INS
#include vertex_instancing_extension // INSrgb INSpos INSflipx 
#include vertex //DEFAULT



void main(){

    OutColor = texture(DM_Texture, DM_Coord) * vec4(rgb, alpha);
}