#pragma once
#include <iostream>
#include <SDL.h>

#include <GL/glew.h>

#include <SDL_opengl.h>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

#define AppNull (App*)0

typedef void(*DrawCallback)(glm::mat4 transform);

class App 
{
	public: 
		App(const char* title = "OpenGL Application", int width = 1280, int height = 720, bool oldOpenGL = false);
		virtual ~App();
		virtual bool run(DrawCallback callback);
		virtual void background(float r, float g, float b, float a = 1.0f);

	private:
		virtual void updatePerspectiveAndLookAtMatrix();
		void perspective(float perspectiveFOV, float perspectiveNear, float perspectiveFar);
		void lookAt(glm::vec3 lookAtEye, glm::vec3 lookAtCenter, glm::vec3 lookAtUp);

		SDL_Window *window;
		SDL_GLContext context;
		bool canRun;
		glm::mat4 vp;

		glm::vec3 lookAtEye;
		glm::vec3 lookAtCenter;
		glm::vec3 lookAtUp;

		float perspectiveFOV;
		float perspectiveAspect;
		float perspectiveNear;
		float perspectiveFar;

		glm::vec4 bgcolor;
};