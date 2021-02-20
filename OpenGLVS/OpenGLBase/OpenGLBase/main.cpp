#include <App.h>
#include <Cube.h>
#include <Shader.h>
#include <Transform.h>
#include <Camera.h>
#include <Sphere.h>
#include <Time.h>

App *app = AppNull;
Shader *shader = ShaderNull;
Cube *cube = CubeNull;
Sphere *sphere = (Sphere*)NULL;

void init() {
	app = new App();
	shader = new Shader("vertexAndColorShader");
	cube = new Cube();
	sphere = new Sphere();
}

float angle = 1.0f;
bool sobe = true;

bool debugMode = false;

void ShowStatsOverlay(); 
void updateCamera(Camera* camera);

void draw(glm::mat4 projectionMatrix, glm::mat4 viewMatrix, Camera* camera) {
	glm::mat4 vp = projectionMatrix * viewMatrix;
	glm::mat4 model;


	updateCamera(camera);
	if (Input::KeyDown(SDL_SCANCODE_UP)) {
		cube->transform->rotate(glm::vec3(-1.0f, 0.0f, 0.0f), LOCAL_SPACE);
	}
	if (Input::KeyDown(SDL_SCANCODE_DOWN)) {
		cube->transform->rotate(glm::vec3(1.0f, 0.0f, 0.0f), LOCAL_SPACE);
	}
	camera->arcBallTarget = sphere->transform;
	cube->transform->position = glm::vec3(angle, angle, 5.0f);
	camera->update();

	shader->setMVP(vp*cube->transform->getTransform());
	//cube->draw();

	shader->setMVP(vp*sphere->transform->getTransform());
	sphere->draw();

	if (Input::KeyPressed(SDL_SCANCODE_F3)) { debugMode = !debugMode; }
	if (debugMode) 
	{
		ImGui::BeginMainMenuBar();
		
		if (ImGui::BeginMenu("Screen Settings"))
		{
			if (ImGui::Button("Toggle Fullscreen"))
			{
				app->toggleFullscreen();
			}
			ImGui::Spacing();
			ImGui::InputInt("Width", &app->WIDTH);
			ImGui::InputInt("Height", &app->HEIGHT);

			if (ImGui::Button("Change Resolution"))
			{
				app->setResolution(app->WIDTH, app->HEIGHT);
			}
			ImGui::EndMenu();
		}

		ImGui::EndMainMenuBar();

		ShowStatsOverlay();

		//ImGui::ShowDemoWindow();
	}

	//SDL_Log(glm::to_string(camera->transform->position).c_str());
/*
	cube->transform->position += glm::vec3(2.5f, -2.5f, 0.0f);

	shader->setMVP(vp*cube->transform->getTransform());
	cube->draw();

	cube->transform->position += glm::vec3(-2.5f, -2.5f, 0.0f);

	shader->setMVP(vp*cube->transform->getTransform());
	cube->draw();

	cube->transform->position += glm::vec3(-2.5f, 2.5f, 0.0f);

	shader->setMVP(vp*cube->transform->getTransform());
	cube->draw();

	if (cube->transform->position.y > 2.5f) { 
		cube->transform->position = glm::vec3(0.0f, 2.5f, 0.0f);
		sobe = false; 
	}
	else if (cube->transform->position.y < -1.0f) { 
		cube->transform->position = glm::vec3(0.0f, -1.0f, 0.0f);
		sobe = true; 
	}

	if (sobe) {
		cube->transform->position += glm::vec3(0.0f, 0.1f, 0.0f);
	}
	else {
		cube->transform->position += glm::vec3(0.0f, -0.1f, 0.0f);
	}

	shader->setMVP(vp*cube->transform->getTransform());
	cube->draw();
*/
	/*
	cube->transform->position += glm::vec3(0.0f, 0.0f, 2.5f);
	shader->setMVP(vp*cube->transform->getTransform());
	cube->draw();*/


	/*for(int i=0;i<=10;i++){
		for (int j = 0; j <= 10; j++){
			for (int k = 0; k <= 10; k++) {

			cube->transform->position = glm::vec3(float(i) * 4.0f , float(k) * 4.0f, float(j) * 4.0f);

			shader->setMVP(vp*cube->transform->getTransform());
			
			cube->draw();
			}
		}

	}*/

}

void keyboard(SDL_Event event) { }

void end() {
	delete cube;
	delete sphere;
	delete shader;
	delete app;
}

int main(int argc, char *argv[]) {
	init();
	app->run(draw, keyboard);
	end();
	return 0;
}

void updateCamera(Camera* camera) {
	if (Input::KeyDown(SDL_SCANCODE_W)) {
		camera->moveCamera(camera->transform->forward() * -0.5f);
	}
	if (Input::KeyDown(SDL_SCANCODE_S)) {
		camera->moveCamera(camera->transform->forward() * 0.5f);
	}
	if (Input::KeyDown(SDL_SCANCODE_A)) {
		camera->moveCamera(camera->transform->right() * -0.5f);
	}
	if (Input::KeyDown(SDL_SCANCODE_D)) {
		camera->moveCamera(camera->transform->right() * 0.5f);
	}
	if (Input::KeyDown(SDL_SCANCODE_Z)) {
		camera->moveCamera(glm::vec3(0.0f, 1.0f, 0.0f) * 0.5f);
	}
	if (Input::KeyDown(SDL_SCANCODE_X)) {
		camera->moveCamera(glm::vec3(0.0f, 1.0f, 0.0f) * -0.5f);
	}
	if (Input::KeyPressed(SDL_SCANCODE_C)) {
		CameraMode mode = camera->cameraMode == FREE ? ARCBALL : FREE;
		camera->setCameraMode(mode);
		SDL_Log("Mudando modo");
	}
}

void ShowStatsOverlay() {
	ImGuiWindowFlags window_flags = ImGuiWindowFlags_NoMove | ImGuiWindowFlags_NoDecoration | ImGuiWindowFlags_AlwaysAutoResize | ImGuiWindowFlags_NoSavedSettings | ImGuiWindowFlags_NoFocusOnAppearing | ImGuiWindowFlags_NoNav;
	ImGui::SetNextWindowBgAlpha(0.35f); // Transparent background
	const float DISTANCE = 30.0f;

	ImVec2 window_pos = ImVec2(app->WIDTH - DISTANCE, DISTANCE);
	ImVec2 window_pos_pivot = ImVec2(1.0f, 0);
	ImGui::SetNextWindowPos(window_pos, ImGuiCond_Always, window_pos_pivot);

	ImGui::Begin("Stats", NULL, window_flags);
	ImGui::Text("%f", Time::deltaTime());
	ImGui::End();
}