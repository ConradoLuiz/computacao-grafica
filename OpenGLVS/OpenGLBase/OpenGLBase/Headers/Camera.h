#pragma once

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtx/quaternion.hpp>
#include <glm/gtx/string_cast.hpp>
#include <Transform.h>

enum Projection {
	ORTHO,
	PERSPECTIVE
};

enum CameraMode {
	FREE,
	ARCBALL
};

class Camera {
public:
	Camera(float aspect, float FOV, float nearPlane, float farPlane, Projection projection = PERSPECTIVE);
	~Camera();

	void setCameraMode(CameraMode mode);
	void setPosition(glm::vec3 position, glm::vec3 orientation, glm::vec3 up = glm::vec3(0.0f, 1.0f, 0.0f));

	glm::mat4 getProjectionMatrix();
	glm::mat4 getViewMatrix();
	glm::mat4 getViewProjectionMatrix();

	void updateProjection();
	void updateProjection(float aspect, float FOV, float nearPlane, float farPlane, Projection projection = PERSPECTIVE);
	void onMouseUpdate(glm::vec2 mouse);
	
	void rotateCamera(glm::vec2 input);
	void moveCamera(glm::vec3 position);

	Transform *transform;
	
	glm::mat4 viewMatrix;
	glm::mat4 projectionMatrix;

	CameraMode cameraMode = FREE;

	Projection projectionMode = PERSPECTIVE;
	float aspectRatio;
	float FOV;
	float nearPlane;
	float farPlane;
};