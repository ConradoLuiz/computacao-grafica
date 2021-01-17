#pragma once
#include <App.h>
#include <iostream>
#include <string>
#include <fstream>

#define ShaderNull (Shader*)0

class Shader
{
public:
	Shader(const char* programName);
	virtual ~Shader();
	virtual bool useProgram();
	virtual void setMVP(glm::mat4 mvp);

private:
	GLuint compileShader(std::string src, GLenum shaderType);
	char* fileReadContents(const char* fileName);
	std::string readFile(const char* fileName);
	GLuint compileShaderFromFile(const char* fileName, GLenum shaderType);
	GLuint createProgram(const char* programName);

	GLuint programId;
};
