#pragma once
#include <globals.h>
#include <unordered_map> 

class Input
{
	friend class App;
public:
	bool static KeyDown(SDL_Keycode Keycode);
	bool static KeyPressed(SDL_Keycode Keycode);

	glm::vec2 static Mouse();
	glm::vec2 static RelativeMouse();

private: 
	static void setKeyDown(SDL_Keycode Keycode, bool value);
	static void setKeyPressed(SDL_Keycode Keycode, bool value);

	static std::unordered_map<SDL_Keycode, bool> m_keyDown;
	static std::unordered_map<SDL_Keycode, bool> m_keyPressed;

	static glm::vec2 m_mouse;
	static glm::vec2 m_previousMouse;
};