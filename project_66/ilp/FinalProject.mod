/*********************************************
 * OPL 12.6.0.0 Model
 * Author: feng
 * Creation Date: Nov 29, 2017 at 1:39:45 PM
 *********************************************/
// Known Parameters
int hours = ...;
int nNurses = ...;
int minHours = ...;
int maxHours = ...;
int maxConsec = ...;
int maxPresence = ...;

range H = 1..hours;
range N = 1..nNurses;

int demand[h in H] = ...;

//Decision Variables
dvar boolean working[n in N]; //whether nurse n is used;
dvar boolean w[n in N][h in H]; //whether nurse n works or not at hour h;
dvar boolean worksBefore[n in N][h in H]; //whether nurse n starts work before hour h;
dvar boolean worksAfter[n in N][h in H]; //whether nurse n finishes work after hour h;
dvar boolean rest[n in N][h in H]; //whether nurse n rests at hour h;

//Objective function
minimize sum(n in N) working[n];

subject to {
   
    //1. if nurse n works, she/he should work at least minHours;
    forall (n in N)
      sum(h in H) w[n][h]>=working[n]*minHours;
   
    //2. if nurse n works, she/he should work at most maxHours;
    forall (n in N)
      sum(h in H) w[n][h]<=working[n]*maxHours;   
    
    //3. for each hour, at least demand nurses work
    forall (h in H)
      sum(n in N) w[n][h]>=demand[h];
      
    //4. Each nurse should work at most maxConsec consecutive hours;
    forall(n in N)
      forall(h in 1..hours-maxConsec)
        sum(hh in h..h+maxConsec) w[n][hh]<=maxConsec;
      
    //5. no nurse can stay at the hospital for more than maxPresence hours;
    forall (n in N)
      forall (h in 1..hours-maxPresence)
        sum(hh in h+maxPresence..hours) w[n][hh]<=hours*(1-w[n][h]);
    
    //6. whether nurse n works before hour n: if nurse n does not work before hour n, then 0  
    forall (n in N)
      forall (h in H)
        worksBefore[n][h]<=sum(hh in 1..h-1) w[n][hh];
      
    //7. whether nurse n works before hour n: if nurse n does work before hour n, then 1  
     
    forall (n in N)
      forall (h in H)
        worksBefore[n][h]*hours>=sum(hh in 1..h-1) w[n][hh];

    //8. whether nurse n works after hour n: if nurse n does not work after hour n, then 0  
    forall (n in N)
      forall (h in 1..hours-1)
        worksAfter[n][h]<=sum(hh in h+1..hours) w[n][hh];
      
    //9. whether nurse n works before hour n: if nurse n does work after hour n, then 1  
     
    forall (n in N)
      forall (h in 1..hours-1)
        worksAfter[n][h]*hours>=sum(hh in h+1..hours) w[n][hh];
        
    //10. during presence, if nurse n works at hour n, rest=0; or rest=1;
    forall (n in N)
      forall (h in H)
        w[n][h]+rest[n][h]+(1-worksBefore[n][h])+(1-worksAfter[n][h])>=1;
        
     //11. nurse n can not rest for more than 1 consecutive hour
     forall (n in N)
       forall (h in 1..hours-1)
         rest[n][h]+rest[n][h+1]<=1;
}


 execute {
   // Example of postprocessing (should be rewritten to output solution)
  	for (var n in N)
  		for (var h in H)
  			if (working[n] == 1) writeln("nurse " + n + " works"); 
 }  