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
	glDrawElements(GL_POINTS, indeces.size(), GL_UNSIGNED_INT, 0);
}

void Sphere::GenerateVertices()
{
	vertices.clear();

	float teta;
	float phi;

	glm::vec3 zero(0.0f);

	float delta_teta = 1 / (float)m_resolution;
	float delta_phi   = 1 / (float)m_resolution;

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

	unsigned int index = 1;
	
	for (teta = delta_teta; teta <= glm::pi<float>(); teta += delta_teta)
	{
		for (phi = 0.0f; phi <= glm::two_pi<float>(); phi += delta_phi)
		{
			//COLOCAR GLM POLAR COORDINATES
			glm::vec3 pos;
			
			pos.x = m_radius * glm::sin(teta) * glm::cos(phi);
			pos.z = m_radius * glm::sin(teta) * glm::sin(phi);
			pos.y = m_radius * glm::cos(teta);

			glm::vec3 normal = glm::normalize(pos - zero);

			vertices.push_back({
				pos,
				glm::vec3(1.0f),
				glm::vec2(0.5f),
				normal,
				zero,
				zero
			});

			indeces.push_back(index);
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
