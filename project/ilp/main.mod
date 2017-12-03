/*********************************************
 * OPL 12.6.0.0 Model
 * Author: qiaorui
 * Creation Date: Dec 2, 2017 at 10:37:45 AM
 *********************************************/

string testPath = ...;
string benchmarkPath = ...;
 
main {
	var src = new IloOplModelSource("ilp.mod");
	var def = new IloOplModelDefinition(src);
	var cplex = new IloCplex();
	
	var oplDataPath = thisOplModel.dataElements.benchmarkPath;
	
	// Check the validity of the data directory
	var dataDir = new IloOplFile(oplDataPath);
	if( !dataDir.exists ) {
		writeln( "ERROR : Cannot find specified file: ", oplDataPath);
		status = false;
	} else if (dataDir.isDirectory != true) {
		writeln( "ERROR : Not a directory: ", oplDataPath);
		status = false;
	}
	
	var output = new IloOplOutputFile("result.txt");
	var f = dataDir.getFirstFileName();
	while( f != null ) {
		var msg = f;
		var model = new IloOplModel(def,cplex);
		var filePath = dataDir.name + dataDir.separator + f; 
		var data = new IloOplDataSource(filePath);
		model.addDataSource(data);
		model.generate();
		if (cplex.solve()) {
			msg += ", " + cplex.getBestObjValue() + ", " + cplex.getCplexTime() + ", " + cplex.getSolvedTime();
		} else {
			msg += ": ERROR";		
		}
		model.end();
 		data.end();
 		writeln(msg);
		output.writeln(msg);
		f = dataDir.getNextFileName();			
	}
	output.close();
	
 	def.end();
 	cplex.end();
 	src.end();
}