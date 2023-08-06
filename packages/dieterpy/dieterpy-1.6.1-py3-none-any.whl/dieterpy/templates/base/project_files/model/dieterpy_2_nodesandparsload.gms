

***************  UPLOAD TIME-CONSTANT SETS AND PARAMETERS  *********************

***********************************
***** Definition via Upload *******
***********************************

***** Define country set **********

* with iteration
%iter_countries_switch_on%$ontext

*Set n "Nodes" / %iter_countries_set% / ;
*Set l "Lines" / %iter_lines_set% / ;

$include "%MODELDIR%countries-lines.gms"
$ontext
$offtext

* without iteration
%iter_countries_switch_off%$ontext
$GDXin "%data_input_gdx%"
$load n l
;
$ontext
$offtext

************************************

$GDXin "%data_input_gdx%"
$load tech headers_tech tech_dispatch tech_res_con
$load sto headers_sto rsvr headers_reservoir reservoir_data dsm headers_dsm dsm_type
$load technology_data_upload storage_data dsm_data_upload
$load headers_topology topology_data
$load inc
$load ev headers_ev ev_data
$load headers_prosumage_generation headers_prosumage_storage prosumage_data_generation prosumage_data_storage
$load reserves reserves_up_down reserves_spin_nonspin reserves_prim_nonprim headers_reserves reserves_data_upload
$load bu ch heat_storage heat_hp heat_elec heat_fossil headers_heat heat_data_upload
$load h2_tech h2_channel h2_tech_recon headers_h2_parameters_table1 headers_h2_parameters_table2 headers_h2_parameters_table3 headers_h2_parameters_table4 headers_h2_parameters_table5 headers_h2_parameters_table6 headers_h2_parameters_table7 headers_h2_parameters_table8 headers_h2_parameters_table9 headers_h2_parameters_table10 h2_parameter_data_table1 h2_parameter_data_table2 h2_parameter_data_table3 h2_parameter_data_table4 h2_parameter_data_table5 h2_parameter_data_table6 h2_parameter_data_table7 h2_parameter_data_table8 h2_parameter_data_table9 h2_parameter_data_table10
$load headers_nodes, headers_scalar, nodes_data_upload, scalar_data_upload
;

***************  UPLOAD TIME-SERIES SETS AND PARAMETERS  ***********************

***********************************
******* Definition end_hour *******
***********************************

******* Define custom h set *******
%end_hour%$ontext

Set h "Hours" / %h_set% / ;

$ontext
$offtext
***********************************

$GDXin "%time_series_gdx%"
%end_hour%$load h
$load headers_time time_data_upload
$load headers_time_ev ev_time_data_upload
$load reserves_time_data_activation
$load reserves_time_data_provision
$load dh_upload
$load temp_source_upload
$load d_dhw_upload nets_profile
$load h2_time_data
$load h2_p2x_time_data
* $load theta_night
;

* we need all global features as set-coordinates
set
features /%feature_set%/
;

parameter

feat_node(features,n)
;

$GDXin "%feat_node_gdx%"
$load feat_node
;
