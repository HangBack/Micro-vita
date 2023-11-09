# version 330 core

uniform sampler2D textureSampler;

in vec2 texture_coord;
in vec3 object_color;
in vec3 light_color;
flat in int color_status;

out vec4 out_color;

void main(){
    switch(0){
        case 0:
            out_color = vec4(light_color * object_color, 1.0);
            break;
        case 1:
            out_color = vec4(texture2D(textureSampler, texture_coord));
            break;
    }
}