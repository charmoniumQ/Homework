#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;
//#define PRINT

long result(const vector<int>& list) {
	long maxProduct = 0, product = 1;
	for (unsigned int start = 0; start < list.size(); ++start) {
		product = 1;
		for (unsigned int end = start; end < list.size(); ++end) {
			product *= list[end];
			#ifdef PRINT
				cout << "Starting from: list[" << start << "], multiplying in: "
				     << "list[" << end << "], to get: " << product << endl;
			#endif
			maxProduct = max(maxProduct, product);
		}
	}
	return maxProduct;
}

void read() {
	// M == number of cases
	int M = 1;

	// N == number of elements in this case
	int N; cin >> N;
	while (!cin.eof()) {

		// list[0] to list[N - 1] contain the inputs
		vector<int> list (N);
		for (int i = 0; i < N; ++i) {
			cin >> list[i];
			}

		// find and disply result
		long maxProduct = result(list);
		cout << "Case #" << M << ": The maximum product is " << maxProduct
		     << "." << endl << endl;

		// prepare for next case
		cin >> N;
		M++;
	}
}

int main() {
	// int data [] = {-3, 4, 5, 6, -3};
	// vector<int> myvector (&data[0], &data[5]);
	// cout << "(" << result(myvector) << ")" << endl;

	read();
}
