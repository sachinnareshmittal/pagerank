#include <iostream>
#include <vector>
#include <limits.h>
#include <algorithm>
#include <iomanip>
using namespace std;

// print a given matrix
void print_mat(vector< vector<float> > &P){
	for(int i=0;i<P.size();i++){
		for(int j=0;j<P.size();j++){
			cout << P[i][j] << " ";
		}
		cout << endl;
	}
}

// print a given vector
void print_vector(vector<float> &P){
	for(int j=0;j<P.size();j++){
		cout << P[j] << " ";
	}
	cout << endl;
}

// calculate sum of elements of a vector
float sum_elements(vector<float> &V){
	float sum = 0.0;
	for(int i=0;i<V.size();i++){
		sum += V[i];
	}
	return sum;
}

// returns true if both input vectors are equal
bool cmp(vector<float> &V1, vector<float> &V2){
	for(int i=0;i<V1.size();i++){
		if(V1[i] != V2[i])
			return 0;
	}
	return 1;
}

// count the number of outlinks from each node
void count_oh(vector<vector<bool> > &G, vector<int> &oh){
	for(int i=0;i<G.size();i++){
		int n_out = 0;
		for(int j=0;j<G[0].size();j++){
			if(G[i][j]==1)
				n_out++;
		}
		oh.push_back(n_out);
	}
}

// count the number of inlinks to each node
void count_ih(vector<vector<bool> > &G, vector<int> &ih){
	for(int i=0;i<G.size();i++){
		int n_in = 0;
		for(int j=0;j<G[0].size();j++){
			if(G[j][i]==1)
				n_in++;
		}
		ih.push_back(n_in);
	}
}

vector<float> pagerank(vector<vector<bool> > &G, int it, float d){
	// number of nodes
	int n = G.size();

	// outlink hash
	vector<int> oh;
	count_oh(G, oh);

	// inlink hash
	vector<int> ih;
	count_ih(G, ih);

	// pagerank vector initialized to 1/N
	vector<float> opg(n, 1.0/n);

	// new pagerank vector
	vector<float> npg(n);

	if(it == 0){
		int t=0;
		while(true){
			// print_vector(opg);
			float dp = 0.0;
			
			// pagerank from nodes with no outlinks
			for(int p=0;p<n;p++){
				if(oh[p]==0)
					dp += d*opg[p]/n;
			}

			// build new pagerank vector
			for(int p=0;p<n;p++){
				// pagerank from random jump
				npg[p] = dp + (1.0-d)/n;

				// pagerank from inlinks
				for(int ip=0;ip<n;ip++){
					if(G[ip][p]){
						npg[p] += d*opg[ip]/oh[ip];
					}
				}
			}
			if(cmp(opg,npg))
				break;
			opg = npg;
			t++;
		}
		cout << "number of iterations = " << t << endl;
	}else{
		while(it--){
			// print_vector(opg);
			float dp = 0.0;
			
			// pagerank from nodes with no outlinks
			for(int p=0;p<n;p++){
				if(oh[p]==0)
					dp += d*opg[p]/n;
			}

			// build new pagerank vector
			for(int p=0;p<n;p++){
				// pagerank from random jump
				npg[p] = dp + (1.0-d)/n;

				// pagerank from inlinks
				for(int ip=0;ip<n;ip++){
					if(G[ip][p]){
						npg[p] += d*opg[ip]/oh[ip];
					}
				}
			}
			opg = npg;
		}
	}

	return opg;
}

int main(){
	cout << setprecision(10);
	// input number of nodes
	int node_num;
	cin >> node_num;

	// vector for weight of each vector
	vector<float> weights(node_num, (1.0/node_num));

	// graph as adjacency matrix
	vector<vector<bool> >graph(node_num,vector<bool>(node_num,false));

	// takes number of edges as input
	int edge_num;
	cin >> edge_num;

	// number of iterations
	int it;
	cin >> it;

	// damping factor
	float df;
	cin >> df;

	// takes node pairs as input and contructs graph by filling adjacency matrix
	for(int i=0;i<edge_num;i++){
		int n1,n2;
		cin >> n1 >> n2;
		graph[n1][n2] = true;
	}
	// calculating pagerank vector
	vector<float> pg = pagerank(graph, it, df);

	// cout << "ranks" << endl;
	// print pagerank vector
	// print_vector(pg);

	// print sum of all pageranks
	// cout << "sum of all pageranks = " << sum_elements(pg) << endl;

	for(int i=0;i<pg.size();i++){
		cout << "pagerank[" << i << "]\t" << pg[i] << endl;
	}

	return 0;
}