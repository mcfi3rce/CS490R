#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <iostream>
#include <string>
#include <deque>

using namespace std;

string goodFoods[] = {"Hummus", "Avocado Toast", "Peanut Butter", "Tofu Curry", "Guacamole", "Salsa", "Soda"};

deque<string> fridge;

int itemsInFridge = 0;
int fridgeSize = 4;
int numItems = 10;

pthread_cond_t foodAvailable, fridgeEmpty;
pthread_mutex_t openFridge;

void putInFridge(string food) {
	if (fridge.size() >= fridgeSize) {
		cout << "\033[33mFridge is full! " << food << " was left on the counter to mold!\033[0m\n";
		return;
	}
	cout << "\033[32mPut " << food << " in the fridge for guests\033[0m\n";
	fridge.push_back(food);
}

void takeFromFridge(int greed, long threadid) {
	for (int i = 0; i < greed; ++i) {
		if (fridge.empty()) {
			cout << "\033[31mThread " << threadid << ": Fridge is empty, so hungry....\033[0m\n";
		} else {
			string toEat = fridge.front();
			fridge.pop_front();
			cout << "\033[34mThread " << threadid << ": That " << toEat << " was delicious!\033[0m\n";
		}
	}
	return;
}

void *host(void* args) {
	for (int i = 0; i < numItems * 2; ++i) {
		int foodId = rand() % sizeof(goodFoods)/sizeof(*goodFoods);
		pthread_mutex_lock(&openFridge);
		putInFridge(goodFoods[foodId]);
		pthread_mutex_unlock(&openFridge);
		sleep(rand() % 2);
	}

}

void *guest(void* args) {
	long id = (long) args;
	for (int i = 0; i < numItems; ++i) {
		pthread_mutex_lock(&openFridge);
		takeFromFridge(1, id);
		pthread_mutex_unlock(&openFridge);
		sleep(rand() % 4);
	}

}

int main()
{
	pthread_mutex_init(&openFridge, NULL);
	pthread_t hostThread, guestThread1, guestThread2;

	pthread_create(&hostThread, NULL, host, (void *)NULL);
	pthread_create(&guestThread1, NULL, guest, (void *)1);
	pthread_create(&guestThread2, NULL, guest, (void *)2);
	pthread_join(hostThread,NULL);
	pthread_join(guestThread1,NULL);
	pthread_join(guestThread2,NULL);


	return 0;
}
