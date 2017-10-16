/*********************************************
 * OPL 12.6.0.0 Model
 * Author: x
 * Creation Date: Oct 9, 2017 at 9:56:18 AM
 *********************************************/
int nTasks=...;
int nCPUs=...;
range T=1..nTasks;
range C=1..nCPUs;
float rt[t in T]=...;
float rc[c in C]=...;
//int k = ...;
dvar boolean x_tc[t in T, c in C];
dvar float+ z;


execute {
var totalLoad=0;
for (var t=1;t<=nTasks;t++)
totalLoad += rt[t];
writeln("Total load "+ totalLoad);
};

// Objective
minimize z;
subject to{
// Constraint 1
forall(t in T)
sum(c in C) x_tc[t,c] == 1;
// Constraint 2
forall(c in C)
sum(t in T) rt[t]* x_tc[t,c] <= rc[c];
// Constraint 3
forall(c in C)
z >= (1/rc[c])*sum(t in T) rt[t]* x_tc[t,c];
// Constraint 4
//nTasks - sum(t in T, c in C) x_tc[t][c] <= k;
}


execute {
	var taskComplete = true;
	var cpuComplete = true;
	for (var t=1;t<=nTasks;t++) {
		var serve = 0;
		for (var c=1;c<=nCPUs;c++) {
			serve += x_tc[t][c];
		}
		if (serve != 1) {
			taskComplete = false;
			break;		
		}
		writeln("Task " + t + " checked " + serve);
	}
	for (var c=1;c<=nCPUs;c++) {
		var load=0;
		for (var t=1;t<=nTasks;t++)
			load+=(rt[t]* x_tc[t][c]);
		
		if (load <= rc[c]) {
			writeln("CPU " + c + ": correct process");
		} else {
			writeln("CPU " + c + ": error");
			cpuComplete = false;
			break;	
		}
	}
	if (cpuComplete) {
		writeln("All computer cpus running correct");
	} else {
		writeln("Some computer cpus have overloaded");	
	}
	if (taskComplete) {
		writeln("All tasks are served");	
	} else {
		writeln("Some tasks are not served correctlly");	
	}
};


execute {
for (var c=1;c<=nCPUs;c++) {
var load=0;
for (var t=1;t<=nTasks;t++)
load+=(rt[t]* x_tc[t][c]);
load = (1/rc[c])*load;
writeln("CPU " + c + " loaded at " + load + "%");
}
};

 