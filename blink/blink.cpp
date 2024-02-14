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

    CROW_ROUTE(app, "/json")
        .methods("POST"_method)
    ([](const crow::request& req){
        cout << "Printing from JSON: " << endl;
        auto x = crow::json::load(req.body);
        if (!x){
            cout << "Printing from error statement: " <<  "\n\n" << endl;
            return crow::response(400);
        }
        cout << "Printing from main func statement: " <<  "\n\n" << endl;
        int sum = x["a"].i()+x["b"].i();
        std::ostringstream os;
        os << sum;
        return crow::response{os.str()};
    });
    
    app.port(18080).run();
}