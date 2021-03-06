#pragma once
#include <globals.h>
#include <glm/gtx/polar_coordinates.hpp>
#include <VertexArray.h>
#include <VertexBuffer.h>
#include <IndexBuffer.h>
#include <Mesh.h>
#include <Transform.h>
#include <SOIL2.h>

class Sphere
{
public: 
	Sphere(glm::vec3 pos = glm::vec3(1.0f), float radius = 5, unsigned int resolution = 3);
	~Sphere();

	inline float GetRadius() { return m_radius; }
	void draw();
	 
	Transform* transform;

private:
	float m_radius;
	unsigned int m_resolution;
	void GenerateVertices();
	glm::vec3 polarToCart(glm::vec3 &polar);

	std::vector<Vertex> vertices;
	std::vector<unsigned int> indeces;

	unsigned int m_tex2d;
	VertexArray *m_vao;
	VertexBuffer *m_vbo;
	IndexBuffer *m_ebo;

};

