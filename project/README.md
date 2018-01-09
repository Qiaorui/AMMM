# Nurse Scheduling Problem

In this project, we need to design a working schedule for a set of nurses in a way that the number of nurses required is minimized. 

The problem requires that the number of nurses working each hour must fulfill the demand for that hour. In addition, there are some limitations on how the working hours should be scheduled. The working hours of nurses must be within a range: between minimum hour and maximum hour. The nurses must take an one hour break when they reached maximum consecutive hour. Furthermore, the nurses can only stay in the hospital for maximum presence hour.

## Directory overview
```
.   
├── Nurse_Scheduling.py             Parent Class with share function
├── README.md       
├── benchmark/                      Benchmark Instances
├── brkga   
│   └── BRKGA.py                    BRKGA algorithm
├── generator   
│   ├── Generator.py                Benchmark Generator
│   └── main.py     
├── grasp   
│   └── GRASP.py                    GRASP algorithm
├── ilp     
│   ├── config.dat      
│   ├── ilp.mod                     ilp model
│   ├── main.mod                    Use this to run batch test
│   ├── test/  
│   └── unit_test.mod               Unit Test module
├── main.py                         Script to execute Meta-heuristic
├── report.pdf                      Text Report
├── run_ilp.sh                      Script if you dot't want IDE
└── statistic   
    ├── brkga_result.txt    
    ├── grasp_result.txt    
    ├── ilp_result.txt  
    └── statistic_generator.R       Use R to generate statistic plot
```

## Test
Unit Tests are under folder '/ilp/test'.

## Usage

The Python version is Python 3. Execute 'python3' instead of 'python' if your default python version is 2

If you get error form running run_ilp.sh such as '\r': command not found. Do:
```
sed -i 's/\r$//' run_ilp.sh
```

If you get any trouble of using Meta-heuristic
```
python main.py -h
```

### Cplex ILP
Also you can use Cplex IDE
```
./run_ilp file_path
```

### Meta-Heuristic

```
main.py [-h] [-v] [-w OUTPUT_FILE] (-g | -b) path [path ...]

positional arguments:
  path            input file path

optional arguments:
  -h, --help      show this help message and exit
  -v, --verbose   increase output verbosity
  -w OUTPUT_FILE  write to file
  -g, --grasp     use GRASP algorithm
  -b, --brkga     use BRKGA algorithm
```

### Benchmark
Generate Benchmark Instances
```
python generator/main.py
```
Run benchmark using Cplex ILP. Also you can use Cplex IDE
```
./run_ilp.sh
```
Run benchmark using Meta-heuristic
```
python -u main.py (-g | -b) benchmark/*
```

### Statistic
Benchmark results are required
```
cd statistic
Rscript statistic_generator.R
```