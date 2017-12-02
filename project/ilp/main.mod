/*********************************************
 * OPL 12.6.0.0 Model
 * Author: qiaorui
 * Creation Date: Dec 2, 2017 at 10:37:45 AM
 *********************************************/

string dataPath = ...;
int runType = ...;
 
main {
	var src = new IloOplModelSource("ilp.mod");
	var def = new IloOplModelDefinition(src);
	var cplex = new IloCplex();
	var model = new IloOplModel(def,cplex);
	
	
	var oplDataPath = thisOplModel.dataElements.dataPath;
	
	// Check the validity of the data directory
	var dataDir = new IloOplFile(oplDataPath);
	if( !dataDir.exists ) {
		writeln( "ERROR : Cannot find specified file: ", oplDataPath);
		status = false;
	} else if (dataDir.isDirectory != true) {
		writeln( "ERROR : Not a directory: ", oplDataPath);
		status = false;
	}
	var f = dataDir.getFirstFileName();
	while( f != null ) {  	
		var entryName = dataDir.name + dataDir.separator + f; 
		writeln(entryName)
		f = dataDir.getNextFileName();			
	}
	
	/*var data = new IloOplDataSource("sample.dat");
	model.addDataSource(data);
	model.generate();
	if (cplex.solve()) {
		writeln("value " + cplex.getBestObjValue())
	}
	model.end();
 	data.end();
 	def.end();
 	cplex.end();
 	src.end();
 	*/

}