#include <Input.h>

std::unordered_map<SDL_Keycode, bool> Input::m_keyDown;
std::unordered_map<SDL_Keycode, bool> Input::m_keyPressed;
glm::vec2 Input::m_mouse(0.0f, 0.0f);
glm::vec2 Input::m_previousMouse(0.0f, 0.0f);

bool Input::KeyDown(SDL_Keycode keyCode) {
	if (m_keyDown.find(keyCode) == m_keyDown.end())
		m_keyDown[keyCode] = false;
	return m_keyDown[keyCode];
}

void Input::setKeyDown(SDL_Keycode keyCode, bool value) {
	m_keyDown[keyCode] = value;
}

bool Input::KeyPressed(SDL_Keycode keyCode) {
	if (m_keyPressed.find(keyCode) == m_keyPressed.end())
		m_keyPressed[keyCode] = false;
	return m_keyPressed[keyCode];
}

void Input::setKeyPressed(SDL_Keycode keyCode, bool value) {
	m_keyPressed[keyCode] = value;
}

glm::vec2 Input::Mouse() {
	return m_mouse;
}

glm::vec2 Input::RelativeMouse() {
	return m_mouse - m_previousMouse;
}

