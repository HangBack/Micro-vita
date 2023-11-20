# version 330 core

layout(location = 0)in vec3 verticle;
layout(location = 1)in vec3 position;
layout(location = 2)in vec3 scale;
layout(location = 3)in vec3 absolute_color;
layout(location = 4)in vec2 texCoord;

uniform mat4 tran;
uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;


out vec3 object_color;
out vec2 texture_coord;

void main(){
    // gl_Position = view * model * vec4(position, 1.0);   
    // gl_Position = projection * view * vec4(position, 1.0);
    gl_Position = projection * view * model * vec4(verticle * scale + position, 1.0);   
    // gl_Position = vec4(position, 1.0);   
    object_color = absolute_color;
    texture_coord = texCoord;
}