#!/bin/bash

clear

echo "->Start Scripting"
echo "->Detecting OS"
case "$(uname -s)" in

  Darwin)
    echo '  Mac OS Detected, no OPL supported. please change to Linux or Windows'
    ;;

  Linux)
    echo '  Linux Detected, Running...'
    P="$(printenv LD_LIBRARY_PATH)"
    echo $P
    if [ "$P" != "" ]; then 
       echo "find LD_LIBRARY_PATH"
    else
       echo "Create LD_LIBRARY_PATH"
    fi
     # find Applications/ -path "*/CPLEX_*/*" -type d -iname 'cplex'
     #LD_LIBRARY_PATH=/opt/ibm/ILOG/CPLEX_Studio1251/opl/bin/x86-64_sles10_4.1
     #export LD_LIBRARY_PATH
    ;;

  CYGWIN*|MINGW32*|MSYS*)
    echo '  MS Windows Detected, not implement yet'
    ;;

   # Add here more strings to compare
   # See correspondence table at the bottom of this answer

  *)
    echo '  Unknown OS, exit' 
    ;;
esac



echo "->Exit"
