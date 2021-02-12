#pragma once
#include <globals.h>
#include <Camera.h>
#include <Transform.h>
#include <Time.h>
#include <Input.h>
#include <typeinfo>


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
		virtual void toggleFullscreen();
		virtual void setResolution(int width, int height);
		virtual glm::vec2 GetMonitorSize();

		int WIDTH, HEIGHT;

	private:
		void ConfigStyle(ImGuiStyle* style);
		SDL_Window *window;
		SDL_GLContext context;
		bool m_isFullscreen;
		bool canRun;

		void trackKeys(const Uint8 *state);
		
		Camera *camera;
		
		bool canRotateCamera = false;

		glm::vec4 bgcolor;
};