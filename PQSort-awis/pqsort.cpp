#include<queue>
#include<iostream>
using namespace std;

class keyvalue{
    public:
        int key;
        int value;
        keyvalue(int k, int v) : key(k), value(v) {}
};
const auto cmpLambda = 
        [](const keyvalue a, const keyvalue b)
        {
            return b.key < a.key;
        };

void pqsort()
{
    int n;
    cin >> n;

    vector<keyvalue> keyValueVector;
    keyValueVector.reserve(n);
    priority_queue<
        keyvalue, vector<keyvalue>,
        decltype(cmpLambda)>
        pq(cmpLambda, move(keyValueVector));

    int k, v;
    for(int i = 0; i<n; i++)
    {
        cin>>k;
        cin>>v;
        pq.emplace(k,v);
    }

    while( !pq.empty())
    {
        cout << pq.top().value << endl;
        pq.pop();
    }
}

int main(int argc, char **argv)
{
    ios_base::sync_with_stdio(false);
    pqsort();
}