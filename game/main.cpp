#include <SFML/Graphics.hpp>

const int W = 1600;
const int H = 1600;

int main() {

  // create the window
  sf::RenderWindow window(sf::VideoMode(W, H), "My window");

  // run the program as long as the window is open
  while (window.isOpen()) {
    // check all the window's events that were triggered since the last
    // iteration of the loop
    sf::Event event;
    while (window.pollEvent(event)) {
      // "close requested" event: we close the window
      if (event.type == sf::Event::Closed)
        window.close();
    }

    window.clear(sf::Color::Black);

    // draw everything here...

    // end the current frame
    window.display();
  }

  return 0;
}
