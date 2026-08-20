#include <bits/stdc++.h>
using namespace std;
int main()
{

    vector<int> v;
    v.push_back(1);    // add element at the end
    v.emplace_back(2); // add the element at the end
    v.back();          // refer to last element
    v.front();         // refer to starting element
    v[0];              // element at index
    v.at(0);           // element at index
    v.empty();         // returns true if empty
    v.clear();         // removes all elements
    v.size();          // returns size of the elements

    map<int, int> a;
    a.count(1); // returns 1 if key exists
    a.find(4);  // returns iterator // mp.end()

    a.erase(3); // positon  we can also use key

    // sort(start, end)
    // reverse()
}