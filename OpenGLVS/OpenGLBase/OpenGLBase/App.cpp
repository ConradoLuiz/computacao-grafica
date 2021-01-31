#include <App.h>

App::App(const char* title, int width, int height, bool oldOpenGL){
	this->window = (SDL_Window*)0;
	this->canRun = false;
	if (SDL_Init(SDL_INIT_VIDEO) != 0)
	{
		SDL_Log("Unable to initialize SDL: %s", SDL_GetError());
		return;
	}

	if (oldOpenGL)
	{
		//OpenGL compatibility profile - deprecated functions are allowed
		SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_COMPATIBILITY);
	}
	else
	{
		//OpenGL core profile - deprecated functions are disabled
		SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE);
	}
	
	SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3);
	SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 3);
	SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8);

	this->window = SDL_CreateWindow(title, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, width, height, SDL_WINDOW_OPENGL | SDL_WINDOW_RESIZABLE);
	if (!this->window)
	{
		SDL_Log("Unable to create SDL window: %s", SDL_GetError());
		return;
	}
	this->WIDTH = width;
	this->HEIGHT = height;

	this->context = SDL_GL_CreateContext(window);
	if (!context)
	{
		SDL_Log("Unable to create OPENGL context: %s", SDL_GetError());
		return;
	}
	
	glewExperimental = GL_TRUE;

	if (GLEW_OK != glewInit())
	{
		SDL_Log("Falha ao inicializar GLEW");
		return;
	}
	SDL_GL_SetSwapInterval(1);

	float ratio = (1.0f*width) / height;
	this->camera = new Camera(ratio, 45.0f, 0.01f, 1000.0f, PERSPECTIVE);
	this->camera->setCameraMode(FREE);
	this->camera->setPosition(glm::vec3(0.0f, 0.0f, 10.0f), glm::vec3(0.0f, 0.0f, 0.0f));

	glEnable(GL_DEPTH_TEST);
	this->canRun = true;

	this->bgcolor.r = 0.3f;
	this->bgcolor.g = 0.6f;
	this->bgcolor.b = 0.7f;
	this->bgcolor.a = 1.0f;
}

App::~App()
{
	SDL_GL_DeleteContext(this->context);
	SDL_DestroyWindow(this->window);
	SDL_Quit();
}

Uint32 timerCallback(Uint32 interval, void *param)
{
	SDL_Event event;
	SDL_UserEvent userevent;
	userevent.type = SDL_USEREVENT;
	userevent.code = 0;
	userevent.data1 = NULL;
	userevent.data2 = NULL;
	event.type = SDL_USEREVENT;
	event.user = userevent;
	SDL_PushEvent(&event);
	return interval;
}

