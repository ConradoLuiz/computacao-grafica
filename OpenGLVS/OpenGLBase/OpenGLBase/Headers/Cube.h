#pragma once

#include <App.h>
#include <VertexArray.h>
#include <VertexBuffer.h>
#include <IndexBuffer.h>
#include <Mesh.h>
#include <SOIL2.h>

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

	unsigned int m_tex2d;

	VertexArray *m_vao;
	VertexBuffer *m_position_vbo;
	VertexBuffer *m_color_vbo;
	IndexBuffer *m_ebo;
};