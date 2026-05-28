

_DEFAULT_VERTEX_SOURCE = """
        #version 330 core
        in vec2 inPos;
        in vec2 inCoord;

        layout(std140) uniform Projection{
            mat4 unProj;
        };

        uniform vec2 unPos;
        uniform vec2 unSize;

        uniform bool unFlx;
        uniform bool unFly;

        out vec2 DM_Coord;

        void main(){
            vec2 finalPos = inPos * unSize + unPos;
            
            gl_Position = unProj * vec4(finalPos, 0.0, 1.0);
            
            vec2 finalCoord = inCoord;

            if (unFlx) {
                finalCoord.x = 1.0 - finalCoord.x;
            }

            if (unFly) {
                finalCoord.y = 1.0 - finalCoord.y;
            }

            DM_Coord = finalCoord;
        }
    """


_DEFAULT_FRAGMENT_SOURCE = """
        #version 330 core

        in vec2 DM_Coord;
        out vec4 OutColor;

        uniform sampler2D DM_Texture;

        uniform float r;
        uniform float g;
        uniform float b;
        uniform float a;

        void main(){
            OutColor = texture(DM_Texture, DM_Coord) * vec4(r, g, b, a);
        }
    """


_DEFAULT_VERTEX_SOURCE_MESH = """
        #version 330 core

        in vec2 inPos;

        layout(std140) uniform Projection{
            mat4 unProj;
        };

        uniform vec2 unPos;
        uniform vec2 unSize;

        void main(){
            vec2 finalPos = inPos * unSize + unPos;
            
            gl_Position = unProj * vec4(finalPos, 0.0, 1.0);
        }

"""


_DEFAULT_FRAGMENT_SOURCE_MESH = """
        #version 330 core

        out vec4 OutColor;

        uniform float r;
        uniform float g;
        uniform float b;
        uniform float a;

        void main(){
            OutColor = vec4(r, g, b, a);
        }
"""



_DEFAULT_VERTEX_SOURCE_INSTANCE = """
        #version 330 core

in vec2 inPos;
in vec2 inCoord;

/* INSTANCE DATA */

in vec2 instancePos;
in vec2 instanceSize;

in float instanceFlx;
in float instanceFly;


/* UBO */

layout(std140) uniform Projection {
    mat4 unProj;
};

out vec2 DM_Coord;

void main() {

    /* =========================
       INSTANCE TRANSFORM
    ========================= */

    vec2 finalPos =
        inPos * instanceSize +
        instancePos;

    gl_Position =
        unProj *
        vec4(finalPos, 0.0, 1.0);

    /* =========================
       UV
    ========================= */

    vec2 finalCoord = inCoord;

    if (instanceFlx > 0.5) {
        finalCoord.x = 1.0 - finalCoord.x;
    }

    if (instanceFly > 0.5) {
        finalCoord.y = 1.0 - finalCoord.y;
    }

    DM_Coord = finalCoord;
}
    """