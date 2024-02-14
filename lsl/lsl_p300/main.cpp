#include <iostream>
#include <chrono>
#include <thread>
#include <vector>
#include <SDL2/SDL.h>
#include "lsl_cpp.h"

struct Square {
    Uint32 frequency;
    Uint32 interval;
    bool current;
    bool white;
    bool flicker_started;
    Uint32 next_flicker;
    Uint32 start_flicker_time;
	SDL_Rect squareRect;
};

enum class FlickerType {
    UpperSquares,
    LowerSquares,
    Column1,
    Column2
};

void push_sample(lsl::stream_outlet& outlet, std::vector<int> marker) {
    outlet.push_sample(marker);
    std::cout << "Flicker Start Marker: " << marker[0] << std::endl;
}

void flickerSquares(std::vector<Square>& squares, lsl::stream_outlet& outlet) {
    for (auto& square : squares) {
        square.flicker_started = true;
        square.start_flicker_time = SDL_GetTicks();
    }

    // Send LSL marker for flicker start
    push_sample(outlet, {1});
}

void stopFlickering(std::vector<Square>& squares, lsl::stream_outlet& outlet) {
    std::vector<int> marker_end = {0}; // Initialize marker_end here

    for (auto& square : squares) {
        if (square.flicker_started) {
            // Send LSL marker for flicker end
            square.flicker_started = false;
			square.white = false;
        }
    }            
    outlet.push_sample(marker_end);
    std::cout << "Flicker End Marker: 0" << std::endl;
}

int run_flicker(std::vector<Square>& squares, lsl::stream_outlet& outlet, int step, SDL_Renderer* renderer, int duration_ms) {
	bool end = false;
	bool end2 = false;
	squares[0].start_flicker_time = SDL_GetTicks();
	squares[1].start_flicker_time = SDL_GetTicks();
    while (!end2) {
		int i = 0;
		if (end){
			stopFlickering(squares, outlet);
            std::cout << "Flicker End" << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(30));
			end2 = true;
		}

        for (auto& square : squares) {
            square.flicker_started = true;
			Uint32 current_time = SDL_GetTicks();
            Uint32 flicker_time_elapsed = current_time - square.start_flicker_time;

            if (flicker_time_elapsed <= duration_ms) {
                if (current_time >= square.next_flicker) {
                    square.white = !square.white;
                    square.next_flicker = current_time + square.interval;
                }
            } else {
				end = true;
            }

            SDL_Rect squareRect = square.squareRect; // Define your squareRect properly
            SDL_SetRenderDrawColor(renderer, square.white ? 255 : 0, square.white ? 255 : 0, square.white ? 255 : 0, 255);
            SDL_RenderFillRect(renderer, &squareRect);
			i++;
        }
		SDL_RenderPresent(renderer);
        SDL_Delay(10); // Delay to prevent excessive CPU usage
    }
    return (step + 1) % 4;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cout << "Usage: " << argv[0] << " <frequency>\n";
        return 1;
    }

    std::vector<Square> squares(4);
	int horizontal = 1920;
	int vertical = 1080;

    for (int i = 0; i < 4; ++i) {
        squares[i].frequency = std::atoi(argv[1]);
        squares[i].interval = (Uint32)(1000.0 / (2.0 * squares[i].frequency));
        squares[i].white = false;
        squares[i].flicker_started = false;
        squares[i].next_flicker = 0;
        squares[i].start_flicker_time = 0;
        squares[i].current = false;
		if (i < 2) {
        // Upper row
			squares[i].squareRect =  {i * horizontal/2, 0, horizontal/2, vertical/2};
		} else {
			squares[i].squareRect = {(i - 2) * horizontal/2, vertical/2, horizontal/2, vertical/2};
		}
    }

	int duration_ms = 1000 / std::atoi(argv[1]);  // Duration for flickering
	//int duration_ms = 3000;  // Duration for flickering

    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_EVENTS) < 0) {
        std::cout << "SDL could not initialize! SDL_Error: " << SDL_GetError() << std::endl;
        return 1;
    }

    SDL_Window* window = SDL_CreateWindow("Flicker",
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        horizontal, vertical,
        SDL_WINDOW_SHOWN);
    if (window == NULL) {
        std::cout << "Window could not be created! SDL_Error: " << SDL_GetError() << std::endl;
        SDL_Quit();
        return 1;
    }

    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (renderer == NULL) {
        std::cout << "Renderer could not be created! SDL_Error: " << SDL_GetError() << std::endl;
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    // Create LSL outlet
    const int nchannels = 1;
    lsl::stream_info info("FlickerStream", "Markers", nchannels);
    lsl::stream_outlet outlet(info);

    bool quit = false;
    int step = 0;
    bool start = false;
    FlickerType flickerType = FlickerType::UpperSquares;
    std::vector<std::vector<int>> currentSquares = {{0, 1}, {2, 3}, {0, 2}, {1, 3}};

    while (!quit) {
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                quit = true;
            }
            else if (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_o) {
                start = true;
            }
        }
        if (start) {
            std::vector<Square> squares_to_flicker = {squares[currentSquares[step][0]], squares[currentSquares[step][1]]};
            flickerSquares(squares_to_flicker, outlet);
            step = run_flicker(squares_to_flicker, outlet, step, renderer, duration_ms);
            if (step == 0) {
                start = false;
            }
        }
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}

