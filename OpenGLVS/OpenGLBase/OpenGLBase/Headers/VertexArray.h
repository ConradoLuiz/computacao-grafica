#pragma once

#include <VertexBuffer.h>
#include <VertexBufferLayout.h>

class VertexArray
{
public:
	VertexArray();
		
	~VertexArray();

	void AddBuffer(const VertexBuffer& vbo, const VertexBufferLayout& layout);

	void Bind() const;
	void Unbind() const;
private:
	unsigned int m_RendererID;
	unsigned int m_offset;
	unsigned int m_countBuffers;
};