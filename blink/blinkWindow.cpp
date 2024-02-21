#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <lsl_cpp.h>

using namespace std;



int blinkRowsOrCols(vector<string> choices, bool blinkRows){
    // Create the window
    sf::RenderWindow window(sf::VideoMode(800, 800), "Grid Blinking");

    // Define the grid layout 
    const int cols = ceil(sqrt(choices.size()));
    int offset;
    if (cols*cols - cols >= choices.size()) {
        offset = 1;
    } else {
        offset = 0;
    }
    const int rows = cols - offset;

    const float cellSize = 150.f;


    // Define blink frequencies for each cell
    // vector<float> blinkFrequencies = {0.05f, 0.1f, 0.2f, 0.4f, 1.0f, 2.0f, 3.0f, 4.0f, 10.0f};
    vector<float> blinkFrequencies = {2.0f, 3.0f, 4.0f, 10.0f};

    // Create text objects for each cell
    vector<sf::Text> texts;
    sf::Font font;
    font.loadFromFile("fonts\\ARIAL.TTF"); // Load a font

    vector<sf::RectangleShape> rectangles(rows*cols);

    for (int i = 0; i < rows * cols; ++i) {
        // cout << "i: " << i << endl;
        sf::Text text;
        text.setFont(font);
        text.setCharacterSize(24);
        if (i < choices.size()){
            text.setString(choices[i]);
        } else {
            text.setString("Test");
        }
        text.setFillColor(sf::Color::White);
        texts.push_back(text);

        //Create backgrounds
        //sf::RectangleShape rectangle(sf::Vector2f(120.f, 50.f));
        //rectangle.setFillColor(sf::Color(200, 0, 0)); 
        rectangles[i].setPosition(sf::Vector2f(20.f + cellSize, 2*cellSize + 20.f));
        rectangles[i].setSize(sf::Vector2f(cellSize, cellSize));
        rectangles[i].setFillColor(sf::Color(200, 0, 0));
    }

    // Set up clock for blinking
    sf::Clock clock;
    vector<float> blinkoffset = {0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f};
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
                // cout << "Starting inner loop, i: " << i <<", j: " << j << endl;
                if (i * cols + j >= choices.size()){
                    break;
                } 
                // Set position for each cell
                texts[i * cols + j].setPosition(j * cellSize+20, i * cellSize+20);
                window.draw(rectangles[0]);
                // Blink effect based on elapsed time and frequency
                int blinkFrequency;
                if (blinkRows){
                    blinkFrequency = blinkFrequencies[i];
                } else {
                    blinkFrequency = blinkFrequencies[j];
                }
                if (clock.getElapsedTime().asSeconds() - blinkoffset[i * cols + j]>= 1.0f / blinkFrequency) {
                    // cout << "Midloop" << endl;
                
                    texts[i * cols + j].setFillColor(texts[i * cols + j].getFillColor() == sf::Color::White ?
                        sf::Color::Transparent : sf::Color::White);
                    blinkoffset[i * cols + j] = clock.getElapsedTime().asSeconds();
                }

                // Draw the text
                window.draw(texts[i * cols + j]);
                // cout << "Finished inner loop" << endl;
            }
        }

        // Display the window
        window.display();
    }
    return 4;
}

int blinkRows(vector<string> choices){
    return blinkRowsOrCols(choices, true);
}

int blinkCols(vector<string> choices){
    return blinkRowsOrCols(choices, false);
}