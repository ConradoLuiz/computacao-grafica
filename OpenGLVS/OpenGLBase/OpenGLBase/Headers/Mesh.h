#pragma once
#include <globals.h>

struct Vertex {
	// position
	glm::vec3 Position;
	// color
	glm::vec3 Color;
	// texCoords
	glm::vec2 TexCoords;
	// normal
	glm::vec3 Normal;
	// tangent
	glm::vec3 Tangent;
	// bitangent
	glm::vec3 Bitangent;
};