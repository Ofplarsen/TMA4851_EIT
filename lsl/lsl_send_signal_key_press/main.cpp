#include "lsl_cpp.h"
#include <iostream>
#include <vector>
#include <ncurses.h>

int main(int argc, char *argv[]) {
    try {
        // Create a new stream_info
		const int nchannels = 1;
        lsl::stream_info info(argc > 1 ? argv[1] : "SimpleStream", "EEG", nchannels);

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

