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
	SDL_GL_SetSwapInterval(0);

	float ratio = (1.0f*width) / height;
	this->camera = new Camera(ratio, 45.0f, 0.01f, 1000.0f, PERSPECTIVE);
	this->camera->setCameraMode(FREE);
	this->camera->setPosition(glm::vec3(0.0f, 0.0f, 10.0f), glm::vec3(0.0f, 0.0f, 0.0f));

	glEnable(GL_DEPTH_TEST);

	// Setup Dear ImGui context
	IMGUI_CHECKVERSION();
	ImGui::CreateContext();
	ImGuiIO& io = ImGui::GetIO(); (void)io;
	//io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;     // Enable Keyboard Controls
	//io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;      // Enable Gamepad Controls

	// Setup Dear ImGui style
	ImGui::StyleColorsDark();
	ConfigStyle(&ImGui::GetStyle());

	// Setup Platform/Renderer backends
	ImGui_ImplSDL2_InitForOpenGL(this->window, this->context);
	ImGui_ImplOpenGL3_Init("#version 330");

	this->canRun = true;

	this->bgcolor.r = 0.0f;
	this->bgcolor.g = 0.0f;
	this->bgcolor.b = 0.0f;
	this->bgcolor.a = 1.0f;

}

App::~App()
{
	ImGui_ImplOpenGL3_Shutdown();
	ImGui_ImplSDL2_Shutdown();
	ImGui::DestroyContext();

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

	SDL_Keycode keyDownCode = NULL;

	bool imguiMouse = false;
	bool imguiKeys  = false;

	while (!quit)
	{
		LAST = NOW;
		NOW = SDL_GetPerformanceCounter();

		deltaTime = (double)((NOW - LAST) * 1000 / (double)SDL_GetPerformanceFrequency());
		Time::m_deltaTime = (float)deltaTime;

		while (SDL_PollEvent(&event))
		{	
			ImGui_ImplSDL2_ProcessEvent(&event);

			const Uint8 *state = SDL_GetKeyboardState(NULL);
			this->trackKeys(state);
			
			imguiMouse = ImGui::GetIO().WantCaptureMouse;
			imguiKeys  = ImGui::GetIO().WantCaptureKeyboard;

			if (event.type == SDL_QUIT)
			{
				quit = 1;
				break;
			}
			else if (event.type == SDL_MOUSEMOTION) { Input::m_mouse = glm::vec2(event.motion.x, event.motion.y); }

			else if (event.type == SDL_KEYDOWN && !imguiKeys) {
				if (event.key.keysym.scancode != keyDownCode) {
					Input::setKeyPressed(event.key.keysym.scancode, true); 
					keyDownCode = event.key.keysym.scancode; 
				}
			}
			else if (event.type == SDL_KEYUP && !imguiKeys)   { Input::setKeyPressed(event.key.keysym.scancode, false); }

			else if (event.type == SDL_MOUSEBUTTONDOWN && !imguiMouse)
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

			else if (event.type == SDL_USEREVENT)
			{
				glClearBufferfv(GL_COLOR, 0, &this->bgcolor[0]);
				glClearBufferfv(GL_DEPTH, 0, depth);
				
				ImGui_ImplOpenGL3_NewFrame();
				ImGui_ImplSDL2_NewFrame(this->window);
				ImGui::NewFrame();

				callback(this->camera->getProjectionMatrix(), this->camera->getViewMatrix(), this->camera);

				ImGui::EndFrame();
				ImGui::Render();
				ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

				SDL_GL_SwapWindow(this->window);

				if (keyDownCode != NULL) {
					Input::setKeyPressed(keyDownCode, false);
					keyDownCode = NULL;
				}
			}

			else if (event.type == SDL_WINDOWEVENT)
			{
				if (event.window.event == SDL_WINDOWEVENT_RESIZED)
				{
					this->setResolution(event.window.data1, event.window.data2);
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

void App::toggleFullscreen()
{
	m_isFullscreen = !m_isFullscreen;

	if (m_isFullscreen) { 
		SDL_MaximizeWindow(this->window);
		glm::vec2 size = this->GetMonitorSize();
		this->setResolution(size.x, size.y);
	}
	else { this->setResolution(1280, 720); }

	SDL_SetWindowFullscreen(window, m_isFullscreen);
}

void App::setResolution(int width, int height)
{
	this->WIDTH = width;
	this->HEIGHT = height;

	glViewport(0, 0, (GLsizei)width, (GLsizei)height);

	this->camera->updateProjection(((1.0f)*width) / height, 45.0f, 0.01f, 1000.0f, PERSPECTIVE);
	SDL_SetWindowSize(this->window, width, height);
}

glm::vec2 App::GetMonitorSize()
{
	SDL_DisplayMode DM;
	SDL_GetCurrentDisplayMode(0, &DM);
	return glm::vec2(DM.w, DM.h);
}

void App::trackKeys(const Uint8 *state) {
	if (state[SDL_SCANCODE_F3])    { Input::setKeyDown(SDL_SCANCODE_F3,     true); } else { Input::setKeyDown(SDL_SCANCODE_F3,     false); }
	if (state[SDL_SCANCODE_LCTRL]) { Input::setKeyDown(SDL_SCANCODE_LCTRL,  true); } else { Input::setKeyDown(SDL_SCANCODE_LCTRL,  false); }
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
	if (state[SDL_SCANCODE_F])     { Input::setKeyDown(SDL_SCANCODE_F,      true); } else { Input::setKeyDown(SDL_SCANCODE_F,      false); }
	if (state[SDL_SCANCODE_P])     { Input::setKeyDown(SDL_SCANCODE_P,      true); } else { Input::setKeyDown(SDL_SCANCODE_P,      false); }
}

void App::ConfigStyle(ImGuiStyle* style)
{
	style->WindowPadding = ImVec2(15, 15);
	style->WindowRounding = 5.0f;
	style->FramePadding = ImVec2(5, 5);
	style->FrameRounding = 4.0f;
	style->ItemSpacing = ImVec2(12, 8);
	style->ItemInnerSpacing = ImVec2(8, 6);
	style->IndentSpacing = 25.0f;
	style->ScrollbarSize = 15.0f;
	style->ScrollbarRounding = 9.0f;
	style->GrabMinSize = 5.0f;
	style->GrabRounding = 3.0f;

	style->Colors[ImGuiCol_Text] = ImVec4(0.80f, 0.80f, 0.83f, 1.00f);
	style->Colors[ImGuiCol_TextDisabled] = ImVec4(0.24f, 0.23f, 0.29f, 1.00f);
	style->Colors[ImGuiCol_WindowBg] = ImVec4(0.06f, 0.05f, 0.07f, 1.00f);
	style->Colors[ImGuiCol_PopupBg] = ImVec4(0.07f, 0.07f, 0.09f, 1.00f);
	style->Colors[ImGuiCol_Border] = ImVec4(0.80f, 0.80f, 0.83f, 0.88f);
	style->Colors[ImGuiCol_BorderShadow] = ImVec4(0.92f, 0.91f, 0.88f, 0.00f);
	style->Colors[ImGuiCol_FrameBg] = ImVec4(0.10f, 0.09f, 0.12f, 1.00f);
	style->Colors[ImGuiCol_FrameBgHovered] = ImVec4(0.24f, 0.23f, 0.29f, 1.00f);
	style->Colors[ImGuiCol_FrameBgActive] = ImVec4(0.56f, 0.56f, 0.58f, 1.00f);
	style->Colors[ImGuiCol_TitleBg] = ImVec4(0.10f, 0.09f, 0.12f, 1.00f);
	style->Colors[ImGuiCol_TitleBgCollapsed] = ImVec4(0, 0, 0, 0.2f);
	style->Colors[ImGuiCol_TitleBgActive] = ImVec4(0.07f, 0.07f, 0.09f, 1.00f);
	style->Colors[ImGuiCol_MenuBarBg] = ImVec4(0.10f, 0.09f, 0.12f, 1.00f);
	style->Colors[ImGuiCol_ScrollbarBg] = ImVec4(0.10f, 0.09f, 0.12f, 1.00f);
	style->Colors[ImGuiCol_ScrollbarGrab] = ImVec4(0.80f, 0.80f, 0.83f, 0.31f);
	style->Colors[ImGuiCol_ScrollbarGrabHovered] = ImVec4(0.56f, 0.56f, 0.58f, 1.00f);
	style->Colors[ImGuiCol_ScrollbarGrabActive] = ImVec4(0.06f, 0.05f, 0.07f, 1.00f);
	style->Colors[ImGuiCol_CheckMark] = ImVec4(0.80f, 0.80f, 0.83f, 0.31f);
	style->Colors[ImGuiCol_SliderGrab] = ImVec4(0.80f, 0.80f, 0.83f, 0.31f);
	style->Colors[ImGuiCol_SliderGrabActive] = ImVec4(0.06f, 0.05f, 0.07f, 1.00f);
	style->Colors[ImGuiCol_Button] = ImVec4(0.10f, 0.09f, 0.12f, 1.00f);
	style->Colors[ImGuiCol_ButtonHovered] = ImVec4(0.24f, 0.23f, 0.29f, 1.00f);
	style->Colors[ImGuiCol_ButtonActive] = ImVec4(0.56f, 0.56f, 0.58f, 1.00f);
	style->Colors[ImGuiCol_Header] = ImVec4(0.10f, 0.09f, 0.12f, 1.00f);
	style->Colors[ImGuiCol_HeaderHovered] = ImVec4(0.56f, 0.56f, 0.58f, 1.00f);
	style->Colors[ImGuiCol_HeaderActive] = ImVec4(0.06f, 0.05f, 0.07f, 1.00f);
	style->Colors[ImGuiCol_ResizeGrip] = ImVec4(0.00f, 0.00f, 0.00f, 0.00f);
	style->Colors[ImGuiCol_ResizeGripHovered] = ImVec4(0.56f, 0.56f, 0.58f, 1.00f);
	style->Colors[ImGuiCol_ResizeGripActive] = ImVec4(0.06f, 0.05f, 0.07f, 1.00f);
	style->Colors[ImGuiCol_PlotLines] = ImVec4(0.40f, 0.39f, 0.38f, 0.63f);
	style->Colors[ImGuiCol_PlotLinesHovered] = ImVec4(0.25f, 1.00f, 0.00f, 1.00f);
	style->Colors[ImGuiCol_PlotHistogram] = ImVec4(0.40f, 0.39f, 0.38f, 0.63f);
	style->Colors[ImGuiCol_PlotHistogramHovered] = ImVec4(0.25f, 1.00f, 0.00f, 1.00f);
	style->Colors[ImGuiCol_TextSelectedBg] = ImVec4(0.25f, 1.00f, 0.00f, 0.43f);

}