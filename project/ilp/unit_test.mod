
string testPath = ...;
string benchmarkPath = ...;

main {
	var src = new IloOplModelSource("ilp.mod");
	var def = new IloOplModelDefinition(src);
	var cplex = new IloCplex();
	var model = new IloOplModel(def,cplex);
	
	
	var oplDataPath = thisOplModel.dataElements.testPath;
	
	// Check the validity of the data directory
	var dataDir = new IloOplFile(oplDataPath);
	if( !dataDir.exists ) {
		writeln( "ERROR : Cannot find specified file: ", oplDataPath);
	} else if (dataDir.isDirectory != true) {
		writeln( "ERROR : Not a directory: ", oplDataPath);
	}

	// Unit Test 1: test constraint 1
	write("Test - Constraint 1:  ");
	var filePath = dataDir.name + dataDir.separator + "test_c1.dat";
	var data = new IloOplDataSource("sample.dat");
	model.addDataSource(data);
	model.generate();
	if (cplex.solve()) {
		var passed = true;
		for (var h = 1; h <= model.hours && passed; h++) {
			var sum = 0;
			for (var n = 1; n <= model.numNurses; n++) {
				sum += works[n];
			}
			passed = (sum == demand[h]);
		}
		if (passed) {
			write("PASS\n");
		}
	} else {
		write("ERROR! \n");
	}
	
	model.end();
 	data.end();
 	def.end();
 	cplex.end();
 	src.end();
 	
}