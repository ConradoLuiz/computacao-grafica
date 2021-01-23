#include <Transform.h>

Transform::Transform(glm::vec3 position, glm::vec3 rotation) {
	this->position = position;
	this->rotation = glm::quat(glm::vec3(0.0f)) * glm::quat(glm::radians(rotation));
}

Transform::~Transform() {

}

glm::vec3 Transform::up() {
	return glm::normalize( this->rotation * glm::vec3(0.0f, 1.0f, 0.0f));
}

glm::vec3 Transform::forward() {
	return glm::normalize(this->rotation * glm::vec3(0.0f, 0.0f, 1.0f));
}

glm::vec3 Transform::right() {
	return glm::normalize(this->rotation * glm::vec3(1.0f, 0.0f, 0.0f));
}

glm::vec3 Transform::eulerAngles() {
	return glm::eulerAngles(this->rotation);
}

glm::mat4 Transform::toRotationMatrix() {
	return glm::toMat4(this->rotation);
}

glm::mat4 Transform::getTransform() {
	
	return glm::translate(glm::mat4(1.0f), this->position) * this->toRotationMatrix();
}

void Transform::rotate(glm::vec3 axis, float angle) {
	// REVER ESSA FUNÇÃO
	this->rotation = glm::normalize(glm::rotate(this->rotation, glm::radians(angle), glm::normalize(axis)));
	//this->rotation = this->rotation * glm::angleAxis(glm::radians(angle), glm::normalize(axis));
}

void Transform::rotate(glm::vec3 eulerAngles, Space space) {
	
	glm::quat rotation(glm::radians(eulerAngles));

	if (space == LOCAL_SPACE) {
		this->rotation = this->rotation * rotation;
	}
	else if (space == WORLD_SPACE) {
		this->rotation = rotation * this->rotation;
	}
}

