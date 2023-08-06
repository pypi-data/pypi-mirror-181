
********************************************************************************
$ontext
The Dispatch and Investment Evaluation Tool with Endogenous Renewables (DIETER).
Version 1.5.0, April 2021.
Written by Alexander Zerrahn, Wolf-Peter Schill, and Fabian Stöckl.
This work is licensed under the MIT License (MIT).
For more information on this license, visit http://opensource.org/licenses/mit-license.php.
Whenever you use this code, please refer to http://www.diw.de/dieter.
We are happy to receive feedback under wschill@diw.de.
$offtext
********************************************************************************

%DIETERgms%$ontext
%GER_only%$ontext
* This switch off Net Transfer Capacity module when Germany is the only country
NTC.fx(l) = 0 ;
F.fx(l,h) = 0 ;
$ontext
$offtext


********************************************************************************
**** Exogenous EV  *************************************************************
********************************************************************************

%EV%$ontext
%EV_EXOG%$ontext
EV_DISCHARGE.fx(n,ev,h) = 0 ;
RP_EV_G2V.fx(n,reserves,ev,h) = 0 ;
RP_EV_V2G.fx(n,reserves,ev,h) = 0 ;
$ontext
$offtext

********************************************************************************
**** No storage and DSM in first period  ***************************************
********************************************************************************

** No storage inflow in first period **
STO_IN.fx(n,sto,h)$(ord(h) = 1) = 0;

%DSM%$ontext
** No DSM load shifting in the first period **
DSM_UP.fx(n,dsm_shift,h)$(ord(h) = 1) = 0;
DSM_DO.fx(n,dsm_shift,h,hh)$(ord(h) = 1) = 0 ;
DSM_DO.fx(n,dsm_shift,h,h)$(ord(h) = 1) = 0 ;
DSM_UP_DEMAND.fx(n,dsm_shift,h)$(ord(h) = 1) = 0 ;
DSM_DO_DEMAND.fx(n,dsm_shift,h)$(ord(h) = 1) = 0 ;

** No reserves provision by DSM in first period **
RP_DSM_SHIFT.fx(n,reserves,dsm_shift,h)$(ord(h) = 1) = 0;
RP_DSM_CU.fx(n,reserves,dsm_curt,h)$(ord(h) = 1) = 0 ;
RP_DSM_CU.fx(n,reserves,dsm_curt,h)$(ord(h) = 1) = 0 ;

** No provision of PR and negative reserves by DSM load curtailment **
RP_DSM_CU.fx(n,reserves_prim,dsm_curt,h) = 0 ;
RP_DSM_CU.fx(n,reserves_do,dsm_curt,h) = 0 ;

** No provision of PR by DSM load shifting **
RP_DSM_SHIFT.fx(n,reserves_prim,dsm_shift,h) = 0 ;
$ontext
$offtext

********************************************************************************
**** No primary reserves by heating devices  ***********************************
********************************************************************************

%heat%$ontext
%reserves%$ontext
RP_HP.fx(n,reserves_prim,bu,hp,h) = 0 ;
RP_SETS.fx(n,reserves_prim,bu,ch,h) = 0 ;
RP_SETS_AUX.fx(n,reserves_prim,bu,ch,h) = 0 ;
RP_H_ELEC.fx(n,reserves_prim,bu,ch,h) = 0 ;
$ontext
$offtext


********************************************************************************
**** Fixing to reduce model size  **********************************************
********************************************************************************

F.fx(l,h)$(m_ntc(l) = 0) = 0 ;
NTC.fx(l)$(m_ntc(l) = 0) = 0 ;

G_L.fx(n,tech,h)$(m_p(n,tech) = 0) = 0 ;
G_UP.fx(n,tech,h)$(m_p(n,tech) = 0) = 0 ;
G_DO.fx(n,tech,h)$(m_p(n,tech) = 0) = 0 ;
G_RES.fx(n,nondis,h)$(m_p(n,nondis) = 0) = 0 ;
CU.fx(n,tech,h)$(m_p(n,tech) = 0) = 0 ;
N_TECH.fx(n,tech)$(m_p(n,tech) = 0) = 0 ;

