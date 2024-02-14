#include <iostream>
#include <vector>
#include <SDL2/SDL.h>
#include "lsl_cpp.h"

struct Square {
    Uint32 frequency;
    Uint32 interval;
    bool white;
    bool flicker_started;
    Uint32 next_flicker;
    Uint32 start_flicker_time;
};

void flickerUpperSquares(std::vector<Square>& squares) {
    squares[0].flicker_started = true;
    squares[0].start_flicker_time = SDL_GetTicks();

    squares[1].flicker_started = true;
    squares[1].start_flicker_time = SDL_GetTicks();
}

void flickerLowerSquares(std::vector<Square>& squares) {
    squares[2].flicker_started = true;
    squares[2].start_flicker_time = SDL_GetTicks();

    squares[3].flicker_started = true;
    squares[3].start_flicker_time = SDL_GetTicks();
}

void flickerColumn1(std::vector<Square>& squares) {
    squares[0].flicker_started = true;
    squares[0].start_flicker_time = SDL_GetTicks();

    squares[2].flicker_started = true;
    squares[2].start_flicker_time = SDL_GetTicks();
}

void flickerColumn2(std::vector<Square>& squares) {
    squares[1].flicker_started = true;
    squares[1].start_flicker_time = SDL_GetTicks();

    squares[3].flicker_started = true;
    squares[3].start_flicker_time = SDL_GetTicks();
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        std::cout << "Usage: " << argv[0] << " <frequency>\n";
        return 1;
    }

    std::vector<Square> squares(4);

    for (int i = 0; i < 4; ++i) {
        squares[i].frequency = std::atoi(argv[1]);
        squares[i].interval = (Uint32)(1000.0 / (2.0 * squares[i].frequency));
        squares[i].white = false;
        squares[i].flicker_started = false;
        squares[i].next_flicker = 0;
        squares[i].start_flicker_time = 0;
    }

    int duration_ms = 300; // Duration for flickering

    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_EVENTS) < 0) {
        std::cout << "SDL could not initialize! SDL_Error: " << SDL_GetError() << std::endl;
        return 1;
    }

    SDL_Window *window = SDL_CreateWindow("Flicker",
                                          SDL_WINDOWPOS_CENTERED,
                                          SDL_WINDOWPOS_CENTERED,
                                          1920, 1080,
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

    bool quit = false;

    while (!quit) {
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                quit = true;
            }
            else if (event.type == SDL_KEYDOWN) {
                if (event.key.keysym.sym == SDLK_o) {
                    flickerUpperSquares(squares);
                    // Send LSL marker for flicker start
                    std::vector<int> marker_start = {1};
                    outlet.push_sample(marker_start);
                    std::cout << "Flicker Start Marker: 1" << std::endl;
                }
                else if (event.key.keysym.sym == SDLK_p) {
                    flickerLowerSquares(squares);
                    // Send LSL marker for flicker start
                    std::vector<int> marker_start = {1};
                    outlet.push_sample(marker_start);
                    std::cout << "Flicker Start Marker: 1" << std::endl;
                }
                else if (event.key.keysym.sym == SDLK_q) {
                    flickerColumn1(squares);
                    // Send LSL marker for flicker start
                    std::vector<int> marker_start = {1};
                    outlet.push_sample(marker_start);
                    std::cout << "Flicker Start Marker: 1" << std::endl;
                }
                else if (event.key.keysym.sym == SDLK_r) {
                    flickerColumn2(squares);
                    // Send LSL marker for flicker start
                    std::vector<int> marker_start = {1};
                    outlet.push_sample(marker_start);
                    std::cout << "Flicker Start Marker: 1" << std::endl;
                }
            }
        }

        for (int i = 0; i < 4; ++i) {
            if (squares[i].flicker_started) {
                Uint32 current_time = SDL_GetTicks();
                Uint32 flicker_time_elapsed = current_time - squares[i].start_flicker_time;

                if (flicker_time_elapsed <= duration_ms) {
                    if (current_time >= squares[i].next_flicker) {
                        squares[i].white = !squares[i].white;
                        squares[i].next_flicker = current_time + squares[i].interval;
                    }
                } else {
                    // Send LSL marker for flicker end
                    std::vector<int> marker_end = {0};
                    outlet.push_sample(marker_end);
                    std::cout << "Flicker End Marker: 0" << std::endl;

                    squares[i].flicker_started = false;
                }
            }

            // Render each square
            SDL_Rect squareRect;
            if (i < 2) {
                // Upper row
                squareRect = {i * 960, 0, 960, 540};
            } else {
                // Lower row
                squareRect = {(i - 2) * 960, 540, 960, 540};
            }

            SDL_SetRenderDrawColor(renderer, squares[i].white ? 255 : 0, squares[i].white ? 255 : 0, squares[i].white ? 255 : 0, 255);
            SDL_RenderFillRect(renderer, &squareRect);
        }

        SDL_RenderPresent(renderer);
        SDL_Delay(10); // Delay to prevent excessive CPU usage
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}

