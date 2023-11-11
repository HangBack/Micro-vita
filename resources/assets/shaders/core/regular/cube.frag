# version 330 core

uniform sampler2D textureSampler;

in vec2 texture_coord;
in vec3 object_color;
in vec3 light_color;
flat in int color_status;

out vec4 out_color;

vec3 lightColor;
vec4 final_texture;

void main(){
    final_texture = texture2D(textureSampler, texture_coord);

    if (
        light_color.x < 0.05 && 
        light_color.y < 0.05 && 
        light_color.z < 0.05
    ) 
        lightColor = vec3(0.05);
    else 
        lightColor = light_color;

    switch(color_status){
        case 0:
            out_color = vec4(vec3(1.0) * object_color, 1.0);
            break;
        case 1:
            out_color = final_texture * vec4(lightColor, 1.0);
            break;
    }
}