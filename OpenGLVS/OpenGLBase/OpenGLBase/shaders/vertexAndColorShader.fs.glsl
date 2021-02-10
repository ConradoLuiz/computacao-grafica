#version 330 core

out vec4 color;

in vec2 TexCoords;
in vec3 colorToFragmentShader;

uniform sampler2D texture;

void main(void)
{
//	 gl_FragColor = vec4(colorToFragmentShader, 1.0);
	color = texture2D(texture, TexCoords);
}