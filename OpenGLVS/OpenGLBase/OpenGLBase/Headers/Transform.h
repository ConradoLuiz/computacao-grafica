#pragma once

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtx/quaternion.hpp>

enum Space {
	LOCAL_SPACE,
	WORLD_SPACE
};

class Transform {
public: 
	Transform(glm::vec3 position, glm::vec3 rotation = glm::vec3(0.0f));
	glm::vec3 position;
	glm::quat rotation;

	glm::vec3 up();
	glm::vec3 forward();
	glm::vec3 right();

	glm::vec3 eulerAngles();

	void rotate(glm::vec3, float angle);
	void rotate(glm::vec3 eulerAngles, Space space);

	glm::mat4 toRotationMatrix();
	glm::mat4 getTransform();
};