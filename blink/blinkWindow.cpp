#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <lsl_cpp.h>

using namespace std;



int blinkRowsOrCols(vector<string> choices, bool useRows){

    bool timeOut = true;
    int seconds = 5;
    
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
    vector<float> blinkFrequencies = {1.0f, 2.0f, 5.0f, 11.0f, 10.0f, 20.0f};
    //vector<float> blinkFrequencies = {5.0f, 10.0f, 20.0f, 40.0f};

    
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

        //sf::RectangleShape rectangle(sf::Vector2f(120.f, 50.f));
        //rectangle.setFillColor(sf::Color(200, 0, 0)); 
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
        //sf::RectangleShape rectangle(sf::Vector2f(120.f, 50.f));
        //rectangle.setFillColor(sf::Color(200, 0, 0)); 
        
        //cout << "Finished i: " << i << endl;
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

        // Clear the window
        window.clear();
        time = clock.getElapsedTime().asSeconds();

        // cout << "Starting first inner loop" << endl;
        // Draw the grid
        for (int i = 0; i < cols; ++i) {
            //cout << "i is: " << i << endl;
            
            // cout << "1" << endl;
            if (i < num_rectangles){
                window.draw(rectangles[i]);
            }
            // cout << "Starting inner loop, i: " << i <<", j: " << j << endl;
        
            // Blink effect based on elapsed time and frequency
            
            // cout << "2" << endl;
            int blinkFrequency;

            

            blinkFrequency = blinkFrequencies[i];
            
            // cout << "3" << endl;
            // cout << time - blinkoffset[i] << "<=" << "1.0f / " << blinkFrequency << endl;
            if (time - blinkoffset[i]>= 1.0f / blinkFrequency) {
                // cout << "Midloop" << endl;
                
                // cout << "4" << endl;
                if (i < num_rectangles){
                    //if (rectangles[i].getFillColor() == sf::Color(100, i*50+50, 0)){
                    if (rectangles[i].getFillColor() == sf::Color::Black){
                        rectangles[i].setFillColor(sf::Color::White);
                        //rectangles[i].setFillColor(sf::Color(100, 0, i*50+50));
                    } else {
                        rectangles[i].setFillColor(sf::Color::Black);
                        //rectangles[i].setFillColor(sf::Color(100, i*50+50, 0));
                    }
                    blinkoffset[i] = clock.getElapsedTime().asSeconds();
                }
            // cout << "5" << endl;

                    

            }
        }
        
        //cout << "Starting first inner loop" << endl;
        for (int i = 0; i < rows; ++i) {
            //cout << "i is: " << i << endl;
            for (int j = 0; j < cols; ++j) {
                // cout << "Starting inner loop, i: " << i <<", j: " << j << endl;
            
                // Blink effect based on elapsed time and frequency
                /*
                int blinkFrequency;
                if (useRows){
                    blinkFrequency = blinkFrequencies[i];
                } else {
                    blinkFrequency = blinkFrequencies[j];
                }
                if (clock.getElapsedTime().asSeconds() - blinkoffset[i * cols + j]>= 1.0f / blinkFrequency) {
                    texts[i * cols + j].setFillColor(texts[i * cols + j].getFillColor() == sf::Color::White ?
                        sf::Color::Black : sf::Color::White);
                    blinkoffset[i * cols + j] = clock.getElapsedTime().asSeconds();
                }
                */

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