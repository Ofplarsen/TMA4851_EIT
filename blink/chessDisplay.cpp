#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <lsl_cpp.h>

using namespace std;



// Can be set when running program
int SCREEN_SIZE2 = 1000;
bool TIMEOUT2 = true;
int SECONDS2 = 1;
float CELLSIZE2 = 150.f;
const float BOARDCELLSIZE2 = 110.f;

vector<string> getTextureNames(){
    vector<string> names;

    names.push_back("b_pawn_png_128px.png");
    names.push_back("b_knight_png_128px.png");
    names.push_back("b_bishop_png_128px.png");
    names.push_back("b_rook_png_128px.png");
    names.push_back("b_queen_png_128px.png");
    names.push_back("b_king_png_128px.png");
    names.push_back("w_pawn_png_128px.png");
    names.push_back("w_knight_png_128px.png");
    names.push_back("w_bishop_png_128px.png");
    names.push_back("w_rook_png_128px.png");
    names.push_back("w_queen_png_128px.png");
    names.push_back("w_king_png_128px.png");
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
        if (c != "\n" && c != " "){
            sum += 1;
            squares.push_back(c);
        }
    }
    cout << sum << endl;
    return squares;
    
}

int showChessBoardSprites(string displayString){
    cout << displayString << endl;
    vector<string> cells = formatSquares(displayString);
    // Create the window
    int winSize = BOARDCELLSIZE2*8;
    
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
        if (!(image.loadFromFile("sprites2\\" + textureNames[i])))
                std::cout << "Cannot load image";   //Load Image
        
        sf::Texture texture;
        texture.loadFromImage(image);  //Load Texture from image
        textures.push_back(texture);  //Load Texture from image
    }
    
    // Create vector to hold rectangles
    vector<sf::RectangleShape> rectangles;

    // Create rows or columns to blink
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j){
            int offset = BOARDCELLSIZE2/2;
            sf::RectangleShape rect;
            rect.setPosition(sf::Vector2f(BOARDCELLSIZE2*i, BOARDCELLSIZE2*j));
            rect.setSize(sf::Vector2f(BOARDCELLSIZE2, BOARDCELLSIZE2));
            rect.setFillColor((i+j)%2==0 ? sf::Color(240, 217, 181) : sf::Color(181, 136, 99));
            rectangles.push_back(rect);
        }
    }




    // Load a font
    sf::Font font;
    font.loadFromFile("fonts\\ARIAL.TTF"); 
    
    // Create vector to hold cell texts
    vector<sf::Sprite> sprites;

    // Create text objects for each cell
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j){
           
            string text = cells[j*8+i];
            if (text != "."){
                //cout << text << ": " << getTexturePos(text) << endl;
                sf::Sprite sprite;
                sprite.setTexture(textures[getTexturePos(text)]); 
                //sprite.setTexture(textures[k]); 
                float scale = (BOARDCELLSIZE2-30)/128;
                sprite.setScale(scale, scale);
                sprite.setPosition(sf::Vector2f((i+0.35)*BOARDCELLSIZE2-20, (j + 0.35)*BOARDCELLSIZE2-20));
                sprites.push_back(sprite);
            }
        }
    }


    cout << "starting main loop" << endl;
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
            }
            
        }
        for (size_t i = 0; i < sprites.size(); i++)
        {
            window.draw(sprites[i]);
        }
        
        // Display the window
        window.display();
    }
    return 2;
}