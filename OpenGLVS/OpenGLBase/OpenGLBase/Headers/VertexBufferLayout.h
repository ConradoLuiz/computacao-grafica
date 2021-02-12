#pragma once
#include <globals.h>
#include <Mesh.h>

struct VertexBufferElement
{
	unsigned int type;
	unsigned int count;
	unsigned int size;
	bool normalized;

	static unsigned int GetSizeOfType(unsigned int type)
	{
		switch (type)
		{
			case GL_FLOAT:         return 4;
			case GL_UNSIGNED_INT:  return 4;
			case GL_UNSIGNED_BYTE: return 1;
		}
		return 0;
	}

};

class VertexBufferLayout
{
public:
	VertexBufferLayout()
		: m_Stride(0) {};

	template<typename T>
	void Push(unsigned int count)
	{
		static_assert(false);
	}

	template<>
	void Push<float>(unsigned int count)
	{
		VertexBufferElement element = { GL_FLOAT, count, VertexBufferElement::GetSizeOfType(GL_FLOAT), false };
		
		m_Elements.push_back(element);
		m_Stride += count * element.size;
	}

	template<>
	void Push<unsigned int>(unsigned int count)
	{
		VertexBufferElement element = { GL_FLOAT, count, VertexBufferElement::GetSizeOfType(GL_UNSIGNED_INT), false };
		
		m_Elements.push_back(element);
		m_Stride += count * element.size;
	}

	template<>
	void Push<unsigned char>(unsigned int count)
	{
		VertexBufferElement element = { GL_FLOAT, count, VertexBufferElement::GetSizeOfType(GL_UNSIGNED_BYTE), false };

		m_Elements.push_back(element);
		m_Stride += count * element.size;
	}

	template<typename T>
	void Push()
	{
		static_assert(false);
	}

	template <>
	void Push<glm::vec4>()
	{
		unsigned int count = 4;
		VertexBufferElement element = { GL_FLOAT, count, 16, false };
		
		m_Elements.push_back(element);
		m_Stride += element.size;
	}

	template<>
	void Push<glm::vec3>()
	{
		unsigned int count = 3;
		VertexBufferElement element = { GL_FLOAT, count, 12, false };
			
		m_Elements.push_back(element);
		m_Stride += element.size;
	}

	template<>
	void Push<glm::vec2>()
	{
		unsigned int count = 2;
		VertexBufferElement element = { GL_FLOAT, count, 8, false };
		
		m_Elements.push_back(element);
		m_Stride += element.size;
	}

	template<>
	void Push<Vertex>()
	{

		Push<glm::vec3>();
		Push<glm::vec3>();
		Push<glm::vec2>();
		Push<glm::vec3>();
		Push<glm::vec3>();
		Push<glm::vec3>();

		//layout.Push<float>(3);
		//layout.Push<float>(3);
		//layout.Push<float>(2);
		//layout.Push<float>(3);
		//layout.Push<float>(3);
		//layout.Push<float>(3);
	}

	inline unsigned int GetStride() const { return m_Stride; }
	inline const std::vector<VertexBufferElement> GetElements() const& { return m_Elements; }

private:
	std::vector<VertexBufferElement> m_Elements;
	unsigned int m_Stride;
};