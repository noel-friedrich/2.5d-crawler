
#include <iostream>
#include <cmath>
#include "SFML/Graphics.hpp"
#include <list>

#define PI 3.14159274101257324219

bool render(
	sf::RenderWindow* window,
	int fov,
	float posx,
	float posy,
	float rot,
	std::vector<std::vector<sf::Color>> color,
	std::vector<std::vector<int>> matrix
) 
{

	for (int i = 0; i < fov; i++) {
		float rot_i = rot + (PI * ((float) i - (fov / 2))) / 180;
		float s = 0.02 * sin(rot_i);
		float c = 0.02 * cos(rot_i);
		float x = posx;
		float y = posy;

		int n = 0;
		while (matrix[round(x)][round(y)] == 0) {
			x += c;
			y += s;
			n += 1;
		}
		if (n == 0) return true;
		float h = 1 / (0.02 * n);
		float x_coord = window->getSize().x / fov;
		float height = window->getSize().y * h;
		float y_coord = (window->getSize().y / 2) - (height / 2);
		sf::RectangleShape rectangle(sf::Vector2f(x_coord, height));
		rectangle.setPosition(x_coord * i, y_coord);
		rectangle.setFillColor(color[round(x)][round(y)]);
		window->draw(rectangle);
	}
	return false;
}

int rInt(int min, int max) {
	return min + rand() % ((max + 1) - min);
}

std::vector<std::vector<sf::Color>> gen_colors(std::vector<std::vector<int>> matrix)
{
	std::vector<std::vector<sf::Color>> colors;
	for (int i = 0; i < matrix.size(); i++) {
		std::vector<sf::Color> temp;
		for (int j = 0; j < matrix[i].size(); j++) {
			temp.push_back(sf::Color(rInt(50, 100), rInt(50, 100), rInt(50, 100)));
		}
		colors.push_back(temp);
	}
	return colors;
}

int main() {

	srand(5);

	sf::RenderWindow window(sf::VideoMode(1500, 800), "Sim");
	window.setFramerateLimit(60);
	sf::Event event;

	std::vector<std::vector<int>> matrix
		{{1,1,1,1,1},
		 {1,0,0,0,1},
		 {1,0,1,0,1},
		 {1,0,0,0,1},
		 {1,1,1,1,1}};

	std::vector<std::vector<sf::Color>> color = gen_colors(matrix);

	int fov = 125;
	float posx = 1;
	float posy = 1;
	float rot = PI / 4;

	while (window.isOpen()) {
		while (window.pollEvent(event)) {
			if (event.type == sf::Event::EventType::Closed)
				window.close();
		}
		window.clear(sf::Color(255, 255, 255));

		if (sf::Keyboard::isKeyPressed(sf::Keyboard::Up)) {
			posx += 0.02 * cos(rot);
			posy += 0.02 * sin(rot);
		}

		if (sf::Keyboard::isKeyPressed(sf::Keyboard::Down)) {
			posx -= 0.02 * cos(rot);
			posy -= 0.02 * sin(rot);
		}

		if (sf::Keyboard::isKeyPressed(sf::Keyboard::Right))
			rot += PI / 100;

		if (sf::Keyboard::isKeyPressed(sf::Keyboard::Left))
			rot -= PI / 100;

		bool collision = render(&window, fov, posx, posy, rot, color, matrix);
		if (collision) {
			rot = PI / 4;
			posx = 1;
			posy = 1;
			fov = 125;
		}

		window.display();
	}

	return 0;
}
