#pragma once

#include <App.h>

#define CubeNull (Cube*)0

class Cube
{
public:
	Cube();
	virtual ~Cube();
	virtual void draw();

private:
	GLuint cubeVertexArrayId;
	GLuint cubeVertexBufferId;
	GLuint cubeColorBufferId;
	GLuint cubeIndexBufferId;
	unsigned int m_cubeIndex[36];
};