bool App::run(DrawCallback callback, KeyboardCallBack keyboardCallBack)
{
	GLfloat depth[] = { 1.0 };
	SDL_Event event;
	SDL_TimerID timerId;
	int quit = 0;

	if (!this->canRun)
	{
		return false;
	}
	timerId = SDL_AddTimer(40, timerCallback, NULL);
	
	Uint64 NOW = SDL_GetPerformanceCounter();
	Uint64 LAST = 0;
	double deltaTime = 0;


	while (!quit)
	{
		LAST = NOW;
		NOW = SDL_GetPerformanceCounter();

		deltaTime = (double)((NOW - LAST) * 1000 / (double)SDL_GetPerformanceFrequency());
		Time::m_deltaTime = (float)deltaTime;

		while (SDL_PollEvent(&event))
		{	
			const Uint8 *state = SDL_GetKeyboardState(NULL);
			this->trackKeys(state);

			if (event.type == SDL_QUIT)
			{
				quit = 1;
				break;
			}
			else if (event.type == SDL_MOUSEMOTION) { Input::m_mouse = glm::vec2(event.motion.x, event.motion.y); }

			else if (event.type == SDL_USEREVENT)
			{
				glClearBufferfv(GL_COLOR, 0, &this->bgcolor[0]);
				glClearBufferfv(GL_DEPTH, 0, depth);
				
				callback(this->camera->getProjectionMatrix(), this->camera->getViewMatrix(), this->camera);
				SDL_GL_SwapWindow(this->window);
			}

			else if (event.type == SDL_WINDOWEVENT)
			{
				if (event.window.event == SDL_WINDOWEVENT_RESIZED)
				{
					int width = event.window.data1;
					int height = event.window.data2;
					glViewport(0, 0, (GLsizei)width, (GLsizei)height);
					
					this->camera->updateProjection(((1.0f)*width) / height, 45.0f, 0.01f, 1000.0f, PERSPECTIVE);
				}
			}

			else if (event.type == SDL_KEYDOWN) { Input::setKeyPressed(event.key.keysym.scancode, true);  }
			else if (event.type == SDL_KEYUP)   { Input::setKeyPressed(event.key.keysym.scancode, false); }

			else if (event.type == SDL_MOUSEBUTTONDOWN)
			{
				if (event.button.button == SDL_BUTTON_LEFT)
				{
					SDL_Log("Left Button clicked");
				}
				if (event.button.button == SDL_BUTTON_RIGHT)
				{
					this->canRotateCamera = !this->canRotateCamera;
					
					SDL_WarpMouseInWindow(this->window, this->WIDTH / 2, this->HEIGHT / 2);
					SDL_ShowCursor(this->canRotateCamera ? SDL_DISABLE : SDL_ENABLE);
					SDL_SetWindowGrab(this->window, this->canRotateCamera ? SDL_TRUE : SDL_FALSE);
					SDL_SetRelativeMouseMode(this->canRotateCamera ? SDL_TRUE : SDL_FALSE);

				}
			}

			if (event.type == SDL_MOUSEMOTION)
			{
				Input::m_previousMouse = glm::vec2(event.motion.x, event.motion.y);

				if (this->canRotateCamera) this->camera->rotateCamera(glm::vec2(event.motion.xrel, event.motion.yrel));
			}
			
		}
	}
	SDL_RemoveTimer(timerId);
	return true;
}

void App::background(float r, float g, float b, float a)
{
	this->bgcolor.r = r;
	this->bgcolor.g = g;
	this->bgcolor.b = b;
	this->bgcolor.a = a;
}

void App::trackKeys(const Uint8 *state) {
	if (state[SDL_SCANCODE_UP])    { Input::setKeyDown(SDL_SCANCODE_UP,     true); } else { Input::setKeyDown(SDL_SCANCODE_UP,     false); }
	if (state[SDL_SCANCODE_DOWN])  { Input::setKeyDown(SDL_SCANCODE_DOWN,   true); } else { Input::setKeyDown(SDL_SCANCODE_DOWN,   false); }
	if (state[SDL_SCANCODE_LEFT])  { Input::setKeyDown(SDL_SCANCODE_LEFT,   true); } else { Input::setKeyDown(SDL_SCANCODE_LEFT,   false); }
	if (state[SDL_SCANCODE_RIGHT]) { Input::setKeyDown(SDL_SCANCODE_RIGHT,  true); } else { Input::setKeyDown(SDL_SCANCODE_RIGHT,  false); }
	if (state[SDL_SCANCODE_W])     { Input::setKeyDown(SDL_SCANCODE_W,      true); } else { Input::setKeyDown(SDL_SCANCODE_W,      false); }
	if (state[SDL_SCANCODE_S])     { Input::setKeyDown(SDL_SCANCODE_S,      true); } else { Input::setKeyDown(SDL_SCANCODE_S,      false); }
	if (state[SDL_SCANCODE_A])     { Input::setKeyDown(SDL_SCANCODE_A,      true); } else { Input::setKeyDown(SDL_SCANCODE_A,      false); }
	if (state[SDL_SCANCODE_D])     { Input::setKeyDown(SDL_SCANCODE_D,      true); } else { Input::setKeyDown(SDL_SCANCODE_D,      false); }
	if (state[SDL_SCANCODE_Q])     { Input::setKeyDown(SDL_SCANCODE_Q,      true); } else { Input::setKeyDown(SDL_SCANCODE_Q,      false); }
	if (state[SDL_SCANCODE_E])     { Input::setKeyDown(SDL_SCANCODE_E,      true); } else { Input::setKeyDown(SDL_SCANCODE_E,      false); }
	if (state[SDL_SCANCODE_Z])     { Input::setKeyDown(SDL_SCANCODE_Z,      true); } else { Input::setKeyDown(SDL_SCANCODE_Z,      false); }
	if (state[SDL_SCANCODE_X])     { Input::setKeyDown(SDL_SCANCODE_X,      true); } else { Input::setKeyDown(SDL_SCANCODE_X,      false); }
}