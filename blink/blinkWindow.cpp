#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <lsl_cpp.h>

using namespace std;



int blinkRowsOrCols(vector<string> choices, bool useRows){

    bool timeOut = true;
    int seconds = 7;
    
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
    vector<float> blinkFrequencies = {4.0f, 5.0f, 6.0f, 7.0, 11.0f, 13.0f};

    
    // Create text objects for each cell
    vector<sf::Text> texts;
    sf::Font font;
    font.loadFromFile("fonts\\ARIAL.TTF"); // Load a font
    
    int num_rectangles;
    if (useRows){
        num_rectangles = rows;
    } else {
        num_rectangles = cols;

    }
    vector<sf::RectangleShape> rectangles;

    for (int i = 0; i < num_rectangles; ++i) {
        int offset = cellSize/2;
        if (useRows){
            sf::RectangleShape rect;
            rect.setPosition(sf::Vector2f(20.f, 20.f + cellSize*i));
            rect.setSize(sf::Vector2f(cellSize*cols, cellSize));
            rect.setFillColor(sf::Color(0, 0, 0));
            rectangles.push_back(rect);

        } else {
            sf::RectangleShape rect;
            rect.setPosition(sf::Vector2f(20.f + cellSize*i, 20.f));
            rect.setSize(sf::Vector2f(cellSize, cellSize*rows));
            rect.setFillColor(sf::Color(0, 0, 0));
            rectangles.push_back(rect);
        }
    }
    
    for (int i = 0; i < rows * cols; ++i) {
        sf::Text text;
        text.setFont(font);
        text.setCharacterSize(24);
        if (i < choices.size()){
            text.setString(choices[i]);
        } else {
            text.setString("<blank>");
        }
        int c = i%cols;
        int r = i/cols;
        int offset = cellSize/2;

        text.setFillColor(sf::Color::White);
        text.setFillColor(sf::Color(128, 128, 128));
        text.setPosition(sf::Vector2f(offset + c*cellSize, offset + r*cellSize));
        texts.push_back(text);

        //Create backgrounds
    }

    
    cout << "Finished pre loop" << endl;

    // Set up clock for blinking
    sf::Clock clock;
    vector<float> blinkoffset = {0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f};
    // Main loop
    
    float time = clock.getElapsedTime().asSeconds();
    cout << "Starting main loop" << endl;
    while (window.isOpen() && (!timeOut || time < seconds))
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }
        window.clear();
        time = clock.getElapsedTime().asSeconds();

        for (int i = 0; i < cols; ++i) {
            if (i < num_rectangles){
                window.draw(rectangles[i]);
            }
            int blinkFrequency;

            blinkFrequency = blinkFrequencies[i];
            if (time - blinkoffset[i]>= 1.0f / blinkFrequency) {
                if (i < num_rectangles){
                    if (rectangles[i].getFillColor() == sf::Color::Black){
                        rectangles[i].setFillColor(sf::Color::White);
                    } else {
                        rectangles[i].setFillColor(sf::Color::Black);
                    }
                    blinkoffset[i] = clock.getElapsedTime().asSeconds();
                }

            }
        }
        
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                

                // Draw the text
                window.draw(texts[i * cols + j]);
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