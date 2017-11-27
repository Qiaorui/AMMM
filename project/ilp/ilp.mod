/*********************************************
 * OPL 12.6.0.0 Model
 * Author: oliveras
 * Creation Date: Jun 8, 2017 at 11:46:35 AM
 *********************************************/

 // A
 int numNurses = ...;
 int hours = ...;
 range N = 1..numNurses;
 range H = 1..hours;
 
 int demand [h in H]= ...;
 int minHours = ...;
 int maxHours = ...;
 int maxConsec = ...;
 
 // B
 int maxPresence = ...;
 
 // A
 dvar boolean works[n in N][h in H]; // this set of variable should suffice for A). Tells whether nurse n works at hour h
 
 minimize 1; // do not change this for A)
 subject to {
 
 	// This constraint does not make any sense
 	forall(n in N)
 	  	sum (h in H : h%2 == 0) works[n][h] <= 12;
   	  	   	
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
 
