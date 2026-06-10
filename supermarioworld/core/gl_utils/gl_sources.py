
# Default shader
_DEFAULT_VERTEX_SOURCE = """
        #version 330 core
        in vec2 gluminary_input_Position;
        in vec2 gluminary_input_Coordinate;

        layout(std140) uniform Projection{
            mat4 gluminary_Projection;
        };

        uniform vec2 gluminary_Position;
        uniform vec2 gluminary_Size;

        uniform bool gluminary_Flx;
        uniform bool gluminary_Fly;

        out vec2 gluminary_Coordinate;


        vec4 getPosition(){
            vec2 pre_position = gluminary_input_Position * gluminary_Size + gluminary_Position;
            
            vec4 final_position = gluminary_Projection * vec4(pre_position, 0, 1);
            return final_position;
        }

        void giveFragmentUvCoordinate(){
            vec2 finalCoord = gluminary_input_Coordinate;

            if (gluminary_Flx) {
                finalCoord.x = 1.0 - finalCoord.x;
            }

            if (gluminary_Fly) {
                finalCoord.y = 1.0 - finalCoord.y;
            }

            gluminary_Coordinate = finalCoord;
        }


        void main(){
            gl_Position = getPosition();
            
            giveFragmentUvCoordinate();
        }
    """


_DEFAULT_FRAGMENT_SOURCE = """
        #version 330 core

        in vec2 gluminary_Coordinate;
        out vec4 gluminary_FragColor;

        uniform sampler2D gluminary_Texture;

        uniform float gluminary_r;
        uniform float gluminary_g;
        uniform float gluminary_b;
        uniform float gluminary_a;

        
        vec4 getColorFromTexture(){
            return texture(gluminary_Texture, gluminary_Coordinate) * vec4(gluminary_r, gluminary_g, gluminary_b, gluminary_a);
        }


        void main(){
            gluminary_FragColor = getColorFromTexture();
        }
    """


# Mesh shaders
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


# Instance shaders
_DEFAULT_VERTEX_SOURCE_INSTANCE = """
        #version 330 core

in vec2 gluminary_input_Position;
in vec2 gluminary_input_Coordinate;


in vec2 gluminary_instance_Position;
in vec2 gluminary_instance_Size;

in float gluminary_instance_Flx;
in float gluminary_instance_Fly;



layout(std140) uniform Projection {
    mat4 gluminary_Projection;
};


uniform vec2 gluminary_Position;

out vec2 gluminary_Coordinate;

vec4 getPosition(){
    vec2 pre_position = gluminary_input_Position * gluminary_instance_Size + gluminary_instance_Position + gluminary_Position;
            
    vec4 final_position = gluminary_Projection * vec4(pre_position, 0, 1);
    return final_position;
}

void giveFragmentUvCoordinate(){
    vec2 finalCoord = gluminary_input_Coordinate;

    if (gluminary_instance_Flx > 0) {
        finalCoord.x = 1.0 - finalCoord.x;
    }

    if (gluminary_instance_Fly > 0) {
        finalCoord.y = 1.0 - finalCoord.y;
    }

    gluminary_Coordinate = finalCoord;
}



void main() {
    gl_Position = getPosition();

    giveFragmentUvCoordinate();
}
    """