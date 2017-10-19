#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <picosha2.h>
 
int main()
{
	std::ifstream word_file;
	word_file.open("words100k.txt");

	std::vector<std::string> words;
	std::string word;
	while (std::getline (word_file, word)) {
		words.push_back(word);
	}

	word_file.close();

	std::cout << "Number of words read: " << words.size() << std::endl;

	#pragma omp parallel for
	for (int i = 0; i < words.size(); ++i) {
		std::string current_word = words.at(i);
		std::vector<unsigned char> hash(32);

		picosha2::hash256(current_word, hash);
		std::string hash_str = picosha2::bytes_to_hex_string(hash.begin(), hash.end());
	}

	return 0;
}
