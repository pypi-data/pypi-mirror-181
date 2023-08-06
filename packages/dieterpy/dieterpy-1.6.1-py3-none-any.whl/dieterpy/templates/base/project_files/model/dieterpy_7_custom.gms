

%infeasibility%G_INFES.fx(n,h) = 0 ;
%infeasibility%H_INFES.fx(n,bu,ch,h) = 0 ;
%infeasibility%H_DHW_INFES.fx(n,bu,ch,h) = 0 ;

Parameter
m_exog_p(n,tech)
m_exog_sto_e(n,sto)
m_exog_sto_p_in(n,sto)
m_exog_sto_p_out(n,sto)
m_exog_rsvr_p(n,rsvr)
m_exog_rsvr_e(n,rsvr)
m_exog_ntc(l)
;

m_exog_p(n,tech) = technology_data(n,tech,'fixed_capacities') ;
m_exog_sto_e(n,sto) = storage_data(n,sto,'fixed_capacities_energy');
m_exog_sto_p_in(n,sto) = storage_data(n,sto,'fixed_capacities_power_in');
m_exog_sto_p_out(n,sto) = storage_data(n,sto,'fixed_capacities_power_out');
m_exog_rsvr_p(n,rsvr) = reservoir_data(n,rsvr,'fixed_capacities_power');
* m_exog_rsvr_e(n,rsvr) = reservoir_data(n,rsvr,'fixed_capacities_energy');
m_exog_ntc(l) = topology_data(l,'fixed_capacities_ntc');


*** Dispatch model
%dispatch_only%$ontext
N_TECH.fx(n,tech) = m_exog_p(n,tech) ;
N_STO_P_IN.fx(n,sto) = m_exog_sto_p_in(n,sto) ;
N_STO_P_OUT.fx(n,sto) = m_exog_sto_p_out(n,sto) ;
N_STO_E.fx(n,sto) = m_exog_sto_e(n,sto) ;
N_RSVR_P.fx(n,rsvr) =  m_exog_rsvr_p(n,rsvr) ;
NTC.fx(l) = m_exog_ntc(l) ;
$ontext
$offtext

*** Investment model
%investment%$ontext
* N_TECH.lo(n,tech) = technology_data(n,tech,'min_installable') ;
N_TECH.up(n,tech) = technology_data(n,tech,'max_installable') ;

* N_STO_P.lo(n,sto) = storage_data(n,sto,'min_power') ;
* N_STO_E.lo(n,sto) = storage_data(n,sto,'min_energy') ;
N_STO_P_IN.up(n,sto) = storage_data(n,sto,'max_power_in') ;
N_STO_P_OUT.up(n,sto) = storage_data(n,sto,'max_power_out') ;
N_STO_E.up(n,sto) = storage_data(n,sto,'max_energy') ;

* N_RSVR_P.lo(n,rsvr) =  reservoir_data(n,rsvr,'min_power') ;
* N_RSVR_E.lo(n,rsvr) =  reservoir_data(n,rsvr,'min_energy') ;

N_RSVR_P.up(n,rsvr) =  reservoir_data(n,rsvr,'max_power') ;
N_RSVR_E.up(n,rsvr) =  reservoir_data(n,rsvr,'max_energy') ;

* NTC.lo(l) = topology_data(l,'min_installable') ;
NTC.up(l) = topology_data(l,'max_installable') ;
$ontext
$offtext


*** No network transfer
%net_transfer%NTC.fx(l) = 0 ;
%net_transfer%F.fx(l,h) = 0 ;


***** Data iteration **********************************************************

%iter_data_switch%$ontext

Sets
scenario
identifer
;

Parameters
iter_data(h,identifer,scenario)
;

$GDXin "%data_it_gdx%"

$load scenario
$load identifer
$load iter_data
;

$ontext
$offtext

*******************************************************************************

*set used for report
Set feat_included(features);
feat_included(features) = yes$(sum(n, feat_node(features,n))) ;
