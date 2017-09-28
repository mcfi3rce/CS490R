#include <iostream>
#include <thread>
#include <array>
#include <string>

using namespace std;

static const int num_threads = 10;
static const array <string, 5> test_string = {"test", "this", "string", "array", "please"}; 
void test_print() {
	for (int i = 0; i < test_string.size(); ++i) {
		cout << test_string[i] << endl;
	}
	cout << endl;
}

int main() {
	thread t[num_threads];

	for (int i = 0; i < num_threads; ++i) {
		t[i] = thread(test_print);
	}

	cout << "Main thread exiting" << endl;

	for (int i = 0; i < num_threads; ++i) {
		t[i].join();
	}

	return 0;
}
