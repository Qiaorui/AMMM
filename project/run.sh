#!/bin/bash
#clear

echo "->Start Scripting"
X_ARGS='ilp/main.mod ilp/config.dat'

if [ $1 = "test" ]; then
  X_ARGS='ilp/unit_test.mod ilp/config.dat'
fi
if [ $# -eq 2 ]; then
  X_ARGS="$1 $2"
fi

if [ ! -d "benchmark" ]; then
  python generator/main.py
fi

echo "->Detecting OS"
case "$(uname -s)" in

  Darwin)
    echo '  Mac OS Detected, no OPL supported. please change to Linux or Windows'
    ;;

  Linux)
    echo '  Linux Detected, Running...'
    P="$(printenv LD_LIBRARY_PATH)"
    echo $P
    if [ "$P" = "" ]; then 
       echo "Create LD_LIBRARY_PATH"
       LD_LIBRARY_PATH="$(find /opt/ -path "*/CPLEX_*/opl/bin/*" -type d -iname 'x*')"
       if [ "$LD_LIBRARY_PATH" = "" ]; then
           echo "No oplrun direcoty found, exit on error"
           exit
       else
           echo "$P"
           export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
           export PATH=:$LD_LIBRARY_PATH
           oplrun $X_ARGS
       fi
    fi
     # find Applications/ -path "*/CPLEX_*/*" -type d -iname 'cplex'
     #LD_LIBRARY_PATH=/opt/ibm/ILOG/CPLEX_Studio1251/opl/bin/x86-64_sles10_4.1
     #export LD_LIBRARY_PATH
    ;;

  CYGWIN*|MINGW32*|MSYS*)
    echo '  MS Windows Detected, Running...'
    oplrun.exe $X_ARGS
    ;;

   # Add here more strings to compare
   # See correspondence table at the bottom of this answer

  *)
    echo '  Unknown OS, exit' 
    ;;
esac

echo "->Exit"
