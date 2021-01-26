#pragma once
#include <iostream>
#include <SDL.h>

#include <GL/glew.h>

#include <SDL_opengl.h>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtx/quaternion.hpp>
#include <glm/gtx/string_cast.hpp>

#include <Camera.h>
#include <Transform.h>
#include <Time.h>

#define AppNull (App*)0

typedef void(*DrawCallback)(glm::mat4 , glm::mat4, Camera *);
typedef void(*KeyboardCallBack)(SDL_Event);


class App 
{
	public: 
		App(const char* title = "OpenGL Application", int width = 1280, int height = 720, bool oldOpenGL = false);
		virtual ~App();
		virtual bool run(DrawCallback callback, KeyboardCallBack keyboardCallback);
		virtual void background(float r, float g, float b, float a = 1.0f);

	private:
		virtual void updatePerspectiveAndLookAtMatrix();
		void perspective(float perspectiveFOV, float perspectiveNear, float perspectiveFar);
		void lookAt(glm::vec3 lookAtEye, glm::vec3 lookAtCenter, glm::vec3 lookAtUp);
		void rotateCamera(glm::vec2 mouse);
		void updateCamera();

		SDL_Window *window;
		SDL_GLContext context;
		int WIDTH, HEIGHT;
		bool canRun;
		glm::mat4 vp;

		glm::vec3 lookAtEye;
		glm::vec3 lookAtCenter;
		glm::vec3 lookAtUp;

		float perspectiveFOV;
		float perspectiveAspect;
		float perspectiveNear;
		float perspectiveFar;

		glm::mat4 projectionMatrix;
		glm::mat4 viewMatrix;

		Camera *camera;
		Transform *cameraTransform;

		bool canRotateCamera = false;

		glm::vec4 bgcolor;
};