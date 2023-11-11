#version 330 core

uniform sampler2D textureSampler;

in vec2 texture_coord;
out vec4 out_color;

void main()
{
    out_color = texture(textureSampler, texture_coord);
}
