#include <iostream>
#include <vector>
#include <limits.h>
using namespace std;

int l =0;

bool mat_multiply(vector<vector<float> > &t_mat, vector<float> &wts){
	cout<<l<<endl;
	l++;
	vector<float> temp(wts.size());
	
	for(int i =0;i<temp.size();i++){
		float val =0;
		for(int j=0;j<temp.size();j++){
			val += t_mat[i][j]*wts[j];
		}
		temp[i] = val;
	}
	
	for(int i=0;i<temp.size();i++){
		if(temp[i] != wts[i]){
			wts  = temp;
			return false;
		}
	}
	return true;
}

int main(){
	int node_num;
	cin >> node_num;
	vector<float> weights(node_num, float(1.0/node_num));
	vector<vector<bool> >graph(node_num,vector<bool>(node_num,false));
	int edge_num;
	cin >> edge_num;
	///graph construction
	for(int i = 0;i<edge_num;i++){
		int n1,n2;
		cin>>n1>>n2;
		graph[n1][n2] = true;
	}
	float damp;
	cin>>damp;
	cout<<(damp/node_num)<<endl;
	vector<vector<float> > R(node_num,vector<float>(node_num,(damp/node_num)) );
	/// transition matrix t_mat
	vector<vector<float> >t_mat(node_num,vector<float>(node_num,(damp/node_num)));
	cout<<t_mat[0][0]<<endl;
	for(int i =0;i<node_num;i++){
		int outgoing = 0;
		for(int j=0;j<node_num;j++){
			if(graph[i][j]){
				outgoing++;
				}
		}
		for(int j =0;j<node_num;j++){
			
			if(graph[i][j]){
				t_mat[j][i] += (1.0-damp)*(1.0/outgoing);
				///t_mat[j][i] = (1.0-damp)*t_mat[j][i];
				///cout<<t_mat[j][i]<<" hola"<<endl;
			}
		}
	}
	
	/// pagerank iterations
	
	while(!mat_multiply(t_mat,weights));
	cout<<"ranks"<<endl;
	for(int i =0;i<node_num;i++){
		cout<<i<<" rank = "<<weights[i]<<endl;
		
	}
	
}
