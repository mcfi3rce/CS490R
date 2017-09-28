#include <iostream>
#include <thread>
#include <string>

using namespace std;

static const int num_threads = 10;
static const string test_string[] = {"test", "this", "string", "array", "please"};

void test_print() {
	std::cout << "This is a fairly long stream so as to induce printing errors" << std::endl;
}

int main() {
	std::thread t[num_threads];

	for (int i = 0; i < num_threads; ++i) {
		t[i] = std::thread(test_print);
	}

	std::cout << "Main thread exiting" << std::endl;

	for (int i = 0; i < num_threads; ++i) {
		t[i].join();
	}

	return 0;
}
