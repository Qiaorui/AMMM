/*********************************************
 * OPL 12.6.0.0 Model
 * Author: qiaorui
 * Creation Date: Dec 2, 2017 at 10:37:45 AM
 *********************************************/

string testPath = ...;
string benchmarkPath = ...;
 
main {
	
		// Sum function for IloMap Object
	function sum (list) {
		var acc = 0;
		for (var i in list) {
			acc += list[i];		
		}
		return acc;
	}
	
	function mSortFunction(x, y) {
		var str1 = x.split(".")[0].split("_");
		var str2 = y.split(".")[0].split("_");
		var i1 = parseInt(str1[1]);
		var i2 = parseInt(str1[2]);
		var j1 = parseInt(str2[1]);
		var j2 = parseInt(str2[2]);
		
		if (i1 < j1) {
			return -1;		
		} else if (i1 > j1) {
			return 1;		
		} else if (i2 < j2) {
			return -1;		
		} else if (i2 > j2) {
			return 1;		
		} else {
			return 0;		
		}
	}

	// Initialization	
	var src = new IloOplModelSource("ilp.mod");
	var def = new IloOplModelDefinition(src);
	
	var oplDataPath = thisOplModel.dataElements.benchmarkPath;
	thisOplModel.settings.mainEndEnabled = true;

	
	// Check the validity of the data directory
	var dataDir = new IloOplFile(oplDataPath);
	if( !dataDir.exists ) {
		writeln( "ERROR : Cannot find specified file: ", oplDataPath);
	} else if (dataDir.isDirectory != true) {
		writeln( "ERROR : Not a directory: ", oplDataPath);
	}
	

	// Get sorted file name
	var f = dataDir.getFirstFileName();
	var fList = new Array();
	var index = 0;
	while(f != null) {
		fList[index] = f;
		f = dataDir.getNextFileName();
		++index;
	}
	fList.sort(mSortFunction);
	
	// Write CPLEX result to file
	var output = new IloOplOutputFile("result.txt");
	for (var k = 0; k < fList.length; k++) {
		var msg = fList[k];
		var cplex = new IloCplex();
		cplex.tilim = 2400;
		var model = new IloOplModel(def,cplex);
		var filePath = dataDir.name + dataDir.separator + fList[k]; 
		var data = new IloOplDataSource(filePath);
		model.addDataSource(data);
		model.generate();
		if (cplex.solve()) {
			msg += ", " + sum(model.working) + ", " + cplex.getSolvedTime();
		} else {
			msg += ": ERROR";		
		}
		model.end();
 		data.end();
 		cplex.end();
 		writeln(msg);
		output.writeln(msg);
	}
	output.close();
	
	// finish
 	def.end();
 	
 	src.end();
}
