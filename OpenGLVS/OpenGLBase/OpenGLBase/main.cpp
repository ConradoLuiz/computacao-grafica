#include <iostream>
#include <App.h>

App *app = AppNull;

void init() {
	app = new App();
}

void draw(glm::mat4 vp) {
	
}

void end() {
	delete app;
}

int main(int argc, char *argv[]) {
	init();
	app->run(draw);
	end();
	return 0;
}

