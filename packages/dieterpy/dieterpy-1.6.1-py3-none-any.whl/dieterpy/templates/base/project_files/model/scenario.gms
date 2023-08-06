
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


*****************************************
**** Scenario file **********************
*****************************************


* THIS FILE CAN BE LEFT EMPTY WHEN NO PARAMETERS OR VARIABLES WANT TO BE MODIFIED FROM INPUT EXCEL FILES

phi_min_res(n) = 0.8 ;

* Germany only, also adjust Excel, no infeasibility, no Net Transfer Capacity module
NTC.fx(l) = 0 ;
F.fx(l,h) = 0 ;
G_INFES.fx(n,h) = 0 ;
H_INFES.fx(n,bu,ch,h) = 0 ;
H_DHW_INFES.fx(n,bu,ch,h) = 0 ;