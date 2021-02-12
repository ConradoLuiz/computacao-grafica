#include <Cube.h>

Cube::Cube()
{
	transform = new Transform(glm::vec3(3.0f));

	float cubeVertex[] =
	{
		//POSITIONS             //COLORS             // TEX COORDS   //NORMALS

		//FRONT FACE 
		-1.0f, -1.0f,  1.0f,    1.0f,  0.0f, 0.0f,   0.0f, 0.0f,     0.0f, 0.0f,  1.0f,
		 1.0f, -1.0f,  1.0f,    1.0f,  1.0f, 0.0f,   0.0f, 0.5f,     0.0f, 0.0f,  1.0f,
		 1.0f,  1.0f,  1.0f,    0.0f,  1.0f, 0.0f,   0.3f, 0.5f,     0.0f, 0.0f,  1.0f,
		-1.0f,  1.0f,  1.0f,    0.0f,  1.0f, 1.0f,   0.3f, 0.0f,     0.0f, 0.0f,  1.0f,
																				 
		//RIGHT FACE															 
		 1.0f, -1.0f,  1.0f,    1.0f,  1.0f, 0.0f,   0.0f, 0.5f,     1.0f, 0.0f,  0.0f,
		 1.0f, -1.0f, -1.0f,    1.0f,  1.0f, 0.0f,   0.3f, 0.5f,     1.0f, 0.0f,  0.0f,
		 1.0f,  1.0f, -1.0f,    1.0f,  1.0f, 0.0f,   0.3f, 1.0f,     1.0f, 0.0f,  0.0f,
		 1.0f,  1.0f,  1.0f,    0.0f,  1.0f, 0.0f,   0.0f, 1.0f,     1.0f, 0.0f,  0.0f,

		 //BACK FACE
		 1.0f, -1.0f, -1.0f,    1.0f,  1.0f, 0.0f,   0.66f, 0.5f,    0.0f, 0.0f, -1.0f,
		-1.0f, -1.0f, -1.0f,    1.0f,  1.0f, 0.0f,   1.0f,  0.5f,    0.0f, 0.0f, -1.0f,
		-1.0f,  1.0f, -1.0f,    1.0f,  1.0f, 0.0f,   1.0f,  1.0f,    0.0f, 0.0f, -1.0f,
		 1.0f,  1.0f, -1.0f,    1.0f,  1.0f, 0.0f,   0.66f, 1.0f,    0.0f, 0.0f, -1.0f,

		 //LEFT FACE
		-1.0f, -1.0f, -1.0f,    1.0f,  1.0f, 0.0f,   0.66f, 0.0f,    -1.0f, 0.0f,  0.0f,
		-1.0f, -1.0f,  1.0f,    1.0f,  0.0f, 0.0f,   1.0f,  0.0f,    -1.0f, 0.0f,  0.0f,
		-1.0f,  1.0f,  1.0f,    0.0f,  1.0f, 1.0f,   1.0f,  0.5f,    -1.0f, 0.0f,  0.0f,
		-1.0f,  1.0f, -1.0f,    1.0f,  1.0f, 0.0f,   0.66f, 0.5f,    -1.0f, 0.0f,  0.0f,

		//TOP FACE 
		-1.0f,  1.0f,  1.0f,    0.0f,  1.0f, 1.0f,   0.33f, 0.0f,     0.0f, 1.0f,  0.0f,
		 1.0f,  1.0f,  1.0f,    0.0f,  1.0f, 0.0f,   0.66f, 0.0f,     0.0f, 1.0f,  0.0f,
		 1.0f,  1.0f, -1.0f,    1.0f,  1.0f, 0.0f,   0.66f, 0.5f,     0.0f, 1.0f,  0.0f,
		-1.0f,  1.0f, -1.0f,    1.0f,  1.0f, 0.0f,   0.33f, 0.5f,     0.0f, 1.0f,  0.0f,

		//BOTTOM FACE
		-1.0f,  -1.0f,  1.0f,    0.0f,  1.0f, 1.0f,   0.33f, 0.5f,     0.0f, -1.0f,  0.0f,
		 1.0f,  -1.0f,  1.0f,    0.0f,  1.0f, 0.0f,   0.66f, 0.5f,     0.0f, -1.0f,  0.0f,
		 1.0f,  -1.0f, -1.0f,    1.0f,  1.0f, 0.0f,   0.66f, 1.0f,     0.0f, -1.0f,  0.0f,
		-1.0f,  -1.0f, -1.0f,    1.0f,  1.0f, 0.0f,   0.33f, 1.0f,     0.0f, -1.0f,  0.0f
	};

	unsigned int m_cubeIndex[] = { 
		//FRONT FACE
		0, 1, 2,
		2, 3, 0,
		//RIGHT FACE
		4, 5, 6,
		6, 7, 4,
		//BACK FACE
		8, 9, 10,
		10, 11, 8,
		//LEFT FACE
		12, 13, 14,
		14, 15, 12,
		//TOP FACE
		16, 17, 18,
		18, 19, 16,
		//BOTTOM FACE
		20, 21, 22,
		22, 23, 20
	};

	m_tex2d = SOIL_load_OGL_texture(
		"res/textures/dado.png",
		SOIL_LOAD_AUTO, 
		SOIL_CREATE_NEW_ID,
		SOIL_FLAG_MIPMAPS | SOIL_FLAG_INVERT_Y | SOIL_FLAG_NTSC_SAFE_RGB | SOIL_FLAG_COMPRESS_TO_DXT
	);
	
	
	// USANDO 1 VBO COM STRIDE
	m_vao = new VertexArray();
	VertexBufferLayout layout;

	// POSITIONS
	layout.Push<float>(3);
	// COLORS
	layout.Push<float>(3);
	//TEX COORDS
	layout.Push<float>(2);
	//NORMALS
	layout.Push<float>(3);

	m_position_vbo = new VertexBuffer(cubeVertex, sizeof(cubeVertex), GL_STATIC_DRAW);
	m_position_vbo->Bind();
	m_vao->AddBuffer(*m_position_vbo, layout);

	// BUFFER DE INDEX (FACES) -----------------------------------------------------------------------------
	m_ebo = new IndexBuffer(m_cubeIndex, sizeof(m_cubeIndex) / sizeof(unsigned int), GL_STATIC_DRAW);
	m_ebo->Bind();
	

	/*
	//USANDO 2 VBO (1 PARA POSIÇÃO E 1 PARA COR)
	m_vao = new VertexArray();
	VertexBufferLayout *layout = new VertexBufferLayout();

	layout->Push<float>(3);	
	
	m_position_vbo = new VertexBuffer(cubeVertexPosition, sizeof(cubeVertexPosition), GL_STATIC_DRAW);
	m_position_vbo->Bind();
	m_vao->AddBuffer(*m_position_vbo, *layout);

	m_color_vbo = new VertexBuffer(cubeColorPerVertex, sizeof(cubeColorPerVertex), GL_STATIC_DRAW);
	m_color_vbo->Bind();
	m_vao->AddBuffer(*m_color_vbo, *layout);
	
	// BUFFER DE INDEX (FACES) -----------------------------------------------------------------------------
	m_ebo = new IndexBuffer(m_cubeIndex, sizeof(m_cubeIndex) / sizeof(unsigned int), GL_STATIC_DRAW);
	m_ebo->Bind();
	*/
}

Cube::~Cube()
{
	delete m_position_vbo;
	//delete m_color_vbo;
	delete m_ebo;
	delete m_vao;
	delete transform;
}

void Cube::draw()
{
	m_vao->Bind();
	m_ebo->Bind();
	glBindTexture(GL_TEXTURE_2D, m_tex2d);
	glDrawElements(GL_TRIANGLES, sizeof(m_cubeIndex) / sizeof(unsigned int) , GL_UNSIGNED_INT, 0);
}
