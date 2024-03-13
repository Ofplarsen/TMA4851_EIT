#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <lsl_cpp.h>

using namespace std;



// Can be set when running program
bool TIMEOUT = true;
int SECONDS = 7;
const float CELLSIZE = 150.f;
const float BOARDCELLSIZE = 110.f;

vector<string> getTextureNames(){
    vector<string> names;
    names.push_back("W_Pawn.png");
    names.push_back("W_Knight.png");
    names.push_back("W_Bishop.png");
    names.push_back("W_Rook.png");
    names.push_back("W_Queen.png");
    names.push_back("W_King.png");
    names.push_back("B_Pawn.png");
    names.push_back("B_Knight.png");
    names.push_back("B_Bishop.png");
    names.push_back("B_Rook.png");
    names.push_back("B_Queen.png");
    names.push_back("B_King.png");
    return names; 
}

int getTexturePos(string name){
    vector<string> pieceOrder = {"p", "n", "b", "r", "q", "k", "P", "N", "B", "R", "Q", "K"};
    auto it = find(pieceOrder.begin(), pieceOrder.end(), name); 

    // If element was found 
    if (it != pieceOrder.end())  
    { 
      
        // calculating the index 
        // of K 
        int index = it - pieceOrder.begin(); 
        return index;
    } else { 
        // If the element is not 
        // present in the vector 
        cout << "Illegal piece chosen" << endl; 
    } 
    //return names; 
}


vector<string> formatSquares(string displayString){
    vector<string> squares;
    int sum = 0;
    for (size_t i = 0; i < 64+7; i++){
        string c = displayString.substr(i, 1);
        if (c != "\n"){
            sum += 1;
            squares.push_back(c);
        }
    }
    cout << sum << endl;
    return squares;
    
}

int showChessBoardSprites(string displayString){
    
    vector<string> cells = formatSquares(displayString);
    // Create the window
    int winSize = BOARDCELLSIZE*8+40;
    sf::RenderWindow window(sf::VideoMode(winSize, winSize), "Game Board");


    // Define the grid layout 
    const int cols = 8;
    const int rows = 8;
    
    // What dimention to blink across
    int num_rectangles = cols*rows;




    vector<string> textureNames = getTextureNames();
    vector<sf::Texture> textures;
    for (size_t i = 0; i < textureNames.size(); i++)
    {
        sf::Image image;
        if (!(image.loadFromFile("sprites\\B_King.png")))
                std::cout << "Cannot load image";   //Load Image
        
        sf::Texture texture;
        texture.loadFromImage(image);  //Load Texture from image
    }
    
    

    






    
    // Create vector to hold rectangles
    vector<sf::RectangleShape> rectangles;

    // Create rows or columns to blink
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j){
            int offset = BOARDCELLSIZE/2;
            sf::RectangleShape rect;
            rect.setPosition(sf::Vector2f(20.f + BOARDCELLSIZE*i, 20.f + BOARDCELLSIZE*j));
            rect.setSize(sf::Vector2f(BOARDCELLSIZE, BOARDCELLSIZE));
            rect.setFillColor((i+j)%2==1 ? sf::Color(0, 0, 0) : sf::Color(50, 50, 50));
            rectangles.push_back(rect);
        }
    }




    // Load a font
    sf::Font font;
    font.loadFromFile("fonts\\ARIAL.TTF"); 
    
    // Create vector to hold cell texts
    vector<sf::Text> texts;

    // Create text objects for each cell
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j){
            /*
            // Standard settings
            sf::Text text;
            text.setFont(font);
            text.setCharacterSize(24);

            // Set content of text block if it exists
            // string textString = i + ", " + j;
            string textString = cells[j*8+i];
            text.setString(textString);
            

            // Calculate position
            int c = i%cols;
            int r = i/cols;
            int offset = BOARDCELLSIZE/2;

            // Finalize and add text
            text.setFillColor(sf::Color::White);
            text.setPosition(sf::Vector2f(offset + i*BOARDCELLSIZE, offset + j*BOARDCELLSIZE));
            texts.push_back(text);
            */
           
            string text = cells[j*8+i];
            if (text != "."){
                sf::Sprite sprite;
                sprite.setTexture(textures[getTexturePos(text)]); 
                int scale = (BOARDCELLSIZE-10)/32;
                sprite.setScale(scale, scale);

            }
        }
    }

    /*
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
    */


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

        for (size_t i = 0; i < cols; i++)
        {
            for (size_t j = 0; j < rows; j++)
            {
                window.draw(rectangles[i*cols + j]);
                window.draw(texts[i * cols + j]);
            }
            
        }
        /*/
        texture.loadFromImage(image);            //loading the image again into texture

        window.draw(sprite);
        
        */
        // Display the window
        window.display();
    }
    return 2;
}


int showChessBoardString(string displayString){
    
    vector<string> cells = formatSquares(displayString);
    // Create the window
    int winSize = BOARDCELLSIZE*8+40;
    sf::RenderWindow window(sf::VideoMode(winSize, winSize), "Game Board");


    // Define the grid layout 
    const int cols = 8;
    const int rows = 8;
    
    // What dimention to blink across
    int num_rectangles = cols*rows;
    
    // Create vector to hold rectangles
    vector<sf::RectangleShape> rectangles;

    // Create rows or columns to blink
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j){
            int offset = BOARDCELLSIZE/2;
            sf::RectangleShape rect;
            rect.setPosition(sf::Vector2f(20.f + BOARDCELLSIZE*i, 20.f + BOARDCELLSIZE*j));
            rect.setSize(sf::Vector2f(BOARDCELLSIZE, BOARDCELLSIZE));
            rect.setFillColor((i+j)%2==1 ? sf::Color(0, 0, 0) : sf::Color(50, 50, 50));
            rectangles.push_back(rect);
        }
    }




    // Load a font
    sf::Font font;
    font.loadFromFile("fonts\\ARIAL.TTF"); 
    
    // Create vector to hold cell texts
    vector<sf::Text> texts;

    // Create text objects for each cell
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j){
            // Standard settings
            sf::Text text;
            text.setFont(font);
            text.setCharacterSize(24);

            // Set content of text block if it exists
            // string textString = i + ", " + j;
            string textString = cells[j*8+i];
            text.setString(textString);
            

            // Calculate position
            int c = i%cols;
            int r = i/cols;
            int offset = BOARDCELLSIZE/2;

            // Finalize and add text
            text.setFillColor(sf::Color::White);
            text.setPosition(sf::Vector2f(offset + i*BOARDCELLSIZE, offset + j*BOARDCELLSIZE));
            texts.push_back(text);
            
           
          
        }
    }



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

        for (size_t i = 0; i < cols; i++)
        {
            for (size_t j = 0; j < rows; j++)
            {
                window.draw(rectangles[i*cols + j]);
                window.draw(texts[i * cols + j]);
            }
            
        }
        // Display the window
        window.display();
    }
    return 2;
}

int blinkRowsOrCols(vector<string> choices, bool useRows){
    // Can be set when running program

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