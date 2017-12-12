/*********************************************
 * OPL 12.6.0.0 Model
 * Author: Wangyang Ye, Hongping Feng
 * Creation Date: 2017-11-26 at 18:11:17
 *********************************************/

// Available variables
 int numNurses = ...; // number of nurses
 int hours = ...;   
 range N = 1..numNurses;
 range H = 1..hours;
 
 int demand [h in H]= ...; 
 int minHours = ...;
 int maxHours = ...;
 int maxConsec = ...;
 int maxPresence = ...;
 
 // Decision variables
 dvar boolean works[n in N, h in H]; // Tells whether nurse n works at hour h
 dvar boolean worksSomeHour[n in N]; // Tells whether nurse n works some hour  
 dvar boolean worksBefore[n in N, h in H]; // Tells whether nurse n works before hour h;
 dvar boolean worksAfter[n in N, h in H]; // Tells whether nurse n works after hour h;
 dvar boolean rests[n in N, h in H]; // Tells whether nurse n rests at hour h;
 
 // Objective function
 minimize sum(n in N) worksSomeHour[n]; // Minimize the number of nurses that work some hour  
 
 // Constraints
 subject to {
 	// Constraint 1: at least demandh nurses should be working at the hospital
 	forall(h in H)
 	  sum(n in N) works[n, h] >= demand[h];
 	  
 	// Constraint 2: each nurse should work at least minHours hours.
 	forall(n in N)
 	  sum(h in H) works[n, h] >= minHours * worksSomeHour[n];
 	  
 	// Constraint 3: each nurse should work at most maxHours hours
 	forall(n in N)
 	  sum(h in H) works[n, h] <= maxHours * worksSomeHour[n];
 	  
 	// Constraint 4: each nurse should work at most maxConsec consecutive hours.
 	forall(n in N, h in 1..hours-maxConsec)
 	  sum(i in h..h+maxConsec) works[n, i] <= maxConsec;
 	  
 	// Constraint 5: no nurse can stay at the hospital for more than maxPresence hours
 	forall(n in N, h in 1..hours-maxPresence)
 	  sum(i in h+maxPresence..hours) works[n, i] <= hours * (1 - works[n, h]);
 	
 	// Constraint 6: if nurse n works before hour h
 	forall(n in N, h in H)
 	  worksBefore[n, h] <= sum(i in 1..h-1) works[n,i];
 	     
 	// Constraint 7: 
 	forall(n in N, h in H)
 	  worksBefore[n, h] * hours >= sum(i in 1..h-1) works[n,i];
 	
 	// Constraint 8: if nurse n works after hour h
 	forall(n in N, h in H)
 	  worksAfter[n, h] <= sum(i in h+1..hours) works[n,i];
 	  
 	// Constraint 9: 
 	forall(n in N, h in H)
 	  worksAfter[n, h] * hours >= sum(i in h+1..hours) works[n,i];
 	  
 	// Constraint 10: if nurse n does not works at hour h AND 
 	//                works before h AND works after h -> nurse n rests at hour h 
 	forall(n in N, h in H)
 	  works[n, h] + (1 - worksBefore[n, h]) + (1 - worksAfter[n, h]) + rests[n, h] >= 1;
 	
 	// Constraint 11: no nurse can rest for more than one consecutive hour
 	forall(n in N) 
 	  forall(h in 1..hours-1) 
 	    rests[n, h] + rests[n, h+1] <= 1;
 }
 
 execute { // Should not be changed. Assumes that variables works[n][h] are used.
  	for (var n in N) {
		write("Nurse ");
		if (n < 10) write(" ");
		write(n + " works:  ");
		var minHour = -1;
		var maxHour = -1;
		var totalHours = 0;
		for (var h in H) {
		  	if (works[n][h] == 1) {
		  		totalHours++;
		  		write("  W");	
		  		if (minHour == -1) minHour = h;
		  		maxHour = h;			  	
		  	}
		  	else write("  .");
   		}
   		if (minHour != -1) write("  Presence: " + (maxHour - minHour +1));
   		else write("  Presence: 0")
   		writeln ("\t(TOTAL " + totalHours + "h)");		  		  
	}		
	writeln("");
	write("Demand:          ");
	
	for (h in H) {
	if (demand[h] < 10) write(" ");
	write(" " + demand[h]);	
	}
	writeln("");
	write("Assigned:        ");
	for (h in H) {
		var total = 0;
		for (n in N)
			if (works[n][h] == 1) total = total+1;
		if (total < 10) write(" ");
		write(" " + total);		
	}		
}  
 
 