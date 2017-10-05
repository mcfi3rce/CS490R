#include <pthread.h>
#include <unistd.h>
#include <iostream>
#include <string>
#include <ctime>
#include <deque>
#include <stack>

using namespace std;

string goodFoods[] = {"Hummus", "Avocado Toast", "Peanut Butter", "Tofu Curry", "Guacamole", "Salsa", "Hash Browns"};

class Food {
	public:
		Food() {
			validate("Raw Tofu", 3);
		}
		Food(string type) {
			validate(type, 3);
		}
		Food(string type, int timeToExpiration) {
			validate(type, timeToExpiration);
		}
		string getType() const;
		bool isExpired() const {
			return time(0) > expirationTime;
		}
	private:
		void validate(string type, int timeToExpiration) {
			type = type;
			expirationTime = time(0) + timeToExpiration;
		}
		string type;
		time_t expirationTime;
};

class Fridge {
	public:
		Fridge() { }
		int addFood(Food food) {
			add(food);
		}
		Food takeFood(int num) {
			return Food();
		}
		int foodRemaining() {
			return 0;
		}
	private:
		void add(Food item) {}
};
/*
void *test_function(void *param)
{
	int *param_value = (int *)param;
	while(++(*param_value) < 100)
	{
		sleep(1);
	}

	printf("did the thing\n");

	return NULL;
}
*/

int main()
{
	//int x = 0, y = 0;

	/* show the initial values of x and y */
	//printf("x: %d, y: %d\n", x, y);

	/* this variable is our reference to the second thread */
	//pthread_t inc_x_thread;

	/* create a second thread which executes inc_x(&x) */
	/*
	if(pthread_create(&inc_x_thread, NULL, test_function, &x)) {

		fprintf(stderr, "Error creating thread\n");
		return 1;

	}
	*/
	/* increment y to 100 in the first thread */
	//while(++y < 100);

	//printf("y increment finished\n");

	/* wait for the second thread to finish */
	/*
	if(pthread_join(inc_x_thread, NULL)) {

		fprintf(stderr, "Error joining thread\n");
		return 2;

	}
	*/

	/* show the results - x is now 100 thanks to the second thread */
	//printf("x: %d, y: %d\n", x, y);

	cout << goodFoods << endl;
	cout << sizeof(goodFoods) / sizeof(*goodFoods) << endl;
	time_t test = time(NULL);

	cout << test << endl;

	Food yum = Food("Hummus", 1);

	cout << yum.isExpired() << endl;

	sleep(2);

	cout << yum.isExpired() << endl;

	return 0;
}
