#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;
//#define PRINT

long result(const vector<int>& list) {
  long maxProduct = 0, product = 1;
  for (unsigned int start = 0; start < list.size(); ++start) {
	for (unsigned int end = start + 1; end <= list.size(); ++end) {
	  product = 1;
	  for (unsigned int idx = start; idx < end; ++idx) {
		product *= list[idx];
        #ifdef PRINT
		  cout << list[idx] << ", ";
        #endif
	  }
      #ifdef PRINT
	    cout << endl;
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
	cout << "Case #" << M << ": The maximum product is " << maxProduct << "." << endl << endl;

	// prepare for next case
	cin >> N;
	M++;
  }
}

int main() {
  //int data [] = {-3, 4, 5, 6, -3};
  //vector<int> myvector (&data[0], &data[2]);
  //cout << "(" << result(myvector) << ")" << endl;

  read();
}
