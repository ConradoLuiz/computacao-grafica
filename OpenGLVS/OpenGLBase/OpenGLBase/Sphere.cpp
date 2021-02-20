#include "Sphere.h"

Sphere::Sphere(glm::vec3 pos, float radius, unsigned int resolution):
	m_radius(radius), m_resolution(resolution)
{

	m_tex2d = SOIL_load_OGL_texture(
		"res/textures/dado.png",
		SOIL_LOAD_AUTO,
		SOIL_CREATE_NEW_ID,
		SOIL_FLAG_MIPMAPS | SOIL_FLAG_INVERT_Y | SOIL_FLAG_NTSC_SAFE_RGB | SOIL_FLAG_COMPRESS_TO_DXT
	);

	transform = new Transform(pos);

	m_vao = new VertexArray();

	GenerateVertices();
	 
	VertexBufferLayout layout;

	layout.Push<Vertex>();
	
	m_vbo = new VertexBuffer(vertices.data(), vertices.size() * sizeof(Vertex), GL_STATIC_DRAW);
	m_vbo->Bind();
	m_vao->AddBuffer(*m_vbo, layout);

	m_ebo = new IndexBuffer(indeces.data(), indeces.size(), GL_STATIC_DRAW);
	m_ebo->Bind();
}

Sphere::~Sphere() 
{
	delete transform;
	delete m_vao;
	delete m_vbo;
	delete m_ebo;
}

void Sphere::draw() 
{
	m_vao->Bind();
	m_ebo->Bind();
	glBindTexture(GL_TEXTURE_2D, m_tex2d);
	//glDrawElements(GL_POINTS, indeces.size(), GL_UNSIGNED_INT, 0);
	glDrawElements(GL_TRIANGLES, indeces.size(), GL_UNSIGNED_INT, 0);
}

void Sphere::GenerateVertices()
{
	vertices.clear();

	float teta;
	float phi;

	glm::vec3 zero(0.0f);

	float delta_teta = 1 / (float)m_resolution;
	float delta_phi   = 1 / (float)m_resolution;

	int next_teta = glm::pi<float>() / delta_teta + 1;
	int next_phi = glm::two_pi<float>() / delta_phi + 1;

	//std::cout << glm::two_pi<float>();
	
	vertices.push_back({
		zero + glm::vec3(0.0f, 1.0f, 0.0f) * m_radius,
		glm::vec3(0.0f, 1.0f, 0.0f),
		glm::vec2(1.0f),
		glm::vec3(0.0f, 1.0f, 0.0f),
		zero,
		zero
	});

	indeces.push_back(0);
	indeces.push_back(1);
	indeces.push_back(0 + next_teta);

	indeces.push_back(0 + 1 + next_teta);
	indeces.push_back(0 + 1);
	indeces.push_back(0 + 2 + next_teta);

	unsigned int index = 1;
	
	for (phi = delta_phi; phi <= glm::two_pi<float>() + delta_phi; phi += delta_phi)
	{
		for (teta = 0; teta <= glm::pi<float>(); teta += delta_teta)
		{
			glm::vec3 polar(m_radius, teta, phi);

			glm::vec3 pos = polarToCart(polar);
			
			float aux = pos.y;
			pos.y = pos.z;
			pos.z = aux;

			glm::vec3 normal = glm::normalize(pos - zero);

			vertices.push_back({
				pos,
				pos,
				glm::vec2(0.5f),
				normal,
				zero,
				zero
			});

			indeces.push_back(index);
			indeces.push_back(index + 1);
			indeces.push_back(index + 1 + next_teta);

			indeces.push_back(index + 1 + next_teta);
			indeces.push_back(index + 1);
			indeces.push_back(index + 2 + next_teta);

			index++;

		}
	}

	vertices.push_back({
		zero + glm::vec3(0.0f, -1.0f, 0.0f) * m_radius,
		glm::vec3(0.0f, -1.0f, 0.0f),
		glm::vec2(1.0f),
		glm::vec3(0.0f, -1.0f, 0.0f),
		zero,
		zero
	});
	
	indeces.push_back(index);

	//for (const Vertex& v : vertices)
	//{
	//	std::cout << glm::to_string(v.Position).c_str() << std::endl;
	//}

	std::cout << vertices.size();
	std::cout << indeces.size();

	//vertices.push_back({
	//	glm::vec3(-1.0f, -1.0f, 0.0f),
	//	glm::vec3(1.0f),
	//	glm::vec2(1.0f),
	//	glm::vec3(1.0f),
	//	glm::vec3(1.0f),
	//	glm::vec3(1.0f)
	//});

	//vertices.push_back({
	//	glm::vec3(1.0f, -1.0f, 0.0f),
	//	glm::vec3(1.0f),
	//	glm::vec2(1.0f),
	//	glm::vec3(1.0f),
	//	glm::vec3(1.0f),
	//	glm::vec3(1.0f)
	//	});

	//vertices.push_back({
	//	glm::vec3(0.0f, 1.0f, 0.0f),
	//	glm::vec3(1.0f),
	//	glm::vec2(1.0f),
	//	glm::vec3(1.0f),
	//	glm::vec3(1.0f),
	//	glm::vec3(1.0f)
	//});

	//indeces.push_back(0);
	//indeces.push_back(1);
	//indeces.push_back(2);
}

glm::vec3 Sphere::polarToCart(glm::vec3 &polar)
{
	glm::vec3 v;

	v.x = polar.x * glm::sin(polar.y) * glm::cos(polar.z);
	v.y = polar.x * glm::sin(polar.y) * glm::sin(polar.z);
	v.z = polar.x * glm::cos(polar.y);

	return v;
}