
* lpmethod: parameter for choosing an optimizer
*      0 "Automatic selection of an optimizer", 1 "Primal Simplex", 2 " Dual Simplex", 3 "Network Simplex", 4 " Barrier", 5 "Sifting", 6 "Concurrent optimizer"
*      Barrier optimizer offers an approach particularly efficient on large and sparse problems.
* threads: multithreaded parallel barrier, parallel MIP, and concurrent optimizers.
*      These parallel optimizers are implemented to run on hardware platforms with multiple cores.
*      default setting 0 (zero), the number of threads that CPLEX actually uses during a parallel optimization ->
*      is no more than 32 or the number of CPU cores available on the computer where CPLEX is running (whichever is smaller)
*  barcrossalg: if any, crossover is performed at the end of a barrier optimization.
*      -1 No crossover, 0 Automatic: let CPLEX choose; default. 1 Primal crossover, 2  Dual crossover
* barepcomp: Barrier Convergence Tolerance 1e-10 to INF default 1e-8. The Convergence Tolerance sets the tolerance on complementarity for convergence.
*       The barrier algorithm will terminate with an optimal solution if the relative complementarity is smaller than this value.


* Solver options
$onecho > cplex.opt

lpmethod 4
threads 0
$offecho

%no_crossover%$ontext
$onecho > cplex.opt

lpmethod 4
threads 0
SolutionType 2
barepcomp 1e-8
$offecho
$ontext
$offtext

* In case of GUSS tool with parallel processing
$onecho > cplexd.opt

lpmethod 4
threads 1
$offecho

%no_crossover%$ontext
$onecho > cplexd.opt

lpmethod 4
threads 1
SolutionType 2
barepcomp 1e-8
$offecho
$ontext
$offtext