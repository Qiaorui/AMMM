
/*
	Global config information
*/
string testPath = ...;
string benchmarkPath = ...;


/*
	We test 6 general constraints from project.
	We are not considering worksBefore neither worksAfter as our test subjects
	due to they are just decision variable.
*/

main {
	
	// Sum function for IloMap Object
	function sum (list) {
		var acc = 0;
		for (var i in list) {
			acc += list[i];		
		}
		return acc;
	}
	
	
	var src = new IloOplModelSource("ilp.mod");
	var def = new IloOplModelDefinition(src);
	var cplex = new IloCplex();
	
	
	var oplDataPath = thisOplModel.dataElements.testPath;
	
	// Check the validity of the data directory
	var dataDir = new IloOplFile(oplDataPath);
	if( !dataDir.exists ) {
		writeln( "ERROR : Cannot find specified file: ", oplDataPath);
	} else if (dataDir.isDirectory != true) {
		writeln( "ERROR : Not a directory: ", oplDataPath);
	}
	
	/*	Unit Test 1
		For each Hour h, at least demand[h] nurses are working in h.
		
		Description: Fullfill demand constraint and keep nurse as less as possible
		all demand[h] are 1, only 1 nurse should be working
	*/
	write("Test - 1:  ");
	var model = new IloOplModel(def,cplex);
	var filePath = dataDir.name + dataDir.separator + "test_c1.dat";
	var data = new IloOplDataSource(filePath);
	model.addDataSource(data);
	model.generate();
	if (cplex.solve()) {
		var passed = true;
		// works exctaly same number of nurse as demanded
		for (var h = 1; h <= model.hours && passed; h++) {
			var acc = 0;
			for (var n = 1; n <= model.numNurses; n++) {
				acc += model.works[n][h];
			}
			passed = (acc == model.demand[h]);
		}
		// Only one nurse is working
		passed &= (sum(model.working) == 1);
		
		if (passed) {
			write("PASS\n");
		} else {
			write("ERROR!\n");		
		}
	} else {
		write("ERROR! \n");
	}
	model.end();
 	data.end();
 	
	/*	Unit Test 2
		Each nurse should work at least minHours hours
	
		Description: Even we have only 1 demand, but the working nurse should 
		work at least minHours hours which is 3.
	*/
	write("Test - 2:  ");
	model = new IloOplModel(def,cplex);
	filePath = dataDir.name + dataDir.separator + "test_c2.dat";
	data = new IloOplDataSource(filePath);
	model.addDataSource(data);
	model.generate();
	if (cplex.solve()) {
		var passed = true;
		// Check working hours >= minHours
		for (var n in model.works) {
			passed &= sum(model.works[n]) >= model.minHours * model.working[n];		
		}
		// Only one nurse is working
		passed &= (sum(model.working) == 1);
		if (passed) {
			write("PASS\n");
		} else {
			write("ERROR!\n");		
		}
	} else {
		write("ERROR! \n");
	}
	model.end();
 	data.end();
 	
 	
	/*	Unit Test 3
		Each nurse should work at most maxHours hours
	
		Description: We have maxHours 2 with demand [1 1 1]. 
					2 nurses is required.
	*/
	write("Test - 3:  ");
	model = new IloOplModel(def,cplex);
	filePath = dataDir.name + dataDir.separator + "test_c3.dat";
	data = new IloOplDataSource(filePath);
	model.addDataSource(data);
	model.generate();
	if (cplex.solve()) {
		var passed = true;
		// Check working hours <= maxHours
		for (var n in model.works) {
			passed &= sum(model.works[n]) <= model.maxHours;		
		}
		// 2 nurse is working
		passed &= (sum(model.working) == 2);
		if (passed) {
			write("PASS\n");
		} else {
			write("ERROR!\n");		
		}
	} else {
		write("ERROR! \n");
	}
	model.end();
 	data.end();
 	
 	
 	/*	Unit Test 4
 		Each nurse should work at most maxConsec consecutive hours
	
		Description: We have maxHours 4 with demand [1 1 1 1]. 
					 But due to maxConsec is 3, 2 nurses is required.
	*/
	write("Test - 4:  ");
	model = new IloOplModel(def,cplex);
	filePath = dataDir.name + dataDir.separator + "test_c4.dat";
	data = new IloOplDataSource(filePath);
	model.addDataSource(data);
	model.generate();
	if (cplex.solve()) {
		var passed = true;
		// Check working hours <= maxHours
		for (var n in model.works) {
			passed &= sum(model.works[n]) <= model.maxConsec;		
		}
		// 2 nurse is working
		passed &= (sum(model.working) == 2);
		if (passed) {
			write("PASS\n");
		} else {
			write("ERROR!\n");		
		}
	} else {
		write("ERROR! \n");
	}
	model.end();
 	data.end();


 	/*	Unit Test 5
 		No nurse can stay at the hospital for more than maxPresence hours
	
		Description: We have maxHours 5 with demand [1 0 1 0 1]. 
					 But due to maxPresence is 4, 2 nurses is required.
	*/
	write("Test - 5:  ");
	model = new IloOplModel(def,cplex);
	filePath = dataDir.name + dataDir.separator + "test_c5.dat";
	data = new IloOplDataSource(filePath);
	model.addDataSource(data);
	model.generate();
	if (cplex.solve()) {
		var passed = true;
		// 2 nurse is working
		passed &= (sum(model.working) == 2);
		if (passed) {
			write("PASS\n");
		} else {
			write("ERROR!\n");		
		}
	} else {
		write("ERROR! \n");
	}
	model.end();
 	data.end();


 	/*	Unit Test 6
 		No nurse can rest for more than one consecutive hour
	
		Description: We have maxHours 2 with demand [1 0 0 1]. 
					 But due no nurse can rest more than 1 hour, 2 nurses is required.
	*/
	write("Test - 6:  ");
	model = new IloOplModel(def,cplex);
	filePath = dataDir.name + dataDir.separator + "test_c6.dat";
	data = new IloOplDataSource(filePath);
	model.addDataSource(data);
	model.generate();
	if (cplex.solve()) {
		var passed = true;
		// With this data, we expected 2 nurses which works 1 hour.
		for (var n in model.works) {
			passed &= sum(model.works[n]) <= 1;		
		}
		// 2 nurse is working
		passed &= (sum(model.working) == 2);
		if (passed) {
			write("PASS\n");
		} else {
			write("ERROR!\n");		
		}
	} else {
		write("ERROR! \n");
	}
	model.end();
 	data.end();
 	
 	
 	// Finished
 	def.end();
 	cplex.end();
 	src.end();
 	
}