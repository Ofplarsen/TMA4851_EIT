#include "crow.h"
#include <iostream>
#include "blinkWindow.cpp"



using namespace std;
void sendLSL(int signal){
    const int nchannels = 1;

    lsl::stream_info info("FlickerStream", "Markers", nchannels); 
    lsl::stream_outlet outlet(info);

    std::vector<int> marker = {signal};
	outlet.push_sample(marker);
}

int main()
{
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
    ([](const crow::request& req){
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
       sendLSL(1);


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

        
        blinkRows(choiceNames);
        int sum = 4;
        std::ostringstream os;
        os << sum;

        //Send message that blinking is finished.
        sendLSL(0);


        return crow::response{os.str()};
    });
    
    app.port(18080).run();
}