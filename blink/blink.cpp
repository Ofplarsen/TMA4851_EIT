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

crow::json::wvalue json_return_object(bool is_final, vector<string> pathIds){
    crow::json::wvalue json_obj;
    json_obj["is_final"] = is_final;
    json_obj["ids"] = pathIds;
    return json_obj;

}

int main()
{
    // Set up lsl stream
    const int nchannels = 1;
    lsl::stream_info info("FlickerStream", "Markers", nchannels,  0.0, lsl::cf_int16, "MentalChess"); 
    lsl::stream_outlet outlet(info);

    // Create API app
    crow::SimpleApp app;


    CROW_ROUTE(app, "/")([](){
        return "Hello world";
    });

    CROW_ROUTE(app, "/start")([](){
        // cout << "Printing from blinkMain: " << return4() << "\n\n" << endl;
        return "Reached start";
    });

    CROW_ROUTE(app, "/index_data")
        .methods("POST"_method)
    ([&outlet, nchannels](const crow::request& req){
        // Get json from request
        auto x = crow::json::load(req.body);
        if (!x){
            cout << "Printing from error statement: " <<  "\n\n" << endl;
            return crow::response(400);
        }
        // Load fields from json
        auto indices_obj = x["indices"];
        auto state = x["state"];
        auto choices = state["choices"];
        auto display = state["display"];

        cout << display << endl;
        
        vector<string> choiceNames;
        vector<string> pathIds = {};
        vector<crow::json::rvalue> indices = {};
        
        // Load list of choices made
        for (size_t i = 0; i < indices_obj.size(); i++)
        {
            auto obj = indices_obj[i];
            indices.push_back(obj);
        }
        
        bool finished = false;
        bool final_iteration = false;

        while (!finished) {
            // Reset list of choices
            choiceNames = {};

            for (size_t i = 0; i < choices.size(); i++)
            {
                // For each choice, create a list of names
                string name = choices[i]["id"].s();
                choiceNames.push_back(name);
            }
            // If we have traversed all previous choices
            if (indices.size() == 0){
                finished = true;
            } else {
                // Get the indexes of previous choice
                auto index_list = indices[0];
                // Store the remaining choices
                indices = vector<crow::json::rvalue>(indices.begin() + 1, indices.end());

                // Get rows and columns of previous choice
                int i = index_list[0].i();
                int j = index_list[1].i();

                // Calculate previous choice
                const int cols = ceil(sqrt(choices.size()));
                int chosen_index = j + i*cols;
                
                // Save id of previous choice
                pathIds.push_back(choices[chosen_index]["id"].s());

                // Set choices to the sublist of choice within the chosen choice
                auto choices2 = choices[chosen_index]["choices"];
                choices = choices2;

                if (choices.size() == 0){
                    final_iteration = true;
                }
            }
        }

        // Start blinking if more choices need to be made.
        if (!final_iteration){
            // Send start signal
            std::vector<int> marker = {0};
            outlet.push_sample(marker);
        
            // Blink the rows
            blinkRows(choiceNames);

            //Send message that first blinking is finished and second is starting
            marker = {1};
            outlet.push_sample(marker);
            
            // Blink the columns
            blinkCols(choiceNames);

            //Send message that blinking is finished.
            marker = {2};
            outlet.push_sample(marker);
        }
        // Return status and choices made
        return crow::response(json_return_object(final_iteration, pathIds));
    });
    
    // Start API
    app.port(18080).run();
}