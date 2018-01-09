 // INPUT DATA
 int numNurses = ...;
 int hours = ...;
 range N = 1..numNurses;
 range H = 1..hours;
 int demand [h in H]= ...;
 int minHours = ...;
 int maxHours = ...;
 int maxConsec = ...;
 int maxPresence = ...;

 // DECISION VARIABLES
 // whether nurse n works at hour h
 dvar boolean works[n in N, h in H];
 // whether nurse n works
 dvar boolean working[n in N]; 

 
 // objective function
 minimize sum(n in N) working[n];
 
 // constraints
 subject to {
 
 	// 1 min demmand_h nurses in hour h
 	forall(h in H)
 	  	sum (n in N) works[n,h] >= demand[h];
   	  
   	// 2 each nurse should work at least min hours
   	forall (n in N)
   	  	sum (h in H) works[n,h] >= minHours * working[n];
   	  	
   	// 3 each nurse should work at most max hours
   	forall (n in N)
   	  	sum (h in H) works[n,h] <= maxHours * working[n];  
   	  
   	// 4 each nurse should work at most max consec hours  
   	forall (n in N, h in 1..(hours-maxConsec))
   	  	sum (i in h..(h+maxConsec)) works[n,i] <= maxConsec;  
   	
   	// 5 each nurse should not stay in hospital more than max presence hours
   	forall(n in N, h in 1..hours-maxPresence)
 	  sum(i in h+maxPresence..hours) works[n, i] <= hours * (1 - works[n, h]);
 	  	
	// 6 each nurse should not rest consecutively
	forall (n in N, h in 1..(hours-3))
	  	 (1 - works[n,h] + works[n,h+1] + works[n,h+2]) * hours >= sum(i in h+3..hours)works[n,i];
   	
 }
 /*
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
*/
