#include <iostream>
#include <vector>
#include <limits.h>
using namespace std;


void print_mat(vector< vector<float> > &P){
	for(int i=0;i<P.size();i++){
		for(int j=0;j<P.size();j++){
			cout << P[i][j] << " ";
		}
		cout << endl;
	}
}


void print_vector(vector<float> &P){
	for(int j=0;j<P.size();j++){
		cout << P[j] << " ";
	}
	cout << endl;
}

bool mat_multiply(vector<vector<float> > &t_mat, vector<float> &wts){
	// vector for new weight vector
	vector<float> temp(wts.size());

	// matrix multiplication
	for(int i =0;i<temp.size();i++){
		float val =0;
		for(int j=0;j<temp.size();j++){
			val += t_mat[i][j]*wts[j];
		}
		temp[i] = val;
	}
	
	// compares 'temp' vector to 'wts' vector to check if both are same
	for(int i=0;i<temp.size();i++){
		if(temp[i] != wts[i]){
			wts  = temp;
			return false;
		}
	}
	return true;
}

void add_matrix(vector< vector<float> > &P, vector< vector<float> > &R){
	for(int i=0;i<P.size();i++){
		for(int j=0;j<P.size();j++){
			P[i][j] += R[i][j];
		}
	}
}

int main(){
	// input number of nodes
	int node_num;
	cin >> node_num;

	// vector for weight of each vector
	vector<float> weights(node_num, float(1.0/node_num));

	// graph as adjacency matrix
	vector<vector<bool> >graph(node_num,vector<bool>(node_num,false));

	// takes number of edges as input
	int edge_num;
	cin >> edge_num;

	// takes node pairs as input and contructs graph by filling adjacency matrix
	for(int i=0;i<edge_num;i++){
		int n1,n2;
		cin >> n1 >> n2;
		graph[n1][n2] = true;
	}

	// damping factor
	float damp;
	cin >> damp;

	// R matrix
	vector< vector<float> > R(node_num, vector<float>(node_num, (float)damp/node_num) );


	// builds transition matrix from adjacency matrix
	vector<vector<float> >t_mat(node_num,vector<float>(node_num,0));
	for(int i =0;i<node_num;i++){
		int outgoing = 0;
		for(int j=0;j<node_num;j++){
			if(graph[i][j]){
				outgoing++;
				}
		}
		for(int j =0;j<node_num;j++){
			
			if(graph[i][j]){
				t_mat[j][i] = 1.0*(1-damp)/outgoing;
			}
		}
	}

	print_mat(t_mat);
	cout << "\n";
	add_matrix(t_mat, R);
	print_mat(t_mat);
	cout << endl;
	// pagerank iterations
	int it=0;
	while(!mat_multiply(t_mat,weights)){
		print_vector(weights);
		cout << endl;
		it++;
	}
	cout << it << endl;

	// print the final weight matrix representing pageranks
	cout<<"ranks"<<endl;
	for(int i =0;i<node_num;i++){
		cout << i << " rank = " << weights[i] << endl;
		
	}
}
