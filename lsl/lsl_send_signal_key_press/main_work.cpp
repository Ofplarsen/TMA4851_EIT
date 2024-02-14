#include <iostream>
#include <vector>
#include <SDL2/SDL.h>
#include "lsl_cpp.h"

int main(int argc, char *argv[]) {
    if (argc != 3) {
        std::cout << "Usage: " << argv[0] << " <frequency> <duration_ms>\n";
        return 1;
    }

    int frequency = std::atoi(argv[1]);
    int duration_ms = std::atoi(argv[2]);

    if (frequency <= 0 || duration_ms <= 0) {
        std::cout << "Invalid frequency or duration. Please provide positive integer values.\n";
        return 1;
    }

    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_EVENTS) < 0) {
        std::cout << "SDL could not initialize! SDL_Error: " << SDL_GetError() << std::endl;
        return 1;
    }

    SDL_Window *window = SDL_CreateWindow("Flicker",
                                          SDL_WINDOWPOS_CENTERED,
                                          SDL_WINDOWPOS_CENTERED,
                                          800, 600,
                                          SDL_WINDOW_SHOWN);
    if (window == NULL) {
        std::cout << "Window could not be created! SDL_Error: " << SDL_GetError() << std::endl;
        SDL_Quit();
        return 1;
    }

    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
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

    Uint32 interval = (Uint32)(1000.0 / (2.0 * frequency));

    bool quit = false;
    bool white = false;
    bool flicker_started = false;
    Uint32 next_flicker = 0;
	Uint32 start_flicker_time = 0; // Variable to store the time when flickering starts

	while (!quit) {
		SDL_Event event;
		while (SDL_PollEvent(&event)) {
			if (event.type == SDL_QUIT) {
				quit = true;
			}
			else if (event.type == SDL_KEYDOWN) {
				if (event.key.keysym.sym == SDLK_o && !flicker_started) {
					flicker_started = true;
					start_flicker_time = SDL_GetTicks(); // Record the start time of flickering

					// Send LSL marker for flicker start
					std::vector<int> marker_start = {1};
					outlet.push_sample(marker_start);
					std::cout << "Flicker Start Marker: 1" << std::endl;
				}
			}
		}

		if (flicker_started) {
			Uint32 current_time = SDL_GetTicks();
			Uint32 flicker_time_elapsed = current_time - start_flicker_time;

			if (flicker_time_elapsed <= duration_ms) { // Ensure flickering continues within duration
				if (current_time >= next_flicker) {
					white = !white;
					next_flicker = current_time + interval;
				}
			} else {
				// Send LSL marker for flicker end
				std::vector<int> marker_end = {0};
				outlet.push_sample(marker_end);
				std::cout << "Flicker End Marker: 0" << std::endl;

				flicker_started = false;
			}
		}

		SDL_SetRenderDrawColor(renderer, white ? 255 : 0, white ? 255 : 0, white ? 255 : 0, 255);
		SDL_RenderClear(renderer);
		SDL_RenderPresent(renderer);
	}
		SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}

