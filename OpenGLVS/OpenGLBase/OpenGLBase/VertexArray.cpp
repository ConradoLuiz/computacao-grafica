#include <VertexArray.h>

VertexArray::VertexArray() 
	: m_offset(0), m_countBuffers(0)
{
	glGenVertexArrays(1, &m_RendererID);
}

VertexArray::~VertexArray()
{
	glDeleteVertexArrays(1, &m_RendererID);
}

void VertexArray::Bind() const 
{
	glBindVertexArray(m_RendererID);
}

void VertexArray::Unbind() const
{
	glBindVertexArray(0);
}

void VertexArray::AddBuffer(const VertexBuffer& vbo, const VertexBufferLayout& layout)
{
	Bind();
	vbo.Bind();
	const std::vector<VertexBufferElement>& elements = layout.GetElements();
	unsigned int offset = 0;

	for (unsigned int i = 0; i < elements.size(); i++) {
		VertexBufferElement element = elements[i];

		glEnableVertexAttribArray(i + m_countBuffers);
		glVertexAttribPointer(i + m_countBuffers, element.count, element.type, element.normalized, layout.GetStride(), (const void*) offset);
				
		offset += element.count * element.size;
	}
	m_countBuffers++;
}

