#include "crow.h"
#include <iostream>
#include "blinkWindow.cpp"
#include <windows.h>  
//#include "displayChess.cpp"
//#include "surgeChess\\src\\chess_engine.cpp"



using namespace std;

/*
void sendLSL(int signal){
    const int nchannels = 1;

    lsl::stream_info info("FlickerStream", "Markers", nchannels); 
    lsl::stream_outlet outlet(info);

    std::vector<int> marker = {signal};
	outlet.push_sample(marker);
}
*/

void sendLSL2(int signal, lsl::stream_outlet outlet){
    std::vector<int> marker = {signal};
	outlet.push_sample(marker);
}

int main()
{
    const int nchannels = 1;
    lsl::stream_info info("FlickerStream", "Markers", nchannels,  0.0, lsl::cf_int16, "MentalChess"); 
    lsl::stream_outlet outlet(info);


    crow::SimpleApp app;


    CROW_ROUTE(app, "/")([](){
        return "Hello world";
    });

    CROW_ROUTE(app, "/start")([](){
        // cout << "Printing from blinkMain: " << return4() << "\n\n" << endl;
        return "Reached start";
    });

    CROW_ROUTE(app, "/json")
        .methods("POST"_method)
    ([&outlet, nchannels](const crow::request& req){
        
        //old code, keeping in case moving this to func does not work.
        /*
        // Create LSL outlet
        const int nchannels = 1;
        cout << "1" << endl;

        lsl::stream_info info("FlickerStream", "Markers", nchannels);
        lsl::stream_outlet outlet(info);
        
        //Send message that blinking will start
        std::vector<int> marker_start = {1};
		outlet.push_sample(marker_start);
        */
       //sendLSL2(1, outlet);

       std::vector<int> marker = {0};
	    outlet.push_sample(marker);


        //Start blinking
        cout << "Printing from JSON: " << endl;
        auto x = crow::json::load(req.body);
        if (!x){
            cout << "Printing from error statement: " <<  "\n\n" << endl;
            return crow::response(400);
        }
        cout << "Printing from main func statement: " << x["display"] << "\n\n" << endl;

        auto choices = x["choices"];
        vector<string> choiceNames = {};
        for (size_t i = 0; i < choices.size(); i++)
        {
            string name = choices[i]["id"].s();
            choiceNames.push_back(name);
        }
        
        blinkCols(choiceNames);
        cout << "length of vector: " << choices.size() << endl;

        //Send message that blinking is finished.
        //sendLSL2(2, outlet);

        marker = {1};
        outlet.push_sample(marker);
        
        blinkRows(choiceNames);

        //Send message that blinking is finished.
        //sendLSL2(0, outlet);
        marker = {2};
	    outlet.push_sample(marker);


        int sum = 4;
        std::ostringstream os;
        os << sum;
        return crow::response{os.str()};
    });
    
    app.port(18080).run();
}