N_STO_P_IN.fx(n,sto)$(m_sto_p_in(n,sto) = 0) = 0 ;
N_STO_P_OUT.fx(n,sto)$(m_sto_p_out(n,sto) = 0) = 0 ;
N_STO_E.fx(n,sto)$(m_sto_e(n,sto) = 0) = 0 ;
STO_IN.fx(n,sto,h)$(m_sto_p_in(n,sto) = 0) = 0 ;
STO_OUT.fx(n,sto,h)$(m_sto_p_out(n,sto) = 0) = 0 ;
STO_L.fx(n,sto,h)$(m_sto_p_in(n,sto) = 0) = 0 ;
* RP_STO_IN.fx(n,reserves,sto,h)$(m_sto_p_in(n,sto) = 0) = 0 ;
* RP_STO_OUT.fx(n,reserves,sto,h)$(m_sto_p_in(n,sto) = 0) = 0 ;

RSVR_OUT.fx(n,rsvr,h)$(m_rsvr_p_out(n,rsvr) = 0) = 0 ;
RSVR_L.fx(n,rsvr,h)$(m_rsvr_p_out(n,rsvr) = 0) = 0 ;
N_RSVR_E.fx(n,rsvr)$(m_rsvr_p_out(n,rsvr) = 0) = 0 ;
N_RSVR_P.fx(n,rsvr)$(m_rsvr_p_out(n,rsvr) = 0) = 0 ;

%DSM%$ontext
DSM_CU.fx(n,dsm,h)$(feat_node('dsm',n) = 0 OR m_dsm_cu(n,dsm) = 0) = 0 ;
DSM_UP.fx(n,dsm,h)$(feat_node('dsm',n) = 0 OR m_dsm_shift(n,dsm) = 0) = 0 ;
DSM_DO.fx(n,dsm,h,hh)$(feat_node('dsm',n) = 0 OR m_dsm_shift(n,dsm) = 0) = 0 ;
DSM_UP_DEMAND.fx(n,dsm,h)$(feat_node('dsm',n) = 0 OR m_dsm_shift(n,dsm) = 0) = 0 ;
DSM_DO_DEMAND.fx(n,dsm,h)$(feat_node('dsm',n) = 0 OR m_dsm_shift(n,dsm) = 0) = 0 ;
N_DSM_CU.fx(n,dsm)$(feat_node('dsm',n) = 0 OR m_dsm_cu(n,dsm) = 0) = 0 ;
N_DSM_SHIFT.fx(n,dsm)$(feat_node('dsm',n) = 0 OR m_dsm_shift(n,dsm) = 0) = 0 ;
$ontext
$offtext

%reserves%$ontext
RP_DIS.fx(n,reserves,tech,h)$(feat_node('reserves',n) = 0 OR m_p(n,tech) = 0) = 0 ;
RP_NONDIS.fx(n,reserves,tech,h)$(feat_node('reserves',n) = 0 OR m_p(n,tech) = 0) = 0 ;
RP_STO_IN.fx(n,reserves,sto,h)$(feat_node('reserves',n) = 0 OR m_sto_p_in(n,sto) = 0) = 0 ;
RP_STO_OUT.fx(n,reserves,sto,h)$(feat_node('reserves',n) = 0 OR m_sto_p_in(n,sto) = 0) = 0 ;
RP_EV_V2G.fx(n,reserves,ev,h)$(feat_node('reserves',n) = 0) = 0 ;
RP_EV_G2V.fx(n,reserves,ev,h)$(feat_node('reserves',n) = 0) = 0 ;
RP_DSM_CU.fx(n,reserves,dsm_curt,h)$(feat_node('reserves',n) = 0 OR m_dsm_cu(n,dsm_curt) = 0) = 0 ;
RP_DSM_SHIFT.fx(n,reserves,dsm_shift,h)$(feat_node('reserves',n) = 0 OR m_dsm_shift(n,dsm_shift) = 0) = 0 ;
RP_RSVR.fx(n,reserves,rsvr,h)$(feat_node('reserves',n) = 0  OR m_rsvr_p_out(n,rsvr) = 0) = 0 ;
$ontext
$offtext

