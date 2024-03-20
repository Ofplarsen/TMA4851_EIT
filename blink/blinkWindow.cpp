#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <lsl_cpp.h>

using namespace std;



// Can be set when running program
int SCREEN_SIZE = 1000;
bool TIMEOUT = true;
int SECONDS = 6;
float CELLSIZE = 150.f;
const float BOARDCELLSIZE = 110.f;


int blinkRowsOrCols(vector<string> choices, bool useRows){
    
    // Define the grid layout 
    const int cols = ceil(sqrt(choices.size()));
    int offset;
    if (cols*cols - cols >= choices.size()) {
        offset = 1;
    } else {
        offset = 0;
    }
    const int rows = cols - offset;

    // Can be set when running program
    //CELLSIZE = SCREEN_SIZE-40/rows;

    // Define blink frequencies for each cell
    vector<float> blinkFrequencies = {4.0f, 5.0f, 6.0f, 7.0, 11.0f, 13.0f};
    
    // Create the window
    //sf::RenderWindow window(sf::VideoMode(CELLSIZE*rows+40, CELLSIZE*cols + 40), "Grid Blinking");
    sf::RenderWindow window(sf::VideoMode(800, 800), "Grid Blinking");

    
    
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

int blinkRowsOrColsp300(vector<string> choices, bool useRows){
    // 600  
    const int P300WAIT = 200;
    const int P300BLINK = 125;
    const int P300TOTAL = 800;
    // Define the grid layout 
    const int cols = ceil(sqrt(choices.size()));
    int offset;
    if (cols*cols - cols >= choices.size()) {
        offset = 1;
    } else {
        offset = 0;
    }
    const int rows = cols - offset;

    // Create the window
    //sf::RenderWindow window(sf::VideoMode(CELLSIZE*rows+40, CELLSIZE*cols + 40), "Grid Blinking");
    sf::RenderWindow window(sf::VideoMode(800, 800), "Grid Blinking");

    
    
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
    
    // Main loop
    float lastCheckin = 0.0;
    float time = clock.getElapsedTime().asMilliseconds() - lastCheckin;
    bool blink = false;
    int rowColNum = 0;
    bool finished = false;
    
    sf::Color newColor = sf::Color::Green;

    while (window.isOpen() && !finished)
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
        time = clock.getElapsedTime().asMilliseconds() - lastCheckin;

        // cout << time << ", " << blink << endl;

        if (time > P300WAIT && time <= P300WAIT + P300BLINK && !blink ){
            newColor = sf::Color::White;
            blink = true;
        } else if (time > P300WAIT + P300BLINK && blink) {
            newColor = sf::Color::Black;
            blink = false;
        }



        // Draw rectangles
        for (int i = 0; i < cols; ++i) {
            // Print rectangle if it exists
            if (i < num_rectangles){
                // Draw row or column
                window.draw(rectangles[i]);

                if (i == rowColNum && newColor != sf::Color::Green) {
                    rectangles[i].setFillColor(newColor);
                    if (newColor == sf::Color::Black) {
                        rowColNum++;
                    }
                    newColor = sf::Color::Green;
                    
                    
                }
            }
        }
        // Draw the text
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                window.draw(texts[i * cols + j]);
            }
        }
        if (time > P300TOTAL){
            if (rowColNum == num_rectangles){
                finished = true;
            }
            lastCheckin += P300TOTAL;
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

int blinkRowsp300(vector<string> choices){
    return blinkRowsOrColsp300(choices, true);
}

int blinkColsp300(vector<string> choices){
    return blinkRowsOrColsp300(choices, false);
}