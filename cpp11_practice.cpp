#include <iostream>
#include <thread>
#include <mutex>
#include <array>
#include <vector>
#include <string>
#include <chrono>
#include <cxxopts.hpp>

using namespace std;

static mutex talking_stick;
static const int num_threads = 10;
static const array<string, 5> test_string = {"Test", "this", "array", "of", "strings"}; 

void test_print(bool use_mut, int thread_id) {
	if (use_mut) {
		talking_stick.lock();
	}
	for (int i = 0; i < test_string.size(); ++i) {
		cout << test_string[i] << " ";
		this_thread::sleep_for(chrono::milliseconds(10));
	}
	cout << endl;
	if (use_mut) {
		talking_stick.unlock();
	}
}

int main(int argc, char* argv[]) {
	cxxopts::Options options("Talking Stick", "To demonstrate a trivial issue with threading");

	options.add_options()
		("m,mutex", "Use mutex");

	options.parse(argc, argv);

	bool use_talking_stick = false;

	if (options.count("m") && options["mutex"].as<bool>()) {
		use_talking_stick = true;
		cout << "Using mutex" << endl;
	}

	vector<thread> threads;

	for (int i = 0; i < num_threads; ++i) {
		threads.push_back(thread(test_print, use_talking_stick, i));
	}

	for (auto &t : threads) {
		t.join();
	}

	cout << "Main thread exiting" << endl;
	return 0;
}
