#version 330 core

out vec4 color;

in vec3 colorToFragmentShader;
in vec2 TexCoords;
in vec3 Normal;

uniform sampler2D texture;

void main(void)
{
//	gl_FragColor = vec4(colorToFragmentShader, 1.0);
//	color = texture2D(texture, TexCoords);
//	color = vec4(abs(Normal), 1.0);
	color = vec4(1.0);
}