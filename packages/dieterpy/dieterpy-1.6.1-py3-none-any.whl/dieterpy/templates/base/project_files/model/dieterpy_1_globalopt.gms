

**************************
***** GLOBAL OPTIONS *****
**************************

* Set in ontrol_variables.csv to set end hour -> work in progress to be implemented
$setglobal end_hour %py_end_hour%
$setglobal h_set %py_h_set%


* Set in feature_configuration.csv to choose model modules
$setglobal DSM %py_dsm%

$setglobal prosumage %py_prosumage%
$setglobal heat %py_heat%

$setglobal reserves %py_reserves%
$setglobal reserves_endogenous %py_reserves_endogenous%
$setglobal reserves_exogenous %py_reserves_exogenous%

$setglobal P2H2 %py_hydrogen%
$setglobal Simplified_transporation %py_simplified_H2_transporation%
$setglobal Time_consuming_transportation %py_time_consuming_H2_transportation%

* Set in feature_configuration.csv to choose whether electric vehicle module is activated or not
* if EV_endogenous is activated than EV module is switch on and solved endogenously
* if additionally EV_exogenous is activated than EV module is solved exogeneously
$setglobal EV %py_ev%
$setglobal EV_EXOG %py_ev_exogenous%

* Set in control_variables.csv whether the model optimizes only dispatch or also investments
*----------> Not implemented yet. 'Investment' by default.
$setglobal dispatch_only %py_dispatch_only%
$setglobal investment %py_investment%

* Set in control_variables.csv
*----------> Not implemented yet. 'Investment' by default.
$setglobal net_transfer %py_network_transfer%

* Set star for no crossover to speed up calculation time by skipping crossover in LP solver
$setglobal no_crossover %py_no_crossover%

* Set star for infeasibility activation
$setglobal infeasibility %py_infeasibility%

* automatically imported
$setglobal feature_set %py_feature_set%


* --------------------------- GDX INPUT FILES ----------------------------------
$setglobal data_input_gdx %py_data_input_gdx%
$setglobal time_series_gdx %py_time_series_gdx%
$setglobal feat_node_gdx %py_feat_node_gdx%
$setglobal data_it_gdx %py_data_it_gdx%

* ------------- COUNTRY SET ITERATION -----------------------------------------

*switches
$setglobal iter_countries_switch_on   %py_iter_countries_switch_on%
$setglobal iter_countries_switch_off  %py_iter_countries_switch_off%

* set countries
$setglobal iter_countries_set         %py_iter_countries_set%

* set lines
$setglobal iter_lines_set             %py_iter_lines_set%

* ------------- TIME SERIES ITERATION -----------------------------------------

* switch
$setglobal iter_data_switch           %py_iter_data_switch%

* ------------- DISPLAY GLOBAL OPTIONS -----------------------------------------
display

"end_hour %end_hour% ,",
"h_set: %h_set% ,",
"feature_set: %feature_set% ,",

"DSM: %DSM% ,",
"reserves: %reserves% ,",
"prosumage: %prosumage% ,",
"heat: %heat% ,",
"EV_endogenous: %EV% ,",
"EV_exogenous: %EV_EXOG% ,",
"no_crossover: %no_crossover% ,",
"dispatch_only: %dispatch_only% ,",
"investment: %investment% ,",
"net_transfer: %net_transfer% ,",

"iter_countries_switch_on: %iter_countries_switch_on% ,",
"iter_countries_switch_off: %iter_countries_switch_off% ,",
"iter_countries_set: %iter_countries_set% ,",
"iter_lines_set: %iter_lines_set% ,",
"iter_data_switch: %iter_data_switch% ,"
;

********************************************************************************

* Sanity checks
$if "%reserves_endogenous%%reserves_exogenous%" == "**" $abort Choose only one reserve option (endogenous or exogenous)! ;
$if "%reserves_endogenous%%reserves_exogenous%" == "*" $if %reserves% == "" $abort reserves must be activated if choose either endogenous or exogenous! ;
$if "%EV%" == "" $if "%EV_EXOG%" == "*" $abort Switch on ev_exogenous in feature_configuration.csv! ;
* $if "%dispatch_only%" == "*" $if "%investment%" == "*" $abort Choose an appropriate option! ;
* $if "%dispatch_only%" == "" $if "%investment%" == "" $abort Choose one option, either dispatch or investment! ;

