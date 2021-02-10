#version 330 core

layout (location=0) in vec3 position;
layout (location=1) in vec3 color;
layout (location=2) in vec2 a_TexCoord;

uniform mat4 MVP;
out vec3 colorToFragmentShader;
out vec2 TexCoords;

void main(void)
{
	gl_Position = MVP * vec4(position, 1.0);
	colorToFragmentShader = color;
	TexCoords = a_TexCoord;
}