# version 330 core

uniform sampler2D textureSampler;

in vec2 texture_coord;
in vec4 object_color;
in vec4 light_color;
flat in int color_status;

out vec4 out_color;

vec4 lightColor;
vec4 objectColor;
vec4 finalTexture;

void main(){
    finalTexture = texture2D(textureSampler, texture_coord);
    lightColor = light_color;
    objectColor = object_color;

    bool drop_condition = 
        lightColor.x < 0.00005 &&
        lightColor.y < 0.00005 &&
        lightColor.z < 0.00005 &&
        abs(lightColor.w - 1.0) < 0.000001;

    if (drop_condition)
        lightColor = vec4(1.0);
    else
        for(int i = 0; i < 4; i++)
            if (lightColor[i] < 0.05)
                lightColor[i] = 0.05;

    switch(color_status){
        case 0:
            out_color = vec4(lightColor) * vec4(objectColor);
            break;
        case 1:
            out_color = finalTexture * vec4(lightColor);
            break;
    }
}