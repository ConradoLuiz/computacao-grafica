#version 330 core

in vec3 colorToFragmentShader;

void main(void)
{
	gl_FragColor = vec4(colorToFragmentShader, 1.0);
}