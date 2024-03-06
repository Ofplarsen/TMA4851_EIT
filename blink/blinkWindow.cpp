#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <lsl_cpp.h>

using namespace std;



int showChessBoardString(string displayString){
    
    // Create the window
    sf::RenderWindow window(sf::VideoMode(800, 800), "Game Board");


    // Load a font
    sf::Font font;
    font.loadFromFile("fonts\\ARIAL.TTF"); 

    // Create text object
    sf::Text text;

    // Standard settings
    text.setFont(font);
    text.setCharacterSize(24);
    int offset = 20;

    // Set content of text block if it exists
    text.setString(displayString);


    // Finalize and add text
    text.setFillColor(sf::Color::White);
    text.setPosition(sf::Vector2f(offset, offset));


     while (window.isOpen())
    {
        // Check if window is closed
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // Reset window
        window.clear();
        
        window.draw(text);
        
        // Display the window
        window.display();
    }
    return 2;
}

int blinkRowsOrCols(vector<string> choices, bool useRows){
    // Can be set when running program
    bool TIMEOUT = true;
    int SECONDS = 7;
    const float CELLSIZE = 150.f;

    // Define blink frequencies for each cell
    vector<float> blinkFrequencies = {4.0f, 5.0f, 6.0f, 7.0, 11.0f, 13.0f};
    
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
    
    // What dimention to blink across
    int num_rectangles;
    if (useRows){
        num_rectangles = rows;
    } else {
        num_rectangles = cols;
    }

    // Create vector to hold rectangles
    vector<sf::RectangleShape> rectangles;

    // Create rows or columns to blink
    for (int i = 0; i < num_rectangles; ++i) {
        int offset = CELLSIZE/2;
        if (useRows){
            sf::RectangleShape rect;
            rect.setPosition(sf::Vector2f(20.f, 20.f + CELLSIZE*i));
            rect.setSize(sf::Vector2f(CELLSIZE*cols, CELLSIZE));
            rect.setFillColor(sf::Color(0, 0, 0));
            rectangles.push_back(rect);

        } else {
            sf::RectangleShape rect;
            rect.setPosition(sf::Vector2f(20.f + CELLSIZE*i, 20.f));
            rect.setSize(sf::Vector2f(CELLSIZE, CELLSIZE*rows));
            rect.setFillColor(sf::Color(0, 0, 0));
            rectangles.push_back(rect);
        }
    }
    
    // Create vector to hold cell texts
    vector<sf::Text> texts;

    // Load a font
    sf::Font font;
    font.loadFromFile("fonts\\ARIAL.TTF"); 

    // Create text objects for each cell
    for (int i = 0; i < rows * cols; ++i) {
        // Standard settings
        sf::Text text;
        text.setFont(font);
        text.setCharacterSize(24);

        // Set content of text block if it exists
        if (i < choices.size()){
            text.setString(choices[i]);
        } else {
            text.setString("<blank>");
        }

        // Calculate position
        int c = i%cols;
        int r = i/cols;
        int offset = CELLSIZE/2;

        // Finalize and add text
        text.setFillColor(sf::Color(128, 128, 128));
        text.setPosition(sf::Vector2f(offset + c*CELLSIZE, offset + r*CELLSIZE));
        texts.push_back(text);
    }


    // Set up clock for blinking
    sf::Clock clock;

    // Create vector for calculating when to blink different rows or columns
    vector<float> blinkoffset = {0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f};
    
    // Main loop
    float time = clock.getElapsedTime().asSeconds();
    while (window.isOpen() && (!TIMEOUT || time < SECONDS))
    {
        // Check if window is closed
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // Reset window
        window.clear();

        // Load current time
        time = clock.getElapsedTime().asSeconds();

        // Draw rectangles
        for (int i = 0; i < cols; ++i) {
            // Print rectangle if it exists
            if (i < num_rectangles){
                // Draw row or column
                window.draw(rectangles[i]);

                // Check if it is time to blink rectangle
                if (time - blinkoffset[i]>= 1.0f / blinkFrequencies[i]) {
                    // Blink rectangle by switching color
                    rectangles[i].setFillColor(rectangles[i].getFillColor() == sf::Color::Black ? sf::Color::White : sf::Color::Black);

                    // Reset time when last rectangle was blinked
                    blinkoffset[i] = clock.getElapsedTime().asSeconds();
                }
            }
        }
        // Draw the text
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
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