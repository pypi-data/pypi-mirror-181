import os
import argparse

home = os.path.expanduser("~")
template = """#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define nL "\\n"
#define pb push_back
#define mk make_pair
#define pii pair<int, int>
#define a first
#define b second
#define vi vector<int>
#define all(x) (x).begin(), (x).end()
#define umap unordered_map
#define uset unordered_set
#define MOD 1000000007
#define imax INT_MAX
#define imin INT_MIN
#define exp 1e9
#define sz(x) (int((x).size()))
int32_t main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int ttt; cin >> ttt;
    while(ttt--) {
        cout << ttt << endl;
    }
    return 0;
}"""

usaco_template = """/*
ID: %s
LANG: C++11
TASK: %s
*/
#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define nL "\\n"
#define pb push_back
#define mk make_pair
#define pii pair<int, int>
#define a first
#define b second
#define vi vector<int>
#define all(x) (x).begin(), (x).end()
#define umap unordered_map
#define uset unordered_set
#define MOD 1000000007
#define imax INT_MAX
#define imin INT_MIN
#define exp 1e9
#define sz(x) (int((x).size()))
int32_t main()
{
    ifstream fin("%s.in");
    ofstream fout("%s.out");
    return 0;
}"""


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file to run")
    parser.add_argument("-u", "--usaco", help="use usaco template", action="store_true")
    args = parser.parse_args()
    if not os.path.exists(f"{args.filename}.cpp"):
        with open(f"{args.filename}.cpp", "w+") as f:
            if args.usaco:
                if os.path.exists(os.path.join(home, ".usaco")):
                    with open(os.path.join(home, ".usaco")) as f2:
                        username = f2.readline().strip()
                else:
                    username = input("Please enter your usaco username: ")
                    with open(os.path.join(home, ".usaco"), "w+") as f2:
                        f2.write(username)

                f.write(usaco_template % (username, args.filename, args.filename, args.filename))
            else:
                f.write(template)
    else:
        os.system(f"g++ {args.filename}.cpp")
        os.system(f"./a.out")
        os.system(f"rm -rf ./a.out")


if __name__ == "__main__":
    cli()