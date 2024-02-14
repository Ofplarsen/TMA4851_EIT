#include "crow.h"
#include <iostream>
#include "blinkMain.cpp"



using namespace std;


int main()
{
    crow::SimpleApp app;

    CROW_ROUTE(app, "/")([](){
        return "Hello world";
    });

    CROW_ROUTE(app, "/start")([](){
        cout << "Printing from blinkMain: " << return4() << "\n\n" << endl;
        return "Reached start";
    });
    
    app.port(18080).run();
}