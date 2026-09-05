#include <cstdlib>
#include <iostream>

int main() {
    const char* secret = std::getenv("DEMO_SECRET");
    if (secret == nullptr || secret[0] == '\0') {
        std::cerr << "DEMO_SECRET is missing or empty. Set it with `sotto set DEMO_SECRET`, then run this demo with `sotto run -- <command>`.\n";
        return 1;
    }

    std::cout << "Sotto demo: secret loaded successfully.\n";
    return 0;
}
