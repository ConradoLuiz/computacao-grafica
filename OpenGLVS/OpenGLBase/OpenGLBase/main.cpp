#include <App.h>
#include <Cube.h>
#include <Shader.h>
#include <Transform.h>
#include <Camera.h>
#include <Time.h>

App *app = AppNull;
Shader *shader = ShaderNull;
Cube *cube = CubeNull;
Transform *cubeTransform = new Transform(glm::vec3(0.0f, 0.0f, 0.0f));

void init() {
	app = new App();
	shader = new Shader("vertexAndColorShader");
	cube = new Cube();
}

float angle = 1.0f;
bool sobe = true;

void updateCamera(Camera* camera) {
	if(Input::KeyDown(SDL_SCANCODE_W)){
		camera->moveCamera(camera->transform->forward() * -0.5f);
	}
	if(Input::KeyDown(SDL_SCANCODE_S)){
		camera->moveCamera(camera->transform->forward() * 0.5f);
	}
	if(Input::KeyDown(SDL_SCANCODE_A)){
		camera->moveCamera(camera->transform->right() * -0.5f);
	}
	if(Input::KeyDown(SDL_SCANCODE_D)){
		camera->moveCamera(camera->transform->right() * 0.5f);
	}
	if(Input::KeyDown(SDL_SCANCODE_Z)){
		camera->moveCamera(glm::vec3(0.0f, 1.0f, 0.0f) * 0.5f);
	}
	if(Input::KeyDown(SDL_SCANCODE_X)){
		camera->moveCamera(glm::vec3(0.0f, 1.0f, 0.0f) * -0.5f);
	}
	if(Input::KeyPressed(SDL_SCANCODE_C)){
		CameraMode mode = camera->cameraMode == FREE ? ARCBALL : FREE;
		camera->setCameraMode(mode);
		SDL_Log("Mudando modo");
	}
}

void draw(glm::mat4 projectionMatrix, glm::mat4 viewMatrix, Camera* camera) {
	glm::mat4 vp = projectionMatrix * viewMatrix;
	glm::mat4 model;


	updateCamera(camera);
	if (Input::KeyDown(SDL_SCANCODE_UP)) {
		cubeTransform->rotate(glm::vec3(-1.0f, 0.0f, 0.0f), LOCAL_SPACE);
	}
	if (Input::KeyDown(SDL_SCANCODE_DOWN)) {
		cubeTransform->rotate(glm::vec3(1.0f, 0.0f, 0.0f), LOCAL_SPACE);
	}
	camera->arcBallTarget = cubeTransform;
	cubeTransform->position = glm::vec3(angle, angle, 5.0f);
	camera->update();

	shader->setMVP(vp*cubeTransform->getTransform());
	cube->draw();
	//SDL_Log(glm::to_string(camera->transform->position).c_str());
/*
	cubeTransform->position += glm::vec3(2.5f, -2.5f, 0.0f);

	shader->setMVP(vp*cubeTransform->getTransform());
	cube->draw();

	cubeTransform->position += glm::vec3(-2.5f, -2.5f, 0.0f);

	shader->setMVP(vp*cubeTransform->getTransform());
	cube->draw();

	cubeTransform->position += glm::vec3(-2.5f, 2.5f, 0.0f);

	shader->setMVP(vp*cubeTransform->getTransform());
	cube->draw();

	if (cubeTransform->position.y > 2.5f) { 
		cubeTransform->position = glm::vec3(0.0f, 2.5f, 0.0f);
		sobe = false; 
	}
	else if (cubeTransform->position.y < -1.0f) { 
		cubeTransform->position = glm::vec3(0.0f, -1.0f, 0.0f);
		sobe = true; 
	}

	if (sobe) {
		cubeTransform->position += glm::vec3(0.0f, 0.1f, 0.0f);
	}
	else {
		cubeTransform->position += glm::vec3(0.0f, -0.1f, 0.0f);
	}

	shader->setMVP(vp*cubeTransform->getTransform());
	cube->draw();
*/
	/*
	cubeTransform->position += glm::vec3(0.0f, 0.0f, 2.5f);
	shader->setMVP(vp*cubeTransform->getTransform());
	cube->draw();*/


	/*for(int i=0;i<=10;i++){
		for (int j = 0; j <= 10; j++){
			for (int k = 0; k <= 10; k++) {

			cubeTransform->position = glm::vec3(float(i) * 4.0f , float(k) * 4.0f, float(j) * 4.0f);

			shader->setMVP(vp*cubeTransform->getTransform());
			
			cube->draw();
			}
		}

	}*/

}

void keyboard(SDL_Event event) {
	
	//switch (event.key.keysym.sym){
	//	case SDLK_UP:
	//		cubeTransform->rotate(glm::vec3(-1.0f,0.0f,0.0f), LOCAL_SPACE);
	//		break;
	//	case SDLK_DOWN:
	//		cubeTransform->rotate(glm::vec3(1.0f, 0.0f, 0.0f), LOCAL_SPACE);
	//		break;
	//	case SDLK_LEFT:
	//		cubeTransform->rotate(glm::vec3(0.0, 0.0f, 1.0f), LOCAL_SPACE);
	//		break;
	//	case SDLK_RIGHT:
	//		cubeTransform->rotate(glm::vec3(0.0, 0.0f, -1.0f), LOCAL_SPACE);
	//		break;
	//			
	//	case SDLK_e:
	//		cubeTransform->rotate(glm::vec3(0.0, -1.0f, 0.0), LOCAL_SPACE);
	//		break;
	//	case SDLK_q:
	//		cubeTransform->rotate(glm::vec3(0.0, 1.0f, 0.0), LOCAL_SPACE);
	//		break;

	//	case SDLK_f:
	//		cubeTransform->position += cubeTransform->forward() * -1.0f * Time::deltaTime();
	//		break;
	//	case SDLK_g:
	//		cubeTransform->position += cubeTransform->forward() * 1.0f;
	//		break;
	//	/*case SDLK_a:
	//		cubeTransform->position += cubeTransform->right() * -1.0f;
	//		break;
	//	case SDLK_d:
	//		cubeTransform->position += cubeTransform->right() * 1.0f;
	//		break;*/

	//	case SDLK_i:
	//		cubeTransform->rotate(glm::vec3(-1.0f, 0.0f, 0.0f), WORLD_SPACE);
	//		break;
	//	case SDLK_k:
	//		cubeTransform->rotate(glm::vec3(1.0f, 0.0f, 0.0f), WORLD_SPACE);
	//		break;
	//	case SDLK_j:
	//		cubeTransform->rotate(glm::vec3(0.0, 0.0f, 1.0f), WORLD_SPACE);
	//		break;
	//	case SDLK_l:
	//		cubeTransform->rotate(glm::vec3(0.0, 0.0f, -1.0f), WORLD_SPACE);
	//		break;
	//	default:
	//		break;
	//}

}

void end() {
	delete cube;
	delete cubeTransform;
	delete shader;
	delete app;
}

int main(int argc, char *argv[]) {
	init();
	app->run(draw, keyboard);
	end();
	return 0;
}

