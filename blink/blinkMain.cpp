#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>

int return4(){
    // Create the window
    sf::RenderWindow window(sf::VideoMode(400, 400), "Grid Blinking");

    // Define the grid layout (2x2)
    const int rows = 3;
    const int cols = 3;
    const float cellWidth = 100.f;
    const float cellHeight = 100.f;

    // Define blink frequencies for each cell
    std::vector<float> blinkFrequencies = {0.05f, 0.1f, 0.2f, 0.4f, 1.0f, 2.0f, 3.0f, 4.0f, 10.0f};

    // Create text objects for each cell
    std::vector<sf::Text> texts;
    sf::Font font;
    font.loadFromFile("build\\resources\\ARIAL.TTF"); // Load a font

    for (int i = 0; i < rows * cols; ++i) {
        sf::Text text;
        text.setFont(font);
        text.setCharacterSize(24);
        text.setString(std::to_string(i + 1));
        text.setFillColor(sf::Color::White);
        texts.push_back(text);
    }

    // Set up clock for blinking
    sf::Clock clock;
    std::vector<float> blinkoffset = {0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f};
    // Main loop
    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // Clear the window
        window.clear();

        // Draw the grid
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                // Set position for each cell
                texts[i * cols + j].setPosition(j * cellWidth+20, i * cellHeight+20);

                // Blink effect based on elapsed time and frequency
                if (clock.getElapsedTime().asSeconds() - blinkoffset[i * cols + j]>= 1.0f / blinkFrequencies[i * cols + j]) {
                    texts[i * cols + j].setFillColor(texts[i * cols + j].getFillColor() == sf::Color::White ?
                        sf::Color::Transparent : sf::Color::White);
                    blinkoffset[i * cols + j] = clock.getElapsedTime().asSeconds();
                }

                // Draw the text
                window.draw(texts[i * cols + j]);
            }
        }

        // Display the window
        window.display();
    }
    return 4;
}


int main2()
{
    // Create the window
    sf::RenderWindow window(sf::VideoMode(400, 400), "Grid Blinking");

    // Define the grid layout (2x2)
    const int rows = 3;
    const int cols = 3;
    const float cellWidth = 100.f;
    const float cellHeight = 100.f;

    // Define blink frequencies for each cell
    std::vector<float> blinkFrequencies = {0.05f, 0.1f, 0.2f, 0.4f, 1.0f, 2.0f, 3.0f, 4.0f, 10.0f};

    // Create text objects for each cell
    std::vector<sf::Text> texts;
    sf::Font font;
    font.loadFromFile("build\\resources\\ARIAL.TTF"); // Load a font

    for (int i = 0; i < rows * cols; ++i) {
        sf::Text text;
        text.setFont(font);
        text.setCharacterSize(24);
        text.setString(std::to_string(i + 1));
        text.setFillColor(sf::Color::White);
        texts.push_back(text);
    }

    // Set up clock for blinking
    sf::Clock clock;
    std::vector<float> blinkoffset = {0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f};
    // Main loop
    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // Clear the window
        window.clear();

        // Draw the grid
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                // Set position for each cell
                texts[i * cols + j].setPosition(j * cellWidth+20, i * cellHeight+20);

                // Blink effect based on elapsed time and frequency
                if (clock.getElapsedTime().asSeconds() - blinkoffset[i * cols + j]>= 1.0f / blinkFrequencies[i * cols + j]) {
                    texts[i * cols + j].setFillColor(texts[i * cols + j].getFillColor() == sf::Color::White ?
                        sf::Color::Transparent : sf::Color::White);
                    blinkoffset[i * cols + j] = clock.getElapsedTime().asSeconds();
                }

                // Draw the text
                window.draw(texts[i * cols + j]);
            }
        }

        // Display the window
        window.display();
    }

    return 0;
}