%prosumage%$ontext
CU_PRO.fx(n,res,h)$(feat_node('prosumage',n) = 0 OR m_res_pro(n,res) = 0) = 0 ;
G_MARKET_PRO2M.fx(n,res,h)$(feat_node('prosumage',n) = 0 OR m_res_pro(n,res) = 0) = 0 ;
G_MARKET_M2PRO.fx(n,h)$(feat_node('prosumage',n) = 0) = 0 ;
G_RES_PRO.fx(n,res,h)$(feat_node('prosumage',n) = 0 OR m_res_pro(n,res) = 0) = 0 ;
STO_IN_PRO2PRO.fx(n,res,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_IN_PRO2M.fx(n,res,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_IN_M2PRO.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_IN_M2M.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_OUT_PRO2PRO.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_OUT_PRO2M.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_OUT_M2PRO.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_OUT_M2M.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_L_PRO2PRO.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_L_PRO2M.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_L_M2PRO.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_L_M2M.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
N_STO_E_PRO.fx(n,sto)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
N_STO_P_PRO.fx(n,sto)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_L_PRO.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
N_RES_PRO.fx(n,res)$(feat_node('prosumage',n) = 0 OR m_res_pro(n,res) = 0) = 0 ;
$ontext
$offtext

%EV%$ontext
EV_CHARGE.fx(n,ev,h)$(feat_node('ev',n) = 0) = 0 ;
EV_DISCHARGE.fx(n,ev,h)$(feat_node('ev',n) = 0) = 0 ;
EV_L.fx(n,ev,h)$(feat_node('ev',n) = 0) = 0 ;
EV_PHEVFUEL.fx(n,ev,h)$(feat_node('ev',n) = 0) = 0 ;
EV_GED.fx(n,ev,h)$(feat_node('ev',n) = 0) = 0 ;
RP_EV_V2G.fx(n,reserves,ev,h)$(feat_node('ev',n) = 0) = 0 ;
RP_EV_G2V.fx(n,reserves,ev,h)$(feat_node('ev',n) = 0) = 0 ;
$ontext
$offtext

%heat%$ontext
H_DIR.fx(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_SETS_LEV.fx(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_SETS_IN.fx(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_SETS_OUT.fx(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_HP_IN.fx(n,bu,ch,hh)$(feat_node('heat',n) = 0) = 0 ;
H_STO_LEV.fx(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_STO_IN_HP.fx(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_STO_IN_ELECTRIC.fx(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_ELECTRIC_IN.fx(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_STO_IN_FOSSIL.fx(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_STO_OUT.fx(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_DHW_DIR.fx(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_DHW_STO_OUT.fx(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_DHW_AUX_ELEC_IN.fx(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_DHW_AUX_LEV.fx(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_DHW_AUX_OUT.fx(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
$ontext
$offtext
%P2H2%$ontext
H2_N_PROD_CENT.fx(n,h2_tech)$( h2_tech_avail_sw(n,h2_tech) = 0 ) = 0 ;
H2_N_PROD_DECENT.fx(n,h2_tech)$( h2_tech_avail_sw(n,h2_tech) = 0 ) = 0 ;
H2_PROD_OUT.fx(n,h2_tech,h2_channel,h)$( h2_tech_avail_sw(n,h2_tech) = 0 OR h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_E_H2_IN.fx(n,h2_tech,h2_channel,h)$( h2_tech_avail_sw(n,h2_tech) = 0 OR h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_N_PROD_AUX.fx(n,h2_tech,h2_channel)$( h2_tech_avail_sw(n,h2_tech) = 0 OR h2_channel_avail_sw(n,h2_channel) = 0 OR h2_prod_aux_sw(n,h2_tech,h2_channel) = 0 ) = 0 ;
H2_PROD_AUX_IN.fx(n,h2_tech,h2_channel,h)$( h2_tech_avail_sw(n,h2_tech) = 0 OR h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_PROD_AUX_OUT.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_HYD_LIQ_OUT.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_N_HYD_LIQ.fx(n,h2_channel)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_hyd_liq_sw(n,h2_channel) = 0 ) = 0 ;
H2_STO_P_OUT.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_STO_P_IN.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_STO_P_L.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_sto_p_sw(n,h2_channel) = 0 ) = 0 ;
H2_N_STO.fx(n,h2_channel)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_sto_p_sw(n,h2_channel) = 0 ) = 0 ;
H2_STO_P_L0.fx(n,h2_channel)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_sto_p_sw(n,h2_channel) = 0 ) = 0 ;
H2_AUX_PRETRANS_OUT.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_N_AUX_PRETRANS.fx(n,h2_channel)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_aux_pretrans_sw(n,h2_channel) = 0 ) = 0 ;
H2_TRANS_OUT.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_N_TRANS.fx(n,h2_channel)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_trans_sw(n,h2_channel) = 0 ) = 0 ;
H2_N_AVAI_TRANS.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_trans_sw(n,h2_channel) = 0 ) = 0 ;
H2_AUX_BFLP_STO_OUT.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_AUX_BFLP_STO_IN.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_N_AUX_BFLP_STO.fx(n,h2_channel)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_aux_bflp_sto_sw(n,h2_channel) = 0 ) = 0 ;
H2_LP_STO_OUT.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_LP_STO_L.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_lp_sto_sw(n,h2_channel) = 0 ) = 0 ;
H2_N_LP_STO.fx(n,h2_channel)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_lp_sto_sw(n,h2_channel) = 0 ) = 0 ;
H2_LP_STO_L0.fx(n,h2_channel)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_lp_sto_sw(n,h2_channel) = 0 ) = 0 ;
H2_DEHYD_EVAP_OUT.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_N_DEHYD_EVAP.fx(n,h2_channel)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_dehyd_evap_sw(n,h2_channel) = 0 ) = 0 ;
H2_AUX_BFMP_STO_OUT.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_N_AUX_BFMP_STO.fx(n,h2_channel)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_aux_BFMP_sto_sw(n,h2_channel) = 0 ) = 0 ;
H2_MP_STO_OUT.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_MP_STO_L.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_MP_sto_sw(n,h2_channel) = 0 ) = 0 ;
H2_N_MP_STO.fx(n,h2_channel)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_MP_sto_sw(n,h2_channel) = 0 ) = 0 ;
H2_MP_STO_L0.fx(n,h2_channel)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_MP_sto_sw(n,h2_channel) = 0 ) = 0 ;
H2_AUX_BFHP_STO_OUT.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_AUX_BFHP_STO_IN.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_N_AUX_BFHP_STO.fx(n,h2_channel)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_aux_bfhp_sto_sw(n,h2_channel) = 0 ) = 0 ;
H2_N_HP_STO.fx(n,h2_channel)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_hp_sto_sw(n,h2_channel) = 0 ) = 0 ;
H2_HP_STO_OUT.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_HP_STO_L.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_hp_sto_sw(n,h2_channel) = 0 ) = 0 ;
H2_HP_STO_L0.fx(n,h2_channel)$(h2_channel_avail_sw(n,h2_channel) = 0 OR h2_hp_sto_sw(n,h2_channel) = 0 ) = 0 ;
H2_AUX_BFFUEL_OUT.fx(n,h2_channel,h)$( h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_N_AUX_BFFUEL.fx(n,h2_channel)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_aux_bffuel_sw(n,h2_channel) = 0 ) = 0 ;
H2_N_RECON_AUX.fx(n,h2_channel,h2_tech_recon)$( h2_recon_aux_sw(n,h2_channel,h2_tech_recon) = 0 OR h2_tech_recon_sw(n,h2_tech_recon) = 0 OR h2_channel_avail_sw(n,h2_channel) = 0 ) = 0 ;
H2_RECON_AUX_OUT.fx(n,h2_channel,h2_tech_recon,h)$( h2_channel_avail_sw(n,h2_channel) = 0 OR h2_recon_sw(n,h2_channel) = 0 OR h2_tech_recon_sw(n,h2_tech_recon) = 0 ) = 0 ;
H2_N_RECON.fx(n,h2_tech_recon)$( h2_tech_recon_sw(n,h2_tech_recon) = 0 ) = 0 ;
H2_E_RECON_OUT.fx(n,h2_channel,h2_tech_recon,h)$( h2_tech_recon_sw(n,h2_tech_recon) = 0 OR h2_channel_avail_sw(n,h2_channel) = 0 OR h2_recon_sw(n,h2_channel) = 0 ) = 0 ;
* H2_N_RECON.fx(n,h2_tech_recon)$(h2_bi_recon_set(n,h2_tech_recon)) = 0 ;
H2_BYPASS_1.fx(n,h2_tech,h2_channel,h)$( h2_bypass_1_sw(n,h2_tech,h2_channel) = 0 OR h2_channel_avail_sw(n,h2_channel) = 0 OR h2_bypass_1_sw(n,h2_tech,h2_channel) = 0 ) = 0 ;
H2_BYPASS_2.fx(n,h2_channel,h)$( h2_bypass_2_sw(n,h2_channel) = 0 OR h2_channel_avail_sw(n,h2_channel) = 0 OR h2_bypass_2_sw(n,h2_channel) = 0 ) = 0 ;

*** Fixing PEM for decentralized production ***

H2_N_PROD_DECENT.fx(n,'ALK') = 0 ;
H2_E_H2_IN.fx(n,'ALK','fuel_decent',h) = 0 ;
H2_PROD_OUT.fx(n,'ALK','fuel_decent',h) = 0 ;
H2_N_PROD_AUX.fx(n,'ALK','fuel_decent') = 0 ;
H2_PROD_AUX_IN.fx(n,'ALK','fuel_decent',h) = 0 ;
$ontext
$offtext

