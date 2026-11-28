#include <bits/stdc++.h>
using namespace std;
typedef unsigned int u32;
const u32 HI=2095104u, LO=2047u;
u32 base[16]={63491,1386508,235568,0,151748,287504,0,0,558408,1246721,1835170,0,1246721,1835170,0,0};
long long cnt=0,found=0;
// exact cover with <=6 sets
bool cover(vector<u32>&F){
  sort(F.begin(),F.end()); F.erase(unique(F.begin(),F.end()),F.end());
  // remove dominated
  vector<u32> G; for(u32 a:F){bool dom=false; for(u32 b:F) if(b!=a && (a&b)==a){dom=true;break;} if(!dom) G.push_back(a);}
  vector<char> cur(2048,0); cur[0]=1;
  for(int step=0;step<6;step++){
    vector<char> nx=cur;
    for(int s=0;s<2048;s++) if(cur[s]) for(u32 m:G) nx[s|m]=1;
    cur=nx; if(cur[LO]) return true;
  }
  return cur[LO];
}
u32 w[32]; int len;
void check(int pat[3], int idx[3][2]){
  cnt++;
  vector<u32> F; u32 un=0;
  for(int i=0;i<len;i++) for(int j=i;j<len;j++){u32 p=w[i]&w[j]; if((p&HI)==0){F.push_back(p); un|=p;}}
  if((un&LO)!=LO) return;
  if(cover(F)){found++; printf("FOUND pat=%d%d%d g0=(%d,%d) g1=(%d,%d) g2=(%d,%d)\n",pat[0],pat[1],pat[2],idx[0][0],idx[0][1],idx[1][0],idx[1][1],idx[2][0],idx[2][1]); fflush(stdout);}
}
int main(){
  int pats[4][3]={{0,0,0},{1,0,0},{0,1,0},{0,0,1}};
  for(auto&pat:pats){
    int idx[3][2];
    function<void(int)> rec=[&](int g){
      if(g==3){check(pat,idx);return;}
      int L=16+g;
      for(int i=0;i<L;i++) for(int j=i;j<L;j++){
        idx[g][0]=i;idx[g][1]=j;
        w[16+g]= pat[g]? (w[i]&w[j]) : (w[i]|w[j]);
        len=16+g+1; rec(g+1);
      }
    };
    for(int i=0;i<16;i++) w[i]=base[i];
    rec(0);
  }
  printf("configs %lld found %lld\n",cnt,found);
}
