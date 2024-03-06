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
    const int nchannels = 1;
    lsl::stream_info info("FlickerStream", "Markers", nchannels,  0.0, lsl::cf_int16, "MentalChess"); 
    lsl::stream_outlet outlet(info);

    std::vector<int> marker = {1};
	outlet.push_sample(marker);

    cout << "outlet: " << endl;
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

        //Start blinking
        std::cout << "Printing from JSON: " << endl;
        auto x = crow::json::load(req.body);
        if (!x){
            cout << "Printing from error statement: " <<  "\n\n" << endl;
            return crow::response(400);
        }

        auto indices_obj = x["indices"];

        auto state = x["state"];
        auto choices = state["choices"];
        
        vector<string> choiceNames = {};
        vector<string> pathIds = {};
        vector<crow::json::rvalue> indices = {};

        for (size_t i = 0; i < indices_obj.size(); i++)
        {
            auto obj = indices_obj[i];
            indices.push_back(obj);
        }

        bool finished = false;
        bool final_iteration = false;
        while (!finished) {
            cout << "starting loop: " << endl;
            for (size_t i = 0; i < choices.size(); i++)
            {
                string name = choices[i]["id"].s();
                choiceNames.push_back(name);
            }
            if (indices.size() == 0){
                finished = true;
            } else {
                cout << "starting else" << endl;

                
                auto index_list = indices[0];
                indices = vector<crow::json::rvalue>(indices.begin() + 1, indices.end());

                int i = index_list[0].i();
                int j = index_list[1].i();

                const int cols = ceil(sqrt(choices.size()));
                int chosen_index = j + i*cols;
                std::cout << "i: " << i << ", j " << j << ": " << chosen_index << endl;

                cout << "Id is " << choices[chosen_index]["id"] << endl;
                pathIds.push_back(choices[chosen_index]["id"].s());
                cout << chosen_index << endl;
                cout << choices[chosen_index] << endl;
                cout << choices[chosen_index]["choices"] << endl;
                auto choices2 = choices[chosen_index]["choices"];
                cout << "choices2: " << choices2 << endl;
                choices = choices2;

                choiceNames = {};
                cout << "Finished else" << endl;
                if (choices.size() == 0){
                    final_iteration = true;


                    cout << "final it" << endl;



                    //return crow::response(std::move(outList));
                    
                }
            }
        }
        cout << "ending loop" << endl;
        if (!final_iteration){
            std::vector<int> marker = {0};

            cout << "Sending signal" << endl;
            outlet.push_sample(marker);
            cout << "signal sent" << endl;
            cout << choices << endl;
            cout << "Printing from main func statement: " << x["state"]["display"] << "\n\n" << endl;
            cout << "Success" << endl;
        
            
            blinkRows(choiceNames);
            cout << "length of vector: " << choices.size() << endl;

            //Send message that blinking is finished.
            //sendLSL2(2, outlet);

            marker = {1};
            outlet.push_sample(marker);
            
            blinkCols(choiceNames);

            //Send message that blinking is finished.
            //sendLSL2(0, outlet);
            marker = {2};
            outlet.push_sample(marker);
        }
        
        return crow::response(json_return_object(final_iteration, pathIds));
    });
    
    app.port(18080).run();
}