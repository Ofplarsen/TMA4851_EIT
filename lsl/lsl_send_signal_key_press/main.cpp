#include "lsl_cpp.h"
#include <iostream>
#include <vector>
#include <ncurses.h>

int main() {
    try {
        // Create a new stream_info
        lsl::stream_info info("KeyboardInput", "Markers", 1, 1, lsl::cf_int32, "myuniqueid123456");

        // Create the outlet
        lsl::stream_outlet outlet(info);

        // Initialize ncurses
        initscr();
        cbreak();
        noecho();
        keypad(stdscr, TRUE);

        // Loop until 'q' is pressed
        while (true) {
            int ch = getch();
            if (ch == 'o') {
                // Send 1 through the outlet when 'o' is pressed
                std::vector<int> marker_sample = {1};
                outlet.push_sample(marker_sample);
                std::cout << "Sent marker: 1" << std::endl;
            }
            if (ch == 'q') {
                break; // Break the loop if 'q' is pressed
            }
        }

        // Cleanup ncurses
        endwin();
    } catch (std::exception &e) {
        std::cerr << "Got an exception: " << e.what() << std::endl;
    }

    return 0;
}

