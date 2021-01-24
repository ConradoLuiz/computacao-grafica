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

	this->perspectiveAspect = (1.0f*width) / height;
	this->camera = new Camera(this->perspectiveAspect, 45.0f, 0.01f, 1000.0f, PERSPECTIVE);
	this->camera->setPosition(glm::vec3(20.0f, 10.0f, 40.0f), glm::vec3(-20.0f, 0.0f, 0.0f));

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

void App::updatePerspectiveAndLookAtMatrix()
{
	this->projectionMatrix = glm::perspective(this->perspectiveFOV, this->perspectiveAspect, this->perspectiveNear, this->perspectiveFar);
	this->viewMatrix = glm::lookAt(this->cameraTransform->position, this->cameraTransform->position + this->cameraTransform->forward() * -5.0f , this->cameraTransform->up());
	
	this->vp = this->projectionMatrix * this->viewMatrix;
}

void App::perspective(float perspectiveFOV, float perspectiveNear, float perspectiveFar)
{
	this->perspectiveFOV = perspectiveFOV;
	this->perspectiveNear = perspectiveNear;
	this->perspectiveFar = perspectiveFar;
	this->updatePerspectiveAndLookAtMatrix();
}

void App::lookAt(glm::vec3 lookAtEye, glm::vec3 lookAtCenter, glm::vec3 lookAtUp)
{
	this->lookAtEye = lookAtEye;
	this->lookAtCenter = lookAtCenter;
	this->lookAtUp = lookAtUp;
	this->updatePerspectiveAndLookAtMatrix();
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
	
	

	while (!quit)
	{
		while (SDL_PollEvent(&event))
		{
			
			if (event.type == SDL_QUIT)
			{
				quit = 1;
				break;
			}

			else if (event.type == SDL_USEREVENT)
			{
				glClearBufferfv(GL_COLOR, 0, &this->bgcolor[0]);
				glClearBufferfv(GL_DEPTH, 0, depth);
				
				callback(this->camera->getProjectionMatrix(), this->camera->getViewMatrix());
				SDL_GL_SwapWindow(this->window);
			}

			else if (event.type == SDL_WINDOWEVENT)
			{
				if (event.window.event == SDL_WINDOWEVENT_RESIZED)
				{
					int width = event.window.data1;
					int height = event.window.data2;
					glViewport(0, 0, (GLsizei)width, (GLsizei)height);
					this->perspectiveAspect = ((1.0f)*width) / height;
					//this->updatePerspectiveAndLookAtMatrix();
					this->camera->updateProjection(this->perspectiveAspect, 45.0f, 0.01f, 1000.0f, PERSPECTIVE);
				}
			}

			else if (event.type == SDL_KEYDOWN)
			{	
				keyboardCallBack(event);
				switch (event.key.keysym.sym) {
					case SDLK_w:
						this->camera->moveCamera(this->camera->transform->forward() * -0.5f);
						break;
					case SDLK_s:
						this->camera->moveCamera(this->camera->transform->forward() * 0.5f);
						break;
					case SDLK_a:
						this->camera->moveCamera(this->camera->transform->right() * -0.5f);
						break;
					case SDLK_d:
						this->camera->moveCamera(this->camera->transform->right() * 0.5f);
						break;
					case SDLK_z:
						this->camera->moveCamera(this->camera->transform->up() * 0.5f);
						break;
					case SDLK_x:
						this->camera->moveCamera(this->camera->transform->up() * -0.5f);
						break;
				}
			}

			else if (event.type == SDL_MOUSEMOTION)
			{
				//SDL_Log("Mouse Position %dx%d", event.motion.xrel, event.motion.yrel);

				//if(this->canRotateCamera) this->rotateCamera(glm::vec2(event.motion.xrel, event.motion.yrel));
				if (this->canRotateCamera) this->camera->rotateCamera(glm::vec2(event.motion.xrel, event.motion.yrel));
			}

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
			
		}
	}
	SDL_RemoveTimer(timerId);
	return true;
}

void App::rotateCamera(glm::vec2 mouse) {

	this->cameraTransform->rotate(glm::vec3(-mouse.y , 0.0f, 0.0f)/10.0f, LOCAL_SPACE);
	this->cameraTransform->rotate(glm::vec3(0.0F, -mouse.x, 0.0f) / 10.0f, WORLD_SPACE);

	this->updateCamera();
	
}

void App::updateCamera() {

	glm::vec3 cameraLookAt = this->cameraTransform->position + (this->cameraTransform->forward() * -5.0f);

	this->viewMatrix = glm::lookAt(
		this->cameraTransform->position,
		cameraLookAt,
		this->cameraTransform->up()
	);

	//this->viewMatrix = glm::inverse(this->cameraTransform->getTransform());
	
}


void App::background(float r, float g, float b, float a)
{
	this->bgcolor.r = r;
	this->bgcolor.g = g;
	this->bgcolor.b = b;
	this->bgcolor.a = a;
}
