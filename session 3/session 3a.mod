/*********************************************
 * OPL 12.5.1.0 Model
 * Author: qiaorui.xiang
 * Creation Date: 16/10/2017 at 10:37:36
 *********************************************/
int nTasks=...;
int nThreads=...;
int nCPUs=...;
int nCores=...;
range T=1..nTasks;
range C=1..nCPUs;
range K=1..nCores;
range H=1..nThreads;
float rh[h in H]=...;
float rc[c in C]=...;
int CK[c in C, k in K]=...;
int TH[t in T, h in H]=...;
dvar boolean x_tc[t in T, c in C];
dvar boolean x_hk[h in H, k in K];
//dvar float+ z;
dvar boolean x_c[c in C];

// Objective
minimize sum(c in C)x_c[c];
subject to{
// Constraint 1
forall(h in H)
	sum(k in K) x_hk[h,k] == 1;
// Constraint 2
forall(t in T, c in C)
	sum(h in H: TH[t,h] == 1, k in K: CK[c,k] ==1) x_hk[h,k] == sum(h in H)TH[t,h]*x_tc[t,c];
// Constraint 3
forall(c in C, k in K:CK[c,k] == 1)
  	sum(h in H)rh[h] * x_hk[h,k] <= rc[c];
// Constraint 4
//forall(c in C)
//	z >= (1/(sum(k in K)CK[c,k]*rc[c])) * sum(h in H, k in K:CK[c,k]==1)x_hk[h,k]*rh[h];
	
forall(c in C)
  x_c[c] * nTasks >= sum(t in T)x_tc[t,c];
}
