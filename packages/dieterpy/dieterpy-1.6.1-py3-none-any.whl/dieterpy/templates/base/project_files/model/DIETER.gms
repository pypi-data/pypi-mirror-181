
********************************************************************************
$ontext
The Dispatch and Investment Evaluation Tool with Endogenous Renewables (DIETER).
Version 1.5.0, April 2021.
Written by Alexander Zerrahn, Wolf-Peter Schill, and Fabian St�ckl.
This work is licensed under the MIT License (MIT).
For more information on this license, visit http://opensource.org/licenses/mit-license.php.
Whenever you use this code, please refer to http://www.diw.de/dieter.
We are happy to receive feedback under wschill@diw.de.
$offtext
********************************************************************************

$setglobal DIETERgms ""

%DIETERgms%$setglobal MODELDIR %py_modeldir%

**************************
***** GLOBAL OPTIONS *****
**************************

%DIETERgms%$include "%MODELDIR%dieterpy_1_globalopt.gms"

%DIETERgms%$ontext

* Set star to skip Excel upload and load data from gdx
$setglobal skip_Excel ""

* Germany only - also adjust Excel inputs! by adding a empty column after DE node in spatial sheet
$setglobal GER_only "*"

* Set star to activate options
$setglobal DSM ""

$setglobal reserves_endogenous ""
$setglobal reserves_exogenous ""

$setglobal prosumage ""

$setglobal heat ""

$setglobal EV ""
$setglobal EV_EXOG ""

* Set star to activate P2H2 module (The two sub-modules: "re-conversion" and "H2 production and distribution for traffic" are controlled in more detail via the data_input Excel file!)
$setglobal P2H2 "*"
$setglobal Simplified_transporation "*"
$setglobal Time_consuming_transportation ""

$setglobal reserves "%reserves_endogenous%%reserves_exogenous%"

* Set star for no crossover to speed up calculation time by skipping crossover in LP solver
$setglobal no_crossover ""

$ontext
$offtext
* This closes the DIETERgms

********************************************************************************

* Sanity checks

$if "%reserves%" == "**" $abort Choose only one reserve option (endogenous or exogenous)! ;
$if "%EV%" == "" $if "%EV_EXOG%" == "*" $abort Switch on EV! ;
$if "%P2H2%" == "*" $if "%Simplified_transporation%" == "%Time_consuming_transportation%" $abort Choose one but only one type of transportation - either simplified or time consuming! ;

********************************************************************************

**************************
***** SOLVER OPTIONS *****
**************************

options
lp = CPLEX
optcr = 0.00
reslim = 10000000
limrow = 0
limcol = 0
dispwidth = 15
solprint = off
sysout = off
;

********************************************************************************

**************************
***** Dataload *****
**************************

%DIETERgms%$ontext
* Inclusion of scenario
$include "dataload.gms"
$ontext
$offtext

%DIETERgms%$include "%MODELDIR%dataload.gms"

********************************************************************************

%DIETERgms%$ontext
*************************************
***** Features for single nodes *****
*************************************

Set
features /dsm, ev, reserves, prosumage, heat, P2H2/
;

Table
feat_node(features,n)
                    DE
%DSM%$ontext
dsm                 0
$ontext
$offtext
%DIETERgms%$ontext
%reserves%$ontext
reserves            0
$ontext
$offtext
%DIETERgms%$ontext
%ev%$ontext
ev                  0
$ontext
$offtext
%DIETERgms%$ontext
%prosumage%$ontext
prosumage           0
$ontext
$offtext
%DIETERgms%$ontext
%heat%$ontext
heat                0
$ontext
$offtext
%DIETERgms%$ontext
%P2H2%$ontext
P2H2                1
$ontext
$offtext
;

$ontext
$offtext
* This closes the DIETERgms


***** Reduce problem size by removing entries of nodes not included in the feat_node parameter  *****

%DSM%$ontext
m_dsm_cu(n,dsm_curt)$(feat_node('dsm',n) = 0) = 0 ;
m_dsm_shift(n,dsm_shift)$(feat_node('dsm',n) = 0) = 0 ;
$ontext
$offtext

%prosumage%$ontext
m_res_pro(n,res)$(feat_node('prosumage',n) = 0) = 0 ;
m_sto_pro_e(n,sto)$(feat_node('prosumage',n) = 0) = 0 ;
m_sto_pro_p(n,sto)$(feat_node('prosumage',n) = 0) = 0 ;
$ontext
$offtext

%heat%$ontext
dh(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
d_dhw(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
$ontext
$offtext

Set
map_n_tech(n,tech)
map_n_sto(n,sto)
map_n_rsvr(n,rsvr)
map_n_dsm(n,dsm)
map_n_ev(n,ev)
map_l(l)
map_n_sto_pro(n,sto)
map_n_res_pro(n,tech)
;

map_n_tech(n,tech) = yes$m_p(n,tech) ;
map_n_sto(n,sto) = yes$m_sto_p_in(n,sto) ;
map_n_rsvr(n,rsvr) = yes$m_rsvr_p_out(n,rsvr) ;
map_n_dsm(n,dsm_curt) = yes$m_dsm_cu(n,dsm_curt) ;
map_n_dsm(n,dsm_shift) = yes$m_dsm_shift(n,dsm_shift) ;
map_n_ev(n,ev) = yes$phi_ev(n,ev) ;
map_l(l) = yes$m_ntc(l) ;
map_n_sto_pro(n,sto) = yes$m_sto_pro_p(n,sto) ;
map_n_res_pro(n,res) = yes$m_res_pro(n,res) ;
;

* No interconnections between non-adjacent or nonuploaded nodes
m_ntc(l)$( smax(n,inc(l,n)) = 0 OR smin(n,inc(l,n)) = 0 ) = 0 ;

********************************************************************************
***** Model *****
********************************************************************************

%DIETERgms%$ontext
* Inclusion of scenario
$include "model.gms"
$ontext
$offtext

%DIETERgms%$include "%MODELDIR%model.gms"

********************************************************************************
***** Options, fixings, report preparation *****
********************************************************************************

%DIETERgms%$include "%MODELDIR%dieterpy_6_solveropt.gms"

%DIETERgms%$ontext

* Solver options
$onecho > cplex.opt
lpmethod 4
threads 0
SolutionType 2
barepcomp 1e-8
datacheck 2
quality 1
predual -1
$offecho

%no_crossover%$ontext
$onecho > cplex.opt
lpmethod 4
threads 0
barcrossalg -1
SolutionType 2
barepcomp 1e-8
datacheck 2
quality 1
predual -1
$offecho
$ontext
$offtext
;

$ontext
$offtext
* This closes the DIETERgms

dieter.OptFile = 1;
dieter.holdFixed = 1;


%DIETERgms%$ontext
* Inclusion of scenario
$include "scenario.gms"
$ontext
$offtext

%DIETERgms%$ontext
* Inclusion of scenario
$include "fix.gms"
$ontext
$offtext


%DIETERgms%$include "%MODELDIR%fix.gms"
%DIETERgms%$include "%MODELDIR%dieterpy_7_custom.gms"

********************************************************************************
***** Solve *****
********************************************************************************

%DIETERgms%$ontext
solve DIETER using lp min Z;

execute_unload "results.gdx";
$ontext
$offtext
