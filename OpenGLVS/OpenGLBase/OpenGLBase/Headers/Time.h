#pragma once
#include <App.h>

class Time
{
	friend class App;
private:
	static float m_deltaTime;

public:
	static float deltaTime();
}; 
	

