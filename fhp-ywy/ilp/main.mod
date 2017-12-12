/*********************************************
 * OPL 12.6.0.0 Model
 * Author: ywy44
 * Creation Date: 9 Dec 2017 at 11:24:44
 *********************************************/

main { 
	var instancesDirPath = "./instances";
	// Initialization 
	var src = new IloOplModelSource("ProjectModel.mod");
	var def = new IloOplModelDefinition(src);
	var cplex = new IloCplex();
	// Set time limit
	cplex.TiLim=600.0;
	
	var directory = new IloOplFile(instancesDirPath); 
	// Check if it exists
	if (!directory.exists) {
    	writeln( "ERROR: Cannot find specified file (" + instancesDirPath + ")");
	}
	// Check if it is a directory
	else if (directory.isDirectory != true) {
		writeln( "ERROR: It's not a directory (" + instancesDirPath + ")");	
	}
	// Solve all instances in the instance directory
	else {
    	var resultFile = new IloOplOutputFile("result.txt");
    	var dataFileName = directory.getFirstFileName();
	    while (dataFileName != null) {
	        var model = new IloOplModel(def,cplex);
			var data = new IloOplDataSource(instancesDirPath + directory.separator + dataFileName);
			model.addDataSource(data);
			model.generate();
	        if (cplex.solve()) {
				var result = dataFileName + ", " + cplex.getObjValue() + ", " + cplex.getSolvedTime();
			}
			else {
				var result = dataFileName + ": Cannot be solved."
			}
			resultFile.writeln(result);
			writeln(result);
			model.end();
			data.end();
	       	// Get next instance file's name
      		dataFileName = directory.getNextFileName();
    	}
  	}
	
	resultFile.close();		 
	def.end();
	cplex.end();
	src.end();
};