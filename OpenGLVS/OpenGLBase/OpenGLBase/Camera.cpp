#include <Camera.h>
#include <SDL.h>
Camera::Camera(float aspect, float FOV, float nearPlane, float farPlane, Projection projection) {

	this->projectionMode = projection;
	this->FOV = FOV;
	this->aspectRatio = aspect;
	this->nearPlane = nearPlane;
	this->farPlane = farPlane;

	this->transform = new Transform(glm::vec3(0.0f, 2.0f, -5.0f), glm::vec3(10.0f, 0.0f, 0.0f));
	this->updateProjection();
	
}

Camera::~Camera(){ }

void Camera::updateProjection() {
	if (this->projectionMode == PERSPECTIVE) {
		this->projectionMatrix = glm::perspective(this->FOV, this->aspectRatio, this->nearPlane, this->farPlane);
		this->viewMatrix = glm::lookAt(this->transform->position, this->transform->position + this->transform->forward() * -2.0f, this->transform->up());
	}
}

void Camera::updateProjection(float aspect, float FOV, float nearPlane, float farPlane, Projection projection) {

	this->projectionMode = projection;
	this->FOV = FOV;
	this->aspectRatio = aspect;
	this->nearPlane = nearPlane;
	this->farPlane = farPlane;

	this->updateProjection();
}

void Camera::setCameraMode(CameraMode mode) {
	this->cameraMode = mode;
	/*this->transform->position = this->arcBallTarget->position + this->arcBallTarget->forward() * -5.0f;*/
}

void Camera::setPosition(glm::vec3 position, glm::vec3 orientation, glm::vec3 up) {
	this->transform->position = position;
	this->transform->rotation = glm::quat(orientation);
}

glm::mat4 Camera::getProjectionMatrix() {
	return this->projectionMatrix;
}

glm::mat4 Camera::getViewMatrix() {
	return glm::inverse(this->transform->getTransform());
}

glm::mat4 Camera::getViewProjectionMatrix() {
	return this->projectionMatrix * glm::inverse(this->transform->getTransform());
}

void Camera::onMouseUpdate(glm::vec2 mouse) {
	this->rotateCamera(mouse);
}

void Camera::moveCamera(glm::vec3 position) {
	this->transform->position += position;
}

void Camera::rotateCamera(glm::vec2 input) {
	if (this->cameraMode == FREE) {
		this->transform->rotate(glm::vec3(-input.y, 0.0f, 0.0f) / 10.0f, LOCAL_SPACE);
		this->transform->rotate(glm::vec3(0.0F, -input.x, 0.0f) / 10.0f, WORLD_SPACE);
	}
	else if (this->cameraMode == ARCBALL) {

		glm::vec3 newPosition;

		newPosition = (glm::angleAxis(glm::radians(-input.y), this->transform->right()) * (this->transform->position - this->arcBallTarget->position)) + this->arcBallTarget->position;
		newPosition = (glm::angleAxis(glm::radians(-input.x), glm::vec3(0.0f, 1.0f, 0.0f)) *  (newPosition - this->arcBallTarget->position)) + this->arcBallTarget->position;

		this->transform->position = newPosition;

		glm::vec3 direction = this->arcBallTarget->position - this->transform->position;

		direction = glm::normalize(direction);

		float steepness = glm::dot(direction, this->arcBallTarget->up());
		//CORRECT FOR CAMERA FLIPPING UPSIDE DOWN
		if (glm::abs(steepness) > .98f) {
			float correction;
			if (steepness < 0) { correction = -5; }
			else { correction = 5; }
			newPosition = this->transform->position * glm::angleAxis(glm::radians(correction), this->transform->right());
		}

		//CLAMP DISTANCE TO TARGET
		if (glm::length(newPosition - this->arcBallTarget->position) > this->arcBallDistance) {
			newPosition = this->arcBallTarget->position + glm::normalize(newPosition - this->arcBallTarget->position) * this->arcBallDistance;
		}
		if (glm::length(newPosition - this->arcBallTarget->position) < (this->arcBallDistance - .2f)) {
			newPosition = this->arcBallTarget->position + glm::normalize(newPosition - this->arcBallTarget->position) * this->arcBallDistance;
		}

		this->transform->position = newPosition;
		this->transform->lookAt(this->arcBallTarget->position);
	}
}