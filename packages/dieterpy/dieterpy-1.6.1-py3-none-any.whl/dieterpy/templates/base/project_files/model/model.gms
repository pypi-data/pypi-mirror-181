
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

Variables
Z                Value objective function [Euro]
F(l,h)           Energy flow over link l in hour h [MWh]
;

Positive Variables
G_L(n,tech,h)            Generation level in hour h [MWh]
G_UP(n,tech,h)           Generation upshift in hour h [MWh]
G_DO(n,tech,h)           Generation downshift in hour h [MWh]

G_RES(n,tech,h)          Generation renewables type res in hour h [MWh]
CU(n,tech,h)             Renewables curtailment technology res in hour h [MWh]

STO_IN(n,sto,h)          Storage inflow technology sto hour h [MWh]
STO_OUT(n,sto,h)         Storage outflow technology sto hour h [MWh]
STO_L(n,sto,h)           Storage level technology sto hour h [MWh]

EV_CHARGE(n,ev,h)        Electric vehicle charging vehicle profile ev hour h [MWh]
EV_DISCHARGE(n,ev,h)     Electric vehicle discharging vehicle profile ev hour h [MWh]
EV_L(n,ev,h)             Electric vehicle charging level vehicle profile ev hour h [MWh]
EV_PHEVFUEL(n,ev,h)      Plug in hybrid electric vehicle conventional fuel use vehicle profile ev hour h [MWh]
EV_GED(n,ev,h)           Grid electricity demand for mobility vehicle profile ev hour h [MWh]

N_TECH(n,tech)           Technology tech built [MW]
N_STO_E(n,sto)           Storage technology built - Energy [MWh]
N_STO_P_IN(n,sto)        Storage loading capacity built [MW]
N_STO_P_OUT(n,sto)       Storage discharging capacity built [MW]

DSM_CU(n,dsm,h)          DSM: Load curtailment hour h [MWh]
DSM_UP(n,dsm,h)          DSM: Load shifting up hour h technology dsm [MWh]
DSM_DO(n,dsm,h,hh)       DSM: Load shifting down in hour hh to account for upshifts in hour h technology dsm [MWh]

DSM_UP_DEMAND(n,dsm,h)   DSM: Load shifting up active for wholesale demand in hour h of technology dsm [MWh]
DSM_DO_DEMAND(n,dsm,h)   DSM: Load shifting down active for wholesale demand in hour h of technology dsm [MWh]

N_DSM_CU(n,dsm)          DSM: Load curtailment capacity [MW]
N_DSM_SHIFT(n,dsm)       DSM: Load shifting capacity [MWh]

RP_DIS(n,reserves,tech,h)        Reserve provision by conventionals in hour h [MW]
RP_NONDIS(n,reserves,tech,h)     Reserve provision by renewables in hour h [MW]
RP_STO_IN(n,reserves,sto,h)      Reserve provision by storage in in hour h [MW]
RP_STO_OUT(n,reserves,sto,h)     Reserve provision by storage out in hour h [MW]
RP_EV_V2G(n,reserves,ev,h)       Reserve provision by electric vehicles V2G hour h [MW]
RP_EV_G2V(n,reserves,ev,h)       Reserve provision by electric vehicles G2V hour h [MW]
RP_DSM_CU(n,reserves,dsm,h)      Reserve provision by DSM load curtailment in hour h [MW]
RP_DSM_SHIFT(n,reserves,dsm,h)   Reserve provision by DSM load shifting in hour h [MW]
RP_RSVR(n,reserves,rsvr,h)       Reserve provision by reservoirs h [MW]
RP_SETS(n,reserves,bu,ch,h)      Reserve provision by SETS [MW]
RP_SETS_AUX(n,reserves,bu,ch,h)  Reserve provision by SETS auxiliary DHW modules [MW]
RP_HP(n,reserves,bu,ch,h)        Reserve provision by heat pumps [MW]
RP_H_ELEC(n,reserves,bu,ch,h)    Reserve provision by hybrid electric heaters [MW]

CU_PRO(n,tech,h)                 Prosumage: curtailment of renewable generation in hour h [MWh]
G_MARKET_PRO2M(n,tech,h)         Prosumage. energy sent to market in hour h [MWh]
G_MARKET_M2PRO(n,h)              Prosumage: withdrawal of energy from market in hour h [MWh]
G_RES_PRO(n,tech,h)              Prosumage: hourly renewables generation in hour h [MWh]
STO_IN_PRO2PRO(n,tech,sto,h)     Prosumage: storage loading from generation for discharging to consumption in hour h [MWh]
STO_IN_PRO2M(n,tech,sto,h)       Prosumage: storage loading from generation for discharging to market in hour h [MWh]
STO_IN_M2PRO(n,sto,h)            Prosumage: storage loading from market for discharging to consumption in hour h [MWh]
STO_IN_M2M(n,sto,h)              Prosumage: storage loading from market for discharging to market in hour h [MWh]
STO_OUT_PRO2PRO(n,sto,h)         Prosumage: storage discharging to consumption from generation in hour h [MWh]
STO_OUT_PRO2M(n,sto,h)           Prosumage: storage discharging to market from generation in hour h [MWh]
STO_OUT_M2PRO(n,sto,h)           Prosumage: storage discharging to consumption from market in hour h [MWh]
STO_OUT_M2M(n,sto,h)             Prosumage: storage discharging to market from market in hour h [MWh]
STO_L_PRO2PRO(n,sto,h)           Prosumage: storage level generation to consumption in hour h [MWh]
STO_L_PRO2M(n,sto,h)             Prosumage: storage level generation to market in hour h [MWh]
STO_L_M2PRO(n,sto,h)             Prosumage: storage level market to consumotion in hour h [MWh]
STO_L_M2M(n,sto,h)               Prosumage: storage level market to market in hour h [MWh]
N_STO_E_PRO(n,sto)               Prosumage: installed storage energy [MWh]
N_STO_P_PRO(n,sto)               Prosumage: installed storage power [MW]
STO_L_PRO(n,sto,h)               Prosumage: overall storage level in hour h [MWh]
N_RES_PRO(n,tech)                Prosumage: installed renewables capacities [MW]

NTC(l)                           Trade: installed NTC on line l [MW]

RSVR_OUT(n,rsvr,h)               Reservoirs: outflow in hour h [MWh]
RSVR_L(n,rsvr,h)                 Reservoirs: level in hour h [MWh]
N_RSVR_E(n,rsvr)                 Reservoirs: installed energy capacity [MWh]
N_RSVR_P(n,rsvr)                 Reservoirs: installed power capacity [MW]

H_DIR(n,bu,ch,h)                 Heating: direct heating in hour h for building type bu with haeting technology ch [MWh]
H_SETS_LEV(n,bu,ch,h)            Heating: storage level SETS technologies [MWh]
H_SETS_IN(n,bu,ch,h)             Heating: storage inflow SETS technologies [MWh]
H_SETS_OUT(n,bu,ch,h)            Heating: storage outflow SETS technologies [MWh]
H_HP_IN(n,bu,ch,hh)              Heating: electricity demand heat pump technologies [MWh]
H_STO_LEV(n,bu,ch,h)             Heating: storage level storage technologies [MWh]
H_STO_IN_HP(n,bu,ch,h)           Heating: storage inflow from heat pumps to storage technologies [MWh]
H_STO_IN_ELECTRIC(n,bu,ch,h)     Heating: storage inflow from electric heating to storage technologies [MWh]
H_ELECTRIC_IN(n,bu,ch,h)         Heating: hybrid electric heaters electricity demand [MWh]
H_STO_IN_FOSSIL(n,bu,ch,h)       Heating: storage inflow from nonelectric heating to storage technologies [MWh]
H_STO_OUT(n,bu,ch,h)             Heating: storage outflow from storage technologies [MWh]

H_DHW_DIR(n,bu,ch,h)             Heating - domestic hot water: provision in case of direct electric heating [MWh]
H_DHW_STO_OUT(n,bu,ch,h)         Heating - domestic hot water: DHW storage outflow [MWh]

H_DHW_AUX_ELEC_IN(n,bu,ch,h)     Heating - domestic hot water: electrical energy input of auxiliary hot water tank for SETS [MWh]
H_DHW_AUX_LEV(n,bu,ch,h)         Heating - domestic hot water: level of auxiliary hot water tank for SETS [MWh]
H_DHW_AUX_OUT(n,bu,ch,h)         Heating - domestic hot water: auxiliary DHW provision for SETS [MWh]

H2_N_PROD_CENT(n,h2_tech)                                       P2H2 - centralized electrolysis capacity (in terms of electricity inflow)
H2_N_PROD_DECENT(n,h2_tech)                                     P2H2 - decentralized electrolysis capacity (in terms of electricity inflow)
H2_E_H2_IN(n,h2_tech,h2_channel,h)                              P2H2 - electricity consumption for electrolysis (in terms of electricity inflow)
H2_PROD_OUT(n,h2_tech,h2_channel,h)                             P2H2 - H2 flow out after electrolysis (kWh in terms of the lower heating value (LHV) of H2) (= inflow for the next process)

H2_N_PROD_AUX(n,h2_tech,h2_channel)                             P2H2 - capacity to bring H2 into the right "form" for distribution after electrolysis
H2_PROD_AUX_IN(n,h2_tech,h2_channel,h)                          P2H2 - H2 flow in for this process (no losses modelled)
H2_PROD_AUX_OUT(n,h2_channel,h)                                 P2H2 - H2 flow out for this process (as no losses: identical to flow in) (= inflow for the next process)

H2_N_HYD_LIQ(n,h2_channel)                                      P2H2 - H2 hydration capacity (in terms of H2 flow)
H2_HYD_LIQ_OUT(n,h2_channel,h)                                  P2H2 - H2 hydration flow out (no losses modelled) (= inflow for the next process)

H2_N_STO(n,h2_channel)                                          P2H2 - H2 production site storage capacity (in terms of H2) (potential losses during storage)
H2_STO_P_OUT(n,h2_channel,h)                                    P2H2 - H2 production site storage flow out for each hour (in terms of H2 flow) (= inflow for the next process)
H2_STO_P_IN(n,h2_channel,h)                                     P2H2 - H2 production site storage flow in for each hour (in terms of H2 flow)
H2_STO_P_L(n,h2_channel,h)                                      P2H2 - H2 production site storage filling level for each hour (in terms of H2)
H2_STO_P_L0(n,h2_channel)                                       P2H2 - H2 production site storage initial fillin attributed (in terms of H2)

H2_N_AUX_PRETRANS(n,h2_channel)                                 P2H2 - capacity to bring H2 into the right "form" for transportation after storage
H2_AUX_PRETRANS_OUT(n,h2_channel,h)                             P2H2 - H2 flow out (no losses modelled) (= inflow for the next process)

H2_N_TRANS(n,h2_channel)                                        P2H2 - H2 transporation capacity (in terms of H2 flow)
H2_N_AVAI_TRANS(n,h2_channel,h)                                 P2H2 - H2 available transporation capacity (in terms of H2 flow)
H2_TRANS_OUT(n,h2_channel,h)                                    P2H2 - H2 transportation flow out (no losses modelled) (= inflow for the next process)

H2_AUX_BFLP_STO_OUT(n,h2_channel,h)                             P2H2 - auxiliary process before LP storage outflow
H2_N_AUX_BFLP_STO(n,h2_channel)                                 P2H2 - auxiliary process before LP storage capacity

H2_N_LP_STO(n,h2_channel)                                       P2H2 - LP storage capacity (in terms of H2) (potential losses during storage)
H2_LP_STO_OUT(n,h2_channel,h)                                   P2H2 - LP storge out (no losses modelled) (= inflow for the next process) (in terms of H2 flow)
H2_LP_STO_L(n,h2_channel,h)                                     P2H2 - LP storage filling level for each hour (in terms of H2)
H2_LP_STO_L0(n,h2_channel)                                      P2H2 - LP storage initial filling attributed (in terms of H2)
H2_AUX_BFLP_STO_IN(n,h2_channel,h)                              P2H2 - auxiliary process before LP storge inflow (no losses modelled) (= inflow for the next process) (in terms of H2 flow)

H2_N_DEHYD_EVAP(n,h2_channel)                                   P2H2 - H2 dehydration capacity (in terms of H2 flow)
H2_DEHYD_EVAP_OUT(n,h2_channel,h)                               P2H2 - H2 dehydration flow out (no losses modelled) (= inflow for the next process)

H2_AUX_BFMP_STO_OUT(n,h2_channel,h)                             P2H2 - auxiliary process before MP storage outflow
H2_N_AUX_BFMP_STO(n,h2_channel)                                 P2H2 - auxiliary process before MP storage capacity

H2_N_MP_STO(n,h2_channel)                                       P2H2 - MP storage capacity (in terms of H2) (potential losses during storage)
H2_MP_STO_L(n,h2_channel,h)                                     P2H2 - MP storage filling level for each hour (in terms of H2)
H2_MP_STO_L0(n,h2_channel)                                      P2H2 - MP storage initial filling attributed (in terms of H2)
H2_MP_STO_OUT(n,h2_channel,h)                                   P2H2 - MP storge out (no losses modelled) (= inflow for the next process) (in terms of H2 flow)

H2_N_AUX_BFHP_STO(n,h2_channel)                                 P2H2 - auxiliary process before HP storage outflow
H2_AUX_BFHP_STO_OUT(n,h2_channel,h)                             P2H2 - auxiliary process before HP storage capacity
H2_AUX_BFHP_STO_IN(n,h2_channel,h)                              P2H2 - auxiliary process before HP storge inflow (no losses modelled) (= inflow for the next process) (in terms of H2 flow)

H2_N_HP_STO(n,h2_channel)                                       P2H2 - HP storage capacity (in terms of H2) (potential losses during storage)
H2_HP_STO_OUT(n,h2_channel,h)                                   P2H2 - HP storage flow out for each hour (in terms of H2 flow)
H2_HP_STO_L(n,h2_channel,h)                                     P2H2 - HP storage filling level for each hour (in terms of H2)
H2_HP_STO_L0(n,h2_channel)                                      P2H2 - HP storage part of initial filling attributed to a channel (in terms of H2)

H2_AUX_BFFUEL_OUT(n,h2_channel,h)                               P2H2 - auxiliary process before fueling outflow
H2_N_AUX_BFFUEL(n,h2_channel)                                   P2H2 - auxiliary process before fueling capacity

H2_BYPASS_1(n,h2_tech,h2_channel,h)                             P2H2 - bypass flow from production sites to auxiliary process before transportation
H2_BYPASS_2(n,h2_channel,h)                                     P2H2 - bypass flow from unloading to auxiliary process before HP storage

H2_N_RECON_AUX(n,h2_channel,h2_tech_recon)                      P2H2 - capacity to bring H2 into the right "form" for reconversion
H2_RECON_AUX_OUT(n,h2_channel,h2_tech_recon,h)                  P2H2 - H2 flow in for this process (no losses modelled)

H2_N_RECON(n,h2_tech_recon)                                     P2H2 - re-conversion capacity (in terms of H2 inflow)
H2_E_RECON_OUT(n,h2_channel,h2_tech_recon,h)                    P2H2 - electricity generation at re-conversion (in terms of electricity outflow)

H2_CHANNEL_SHARE(n,h2_channel)                                  P2H2 - share of filling stations supplied by either channel (only one channel per filling station allowed)
;

********************************************************************************

Equations
* Objective
obj                                                         Objective cost minimization

* Energy balance
con1a_bal(n,h)                                              Energy Balance

* Load change costs
con2a_loadlevel(n,tech,h)                                   Load change costs: Level
con2b_loadlevelstart(n,tech,h)                              Load change costs: Level for first period

* Capacity contraints and flexibility constraints
con3a_maxprod_dispatchable(n,tech,h)                        Capacity Constraint conventionals
con3b_minprod_dispatchable(n,tech,h)                        Minimum production conventionals if reserves contracted
con3c_flex_reserves_spin(n,tech,reserves,h)                 Flexibility of conventionals for reserves provision
con3d_flex_reserves_nonspin(n,tech,reserves,h)              Flexibility of conventionals for reserves provision
con3e_maxprod_res(n,tech,h)                                 Capacity constraints renewables
con3f_minprod_res(n,tech,h)                                 Minimum production RES if reserves contracted

* Storage constraints
con4a_stolev_start(n,sto,h)                                 Storage Level Dynamics Initial Condition
con4b_stolev(n,sto,h)                                       Storage Level Dynamics
con4c_stolev_max(n,sto,h)                                   Storage Power Capacity
con4d_maxin_sto(n,sto,h)                                    Storage maximum inflow
con4e_maxout_sto(n,sto,h)                                   Storage maximum outflow
con4f_resrv_sto(n,sto,h)                                    Constraint on reserves (up)
con4g_resrv_sto(n,sto,h)                                    Constraint on reserves (down)
con4h_maxout_lev(n,sto,h)                                   Maximum storage outflow - no more than level of last period
con4i_maxin_lev(n,sto,h)                                    Maximum storage inflow - no more than ebergy capacity minus level of last period
con4j_ending(n,sto,h)                                       End level equal to initial level
con4k_PHS_EtoP(n,sto)                                       Maximum E to P ratio for PHS

* Minimum restrictions for renewables and biomass
con5a_minRES(n)                                             Minimum yearly renewables requirement
con5b_max_energy(n,tech)                                    Maximum yearly biomass energy

* DSM conditions: Load curtailment
con6a_DSMcurt_duration_max(n,dsm,h)                         Maximum curtailment energy budget per time
con6b_DSMcurt_max(n,dsm,h)                                  Maximum curtailment per period

* DSM conditions: Load shifting
con7a_DSMshift_upanddown(n,dsm,h)                           Equalization of upshifts and downshifts in due time
con7b_DSMshift_granular_max(n,dsm,h)                        Maximum shifting in either direction per period
con7c_DSM_distrib_up(n,dsm,h)                               Distribution of upshifts between wholesale and reserves
con7d_DSM_distrib_do(n,dsm,h)                               Distribution of downshifts between wholesale and reserves
con7e_DSMshift_recovery(n,dsm,h)                            Recovery times

* Maximum installation conditions
con8a_max_I_power(n,tech)                                   Maximum installable capacities: electricity generation
con8b_max_I_sto_e(n,sto)                                    Maximum installable capacities: storage energy
con8c_max_I_sto_p_in(n,sto)                                 Maximum installable capacities: storage power charging
con8d_max_I_sto_p_out(n,sto)                                Maximum installable capacities: storage power discharging
con8e_max_I_dsm_cu(n,dsm)                                   Maximum installable capacities: DSM curtailment
con8f_max_I_dsm_shift_pos(n,dsm)                            Maximum installable capacities: DSM shifting
con8g_max_pro_res(n,tech)                                   Maximum installable capacities: renewables prosumagers
con8h_max_pro_sto_e(n,sto)                                  Maximum installable capacities: storage energy prosumagers
con8i_max_sto_pro_p(n,sto)                                  Maximum installable capacities: storage power prosumagers
con8j_max_I_ntc(l)                                          Maximum installable capacities: NTC             
con8k_max_I_rsvr_e(n,rsvr)                                  Maximum installable capacities: reservoir energy
con8l_max_I_rsvr_p_out(n,rsvr)                              Maximum installable capacities: reservoir power out

* Reserves
con9a_reserve_prov_endogenous(n,reserves,h)                 Reserve provision SR and MR (endogenous reserve provision)
con9a_reserve_prov_exogenous(n,reserves,h)                  Reserve provision SR and MR (exogenous reserve provision)
con9b_reserve_prov_PR_endogenous(n,reserves,h)              Reserve provision PR (endogenous reserve provision)
con9b_reserve_prov_PR_exogenous(n,reserves,h)               Reserve provision PR (exogenous reserve provision)

* Electric vehicles
con10a_ev_ed(n,ev,h)                                        Energy balance of electric vehicles
con10b_ev_chargelev_start(ev,h,n)                           Cumulative charging level in the first hour
con10c_ev_chargelev(ev,h,n)                                 Cumulative charging level in hour h
con10d_ev_chargelev_max(n,ev,h)                             Cumulative maximal charging level
con10e_ev_maxin(n,ev,h)                                     Cumulative maximal charging power
con10f_ev_maxout(n,ev,h)                                    Cumulative maximal discharging power
con10g_ev_chargelev_ending(n,ev,h)                          Cumulative charging level in the last hour
con10h_ev_minin(n,ev,h)                                     Cumulative minimal charging power
con10i_ev_maxin_lev(n,ev,h)                                 Cumulative maximal charging limit
con10j_ev_minout(n,ev,h)                                    Cumulative minimal discharging power
con10k_ev_maxout_lev(n,ev,h)                                Cumulative maximal discharging limit
con10l_ev_exog(n,ev,h)                                      Exogenous EV charging

* Prosumage
con11a_pro_distrib(n,tech,h)                                Prosumage: distribution of generated energy
con11b_pro_balance(n,h)                                     Prosumage: energy balance
con11c_pro_selfcon(n)                                       Prosumage: minimum self-generation requirement
con11d_pro_stolev_PRO2PRO(n,sto,h)                          Prosumage: storage level prosumager-to-prosumagers
con11e_pro_stolev_PRO2M(n,sto,h)                            Prosumage: storage level prosumagers-to-market
con11f_pro_stolev_M2PRO(n,sto,h)                            Prosumage: storage level market-to-prosumagers
con11g_pro_stolev_M2M(n,sto,h)                              Prosumage: storage level market-to-market
con11h_1_pro_stolev_start_PRO2PRO(n,sto,h)                  Prosumage: storage level initial conditions
con11h_2_pro_stolev_start_PRO2M(n,sto,h)                    Prosumage: storage level initial conditions
con11h_3_pro_stolev_start_M2PRO(n,sto,h)                    Prosumage: storage level initial conditions
con11h_4_pro_stolev_start_M2M(n,sto,h)                      Prosumage: storage level initial conditions
con11i_pro_stolev(n,sto,h)                                  Prosumage: storage level total
con11j_pro_stolev_max(n,sto,h)                              Prosumage: maximum overall storage level
con11k_pro_maxin_sto(n,sto,h)                               Prosumage: maximum storage inflow
con11l_pro_maxout_sto(n,sto,h)                              Prosumage: maximum storage outflow
con11m_pro_maxout_lev(n,sto,h)                              Prosumage: maximum storage outflow linked to level
con11n_pro_maxin_lev(n,sto,h)                               Prosumage: maximum storage inflow linked to level
con11o_pro_ending(n,sto,h)                                  Prosumage: storage ending condition

* Cross-nodal trade
con12a_max_f(l,h)                                           Maximum energy flow limited to positive NTC
con12b_min_f(l,h)                                           Minimum energy flow limited to negative NTC

* Resevoirs
con13a_rsvrlev_start(n,rsvr,h)                              Reservoir level law of motion initial condition
con13b_rsvrlev(rsvr,h,n)                                    Reservoir level law of motion
con13c_rsvrlev_max(n,rsvr,h)                                Maximum reservoir energy level
con13d_maxout_rsvr(rsvr,h,n)                                Maximum hourly reservoir outflow in relation to installed power capacity
con13e_resrv_rsvr(n,rsvr,h)                                 Minimum hourly reservoir outflow in relation to provided negativr reserves
con13f_maxout_lev(n,rsvr,h)                                 Maximum hourly reservoir outflow in relation tom installed energy capacity
con13g_ending(n,rsvr,h)                                     Reservoir level law of motion ending condition
* con13h_smooth(n,rsvr,h)                                     Smooth reservoir outflow
con13i_min_level(n,rsvr,h)                                  Reservoir minimum level
con13j_min_FLH(n,rsvr)

* Residential heat
con14a_heat_balance(n,bu,ch,h)                              Space heating energy balance
con14b_dhw_balance(n,bu,ch,h)                               Domestic hot water energy balance
con14c_sets_level(n,bu,ch,h)                                SETS - level law of motion
con14d_sets_level_start(n,bu,ch,h)                          SETS - storage level initial condition
con14e_sets_maxin(n,bu,ch,h)                                SETS - maximum energy inflow
con14f_sets_maxout(n,bu,ch,h)                               SETS - maximum energy outflow
con14g_sets_minin(n,bu,ch,h)                                SETS - minimum energy inflow if reserves contracted
con14h_sets_maxlev(n,bu,ch,h)                               SETS - maximum storage level
con14i_sets_aux_dhw_level(n,bu,ch,h)                        SETS auxiliary DHW module - storage level law of motion
con14j_sets_aux_dhw_level_start(n,bu,ch,h)                  SETS auxiliary DHW module - storage level initial consition
con14k_sets_aux_dhw_maxin(n,bu,ch,h)                        SETS auxiliary DHW module - maximum energy inflow
con14l_sets_aux_dhw_minin(n,bu,ch,h)                        SETS auxiliary DHW module - minimum energy inflow if reserves contracted
con14m_sets_aux_dhw_maxlev(n,bu,ch,h)                       SETS auxiliary DHW module - maximum storage level
con14n_hp_in(n,bu,ch,h)                                     Heat pumps - electricity demand
con14o_hp_maxin(n,bu,ch,h)                                  Heat pumps - maximum electricity demand
con14p_hp_minin(n,bu,ch,h)                                  Heat pumps - minimum electricity demand if reserves contracted
con14q_storage_elec_in(n,bu,ch,h)                           Hybrid electric heating - electricity demand
con14r_storage_elec_maxin(n,bu,ch,h)                        Hybrid electric heating - maximum electricity demand
con14s_storage_elec_minin(n,bu,ch,h)                        Hybrid electric heating - minimum electricity demand if reserves contracted
con14t_storage_level(n,bu,ch,h)                             Storage heating - level law of motion
con14u_storage_level_start(n,bu,ch,h)                       Hybrid electric heating - storage level initial condition
con14v_storage_maxlev(n,bu,ch,h)                            Hybrid electric heating - maximum storage level

* P2H2

* Electrolysis_Centers
h2_con2a(n,h2_tech,h2_tech_recon,h)                         Capacity of centralised electrolysis
h2_con2b(n,h2_tech,h)                                       Capacity of decentralised electrolysis
h2_con3(n,h2_tech,h2_channel,h)                             Hydrogen outflow from electrolysis (Bypass1)

* aux_prod_site
h2_con4(n,h2_tech,h2_channel,h)                             Production auxiliaries capacity
h2_con5(n,h2_tech,h2_channel,h)                             Electrolysis Hydrogen outflow bypassed
h2_con6(n,h2_channel,h)                                     Production aixiliaries hydrogen outflow

* hydration_liquefaction
h2_con7(n,h2_channel,h)                                     Hydrogenation and liquefaction outflow
h2_con8(n,h2_channel,h)                                     Hydrogenation and liquefaction Capacity

* prod_site_storage
h2_con9(n,h2_channel,h)                                     Hydrogen inflow of the storage at productione sites
h2_con10(n,h2_channel,h)                                    Capacity of the storage at production sites
h2_con11a(n,h2_channel,h)                                   Filling level of the storage at production sites
h2_con11b(n,h2_channel,h)                                   Initial filling level of the storage at production sites
h2_con11c(n,h2_channel)                                     Minimum of initial filling level of the storage at production sites
h2_con11d(n,h2_channel,h)                                   Initial filling level of the storage at production sites equal to that of the last one
h2_con11e(n,h2_channel,h)                                   Minimum of filling level of the storage at production sites

* aux_bftrans
h2_con12(n,h2_channel,h)                                    Outflow of the auxiliary process before transportation (bypass 1)
h2_con13(n,h2_channel,h)                                    Capacity of the auxiliary process before transportation
h2_con13b(n,h2_channel,h)                                   Capacity of filling stations for handling hydrogen outflow of the auxiliary process before transportation

* transportation
h2_con14a(n,h2_channel,h)                                   Hydrogen outflow of transportation (simplified form)
h2_con14b(n,h2_channel,h)                                   Capacity of transportation (simplified form)
h2_con14c(n,h2_channel,h)                                   Hydrogen outflow of transportation (time-consuming form) (delivery in the same year)

h2_con15a(n,h2_channel,h)                                   Hydrogen outflow of transportation (time-consuming form)
h2_con15b(n,h2_channel,h)                                   Hydrogen outflow of transportation (re-conversion channel)
h2_con114(n,h2_channel,h)                                   Available capacity of transportation (time-consuming form)
h2_con115(n,h2_channel,h)                                   Total capacity of transportation (time-consuming form)

* aux_bflp_storage
h2_con_1(n,h2_channel,h)                                    Hydrogen outflow of the auxiliary process before LP storage
h2_con_2(n,h2_channel,h)                                    Capacity of the auxiliary process before LP storage
h2_con17e(n,h2_channel,h)                                   Hydrogen inflow of the auxiliary process before LP storage (bypass 2)

* LP_storage
h2_con16a(n,h2_channel,h)                                   Capacity of the LP storage
h2_con16b(n,h2_channel,h)                                   Upper bound of the capacity of the LP storage (filling stations)
h2_con16c(n,h2_channel,h)                                   Upper bound of the capacity of the LP storage (re-conversion channel)
h2_con17a(n,h2_channel,h)                                   Filling level of the LP storage
h2_con17b(n,h2_channel,h)                                   Initial filling level of the LP storage
h2_con17c(n,h2_channel)                                     Minimum of initial filling level of the LP storage
h2_con17d(n,h2_channel,h)                                   Initial filling level of the LP storage equal to that of the last one
h2_con17g(n,h2_channel,h)                                   Minimum of filling level of the LP storage

* dehydration_evaporation
h2_con18(n,h2_channel,h)                                    Outflow of dehydration and evaporation
h2_con19(n,h2_channel,h)                                    Capacity of dehydration and evaporation

* aux_bfMP_storage
h2_con_7(n,h2_channel,h)                                    Outflow of  the auxiliary process before MP storage
h2_con_8(n,h2_channel,h)                                    Capacity of the auxiliary process before MP storage

* MP_storage
h2_con_3(n,h2_channel,h)                                    Capacity of the MP storage
h2_con_4a(n,h2_channel,h)                                   Filling level of the MP storage
h2_con_4b(n,h2_channel,h)                                   Initial filling level of the MP storage
h2_con_4c(n,h2_channel)                                     Minimum of initial filling level of the LP storage
h2_con_4d(n,h2_channel,h)                                   Initial filling level of the MP storage equal to that of the last one
h2_con_4e(n,h2_channel,h)                                   Minimum of filling level of the MP storage
h2_con_4f(n,h2_channel,h)                                   Upper bound of the capacity of the MP storage (filling stations)
h2_con_4g(n,h2_channel,h)                                   Upper bound of the capacity of the MP storage (re-conversion channel)


* aux_bfhp_storage
h2_con21(n,h2_channel,h)                                    Hydrogen outflow of the auxiliary process before HP storage
h2_con21b(n,h2_channel,h)                                   Hydrogen inflow of the auxiliary process before HP storage (bypass 2)
h2_con22(n,h2_channel,h)                                    Capacity of the auxiliary process before HP storage

* hp_storage
h2_con24(n,h2_channel,h)                                    Capacity of the HP storage
h2_con25a(n,h2_channel,h)                                   Filling level of the HP storage
h2_con25b(n,h2_channel,h)                                   Initial filling level of the HP storage
h2_con25c(n,h2_channel,h)                                   Initial filling level of the HP storage equal to that of the last one
h2_con25d(n,h2_channel,h)                                   Min. of filling level of the HP storage
h2_con25e(n,h2_channel,h)                                   Upper bound of the capacity of the HP storage (filling stations)
h2_con25f(n,h2_channel,h)                                   Upper bound of the capacity of the HP storage (re-conversion channel)

* aux_bffuel
h2_con_5(n,h2_channel,h)                                    Outflow of the auxiliary process before fueling
h2_con_6(n,h2_channel,h)                                    Capacity of the auxiliary process before MP storage

* matching demand and supply
h2_con28a(n,h,h2_channel)                                   Demand of the filling stations for hydrogen
h2_con28b(n)                                                Sum of shares of all channels
h2_con29(n,h,h2_channel)                                    Demand matching for p2x other than H2

* aux_recon_site
h2_con31(n,h2_channel,h2_tech_recon,h)                      Capacity of the auxliary process  before re-conversion
h2_con32(n,h2_channel,h)                                    Distribution of the outflow of the auxiliary process before re-conversion

* recon
h2_con33(n,h2_tech_recon,h)                                 Capacity of the re-conversion process
h2_con34(n,h2_channel,h2_tech_recon,h)                      Electricity generation of the re-conversion process

%DIETERgms%$include "%MODELDIR%dieterpy_3_definenewconstr.gms"

;

********************************************************************************

* ---------------------------------------------------------------------------- *
***** Objective function *****
* ---------------------------------------------------------------------------- *

obj..
         Z =E=
                   sum( (h,map_n_tech(n,dis)) , c_m(n,dis)*G_L(n,dis,h) )
                 + sum( (h,map_n_tech(n,dis))$(ord(h)>1) , c_up(n,dis)*G_UP(n,dis,h) )
                 + sum( (h,map_n_tech(n,dis))$(ord(h)>1) , c_do(n,dis)*G_DO(n,dis,h) )
                 + sum( (h,map_n_tech(n,nondis)) , c_cu(n,nondis)*CU(n,nondis,h) + c_vom(n,nondis)*G_RES(n,nondis,h) )
                 + sum( (h,map_n_sto(n,sto)) , c_m_sto_in(n,sto) * STO_IN(n,sto,h) + c_m_sto_out(n,sto) * STO_OUT(n,sto,h) )
%DSM%$ontext
                 + sum( (h,map_n_dsm(n,dsm_curt)) , c_m_dsm_cu(n,dsm_curt)*DSM_CU(n,dsm_curt,h) )
                 + sum( (h,map_n_dsm(n,dsm_shift)) , c_m_dsm_shift(n,dsm_shift) * DSM_UP_DEMAND(n,dsm_shift,h) )
                 + sum( (h,map_n_dsm(n,dsm_shift)) , c_m_dsm_shift(n,dsm_shift) * DSM_DO_DEMAND(n,dsm_shift,h) )
$ontext
$offtext
%EV%$ontext
                 + sum( (h,map_n_ev(n,ev)) , c_m_ev_cha(n,ev) * EV_CHARGE(n,ev,h) )
                 + sum( (h,map_n_ev(n,ev)) , c_m_ev_dis(n,ev) * EV_DISCHARGE(n,ev,h) )
                 + sum( (h,map_n_ev(n,ev)) , pen_phevfuel(n,ev) * EV_PHEVFUEL(n,ev,h) )
$ontext
$offtext
                 + sum( map_n_tech(n,tech) , c_i(n,tech)*N_TECH(n,tech) )
                 + sum( map_n_tech(n,tech) , c_fix(n,tech)*N_TECH(n,tech) )
                 + sum( map_n_sto(n,sto) , c_i_sto_e(n,sto)*N_STO_E(n,sto) + c_i_sto_p_in(n,sto)*N_STO_P_IN(n,sto) + c_i_sto_p_out(n,sto)*N_STO_P_OUT(n,sto) )
                 + sum( map_n_sto(n,sto) , c_fix_sto_p_in(n,sto)*N_STO_P_IN(n,sto) + c_fix_sto_p_out(n,sto)*N_STO_P_OUT(n,sto) + c_fix_sto_e(n,sto)*N_STO_E(n,sto) )
%DSM%$ontext
                 + sum( map_n_dsm(n,dsm_curt) , c_i_dsm_cu(n,dsm_curt)*N_DSM_CU(n,dsm_curt) )
                 + sum( map_n_dsm(n,dsm_curt) , c_fix_dsm_cu(n,dsm_curt)*N_DSM_CU(n,dsm_curt) )
                 + sum( map_n_dsm(n,dsm_shift) , c_i_dsm_shift(n,dsm_shift)*N_DSM_SHIFT(n,dsm_shift) )
                 + sum( map_n_dsm(n,dsm_shift) , c_fix_dsm_shift(n,dsm_shift)*N_DSM_SHIFT(n,dsm_shift) )
$ontext
$offtext
%reserves%$ontext
                 + sum( (h,map_n_sto(n,sto),reserves_up) , phi_reserves_call(n,reserves_up,h) * c_m_sto_out(n,sto) * RP_STO_OUT(n,reserves_up,sto,h) )
                 - sum( (h,map_n_sto(n,sto),reserves_up) , phi_reserves_call(n,reserves_up,h) * c_m_sto_in(n,sto) * RP_STO_IN(n,reserves_up,sto,h) )
                 - sum( (h,map_n_sto(n,sto),reserves_do) , phi_reserves_call(n,reserves_do,h) * c_m_sto_out(n,sto) * RP_STO_OUT(n,reserves_do,sto,h) )
                 + sum( (h,map_n_sto(n,sto),reserves_do) , phi_reserves_call(n,reserves_do,h) * c_m_sto_in(n,sto) * RP_STO_IN(n,reserves_do,sto,h) )
                 + sum( (h,map_n_rsvr(n,rsvr),reserves_up) , RP_RSVR(n,reserves_up,rsvr,h) * phi_reserves_call(n,reserves_up,h) * c_m_rsvr(n,rsvr) )
                 - sum( (h,map_n_rsvr(n,rsvr),reserves_do) , RP_RSVR(n,reserves_do,rsvr,h) * phi_reserves_call(n,reserves_do,h) * c_m_rsvr(n,rsvr) )
$ontext
$offtext
%reserves%$ontext
%EV%$ontext
%EV_EXOG%        + sum( (h,map_n_ev(n,ev),reserves_up) , RP_EV_V2G(n,reserves_up,ev,h) * phi_reserves_call(n,reserves_up,h) * c_m_ev_dis(n,ev) )
%EV_EXOG%        - sum( (h,map_n_ev(n,ev),reserves_do) , RP_EV_V2G(n,reserves_do,ev,h) * phi_reserves_call(n,reserves_do,h) * c_m_ev_cha(n,ev) )
$ontext
$offtext
%DSM%$ontext
%reserves%$ontext
                 + sum( (h,map_n_dsm(n,dsm_curt),reserves_up) , RP_DSM_CU(n,reserves_up,dsm_curt,h) * phi_reserves_call(n,reserves_up,h) * c_m_dsm_cu(n,dsm_curt) )
                 + sum( (h,map_n_dsm(n,dsm_shift),reserves) , RP_DSM_SHIFT(n,reserves,dsm_shift,h) * phi_reserves_call(n,reserves,h) * c_m_dsm_shift(n,dsm_shift) )
$ontext
$offtext
%prosumage%$ontext
                 + sum( map_n_res_pro(n,res) , c_i(n,res)*N_RES_PRO(n,res) )
                 + sum( map_n_res_pro(n,res) , c_fix(n,res)*N_RES_PRO(n,res) )

                 + sum( map_n_sto_pro(n,sto) , c_i_sto_e(n,sto)*N_STO_E_PRO(n,sto) )
                 + sum( map_n_sto_pro(n,sto) , c_fix_sto_p_in(n,sto)*N_STO_P_PRO(n,sto) + c_fix_sto_e(n,sto) * N_STO_E_PRO(n,sto) )
                 + sum( map_n_sto_pro(n,sto) , c_i_sto_p_in(n,sto)*N_STO_P_PRO(n,sto) )

                 + sum( (h,map_n_sto_pro(n,sto)) , c_m_sto_out(n,sto) * ( STO_OUT_PRO2PRO(n,sto,h) + STO_OUT_M2PRO(n,sto,h) + STO_OUT_PRO2M(n,sto,h) + STO_OUT_M2M(n,sto,h)) + c_m_sto_in(n,sto) * ( sum( res , STO_IN_PRO2PRO(n,res,sto,h) + STO_IN_PRO2M(n,res,sto,h)) + STO_IN_M2PRO(n,sto,h) + STO_IN_M2M(n,sto,h) ) )
$ontext
$offtext
                 + sum( map_l(l) , (c_i_ntc(l) + c_fix_ntc(l)) * NTC(l) )
                 + sum( (h,map_l(l)) , c_m_ntc(l) * F(l,h) )

                 + sum( (h,map_n_rsvr(n,rsvr)), c_m_rsvr(n,rsvr) * RSVR_OUT(n,rsvr,h) )
                 + sum( map_n_rsvr(n,rsvr) , c_i_rsvr_e(n,rsvr) * N_RSVR_E(n,rsvr) + c_i_rsvr_p_out(n,rsvr) * N_RSVR_P(n,rsvr) )
                 + sum( map_n_rsvr(n,rsvr) , c_fix_rsvr_p_out(n,rsvr) * N_RSVR_P(n,rsvr) + c_fix_rsvr_e(n,rsvr) * N_RSVR_E(n,rsvr) )
%heat%$ontext
                 + sum( (h,n,bu,hfo) , pen_heat_fuel(n,bu,hfo) * H_STO_IN_FOSSIL(n,bu,hfo,h))
$ontext
$offtext
                 + sum( (h,n) , c_infes * G_INFES(n,h) )
%heat%$ontext
                 + sum( (n,bu,ch,h) , c_h_infes * H_INFES(n,bu,ch,h) )
                 + sum( (n,bu,ch,h) , c_h_dhw_infes * H_DHW_INFES(n,bu,ch,h) )
$ontext
$offtext

%P2H2%$ontext

* prod
                 + sum( (n,h2_tech) , ( h2_prod_c_ad_a_overnight(n,h2_tech) + h2_prod_c_ad_a_fix(n,h2_tech) + h2_prod_c_ad_a_fix2(n,h2_tech) ) * H2_N_PROD_CENT(n,h2_tech) )
                 + sum( (n,h2_tech) , ( h2_prod_c_a_overnight(n,h2_tech) + h2_prod_c_a_fix(n,h2_tech) + h2_prod_c_a_fix2(n,h2_tech) ) * H2_N_PROD_DECENT(n,h2_tech) )
* aux_prod_site
                 + sum( (n,h2_tech,h2_channel) , h2_prod_aux_sw(n,h2_tech,h2_channel) * h2_prod_aux_c_a_overnight(n,h2_tech,h2_channel) * H2_N_PROD_AUX(n,h2_tech,h2_channel) )
* hydration_liquefaction
                 + sum( (n,h2_channel) , h2_hyd_liq_sw(n,h2_channel) * h2_hyd_liq_c_a_overnight(n,h2_channel) * H2_N_HYD_LIQ(n,h2_channel) )
                 + sum( (n,h2_channel,h) , h2_hyd_liq_sw(n,h2_channel) * H2_PROD_AUX_OUT(n,h2_channel,h) * h2_hyd_liq_c_vom(n,h2_channel) )
* prod_site_storage
                 + sum( (n,h2_channel) , h2_sto_p_sw(n,h2_channel) * h2_sto_p_c_a_overnight(n,h2_channel) * H2_N_STO(n,h2_channel) )
* aux_bftrans
                 + sum ( (n,h2_channel) , h2_aux_pretrans_sw(n,h2_channel) * h2_aux_pretrans_c_a_overnight(n,h2_channel) * H2_N_AUX_PRETRANS(n,h2_channel) )
* transportation
                 + sum ( (n,h2_channel) , h2_trans_sw(n,h2_channel) * h2_trans_c_a_overnight(n,h2_channel) * H2_N_TRANS(n,h2_channel) )
                 + sum ( (n,h2_channel,h) , h2_trans_sw(n,h2_channel) * h2_trans_c_var(n,h2_channel) * H2_AUX_PRETRANS_OUT(n,h2_channel,h) * h2_trans_dist(n,h2_channel))

* aux_bflp_storage
                 + sum( (n,h2_channel) , h2_aux_bflp_sto_sw(n,h2_channel) * h2_aux_bflp_sto_c_a_overnight(n,h2_channel) * H2_N_AUX_BFLP_STO(n,h2_channel) )

* lp_storage
                 + sum ( (n,h2_channel) , h2_lp_sto_sw(n,h2_channel) * h2_lp_sto_c_a_overnight(n,h2_channel) * H2_N_LP_STO(n,h2_channel) )
* dehydration_evaporation
                 + sum ( (n,h2_channel) , h2_dehyd_evap_sw(n,h2_channel) * h2_dehyd_evap_c_a_overnight(n,h2_channel) * H2_N_DEHYD_EVAP(n,h2_channel) )
                 + sum ( (n,h2_channel,h) , h2_dehyd_evap_sw(n,h2_channel) * h2_dehyd_evap_gas_sw(n,h2_channel) * h2_dehyd_evap_gas(n,h2_channel) * h2_c_gas(n) * H2_LP_STO_OUT(n,h2_channel,h) )
                 + sum ( (n,h2_channel,h) , h2_dehyd_evap_sw(n,h2_channel) * h2_dehyd_evap_gas_sw(n,h2_channel) * h2_dehyd_evap_gas(n,h2_channel) * H2_LP_STO_OUT(n,h2_channel,h) * 0.001 * carbon_content(n,'CCGT') * CO2price(n,'CCGT') )

* aux_bfMP_storage
                 + sum( (n,h2_channel) , h2_aux_bfMP_sto_sw(n,h2_channel) * h2_aux_bfMP_sto_c_a_overnight(n,h2_channel) * H2_N_AUX_BFMP_STO(n,h2_channel) )


* MP_storage
                 + sum( (n,h2_channel) , h2_MP_sto_sw(n,h2_channel) * h2_MP_sto_c_a_overnight(n,h2_channel) * H2_N_MP_STO(n,h2_channel) )

* aux_bffilling_storage
                 + sum ( (n,h2_channel) ,  h2_aux_bfhp_sto_sw(n,h2_channel) * aux_bfhp_sto_c_a_overnight(n,h2_channel) * H2_N_AUX_BFHP_STO(n,h2_channel) )
* filling_storage
                 + sum ( (n,h2_channel) , h2_hp_sto_sw(n,h2_channel) * h2_hp_sto_c_a_overnight(n,h2_channel) * H2_N_HP_STO(n,h2_channel) )

* aux_bffuel_storage
                 + sum( (n,h2_channel) , h2_aux_bffuel_sw(n,h2_channel) * h2_aux_bffuel_c_a_overnight(n,h2_channel) * H2_N_AUX_BFFUEL(n,h2_channel) )

* aux_recon_site
                 + sum ( (n,h2_channel,h2_tech_recon) , h2_recon_aux_sw(n,h2_channel,h2_tech_recon) * h2_recon_aux_c_a_overnight(n,h2_channel,h2_tech_recon) * H2_N_RECON_AUX(n,h2_channel,h2_tech_recon) )
* recon
                 + sum ( (n,h2_tech_recon) ,  h2_recon_c_a_overnight(n,h2_tech_recon) * H2_N_RECON(n,h2_tech_recon) )
                 + sum ( (n,h2_channel,h2_tech_recon,h) , H2_RECON_AUX_OUT(n,h2_channel,h2_tech_recon,h) * h2_recon_c_vom(n,h2_tech_recon) )

$ontext
$offtext

;

* ---------------------------------------------------------------------------- *
***** Energy balance and load levels *****
* ---------------------------------------------------------------------------- *

* Energy balance
con1a_bal(n,hh)..
         ( 1 - phi_pro_load(n) ) * d(n,hh) + sum( map_n_sto(n,sto) , STO_IN(n,sto,hh) )
%DSM%$ontext
         + sum( map_n_dsm(n,dsm_shift) , DSM_UP_DEMAND(n,dsm_shift,hh) )
$ontext
$offtext
%EV%$ontext
         + sum( map_n_ev(n,ev) , EV_CHARGE(n,ev,hh) )
$ontext
$offtext
%prosumage%$ontext
         + G_MARKET_M2PRO(n,hh)
         + sum( map_n_sto_pro(n,sto) , STO_IN_M2PRO(n,sto,hh))
         + sum( map_n_sto_pro(n,sto) , STO_IN_M2M(n,sto,hh))
$ontext
$offtext
%heat%$ontext
        + sum( (bu,ch) , theta_dir(n,bu,ch) * (H_DIR(n,bu,ch,hh) + H_DHW_DIR(n,bu,ch,hh)) )
        + sum( (bu,ch) , theta_sets(n,bu,ch) * (H_SETS_IN(n,bu,ch,hh) + H_DHW_AUX_ELEC_IN(n,bu,ch,hh)) )
        + sum( (bu,hp) , theta_hp(n,bu,hp) * H_HP_IN(n,bu,hp,hh) )
        + sum( (bu,hel) , theta_elec(n,bu,hel) * H_ELECTRIC_IN(n,bu,hel,hh) )
$ontext
$offtext


%P2H2%$ontext
* 0.001 to convert kWh electricity demand into MWh demand.
      + 0.001 * (
* prod
                 sum( (h2_tech,h2_channel) , H2_E_H2_IN(n,h2_tech,h2_channel,hh) )
* aux_prod_site
                 + sum( (h2_tech,h2_channel) , h2_prod_aux_sw(n,h2_tech,h2_channel) * h2_prod_aux_ed(n,h2_tech,h2_channel) * H2_PROD_AUX_IN(n,h2_tech,h2_channel,hh) )
* hydration_liquefaction
                 + sum ( h2_channel , h2_hyd_liq_sw(n,h2_channel) * h2_hyd_liq_ed(n,h2_channel) * H2_PROD_AUX_OUT(n,h2_channel,hh) )
* prod_site_storage
                 + sum ( h2_channel , h2_sto_p_sw(n,h2_channel) * H2_STO_P_L(n,h2_channel,hh) * h2_sto_p_ed(n,h2_channel) )
* aux_bftrans
                 + sum ( h2_channel, h2_aux_pretrans_sw(n,h2_channel) * h2_aux_pretrans_ed(n,h2_channel) * (sum(h2_tech,h2_bypass_1_sw(n,h2_tech,h2_channel) * H2_BYPASS_1(n,h2_tech,h2_channel,hh)) + H2_STO_P_OUT(n,h2_channel,hh)) )
* aux_bflp_storage
                 + sum ( h2_channel, h2_aux_bflp_sto_sw(n,h2_channel) * h2_aux_bflp_sto_ed(n,h2_channel) *  H2_AUX_BFLP_STO_IN(n,h2_channel,hh) )
* lp_storage
                 + sum ( h2_channel , h2_lp_sto_sw(n,h2_channel) * H2_LP_STO_L(n,h2_channel,hh) * h2_lp_sto_ed(n,h2_channel) )
* dehydration_evaporation
                 + sum ( h2_channel , ( 1 - h2_dehyd_evap_gas_sw(n,h2_channel) ) * h2_dehyd_evap_sw(n,h2_channel) * h2_dehyd_evap_ed(n,h2_channel) * H2_LP_STO_OUT(n,h2_channel,hh) )
* aux_bfMP_storage
                 + sum ( h2_channel, h2_aux_bfMP_sto_sw(n,h2_channel) * h2_aux_bfMP_sto_ed(n,h2_channel) * H2_DEHYD_EVAP_OUT(n,h2_channel,hh) )
* MP_storage
                 + sum ( h2_channel , h2_MP_sto_sw(n,h2_channel) * H2_MP_STO_L(n,h2_channel,hh) * h2_Mp_sto_ed(n,h2_channel) )
* aux_bffilling_storage
                 + sum ( h2_channel , h2_aux_bfhp_sto_sw(n,h2_channel) * h2_aux_bfhp_sto_ed(n,h2_channel) * H2_AUX_BFHP_STO_IN(n,h2_channel,hh) )
* filling storage
                 + sum ( h2_channel , h2_hp_sto_sw(n,h2_channel) * H2_HP_STO_L(n,h2_channel,hh) * h2_hp_sto_ed(n,h2_channel) )
* aux_bffuel
                 + sum ( h2_channel , h2_aux_bffuel_sw(n,h2_channel) * h2_aux_bffuel_ed(n,h2_channel) * H2_HP_STO_OUT(n,h2_channel,hh) )


* aux_recon_site
                 + sum ( (h2_channel,h2_tech_recon) , h2_recon_aux_sw(n,h2_channel,h2_tech_recon) * h2_recon_aux_ed(n,h2_channel,h2_tech_recon) * H2_RECON_AUX_OUT(n,h2_channel,h2_tech_recon,hh)/(1-H2_eta_recon_aux(n,h2_channel,h2_tech_recon)) )

                 )


$ontext
$offtext





         =E=
         sum( map_n_tech(n,dis) , G_L(n,dis,hh)) + sum( map_n_tech(n,nondis) , G_RES(n,nondis,hh)) + sum( sto , STO_OUT(n,sto,hh) ) + sum( map_n_rsvr(n,rsvr) , RSVR_OUT(n,rsvr,hh))
       - sum( map_l(l) , inc(l,n) * eta_ntc(l) * F(l,hh))
%reserves%$ontext
*Balancing Correction Factor
        + sum( map_n_tech(n,dis) ,
          sum( reserves_do ,  RP_DIS(n,reserves_do,dis,hh) * phi_reserves_call(n,reserves_do,hh))
        - sum( reserves_up ,  RP_DIS(n,reserves_up,dis,hh) * phi_reserves_call(n,reserves_up,hh))
         )
$ontext
$offtext
%DSM%$ontext
         + sum( map_n_dsm(n,dsm_curt) , DSM_CU(n,dsm_curt,hh))
         + sum( map_n_dsm(n,dsm_shift) , DSM_DO_DEMAND(n,dsm_shift,hh))
$ontext
$offtext
%EV%$ontext
        + sum( map_n_ev(n,ev) , EV_DISCHARGE(n,ev,hh) )
$ontext
$offtext
%prosumage%$ontext
         + sum( map_n_res_pro(n,res) , G_MARKET_PRO2M(n,res,hh) )
         + sum( map_n_sto_pro(n,sto) , STO_OUT_PRO2M(n,sto,hh))
         + sum( map_n_sto_pro(n,sto) , STO_OUT_M2M(n,sto,hh))
$ontext
$offtext


%P2H2%$ontext
* 0.001 to convert kWh electricity production into MWh demand.
      + 0.001 * (
* recon
         sum ( (h2_channel,h2_tech_recon) , h2_recon_sw(n,h2_channel) * H2_E_RECON_OUT(n,h2_channel,h2_tech_recon,hh) )

                )

$ontext
$offtext


         + G_INFES(n,hh)
;

con2a_loadlevel(n,dis,h)$(ord(h) > 1 AND map_n_tech(n,dis))..
        G_L(n,dis,h) =E= G_L(n,dis,h-1) + G_UP(n,dis,h) - G_DO(n,dis,h)
;

con2b_loadlevelstart(n,dis,h)$(ord(h) = 1 AND map_n_tech(n,dis))..
         G_L(n,dis,h) =E= G_UP(n,dis,h)
;

* ---------------------------------------------------------------------------- *
***** Hourly maximum generation caps and constraints related to reserves   *****
* ---------------------------------------------------------------------------- *

con3a_maxprod_dispatchable(n,dis,h)$(map_n_tech(n,dis))..
        G_L(n,dis,h)
%reserves%$ontext
        + sum( reserves_up , RP_DIS(n,reserves_up,dis,h))
*Balancing Correction Factor
        + sum( reserves_do ,  RP_DIS(n,reserves_do,dis,h) * phi_reserves_call(n,reserves_do,h))
        - sum( reserves_up ,  RP_DIS(n,reserves_up,dis,h) * phi_reserves_call(n,reserves_up,h))
$ontext
$offtext
        =L= avail(n,dis) * N_TECH(n,dis)
;

con3b_minprod_dispatchable(n,dis,h)$(map_n_tech(n,dis))..
        sum( reserves_do , RP_DIS(n,reserves_do,dis,h))
        =L= G_L(n,dis,h)
* Balancing Correction Factor
        + sum( reserves_do ,  RP_DIS(n,reserves_do,dis,h) * phi_reserves_call(n,reserves_do,h))
        - sum( reserves_up ,  RP_DIS(n,reserves_up,dis,h) * phi_reserves_call(n,reserves_up,h))
;

con3c_flex_reserves_spin(n,dis,reserves_spin,h)$(map_n_tech(n,dis))..
        RP_DIS(n,reserves_spin,dis,h)
        =L= grad_per_min(n,dis) * reserves_reaction(n,reserves_spin) * ( G_L(n,dis,h)
* Balancing Correction Factor
        + sum( reserves_do ,  RP_DIS(n,reserves_do,dis,h) * phi_reserves_call(n,reserves_do,h))
        - sum( reserves_up ,  RP_DIS(n,reserves_up,dis,h) * phi_reserves_call(n,reserves_up,h)) )
;

con3d_flex_reserves_nonspin(n,dis,reserves_nonspin,h)$(map_n_tech(n,dis))..
        RP_DIS(n,reserves_nonspin,dis,h)
        =L= grad_per_min(n,dis) * reserves_reaction(n,reserves_nonspin) * N_TECH(n,dis)
;

con3e_maxprod_res(n,nondis,h)$(map_n_tech(n,nondis))..
        G_RES(n,nondis,h) + CU(n,nondis,h)
%reserves%$ontext
        + sum( reserves_up , RP_NONDIS(n,reserves_up,nondis,h))
$ontext
$offtext
        =E= phi_res(n,nondis,h) * avail(n,nondis) * N_TECH(n,nondis)
;

con3f_minprod_res(n,nondis,h)$(map_n_tech(n,nondis))..
        sum( reserves_do , RP_NONDIS(n,reserves_do,nondis,h))
        =L= G_RES(n,nondis,h)
;

* ---------------------------------------------------------------------------- *
***** Storage constraints *****
* ---------------------------------------------------------------------------- *

con4a_stolev_start(n,sto,h)$(map_n_sto(n,sto) AND ord(h) = 1)..
        STO_L(n,sto,h) =E= phi_sto_ini(n,sto) * avail_sto(n,sto) * N_STO_E(n,sto) + STO_IN(n,sto,h)*eta_sto_in(n,sto) - STO_OUT(n,sto,h)/eta_sto_out(n,sto)
;

con4b_stolev(n,sto,h)$((ord(h)>1) AND map_n_sto(n,sto))..
         STO_L(n,sto,h) =E= eta_sto_self(n,sto) * STO_L(n,sto,h-1) + STO_IN(n,sto,h)*eta_sto_in(n,sto) - STO_OUT(n,sto,h)/eta_sto_out(n,sto)
%reserves%$ontext
         + sum( reserves_do , phi_reserves_call(n,reserves_do,h) * ( RP_STO_IN(n,reserves_do,sto,h)*eta_sto_in(n,sto) + RP_STO_OUT(n,reserves_do,sto,h)/eta_sto_out(n,sto) ))
         - sum( reserves_up , phi_reserves_call(n,reserves_up,h) * ( RP_STO_IN(n,reserves_up,sto,h)*eta_sto_in(n,sto) + RP_STO_OUT(n,reserves_up,sto,h)/eta_sto_out(n,sto) ))
$ontext
$offtext
;

con4c_stolev_max(n,sto,h)$(map_n_sto(n,sto))..
        STO_L(n,sto,h) =L= avail_sto(n,sto) * N_STO_E(n,sto)
;

con4d_maxin_sto(n,sto,h)$(map_n_sto(n,sto))..
        STO_IN(n,sto,h)
%reserves%$ontext
        + sum( reserves_do , RP_STO_IN(n,reserves_do,sto,h))
$ontext
$offtext
        =L= avail_sto(n,sto) * N_STO_P_IN(n,sto)
;

con4e_maxout_sto(n,sto,h)$(map_n_sto(n,sto))..
        STO_OUT(n,sto,h)
%reserves%$ontext
        + sum( reserves_up , RP_STO_OUT(n,reserves_up,sto,h))
$ontext
$offtext
        =L= avail_sto(n,sto) * N_STO_P_OUT(n,sto)
;

con4f_resrv_sto(n,sto,h)$(map_n_sto(n,sto))..
        sum( reserves_up , RP_STO_IN(n,reserves_up,sto,h))
        =L= STO_IN(n,sto,h)
;

con4g_resrv_sto(n,sto,h)$(map_n_sto(n,sto))..
        sum( reserves_do , RP_STO_OUT(n,reserves_do,sto,h))
        =L= STO_OUT(n,sto,h)
;

con4h_maxout_lev(n,sto,h)$(map_n_sto(n,sto))..
        ( STO_OUT(n,sto,h)
%reserves%$ontext
        + sum( reserves_up , RP_STO_OUT(n,reserves_up,sto,h))
$ontext
$offtext
        ) / eta_sto_out(n,sto)
        =L= eta_sto_self(n,sto) * STO_L(n,sto,h-1)
;

con4i_maxin_lev(n,sto,h)$(map_n_sto(n,sto))..
        ( STO_IN(n,sto,h)
%reserves%$ontext
        + sum( reserves_do , RP_STO_IN(n,reserves_do,sto,h))
$ontext
$offtext
        ) * eta_sto_in(n,sto)
        =L= avail_sto(n,sto) * N_STO_E(n,sto) - eta_sto_self(n,sto) * STO_L(n,sto,h-1)
;

con4j_ending(n,sto,h)$(ord(h) = card(h) AND map_n_sto(n,sto))..
         STO_L(n,sto,h) =E= phi_sto_ini(n,sto) * avail_sto(n,sto) * N_STO_E(n,sto)
;

con4k_PHS_EtoP(n,sto)$(map_n_sto(n,sto))..
        N_STO_E(n,sto) =L= etop_max(n,sto) * N_STO_P_OUT(n,sto)
;

* ---------------------------------------------------------------------------- *
***** Quotas for renewables and biomass *****
* ---------------------------------------------------------------------------- *

con5a_minRES(n)..
sum( h , G_L(n,'bio',h) + sum( map_n_tech(n,nondis) , G_RES(n,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RSVR_OUT(n,rsvr,h))
%reserves%$ontext
         - sum( reserves_do , (sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_do,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_do,rsvr,h))) * phi_reserves_call(n,reserves_do,h))
         + sum( reserves_up , (sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_up,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_up,rsvr,h))) * phi_reserves_call(n,reserves_up,h))
$ontext
$offtext
%prosumage%$ontext
         + sum( map_n_sto_pro(n,sto) , STO_OUT_PRO2PRO(n,sto,h) + STO_OUT_PRO2M(n,sto,h)) + sum( map_n_res_pro(n,res) , G_MARKET_PRO2M(n,res,h) + G_RES_PRO(n,res,h))
$ontext
$offtext
)
        =G= phi_min_res(n) * sum( h ,
         sum( map_n_tech(n,dis) , G_L(n,dis,h)) + sum( map_n_tech(n,nondis) , G_RES(n,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RSVR_OUT(n,rsvr,h))
%reserves%$ontext
         - sum( reserves_do , (sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_do,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_do,rsvr,h))) * phi_reserves_call(n,reserves_do,h))
         + sum( reserves_up , (sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_up,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_up,rsvr,h))) * phi_reserves_call(n,reserves_up,h))
$ontext
$offtext
%prosumage%$ontext
         + sum( map_n_res_pro(n,res) , phi_res(n,res,h) * N_RES_PRO(n,res) - CU_PRO(n,res,h))
$ontext
$offtext
         )
;

con5b_max_energy(n,dis)$(map_n_tech(n,dis) AND m_e(n,dis))..
         sum( h , G_L(n,dis,h) ) =L= m_e(n,dis)
;

* ---------------------------------------------------------------------------- *
***** DSM constraints - curtailment *****
* ---------------------------------------------------------------------------- *

con6a_DSMcurt_duration_max(n,dsm_curt,h)$(map_n_dsm(n,dsm_curt))..
         sum( hh$( ord(hh) >= ord(h) AND ord(hh) < ord(h) + t_off_dsm_cu(n,dsm_curt) ) , DSM_CU(n,dsm_curt,hh)
%reserves%$ontext
        + sum( reserves_up , RP_DSM_CU(n,reserves_up,dsm_curt,hh) * phi_reserves_call(n,reserves_up,hh) )
$ontext
$offtext
         )
         =L= N_DSM_CU(n,dsm_curt) * t_dur_dsm_cu(n,dsm_curt)
;

con6b_DSMcurt_max(n,dsm_curt,h)$(map_n_dsm(n,dsm_curt))..
        DSM_CU(n,dsm_curt,h)
%reserves%$ontext
        + sum( reserves_up , RP_DSM_CU(n,reserves_up,dsm_curt,h) )
$ontext
$offtext
          =L= N_DSM_CU(n,dsm_curt)
;

* ---------------------------------------------------------------------------- *
***** DSM constraints - shifting *****
* ---------------------------------------------------------------------------- *

con7a_DSMshift_upanddown(n,dsm_shift,h)$(map_n_dsm(n,dsm_shift))..
         DSM_UP(n,dsm_shift,h) * (1 + eta_dsm_shift(n,dsm_shift))/2 =E= 2/(1+eta_dsm_shift(n,dsm_shift)) * sum( hh$( ord(hh) >= ord(h) - t_dur_dsm_shift(n,dsm_shift) AND ord(hh) <= ord(h) + t_dur_dsm_shift(n,dsm_shift) ) , DSM_DO(n,dsm_shift,h,hh))
;

con7b_DSMshift_granular_max(n,dsm_shift,h)$(map_n_dsm(n,dsm_shift))..
         DSM_UP_DEMAND(n,dsm_shift,h) + DSM_DO_DEMAND(n,dsm_shift,h)
%reserves%$ontext
         + sum( reserves , RP_DSM_SHIFT(n,reserves,dsm_shift,h) )
$ontext
$offtext
         =L= N_DSM_SHIFT(n,dsm_shift)
;

con7c_DSM_distrib_up(n,dsm_shift,h)$(map_n_dsm(n,dsm_shift))..
         DSM_UP(n,dsm_shift,h) =E= DSM_UP_DEMAND(n,dsm_shift,h)
%reserves%$ontext
         + sum( reserves_do , RP_DSM_SHIFT(n,reserves_do,dsm_shift,h) * phi_reserves_call(n,reserves_do,h))
$ontext
$offtext
;

con7d_DSM_distrib_do(n,dsm_shift,h)$(map_n_dsm(n,dsm_shift))..
         sum( hh$( ord(hh) >= ord(h) - t_dur_dsm_shift(n,dsm_shift) AND ord(hh) <= ord(h) + t_dur_dsm_shift(n,dsm_shift) ) , DSM_DO(n,dsm_shift,hh,h) )
                 =E=
         DSM_DO_DEMAND(n,dsm_shift,h)
%reserves%$ontext
         + sum( reserves_up , RP_DSM_SHIFT(n,reserves_up,dsm_shift,h) * phi_reserves_call(n,reserves_up,h))
$ontext
$offtext
;

con7e_DSMshift_recovery(n,dsm_shift,h)$(map_n_dsm(n,dsm_shift))..
         sum( hh$( ord(hh) >= ord(h) AND ord(hh) < ord(h) + t_off_dsm_shift(n,dsm_shift) ) , DSM_UP(n,dsm_shift,hh))
         =L= N_DSM_SHIFT(n,dsm_shift)
;

* ---------------------------------------------------------------------------- *
***** Maximum installation constraints *****
* ---------------------------------------------------------------------------- *

con8a_max_I_power(n,tech)$(map_n_tech(n,tech))..
         N_TECH(n,tech) =L= m_p(n,tech)
;

con8b_max_I_sto_e(n,sto)$(map_n_sto(n,sto))..
         N_STO_E(n,sto) =L= m_sto_e(n,sto)
;

con8c_max_I_sto_p_in(n,sto)$(map_n_sto(n,sto))..
         N_STO_P_IN(n,sto) =L= m_sto_p_in(n,sto)
;

con8d_max_I_sto_p_out(n,sto)$(map_n_sto(n,sto))..
         N_STO_P_OUT(n,sto) =L= m_sto_p_out(n,sto)
;

con8e_max_I_dsm_cu(n,dsm_curt)$(map_n_dsm(n,dsm_curt))..
         N_DSM_CU(n,dsm_curt) =L= m_dsm_cu(n,dsm_curt)
;

con8f_max_I_dsm_shift_pos(n,dsm_shift)$(map_n_dsm(n,dsm_shift))..
         N_DSM_SHIFT(n,dsm_shift) =L= m_dsm_shift(n,dsm_shift)
;

con8g_max_pro_res(n,res)$(map_n_res_pro(n,res))..
         N_RES_PRO(n,res) =L= m_res_pro(n,res)
;

con8h_max_pro_sto_e(n,sto)$(map_n_sto_pro(n,sto))..
         N_STO_E_PRO(n,sto) =L= m_sto_pro_e(n,sto)
;

con8i_max_sto_pro_p(n,sto)$(map_n_sto_pro(n,sto))..
         N_STO_P_PRO(n,sto) =L= m_sto_pro_p(n,sto)
;

con8j_max_I_ntc(l)$(map_l(l))..
         NTC(l) =L= m_ntc(l)
;

con8k_max_I_rsvr_e(n,rsvr)$(map_n_rsvr(n,rsvr))..
         N_RSVR_E(n,rsvr) =L= m_rsvr_e(n,rsvr)
;

con8l_max_I_rsvr_p_out(n,rsvr)$(map_n_rsvr(n,rsvr))..
         N_RSVR_P(n,rsvr) =L= m_rsvr_p_out(n,rsvr)
;

* ---------------------------------------------------------------------------- *
***** Reserve constraints *****
* ---------------------------------------------------------------------------- *

con9a_reserve_prov_endogenous(n,reserves_nonprim,h)..
          sum( map_n_tech(n,dis) , RP_DIS(n,reserves_nonprim,dis,h))
        + sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_nonprim,nondis,h))
        + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_nonprim,rsvr,h))
        + sum( map_n_sto(n,sto) , RP_STO_IN(n,reserves_nonprim,sto,h) + RP_STO_OUT(n,reserves_nonprim,sto,h))
%DSM%$ontext
        + sum( map_n_dsm(n,dsm_curt) , RP_DSM_CU(n,reserves_nonprim,dsm_curt,h))
        + sum( map_n_dsm(n,dsm_shift) , RP_DSM_SHIFT(n,reserves_nonprim,dsm_shift,h) )
$ontext
$offtext
%EV%$ontext
%EV_EXOG%   + sum( map_n_ev(n,ev) , RP_EV_G2V(n,reserves_nonprim,ev,h) + RP_EV_V2G(n,reserves_nonprim,ev,h) )
$ontext
$offtext
%heat%$ontext
        + sum( (bu,ch) , theta_sets(n,bu,ch) * ( RP_SETS(n,reserves_nonprim,bu,ch,h) + RP_SETS_AUX(n,reserves_nonprim,bu,ch,h)) )
        + sum( (bu,ch) , theta_hp(n,bu,ch) * RP_HP(n,reserves_nonprim,bu,ch,h) )
        + sum( (bu,ch) , theta_elec(n,bu,ch) * RP_H_ELEC(n,reserves_nonprim,bu,ch,h) )
$ontext
$offtext
        =E= (
            feat_node('reserves',n) *
            1000 * phi_reserves_share(n,reserves_nonprim) * (
            reserves_intercept(n,reserves_nonprim) + sum( map_n_tech(n,nondis) , reserves_slope(n,reserves_nonprim,nondis) * (N_TECH(n,nondis)
%prosumage%$ontext
            + N_RES_PRO(n,nondis)
$ontext
$offtext
            )/1000 ) ) )$(ord(h) > 1)
;

con9a_reserve_prov_exogenous(n,reserves_nonprim,h)..
          sum( map_n_tech(n,dis) , RP_DIS(n,reserves_nonprim,dis,h))
        + sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_nonprim,nondis,h))
        + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_nonprim,rsvr,h))
        + sum( map_n_sto(n,sto) , RP_STO_IN(n,reserves_nonprim,sto,h) + RP_STO_OUT(n,reserves_nonprim,sto,h))
%DSM%$ontext
        + sum( map_n_dsm(n,dsm_curt) , RP_DSM_CU(n,reserves_nonprim,dsm_curt,h))
        + sum( map_n_dsm(n,dsm_shift) , RP_DSM_SHIFT(n,reserves_nonprim,dsm_shift,h) )
$ontext
$offtext
%EV%$ontext
%EV_EXOG%   + sum( map_n_ev(n,ev) , RP_EV_G2V(n,reserves_nonprim,ev,h) + RP_EV_V2G(n,reserves_nonprim,ev,h) )
$ontext
$offtext
%heat%$ontext
        + sum( (bu,ch) , theta_sets(n,bu,ch) * ( RP_SETS(n,reserves_nonprim,bu,ch,h) + RP_SETS_AUX(n,reserves_nonprim,bu,ch,h)) )
        + sum( (bu,ch) , theta_hp(n,bu,ch) * RP_HP(n,reserves_nonprim,bu,ch,h) )
        + sum( (bu,ch) , theta_elec(n,bu,ch) * RP_H_ELEC(n,reserves_nonprim,bu,ch,h) )
$ontext
$offtext
        =E= feat_node('reserves',n) * reserves_exogenous(n,reserves_nonprim,h)$(ord(h) > 1)
;

con9b_reserve_prov_PR_endogenous(n,reserves_prim,h)..
          sum( map_n_tech(n,dis) , RP_DIS(n,reserves_prim,dis,h))
        + sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_prim,nondis,h))
        + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_prim,rsvr,h))
        + sum( map_n_sto(n,sto) , RP_STO_IN(n,reserves_prim,sto,h) + RP_STO_OUT(n,reserves_prim,sto,h) )
%EV%$ontext
%EV_EXOG%   + sum( map_n_ev(n,ev) , RP_EV_G2V(n,reserves_prim,ev,h) + RP_EV_V2G(n,reserves_prim,ev,h) )
$ontext
$offtext
         =E=
             feat_node('reserves',n) *
             phi_reserves_pr_up(n)* sum( reserves_nonprim , 1000 * phi_reserves_share(n,reserves_nonprim) * (
             reserves_intercept(n,reserves_nonprim) + sum( map_n_tech(n,nondis) , reserves_slope(n,reserves_nonprim,nondis) * (N_TECH(n,nondis)
%prosumage%$ontext
             + N_RES_PRO(n,nondis)
$ontext
$offtext
             )/1000 ) ) )$(ord(h) > 1)
;

con9b_reserve_prov_PR_exogenous(n,reserves_prim,h)..
          sum( map_n_tech(n,dis) , RP_DIS(n,reserves_prim,dis,h))
        + sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_prim,nondis,h))
        + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_prim,rsvr,h))
        + sum( map_n_sto(n,sto) , RP_STO_IN(n,reserves_prim,sto,h) + RP_STO_OUT(n,reserves_prim,sto,h) )
%EV%$ontext
%EV_EXOG%   + sum( map_n_ev(n,ev) , RP_EV_G2V(n,reserves_prim,ev,h) + RP_EV_V2G(n,reserves_prim,ev,h) )
$ontext
$offtext
         =E= feat_node('reserves',n) * reserves_exogenous(n,reserves_prim,h)$(ord(h) > 1)
;

* ---------------------------------------------------------------------------- *
***** Electric vehicle constraints *****
* ---------------------------------------------------------------------------- *

con10a_ev_ed(n,ev,h)$(map_n_ev(n,ev))..
         feat_node('ev',n) *
         ev_ed(n,ev,h) * phi_ev(n,ev) * ev_quant(n)
         =e= EV_GED(n,ev,h) + EV_PHEVFUEL(n,ev,h)$(ev_phev(n,ev)=1)
;

con10b_ev_chargelev_start(ev,h,n)$(map_n_ev(n,ev) AND ord(h) = 1 AND feat_node('ev',n))..
         EV_L(n,ev,h) =E= feat_node('ev',n) * phi_ev_ini(n,ev) * n_ev_e(n,ev) * phi_ev(n,ev) * ev_quant(n)
         + EV_CHARGE(n,ev,h) * eta_ev_in(n,ev)
         - EV_DISCHARGE(n,ev,h) / eta_ev_out(n,ev)
         - EV_GED(n,ev,h)
;

con10c_ev_chargelev(ev,h,n)$(map_n_ev(n,ev) AND ord(h) > 1 AND feat_node('ev',n))..
         EV_L(n,ev,h) =E= EV_L(n,ev,h-1)
         + EV_CHARGE(n,ev,h) * eta_ev_in(n,ev)
         - EV_DISCHARGE(n,ev,h) / eta_ev_out(n,ev)
%reserves%$ontext
%EV_EXOG%   + sum( reserves_do , phi_reserves_call(n,reserves_do,h) * (RP_EV_G2V(n,reserves_do,ev,h)*eta_ev_in(n,ev) + RP_EV_V2G(n,reserves_do,ev,h)/eta_ev_out(n,ev)) )
%EV_EXOG%   - sum( reserves_up , phi_reserves_call(n,reserves_up,h) * (RP_EV_G2V(n,reserves_up,ev,h)*eta_ev_in(n,ev) + RP_EV_V2G(n,reserves_up,ev,h)/eta_ev_out(n,ev)) )
$ontext
$offtext
         - EV_GED(n,ev,h)
;

con10d_ev_chargelev_max(n,ev,h)$(map_n_ev(n,ev) AND feat_node('ev',n))..
         EV_L(n,ev,h)
         =L= n_ev_e(n,ev) * phi_ev(n,ev) * ev_quant(n)
             * feat_node('ev',n)
;

con10e_ev_maxin(n,ev,h)$(map_n_ev(n,ev) AND feat_node('ev',n))..
        EV_CHARGE(n,ev,h)
%reserves%$ontext
        + sum( reserves_do , RP_EV_G2V(n,reserves_do,ev,h))
$ontext
$offtext
        =L= n_ev_p(n,ev,h) * phi_ev(n,ev) * ev_quant(n)
            * feat_node('ev',n)
;

con10f_ev_maxout(n,ev,h)$(map_n_ev(n,ev) AND feat_node('ev',n))..
        EV_DISCHARGE(n,ev,h)
%reserves%$ontext
        + sum( reserves_up , RP_EV_V2G(n,reserves_up,ev,h))
$ontext
$offtext
        =L= n_ev_p(n,ev,h) * phi_ev(n,ev) * ev_quant(n)
            * feat_node('ev',n)
;

con10g_ev_chargelev_ending(n,ev,h)$(map_n_ev(n,ev) AND ord(h) = card(h) AND feat_node('ev',n))..
         EV_L(n,ev,h) =E= phi_ev_ini(n,ev) * n_ev_e(n,ev) * phi_ev(n,ev) * ev_quant(n) * feat_node('ev',n)
;

con10h_ev_minin(n,ev,h)$(map_n_ev(n,ev) AND feat_node('ev',n))..
         0 =L= EV_CHARGE(n,ev,h)
        - sum( reserves_up , RP_EV_G2V(n,reserves_up,ev,h))
;

con10i_ev_maxin_lev(n,ev,h)$(map_n_ev(n,ev))..
        ( EV_CHARGE(n,ev,h)
        + sum( reserves_do , RP_EV_G2V(n,reserves_do,ev,h))
        ) * eta_ev_in(n,ev)
        =L= n_ev_e(n,ev) * phi_ev(n,ev) * ev_quant(n) - EV_L(n,ev,h-1)
;

con10j_ev_minout(n,ev,h)$(map_n_ev(n,ev) AND feat_node('ev',n))..
         0 =L= EV_DISCHARGE(n,ev,h)
        - sum( reserves_do , RP_EV_V2G(n,reserves_do,ev,h))
;

con10k_ev_maxout_lev(n,ev,h)$(map_n_ev(n,ev) AND feat_node('ev',n))..
        ( EV_DISCHARGE(n,ev,h)
        + sum( reserves_up , RP_EV_V2G(n,reserves_up,ev,h))
) / eta_ev_out(n,ev)
        =L= EV_L(n,ev,h-1)
;

con10l_ev_exog(n,ev,h)$(map_n_ev(n,ev) AND feat_node('ev',n))..
         EV_CHARGE(n,ev,h)
         =E=
         ev_ged_exog(n,ev,h) * phi_ev(n,ev) * ev_quant(n)
         * feat_node('ev',n)
;

* ---------------------------------------------------------------------------- *
***** Prosumage constraints *****
* ---------------------------------------------------------------------------- *

con11a_pro_distrib(n,res,h)$(map_n_res_pro(n,res))..
         phi_res(n,res,h) * avail(n,res) * N_RES_PRO(n,res)
         =E=
         CU_PRO(n,res,h) + G_MARKET_PRO2M(n,res,h) + G_RES_PRO(n,res,h) + sum( map_n_sto_pro(n,sto) , STO_IN_PRO2PRO(n,res,sto,h) + STO_IN_PRO2M(n,res,sto,h) )
;

con11b_pro_balance(n,h)..
         phi_pro_load(n) * d(n,h)
         =E=
         sum( map_n_res_pro(n,res) , G_RES_PRO(n,res,h)) + sum( map_n_sto_pro(n,sto) , STO_OUT_PRO2PRO(n,sto,h) + STO_OUT_M2PRO(n,sto,h) ) + G_MARKET_M2PRO(n,h)
;

con11c_pro_selfcon(n)..
         sum( (h,map_n_res_pro(n,res)) , G_RES_PRO(n,res,h) ) + sum( (h,sto) , STO_OUT_PRO2PRO(n,sto,h) )
         =G=
         phi_pro_self(n) * sum( h , phi_pro_load(n) * d(n,h))
;

con11d_pro_stolev_PRO2PRO(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h) > 1 )..
         STO_L_PRO2PRO(n,sto,h) =E= STO_L_PRO2PRO(n,sto,h-1) + sum( map_n_res_pro(n,res) , STO_IN_PRO2PRO(n,res,sto,h)*eta_sto_in(n,sto) - STO_OUT_PRO2PRO(n,sto,h)/eta_sto_out(n,sto) )
;

con11e_pro_stolev_PRO2M(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h) > 1)..
         STO_L_PRO2M(n,sto,h) =E= STO_L_PRO2M(n,sto,h-1) + sum( map_n_res_pro(n,res) , STO_IN_PRO2M(n,res,sto,h)*eta_sto_in(n,sto) - STO_OUT_PRO2M(n,sto,h)/eta_sto_out(n,sto) )
;

con11f_pro_stolev_M2PRO(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h) > 1)..
         STO_L_M2PRO(n,sto,h) =E= STO_L_M2PRO(n,sto,h-1) + STO_IN_M2PRO(n,sto,h)*eta_sto_in(n,sto) - STO_OUT_M2PRO(n,sto,h)/eta_sto_out(n,sto)
;

con11g_pro_stolev_M2M(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h) > 1)..
         STO_L_M2M(n,sto,h) =E= STO_L_M2M(n,sto,h-1) + STO_IN_M2M(n,sto,h)*eta_sto_in(n,sto) - STO_OUT_M2M(n,sto,h)/eta_sto_out(n,sto)
;

con11h_1_pro_stolev_start_PRO2PRO(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h) = 1)..
        STO_L_PRO2PRO(n,sto,h) =E= 0.25 * phi_sto_pro_ini(n,sto) * N_STO_E_PRO(n,sto) + sum( map_n_res_pro(n,res) , STO_IN_PRO2PRO(n,res,sto,h))*eta_sto_in(n,sto) - STO_OUT_PRO2PRO(n,sto,h)/eta_sto_out(n,sto)
;

con11h_2_pro_stolev_start_PRO2M(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h) = 1)..
        STO_L_PRO2M(n,sto,h) =E= 0.25 * phi_sto_pro_ini(n,sto) * N_STO_E_PRO(n,sto) + sum( map_n_res_pro(n,res) , STO_IN_PRO2M(n,res,sto,h))*eta_sto_in(n,sto) - STO_OUT_PRO2M(n,sto,h)/eta_sto_out(n,sto)
;

con11h_3_pro_stolev_start_M2PRO(n,sto,h)$(map_n_sto_pro(n,sto) AND map_n_sto_pro(n,sto) AND ord(h) = 1)..
        STO_L_M2PRO(n,sto,h) =E= 0.25 * phi_sto_pro_ini(n,sto) * N_STO_E_PRO(n,sto) + STO_IN_M2PRO(n,sto,h)*eta_sto_in(n,sto) - STO_OUT_M2PRO(n,sto,h)/eta_sto_out(n,sto)
;

con11h_4_pro_stolev_start_M2M(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h) = 1)..
        STO_L_M2M(n,sto,h) =E= 0.25 * phi_sto_pro_ini(n,sto) * N_STO_E_PRO(n,sto) + STO_IN_M2M(n,sto,h)*eta_sto_in(n,sto) - STO_OUT_M2M(n,sto,h)/eta_sto_out(n,sto)
;

con11i_pro_stolev(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h)>1)..
         STO_L_PRO(n,sto,h) =E= STO_L_PRO2PRO(n,sto,h) +  STO_L_PRO2M(n,sto,h) + STO_L_M2PRO(n,sto,h) + STO_L_M2M(n,sto,h)
;

con11j_pro_stolev_max(n,sto,h)$map_n_sto_pro(n,sto)..
        STO_L_PRO(n,sto,h) =L= avail_sto(n,sto) * N_STO_E_PRO(n,sto)
;

con11k_pro_maxin_sto(n,sto,h)$(map_n_sto_pro(n,sto))..
        sum( map_n_res_pro(n,res) , STO_IN_PRO2PRO(n,res,sto,h) + STO_IN_PRO2M(n,res,sto,h) ) + STO_IN_M2PRO(n,sto,h) + STO_IN_M2M(n,sto,h)
        =L= avail_sto(n,sto) * N_STO_P_PRO(n,sto)
;

con11l_pro_maxout_sto(n,sto,h)$(map_n_sto_pro(n,sto))..
        STO_OUT_PRO2PRO(n,sto,h) + STO_OUT_PRO2M(n,sto,h) + STO_OUT_M2PRO(n,sto,h) + STO_OUT_M2M(n,sto,h)
        =L= avail_sto(n,sto) * N_STO_P_PRO(n,sto)
;

con11m_pro_maxout_lev(n,sto,h)$(map_n_sto_pro(n,sto))..
        ( STO_OUT_PRO2PRO(n,sto,h) + STO_OUT_M2PRO(n,sto,h) + STO_OUT_PRO2M(n,sto,h) + STO_OUT_M2M(n,sto,h) ) / eta_sto_out(n,sto)
        =L= STO_L_PRO(n,sto,h-1)
;

con11n_pro_maxin_lev(n,sto,h)$(map_n_sto_pro(n,sto))..
        ( sum( map_n_res_pro(n,res) , STO_IN_PRO2PRO(n,res,sto,h) + STO_IN_PRO2M(n,res,sto,h) ) + STO_IN_M2PRO(n,sto,h) + STO_IN_M2M(n,sto,h) ) * eta_sto_in(n,sto)
        =L= avail_sto(n,sto) * N_STO_E_PRO(n,sto) - STO_L_PRO(n,sto,h-1)
;

con11o_pro_ending(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h) = card(h))..
         STO_L_PRO(n,sto,h) =E= phi_sto_pro_ini(n,sto) * avail_sto(n,sto) * N_STO_E_PRO(n,sto)
;

* ---------------------------------------------------------------------------- *
***** NTC constraints *****
* ---------------------------------------------------------------------------- *

***** Constraint on energy flow between nodes ******
con12a_max_f(l,h)$(map_l(l))..
         F(l,h) =L= NTC(l)
;

con12b_min_f(l,h)$(map_l(l))..
         F(l,h) =G= -NTC(l)
;

* ---------------------------------------------------------------------------- *
***** Reservoir constraints *****
* ---------------------------------------------------------------------------- *

con13a_rsvrlev_start(n,rsvr,h)$(map_n_rsvr(n,rsvr) AND ord(h) = 1)..
        RSVR_L(n,rsvr,h) =E= phi_rsvr_ini(n,rsvr) * avail_rsvr(n,rsvr) * N_RSVR_E(n,rsvr) +rsvr_in(n,rsvr,h) * N_RSVR_P(n,rsvr) - RSVR_OUT(n,rsvr,h)/eta_rsvr_out(n,rsvr)
;

con13b_rsvrlev(rsvr,h,n)$(ord(h) > 1 AND map_n_rsvr(n,rsvr))..
         RSVR_L(n,rsvr,h) =E= RSVR_L(n,rsvr,h-1) + rsvr_in(n,rsvr,h) * N_RSVR_P(n,rsvr) - RSVR_OUT(n,rsvr,h)/eta_rsvr_out(n,rsvr)
%reserves%$ontext
                - sum( reserves_up , RP_RSVR(n,reserves_up,rsvr,h) * phi_reserves_call(n,reserves_up,h) ) /eta_rsvr_out(n,rsvr)
                + sum( reserves_do , RP_RSVR(n,reserves_do,rsvr,h) * phi_reserves_call(n,reserves_do,h) ) /eta_rsvr_out(n,rsvr)
$ontext
$offtext
;

con13c_rsvrlev_max(n,rsvr,h)$(map_n_rsvr(n,rsvr))..
        RSVR_L(n,rsvr,h) =L= avail_rsvr(n,rsvr) * N_RSVR_E(n,rsvr)
;

con13d_maxout_rsvr(rsvr,h,n)$(map_n_rsvr(n,rsvr))..
        RSVR_OUT(n,rsvr,h)
%reserves%$ontext
        + sum( reserves_up , RP_RSVR(n,reserves_up,rsvr,h))
$ontext
$offtext
        =L= avail_rsvr(n,rsvr) * N_RSVR_P(n,rsvr)
;

con13e_resrv_rsvr(n,rsvr,h)$(map_n_rsvr(n,rsvr))..
        sum( reserves_do , RP_RSVR(n,reserves_do,rsvr,h))
        =L= avail_rsvr(n,rsvr) * RSVR_OUT(n,rsvr,h)
;

con13f_maxout_lev(n,rsvr,h)$(map_n_rsvr(n,rsvr))..
        RSVR_OUT(n,rsvr,h)
%reserves%$ontext
        + sum( reserves_up , RP_RSVR(n,reserves_up,rsvr,h))
$ontext
$offtext
        =L= RSVR_L(n,rsvr,h-1)
;

con13g_ending(n,rsvr,h)$(map_n_rsvr(n,rsvr) AND ord(h) = card(h))..
         RSVR_L(n,rsvr,h) =E= phi_rsvr_ini(n,rsvr) * avail_rsvr(n,rsvr) * N_RSVR_E(n,rsvr)
;

* con13h_smooth(n,rsvr,h)$(map_n_rsvr(n,rsvr) AND feat_node('rsvr_outflow',n))..
*          RSVR_OUT(n,rsvr,h) =G= phi_rsvr_min(n) * sum( hh , rsvr_in(n,rsvr,hh)/1000/card(hh)) * avail_rsvr(n,rsvr) * N_RSVR_E(n,rsvr)
* ;

con13i_min_level(n,rsvr,h)$(map_n_rsvr(n,rsvr))..
         RSVR_L(n,rsvr,h) =G= phi_rsvr_lev_min(n,rsvr) * avail_rsvr(n,rsvr) * N_RSVR_E(n,rsvr)
;

con13j_min_FLH(n,rsvr)$(map_n_rsvr(n,rsvr))..
         sum( h , RSVR_OUT(n,rsvr,h) ) =G= min_flh(n,rsvr) * avail_rsvr(n,rsvr) * N_RSVR_P(n,rsvr)
;


* ---------------------------------------------------------------------------- *
***** Heating constraints *****
* ---------------------------------------------------------------------------- *

* Energy balances
con14a_heat_balance(n,bu,ch,h)$feat_node('heat',n)..
         theta_dir(n,bu,ch) * H_DIR(n,bu,ch,h) + theta_sets(n,bu,ch) * H_SETS_OUT(n,bu,ch,h)+ theta_storage(n,bu,ch) * H_STO_OUT(n,bu,ch,h)
         + theta_sets(n,bu,ch) * (1-eta_heat_stat(n,bu,ch)) * H_SETS_LEV(n,bu,ch,h-1)$(theta_sets(n,bu,ch) AND ord(h) > 1)
         =G= dh(n,bu,ch,h) - H_INFES(n,bu,ch,h)
;

con14b_dhw_balance(n,bu,ch,h)$feat_node('heat',n)..
         theta_storage(n,bu,ch) * H_DHW_STO_OUT(n,bu,ch,h) + theta_dir(n,bu,ch) * H_DHW_DIR(n,bu,ch,h) + theta_sets(n,bu,ch) * H_DHW_AUX_OUT(n,bu,ch,h)
         =E=
         d_dhw(n,bu,ch,h) - H_DHW_INFES(n,bu,ch,h)
;

* SETS
con14c_sets_level(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch) AND ord(h) > 1)..
         H_SETS_LEV(n,bu,ch,h) =E= eta_heat_stat(n,bu,ch) * H_SETS_LEV(n,bu,ch,h-1) + eta_heat_dyn(n,bu,ch) * H_SETS_IN(n,bu,ch,h) - H_SETS_OUT(n,bu,ch,h)
%reserves%$ontext
         - theta_sets(n,bu,ch) * eta_heat_dyn(n,bu,ch) * (sum( reserves_up , RP_SETS(n,reserves_up,bu,ch,h) * phi_reserves_call(n,reserves_up,h) )
         - sum( reserves_do , RP_SETS(n,reserves_do,bu,ch,h) * phi_reserves_call(n,reserves_do,h) ))
$ontext
$offtext
;

con14d_sets_level_start(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch) AND (ord(h) = 1 OR ord(h) = card(h)))..
         H_SETS_LEV(n,bu,ch,h) =E= phi_heat_ini(n,bu,ch) * n_sets_e(n,bu,ch)
;

con14e_sets_maxin(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch))..
         H_SETS_IN(n,bu,ch,h)
%reserves%$ontext
         + theta_sets(n,bu,ch) * sum( reserves_do , RP_SETS(n,reserves_do,bu,ch,h) )
$ontext
$offtext
         =L= n_sets_p_in(n,bu,ch)
;

con14f_sets_maxout(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch))..
         H_SETS_OUT(n,bu,ch,h) =L= n_sets_p_out(n,bu,ch)
;

con14g_sets_minin(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch))..
        sum( reserves_up , RP_SETS(n,reserves_up,bu,ch,h))
        =L= H_SETS_IN(n,bu,ch,h)
;

con14h_sets_maxlev(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch))..
         H_SETS_LEV(n,bu,ch,h) =L= n_sets_e(n,bu,ch)
;

* SETS and DHW
con14i_sets_aux_dhw_level(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch) AND ord(h) > 1)..
         H_DHW_AUX_LEV(n,bu,ch,h) =E= eta_dhw_aux_stat(n,bu,ch) * H_DHW_AUX_LEV(n,bu,ch,h-1) + H_DHW_AUX_ELEC_IN(n,bu,ch,h) - H_DHW_AUX_OUT(n,bu,ch,h)
%reserves%$ontext
         - theta_sets(n,bu,ch) * (sum( reserves_up , RP_SETS_AUX(n,reserves_up,bu,ch,h) * phi_reserves_call(n,reserves_up,h) )
         - sum( reserves_do , RP_SETS_AUX(n,reserves_do,bu,ch,h) * phi_reserves_call(n,reserves_do,h) ))
$ontext
$offtext
;

con14j_sets_aux_dhw_level_start(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch) AND (ord(h) = 1 OR ord(h) = card(h)) )..
         H_DHW_AUX_LEV(n,bu,ch,h) =E= phi_heat_ini(n,bu,ch) * n_sets_dhw_e(n,bu,ch)
;

con14k_sets_aux_dhw_maxin(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch) )..
         H_DHW_AUX_ELEC_IN(n,bu,ch,h)
%reserves%$ontext
         + theta_sets(n,bu,ch) * sum( reserves_do , RP_SETS_AUX(n,reserves_do,bu,ch,h) )
$ontext
$offtext
         =L= n_sets_dhw_p_in(n,bu,ch)
;

con14l_sets_aux_dhw_minin(n,bu,ch,h)$(feat_node('heat',n) AND feat_node('reserves',n) AND theta_sets(n,bu,ch)  )..
        sum( reserves_up , RP_SETS_AUX(n,reserves_up,bu,ch,h))
        =L= H_DHW_AUX_ELEC_IN(n,bu,ch,h)
;

con14m_sets_aux_dhw_maxlev(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch) )..
         H_DHW_AUX_LEV(n,bu,ch,h) =L= n_sets_dhw_e(n,bu,ch)
;

* HEAT PUMPS
con14n_hp_in(n,bu,hp,h)$(feat_node('heat',n) AND theta_hp(n,bu,hp))..
         H_STO_IN_HP(n,bu,hp,h) =E= (H_HP_IN(n,bu,hp,h)
%reserves%$ontext
         - theta_hp(n,bu,hp) * (sum( reserves_up , RP_HP(n,reserves_up,bu,hp,h) * phi_reserves_call(n,reserves_up,h) )
         - sum( reserves_do , RP_HP(n,reserves_do,bu,hp,h) * phi_reserves_call(n,reserves_do,h) ))
$ontext
$offtext
         ) * eta_heat_dyn(n,bu,hp) * ((temp_sink(n,bu,hp)+273.15)/(temp_sink(n,bu,hp) - temp_source(n,bu,hp,h)))
;

con14o_hp_maxin(n,bu,hp,h)$(feat_node('heat',n) AND theta_hp(n,bu,hp))..
         H_HP_IN(n,bu,hp,h)
%reserves%$ontext
         + sum( reserves_do , RP_HP(n,reserves_do,bu,hp,h) )
$ontext
$offtext
         =L= n_heat_p_in(n,bu,hp)
;

con14p_hp_minin(n,bu,hp,h)$(feat_node('heat',n) AND theta_hp(n,bu,hp))..
        sum( reserves_up , RP_HP(n,reserves_up,bu,hp,h))
        =L= H_HP_IN(n,bu,hp,h)
;

* (Hybrid) ELECTRIC HEATING
con14q_storage_elec_in(n,bu,hel,h)$(feat_node('heat',n) AND theta_storage(n,bu,hel) AND theta_elec(n,bu,hel) )..
         H_STO_IN_ELECTRIC(n,bu,hel,h) =E= H_ELECTRIC_IN(n,bu,hel,h)
%reserves%$ontext
         - theta_elec(n,bu,hel) * (sum( reserves_up , RP_H_ELEC(n,reserves_up,bu,hel,h) * phi_reserves_call(n,reserves_up,h) )
         - sum( reserves_do , RP_H_ELEC(n,reserves_do,bu,hel,h) * phi_reserves_call(n,reserves_do,h) ))
$ontext
$offtext
;

con14r_storage_elec_maxin(n,bu,hel,h)$(feat_node('heat',n) AND theta_storage(n,bu,hel) AND theta_elec(n,bu,hel ))..
         H_ELECTRIC_IN(n,bu,hel,h)
%reserves%$ontext
         + sum( reserves_do , RP_H_ELEC(n,reserves_do,bu,hel,h) )
$ontext
$offtext
         =L= n_heat_p_in(n,bu,hel)
;

con14s_storage_elec_minin(n,bu,hel,h)$(feat_node('heat',n) AND feat_node('reserves',n) AND theta_storage(n,bu,hel) AND theta_elec(n,bu,hel) )..
        sum( reserves_up , RP_H_ELEC(n,reserves_up,bu,hel,h))
        =L= H_ELECTRIC_IN(n,bu,hel,h)
;

* HEAT STORAGE
con14t_storage_level(n,bu,hst,h)$(feat_node('heat',n) AND theta_storage(n,bu,hst) AND ord(h) > 1)..
         H_STO_LEV(n,bu,hst,h)
         =E=
         eta_heat_stat(n,bu,hst) * H_STO_LEV(n,bu,hst,h-1) + theta_hp(n,bu,hst)*H_STO_IN_HP(n,bu,hst,h) + theta_elec(n,bu,hst)*H_STO_IN_ELECTRIC(n,bu,hst,h) + theta_fossil(n,bu,hst) * H_STO_IN_FOSSIL(n,bu,hst,h)
         - H_STO_OUT(n,bu,hst,h) - H_DHW_STO_OUT(n,bu,hst,h)
;

con14u_storage_level_start(n,bu,hst,h)$(feat_node('heat',n) AND theta_storage(n,bu,hst) AND (ord(h) = 1 OR ord(h) = card(h)))..
         H_STO_LEV(n,bu,hst,h) =E= phi_heat_ini(n,bu,hst) * theta_storage(n,bu,hst)*n_heat_e(n,bu,hst)
;

con14v_storage_maxlev(n,bu,hst,h)$(feat_node('heat',n) AND theta_storage(n,bu,hst))..
         H_STO_LEV(n,bu,hst,h) =L= n_heat_e(n,bu,hst)
;


* ---------------------------------------------------------------------------- *
***** P2H2 constraints *****
* ---------------------------------------------------------------------------- *

%P2H2%$ontext

* prod
h2_con2a(n,h2_tech,h2_tech_recon,h)$h2_tech_avail_set(n,h2_tech)..
         H2_N_PROD_CENT(n,h2_tech) =g= sum( h2_channel_wo_decent_set , H2_E_H2_IN(n,h2_tech,h2_channel_wo_decent_set,h) )
*                                         + h2_bidirect_sw(n,h2_tech_recon) * h2_bidirect_ratio(n,h2_tech_recon)  * sum( h2_channel_wo_decent_set , H2_E_RECON_OUT(n,h2_channel_wo_decent_set,h2_tech_recon,h)
*                                         $( h2_tech_recon_avail_set(n,h2_tech_recon) AND h2_recon_set(n,h2_channel_wo_decent_set) AND sameAs(h2_tech,h2_tech_recon) ) ) 
        ;

* Alternative formulation of "h2_con2a", gives the same result in a test ... (maybe needs another check)
*h2_con2a(n,h2_tech,h)$ h2_tech_avail_set(n,h2_tech)..
*         H2_N_PROD_CENT(n,h2_tech) =g= sum( h2_channel_wo_decent_set , H2_E_H2_IN(n,h2_tech,h2_channel_wo_decent_set,h) ) +
*sum( h2_channel_wo_decent_set ,
*sum( h2_tech_recon , h2_bidirect_sw(n,h2_tech_recon) * h2_bidirect_ratio(n,h2_tech_recon)  *
*H2_E_RECON_OUT(n,h2_channel_wo_decent_set,h2_tech_recon,h)$( h2_tech_recon_avail_set(n,h2_tech_recon) AND h2_recon_set(n,h2_channel_wo_decent_set) AND sameAs(h2_tech,h2_tech_recon) )
*)) ;





h2_con2b(n,h2_tech,h)$h2_tech_avail_set(n,h2_tech)..
         H2_N_PROD_DECENT(n,h2_tech) =g= H2_E_H2_IN(n,h2_tech,'fuel_decent',h) ;


h2_con3(n,h2_tech,h2_channel,h)$( h2_tech_avail_set(n,h2_tech) AND h2_channel_avail_set(n,h2_channel) )..
         H2_PROD_OUT(n,h2_tech,h2_channel,h) =e= h2_channel_avail_sw(n,h2_channel) * h2_tech_avail_sw(n,h2_tech) * h2_efficiency(n,h2_tech) * H2_E_H2_IN(n,h2_tech,h2_channel,h) ;

* aux_prod_site

h2_con4(n,h2_tech,h2_channel,h)$( h2_prod_aux_set(n,h2_tech,h2_channel) AND h2_tech_avail_set(n,h2_tech) AND h2_channel_avail_set(n,h2_channel) )..
         sum( h2_channel_alias , 1$( h2_prod_aux_set(n,h2_tech,h2_channel_alias) AND h2_tech_avail_set(n,h2_tech) AND h2_channel_avail_set(n,h2_channel_alias) AND h2_sto_p_type(n,h2_channel) = h2_sto_p_type(n,h2_channel_alias) ) ) * H2_N_PROD_AUX(n,h2_tech,h2_channel) =g= sum( h2_channel_alias , H2_PROD_AUX_IN(n,h2_tech,h2_channel_alias,h)$( h2_prod_aux_set(n,h2_tech,h2_channel_alias) AND h2_tech_avail_set(n,h2_tech) AND h2_channel_avail_set(n,h2_channel_alias) AND h2_sto_p_type(n,h2_channel) = h2_sto_p_type(n,h2_channel_alias) ) ) ;


h2_con5(n,h2_tech,h2_channel,h)$( h2_tech_avail_set(n,h2_tech) AND h2_channel_avail_set(n,h2_channel) )..
         H2_PROD_AUX_IN(n,h2_tech,h2_channel,h) + h2_bypass_1_sw(n,h2_tech,h2_channel) * H2_BYPASS_1(n,h2_tech,h2_channel,h) =e= H2_PROD_OUT(n,h2_tech,h2_channel,h) ;
h2_con6(n,h2_channel,h)$h2_channel_avail_set(n,h2_channel)..
         H2_PROD_AUX_OUT(n,h2_channel,h) =e=   sum( h2_tech , (1-h2_prod_aux_sw(n,h2_tech,h2_channel)*h2_eta_prod_aux(n,h2_tech,h2_channel))* H2_PROD_AUX_IN(n,h2_tech,h2_channel,h) )  ;

* hydration_liquefaction
h2_con7(n,h2_channel,h)$h2_channel_avail_set(n,h2_channel)..
         H2_HYD_LIQ_OUT(n,h2_channel,h) =e= (1-h2_hyd_liq_sw(n, h2_channel)* h2_eta_hyd(n,h2_channel)) * H2_PROD_AUX_OUT(n,h2_channel,h) ;


h2_con8(n,h2_channel,h)$( h2_hyd_liq_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         sum( h2_channel_alias , 1$( h2_hyd_liq_set(n,h2_channel_alias) AND h2_channel_avail_set(n,h2_channel_alias) AND h2_sto_p_type(n,h2_channel) = h2_sto_p_type(n,h2_channel_alias) ) ) *  H2_N_HYD_LIQ(n,h2_channel) =g= sum( h2_channel_alias , H2_PROD_AUX_OUT(n,h2_channel_alias,h)$( h2_hyd_liq_set(n,h2_channel_alias) AND h2_channel_avail_set(n,h2_channel_alias) AND h2_sto_p_type(n,h2_channel) = h2_sto_p_type(n,h2_channel_alias) ) ) ;

* prod_site_storage
h2_con9(n,h2_channel,h)$h2_channel_avail_set(n,h2_channel)..
         H2_HYD_LIQ_OUT(n,h2_channel,h) =e= H2_STO_P_IN(n,h2_channel,h) ;

h2_con10(n,h2_channel,h)$( h2_sto_p_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         sum( h2_channel_alias , 1$( h2_sto_p_set(n,h2_channel_alias) AND h2_channel_avail_set(n,h2_channel_alias) AND h2_sto_p_type(n,h2_channel) = h2_sto_p_type(n,h2_channel_alias) ) ) *  H2_N_STO(n,h2_channel) =g= sum( h2_channel_alias , H2_STO_P_L(n,h2_channel_alias,h)$( h2_sto_p_set(n,h2_channel_alias) AND h2_channel_avail_set(n,h2_channel_alias) AND h2_sto_p_type(n,h2_channel) = h2_sto_p_type(n,h2_channel_alias) ) ) ;

h2_con11a(n,h2_channel,h)$( ord(h) > 1 AND h2_channel_avail_set(n,h2_channel) )..
         h2_sto_p_sw(n,h2_channel) * H2_STO_P_L(n,h2_channel,h) =e= h2_sto_p_sw(n,h2_channel) * H2_STO_P_L(n,h2_channel,h-1) * ( 1 - h2_sto_p_eta_stat(n,h2_channel) ) + H2_STO_P_IN(n,h2_channel,h) - H2_STO_P_OUT(n,h2_channel,h) ;
h2_con11b(n,h2_channel,h)$( ord(h) = 1 AND h2_channel_avail_set(n,h2_channel) )..
         h2_sto_p_sw(n,h2_channel) * H2_STO_P_L(n,h2_channel,h) =e= h2_sto_p_sw(n,h2_channel) * H2_STO_P_L0(n,h2_channel) + H2_STO_P_IN(n,h2_channel,h) - H2_STO_P_OUT(n,h2_channel,h) ;
h2_con11c(n,h2_channel)$( h2_channel_avail_set(n,h2_channel) )..
        h2_sto_p_sw(n,h2_channel) * h2_sto_p_phi_ini(n,h2_channel) * sum( h2_channel_alias , 1$( h2_sto_p_set(n,h2_channel_alias) AND h2_channel_avail_set(n,h2_channel_alias) AND h2_sto_p_type(n,h2_channel) = h2_sto_p_type(n,h2_channel_alias) ) ) * H2_N_STO(n,h2_channel) =g= h2_sto_p_sw(n,h2_channel) * sum( h2_channel_alias , H2_STO_P_L0(n,h2_channel_alias)$( h2_sto_p_set(n,h2_channel_alias) AND h2_channel_avail_set(n,h2_channel_alias) AND h2_sto_p_type(n,h2_channel) = h2_sto_p_type(n,h2_channel_alias) ) ) ;

h2_con11d(n,h2_channel,h)$( ord(h) = card(h) AND h2_sto_p_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         h2_sto_p_sw(n,h2_channel) * H2_STO_P_L(n,h2_channel,h) =e= h2_sto_p_sw(n,h2_channel) * H2_STO_P_L0(n,h2_channel) ;

h2_con11e(n,h2_channel,h)$( h2_sto_p_set(n, h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         h2_sto_p_sw(n,h2_channel) * H2_STO_P_L(n,h2_channel,h) =g= H2_N_STO(n,h2_channel) * h2_sto_p_phi_min(n,h2_channel) ;

* aux_bftrans
h2_con12(n,h2_channel,h)$h2_channel_avail_set(n,h2_channel)..
         H2_AUX_PRETRANS_OUT(n,h2_channel,h) =e= (1-h2_aux_pretrans_sw(n,h2_channel)*h2_eta_aux_pretrans (n,h2_channel)) * (sum(h2_tech,h2_bypass_1_sw(n,h2_tech,h2_channel) * H2_BYPASS_1(n,h2_tech,h2_channel,h)) + H2_STO_P_OUT(n,h2_channel,h)) ;
h2_con13(n,h2_channel,h)$( h2_aux_pretrans_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         H2_N_AUX_PRETRANS(n,h2_channel) =g=  H2_AUX_PRETRANS_OUT(n,h2_channel,h) /(1-h2_eta_aux_pretrans (n,h2_channel));

h2_con13b(n,h2_channel,h)$( h2_channel_avail_set(n,h2_channel) AND h2_trans_set(n,h2_channel) AND NOT h2_recon_set(n,h2_channel) )..
         H2_AUX_PRETRANS_OUT(n,h2_channel,h) =l= h2_LKW_cap(n,h2_channel)*( h2_mobility_sw(n,h2_channel)*h2_fill_station_nb(n)*H2_CHANNEL_SHARE(n,h2_channel) + h2_p2x_sw(n,h2_channel)*h2_fill_station_nb_p2x(n,h2_channel) );

*  Simplified_transporation
h2_con114(n,h2_channel,h)$h2_channel_avail_set(n,h2_channel)..
         H2_TRANS_OUT(n,h2_channel,h) =e=  H2_AUX_PRETRANS_OUT(n,h2_channel,h) * ( 1 - h2_trans_sw(n,h2_channel)*h2_trans_eta(n,h2_channel) ) ;
h2_con115(n,h2_channel,h)$( h2_trans_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         H2_N_TRANS(n,h2_channel) =g= H2_AUX_PRETRANS_OUT(n,h2_channel,h) ;

* Time_consuming_transportation
h2_con14a(n,h2_channel,h)$( h2_channel_avail_set(n,h2_channel) AND ( ord(h) > h2_trans_load_time(n,h2_channel) + h2_trans_unload_time(n,h2_channel) + h2_trans_dist(n,h2_channel)/ (2*50) ) AND h2_trans_set(n,h2_channel) )..
         H2_TRANS_OUT(n,h2_channel,h) =e= H2_AUX_PRETRANS_OUT(n,h2_channel,h - (h2_trans_load_time(n,h2_channel) + h2_trans_unload_time(n,h2_channel) + (h2_trans_dist(n,h2_channel)/ ( 2 * 50) ) ) ) * power( 1 - h2_trans_sw(n,h2_channel)*h2_trans_eta(n,h2_channel), max (0,h2_trans_dist(n,h2_channel)/ (2*50)) )  ;
h2_con14b(n,h2_channel,h)$ ( h2_channel_avail_set(n,h2_channel) AND ( ord(h) <= h2_trans_load_time(n,h2_channel) + h2_trans_unload_time(n,h2_channel)+ h2_trans_dist(n,h2_channel)/ (2*50) ) AND h2_trans_set(n,h2_channel) ) ..
         H2_TRANS_OUT(n,h2_channel,h) =e= H2_AUX_PRETRANS_OUT(n,h2_channel, h + ( card (h) -   h2_trans_load_time(n,h2_channel) - h2_trans_unload_time(n,h2_channel) - (h2_trans_dist(n,h2_channel) / ( 50 * 2 )) ) ) * power( (1 - h2_trans_sw(n,h2_channel) *  h2_trans_eta(n,h2_channel)),max(0,h2_trans_dist(n,h2_channel)/ (2*50)) ) ;

h2_con14c(n,h2_channel,h)$(h2_channel_avail_set(n,h2_channel) AND NOT h2_trans_set(n,h2_channel)) ..
         H2_TRANS_OUT(n,h2_channel,h) =e= H2_AUX_PRETRANS_OUT(n,h2_channel,h)  ;

h2_con15a(n,h2_channel,h)$( h2_trans_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         H2_N_AVAI_TRANS(n,h2_channel,h) =g=   H2_AUX_PRETRANS_OUT(n,h2_channel,h) ;
h2_con15b(n,h2_channel,h)$( h2_trans_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel))..
         H2_N_AVAI_TRANS(n,h2_channel,h) =e= H2_N_TRANS(n,h2_channel) - sum( hh , H2_AUX_PRETRANS_OUT(n,h2_channel,hh)$( ( ord(hh)<ord(h) AND ord(h)-ord(hh) < (h2_trans_load_time(n,h2_channel) + h2_trans_unload_time(n,h2_channel) + (h2_trans_dist(n,h2_channel)/50)) ) OR ( ord(h)-1 < (h2_trans_load_time(n,h2_channel) + h2_trans_unload_time(n,h2_channel) + (h2_trans_dist(n,h2_channel)/50)) AND card(hh)-ord(hh) < - ( ord (h) -1 - h2_trans_load_time(n,h2_channel) - h2_trans_unload_time(n,h2_channel) - (h2_trans_dist(n,h2_channel)/50) ) ) ) ) ;

* aux_bflp_storage
h2_con_1(n,h2_channel,h)$h2_channel_avail_set(n,h2_channel)..
         H2_AUX_BFLP_STO_OUT(n,h2_channel,h) =e= (1-h2_aux_bflp_sto_sw(n,h2_channel) * h2_eta_aux_bflp_sto (n,h2_channel)) * H2_AUX_BFLP_STO_IN(n,h2_channel,h) ;
h2_con_2(n,h2_channel,h)$( h2_aux_bflp_sto_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         H2_N_AUX_BFLP_STO(n,h2_channel) =g= H2_AUX_BFLP_STO_IN(n,h2_channel,h) ;

h2_con17e(n,h2_channel,h)$( h2_channel_avail_set(n,h2_channel) )..
         H2_AUX_BFLP_STO_IN(n,h2_channel,h) =e= H2_TRANS_OUT(n,h2_channel,h) - h2_bypass_2_sw(n,h2_channel) * H2_BYPASS_2(n,h2_channel,h)  ;

* lp_storage
h2_con16a(n,h2_channel,h)$( h2_lp_sto_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         H2_N_LP_STO(n,h2_channel) =g= H2_LP_STO_L(n,h2_channel,h) ;
h2_con16b(n,h2_channel,h)$( h2_lp_sto_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) AND NOT h2_recon_set(n,h2_channel)  )..
         H2_N_LP_STO(n,h2_channel) =l= ( h2_mobility_sw(n,h2_channel)*h2_fill_station_nb(n)*H2_CHANNEL_SHARE(n,h2_channel) + h2_p2x_sw(n,h2_channel)*h2_fill_station_nb_p2x(n,h2_channel) ) * h2_lp_sto_station_cap(n,h2_channel) ;
h2_con16c(n,h2_channel,h)$( h2_lp_sto_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) AND h2_recon_set(n,h2_channel)  )..
         H2_N_LP_STO(n,h2_channel) =l= h2_lp_sto_station_cap(n,h2_channel) ;

h2_con17a(n,h2_channel,h)$( ord(h) > 1 AND h2_channel_avail_set(n,h2_channel) )..
         h2_lp_sto_sw(n,h2_channel) * H2_LP_STO_L(n,h2_channel,h) =e= h2_lp_sto_sw(n,h2_channel) * H2_LP_STO_L(n,h2_channel,h-1) *( 1 - h2_lp_sto_eta_stat(n,h2_channel) ) +  H2_AUX_BFLP_STO_OUT(n,h2_channel,h) - H2_LP_STO_OUT(n,h2_channel,h) ;
h2_con17b(n,h2_channel,h)$( ord(h) = 1 AND h2_channel_avail_set(n,h2_channel) )..
         h2_lp_sto_sw(n,h2_channel) * H2_LP_STO_L(n,h2_channel,h) =e= h2_lp_sto_sw(n,h2_channel) * H2_LP_STO_L0(n,h2_channel) +  H2_AUX_BFLP_STO_OUT(n,h2_channel,h) - H2_LP_STO_OUT(n,h2_channel,h) ;
h2_con17c(n,h2_channel)$( h2_channel_avail_set(n,h2_channel) )..
         h2_lp_sto_sw(n,h2_channel) * h2_lp_sto_phi_ini(n,h2_channel) * H2_N_LP_STO(n,h2_channel) =g= h2_lp_sto_sw(n,h2_channel) * H2_LP_STO_L0(n,h2_channel) ;
h2_con17d(n,h2_channel,h)$( ord(h) = card(h) AND h2_lp_sto_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         h2_lp_sto_sw(n,h2_channel) * H2_LP_STO_L(n,h2_channel,h) =e= h2_lp_sto_sw(n,h2_channel) * H2_LP_STO_L0(n,h2_channel) ;

h2_con17g(n,h2_channel,h)$( h2_lp_sto_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         h2_lp_sto_sw(n,h2_channel) * H2_LP_STO_L(n,h2_channel,h)=g= H2_N_LP_STO(n,h2_channel) * h2_lp_sto_phi_min(n,h2_channel) ;

* dehydration_evaporation
h2_con18(n,h2_channel,h)$h2_channel_avail_set(n,h2_channel)..
         H2_DEHYD_EVAP_OUT(n,h2_channel,h) =e= (1-h2_dehyd_evap_sw(n,h2_channel) * h2_eta_dehyd_evap(n,h2_channel)) * H2_LP_STO_OUT(n,h2_channel,h) ;
h2_con19(n,h2_channel,h)$( h2_dehyd_evap_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         H2_N_DEHYD_EVAP(n,h2_channel) =g= H2_LP_STO_OUT(n,h2_channel,h) ;

* aux_bfMP_storage
h2_con_7(n,h2_channel,h)$h2_channel_avail_set(n,h2_channel)..
         H2_AUX_BFMP_STO_OUT(n,h2_channel,h) =e= (1-h2_aux_bfMP_sto_sw(n,h2_channel)*h2_eta_aux_bfmp_sto(n,h2_channel)) * H2_DEHYD_EVAP_OUT(n,h2_channel,h) ;
h2_con_8(n,h2_channel,h)$( h2_aux_bfmp_sto_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         H2_N_AUX_BFMP_STO(n,h2_channel) =g= H2_DEHYD_EVAP_OUT (n,h2_channel,h) ;

* MP_storage
h2_con_3(n,h2_channel,h)$( h2_MP_sto_set(n,h2_channel)AND h2_channel_avail_set(n,h2_channel) )..
         H2_N_MP_STO(n,h2_channel) =g= H2_MP_STO_L(n,h2_channel,h) ;
h2_con_4a(n,h2_channel,h)$( ord(h) > 1 AND h2_channel_avail_set(n,h2_channel) )..
         h2_MP_sto_sw(n,h2_channel) * H2_MP_STO_L(n,h2_channel,h) =e= h2_MP_sto_sw(n,h2_channel) * H2_MP_STO_L(n,h2_channel,h-1) *( 1 - h2_MP_sto_eta_stat(n,h2_channel) ) +   H2_AUX_BFMP_STO_OUT(n,h2_channel,h) - H2_MP_STO_OUT(n,h2_channel,h) ;
h2_con_4b(n,h2_channel,h)$( ord(h) = 1 AND h2_channel_avail_set(n,h2_channel) )..
         h2_MP_sto_sw(n,h2_channel) * H2_MP_STO_L(n,h2_channel,h) =e= h2_MP_sto_sw(n,h2_channel) * H2_MP_STO_L0(n,h2_channel) +   H2_AUX_BFMP_STO_OUT(n,h2_channel,h) - H2_MP_STO_OUT(n,h2_channel,h) ;
h2_con_4c(n,h2_channel)$( h2_channel_avail_set(n,h2_channel) )..
         h2_MP_sto_sw(n,h2_channel) * h2_MP_sto_phi_ini(n,h2_channel) * H2_N_MP_STO(n,h2_channel) =g= h2_MP_sto_sw(n,h2_channel) * H2_MP_STO_L0(n,h2_channel) ;
h2_con_4d(n,h2_channel,h)$( ord(h) = card(h) AND h2_MP_sto_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         h2_MP_sto_sw(n,h2_channel) * H2_MP_STO_L(n,h2_channel,h) =e= h2_MP_sto_sw(n,h2_channel) * H2_MP_STO_L0(n,h2_channel) ;
h2_con_4e(n,h2_channel,h)$( h2_MP_sto_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         h2_MP_sto_sw(n,h2_channel) * H2_MP_STO_L(n,h2_channel,h)=g= H2_N_MP_STO(n,h2_channel) * h2_MP_sto_phi_min(n,h2_channel) ;

h2_con_4f(n,h2_channel,h)$( h2_MP_sto_set(n,h2_channel)AND h2_channel_avail_set(n,h2_channel) AND NOT h2_recon_set(n,h2_channel))..
         H2_N_MP_STO(n,h2_channel) =l= ( h2_mobility_sw(n,h2_channel)*h2_fill_station_nb(n)*H2_CHANNEL_SHARE(n,h2_channel) + h2_p2x_sw(n,h2_channel)*h2_fill_station_nb_p2x(n,h2_channel) ) * h2_MP_sto_station_cap(n,h2_channel) ;

h2_con_4g(n,h2_channel,h)$( h2_MP_sto_set(n,h2_channel)AND h2_channel_avail_set(n,h2_channel)AND h2_recon_set(n,h2_channel))..
         H2_N_MP_STO(n,h2_channel) =l=  h2_MP_sto_station_cap(n,h2_channel) ;

* aux_bffilling_storage
h2_con21(n,h2_channel,h)$h2_channel_avail_set(n,h2_channel)..
         H2_AUX_BFHP_STO_OUT(n,h2_channel,h) =e= (1-h2_aux_bfhp_sto_sw(n,h2_channel)* h2_eta_aux_bfhp_sto(n,h2_channel)) *  H2_AUX_BFHP_STO_IN(n,h2_channel,h);

h2_con21b(n,h2_channel,h)$h2_channel_avail_set(n,h2_channel)..
H2_AUX_BFHP_STO_IN(n,h2_channel,h) =e= H2_MP_STO_OUT(n,h2_channel,h) + h2_bypass_2_sw(n,h2_channel) * H2_BYPASS_2(n,h2_channel,h);

h2_con22(n,h2_channel,h)$( h2_aux_bfhp_sto_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         H2_N_AUX_BFHP_STO(n,h2_channel) =g= H2_AUX_BFHP_STO_IN(n,h2_channel,h) ;

* filling_storage
h2_con24(n,h2_channel,h)$( h2_hp_sto_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         H2_N_HP_STO(n,h2_channel) =g= H2_HP_STO_L(n,h2_channel,h) ;
h2_con25a(n,h2_channel,h)$( ord(h) > 1 AND h2_channel_avail_set(n,h2_channel) )..
          h2_hp_sto_sw(n,h2_channel) * H2_HP_STO_L(n,h2_channel,h) =e= h2_hp_sto_sw(n,h2_channel) * H2_HP_STO_L(n,h2_channel,h-1) * ( 1 - h2_hp_sto_eta_stat(n,h2_channel) ) + H2_AUX_BFHP_STO_OUT(n,h2_channel,h) - H2_HP_STO_OUT(n,h2_channel,h) ;
h2_con25b(n,h2_channel,h)$( ord(h) = 1 AND h2_channel_avail_set(n,h2_channel) )..
         h2_hp_sto_sw(n,h2_channel) * H2_HP_STO_L(n,h2_channel,h) =e= h2_hp_sto_sw(n,h2_channel) * H2_HP_STO_L0(n,h2_channel) +H2_AUX_BFHP_STO_OUT(n,h2_channel,h) - H2_HP_STO_OUT(n,h2_channel,h) ;
h2_con25c(n,h2_channel,h)$( h2_hp_sto_set(n,h2_channel) AND ord(h) = card(h) AND h2_channel_avail_set(n,h2_channel) )..
         h2_hp_sto_sw(n,h2_channel) * H2_HP_STO_L(n,h2_channel,h) =e= h2_hp_sto_sw(n,h2_channel) * H2_HP_STO_L0(n,h2_channel) ;
h2_con25d(n,h2_channel,h)$( h2_hp_sto_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         h2_hp_sto_sw(n,h2_channel) * H2_HP_STO_L(n,h2_channel,h) =g= H2_N_HP_STO(n,h2_channel) * h2_hp_sto_phi_min(n,h2_channel) ;

h2_con25e(n,h2_channel,h)$( NOT h2_recon_set(n,h2_channel) AND h2_hp_sto_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         H2_N_HP_STO(n,h2_channel) =l= ( h2_mobility_sw(n,h2_channel)*h2_fill_station_nb(n)*H2_CHANNEL_SHARE(n,h2_channel) + h2_p2x_sw(n,h2_channel)*h2_fill_station_nb_p2x(n,h2_channel) ) * h2_hp_sto_station_cap(n,h2_channel) ;

h2_con25f(n,h2_channel,h)$(  h2_recon_set(n,h2_channel) AND h2_hp_sto_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         H2_N_HP_STO(n,h2_channel) =l= h2_hp_sto_station_cap(n,h2_channel) ;

* aux_bffuel
h2_con_5(n,h2_channel,h)$h2_channel_avail_set(n,h2_channel)..
         H2_AUX_BFFUEL_OUT(n,h2_channel,h) =e= (1-h2_aux_bffuel_sw(n,h2_channel)*h2_eta_aux_bffuel (n,h2_channel)) *  H2_HP_STO_OUT(n,h2_channel,h) ;
h2_con_6(n,h2_channel,h)$( h2_aux_bffuel_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         H2_N_AUX_BFFUEL(n,h2_channel) =g= H2_HP_STO_OUT(n,h2_channel,h) ;

* matching demand and supply
h2_con28a(n,h,h2_channel)$( h2_mobility_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         H2_AUX_BFFUEL_OUT(n,h2_channel,h) =e= H2_CHANNEL_SHARE(n,h2_channel)* d_h2(n,h) ;
h2_con28b(n)..
         sum( h2_channel , H2_CHANNEL_SHARE(n,h2_channel)$( h2_mobility_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) ) ) =e= 1 * 1$( sum(h, d_h2(n,h) ) <> 0  )  ;
* The condition: 1$( sum(h, d_h2(n,h) ) <> 0  ) allows for turning all H2 channels off if H2 demand is zero.

h2_con29(n,h,h2_channel)$( h2_p2x_set(n,h2_channel) AND h2_channel_avail_set(n,h2_channel) )..
         H2_AUX_BFFUEL_OUT(n,h2_channel,h) =e= d_p2x(n,h,h2_channel) * h2_channel_avail_sw(n,h2_channel) * h2_p2x_sw(n,h2_channel) ;

* aux_recon_site

h2_con31(n,h2_channel,h2_tech_recon,h)$( h2_recon_aux_set(n,h2_channel,h2_tech_recon) AND h2_channel_avail_set(n,h2_channel) )..
         H2_N_RECON_AUX(n,h2_channel,h2_tech_recon) =g= H2_RECON_AUX_OUT(n,h2_channel,h2_tech_recon,h) / (1-h2_eta_recon_aux(n,h2_channel,h2_tech_recon));
h2_con32(n,h2_channel,h)$h2_channel_avail_set(n,h2_channel)..
         sum( h2_tech_recon , (H2_RECON_AUX_OUT(n,h2_channel,h2_tech_recon,h)/(1-h2_recon_aux_sw(n,h2_channel,h2_tech_recon)*h2_eta_recon_aux(n,h2_channel,h2_tech_recon)))$h2_tech_recon_avail_set(n,h2_tech_recon) ) =e=  H2_AUX_BFFUEL_OUT(n,h2_channel,h)$( h2_channel_avail_set(n,h2_channel) AND h2_recon_set(n,h2_channel) ) ;

* recon
* h2_con33(n,h2_tech_recon,h)$(h2_tech_recon_avail_set(n,h2_tech_recon) AND NOT h2_bi_recon_set(n,h2_tech_recon) ) ..  "Old one with h2_bi_recon_set"
h2_con33(n,h2_tech_recon,h)$(h2_tech_recon_avail_set(n,h2_tech_recon)) ..
         H2_N_RECON(n,h2_tech_recon) =g= sum( h2_channel , H2_E_RECON_OUT(n,h2_channel,h2_tech_recon,h) $( h2_tech_recon_avail_set(n,h2_tech_recon) AND h2_channel_avail_set(n,h2_channel) AND h2_recon_set(n,h2_channel) ) ) ;
h2_con34(n,h2_channel,h2_tech_recon,h)..
         H2_E_RECON_OUT(n,h2_channel,h2_tech_recon,h) =e= h2_channel_avail_sw(n,h2_channel) * h2_recon_sw(n,h2_channel) * h2_tech_recon_sw(n,h2_tech_recon) * h2_recon_efficiency(n,h2_tech_recon) * H2_RECON_AUX_OUT(n,h2_channel,h2_tech_recon,h) ;

$ontext
$offtext

%DIETERgms%$include "%MODELDIR%dieterpy_4_developnewconstr.gms"

********************************************************************************
***** MODEL *****
********************************************************************************

model DIETER /
obj

con1a_bal

con2a_loadlevel
con2b_loadlevelstart

con3a_maxprod_dispatchable
%reserves%$ontext
  con3b_minprod_dispatchable
  con3c_flex_reserves_spin
  con3d_flex_reserves_nonspin
$ontext
$offtext
con3e_maxprod_res
%reserves%$ontext
  con3f_minprod_res
$ontext
$offtext

con4a_stolev_start
con4b_stolev
con4c_stolev_max
con4d_maxin_sto
con4e_maxout_sto
%reserves%$ontext
  con4f_resrv_sto
  con4g_resrv_sto
$ontext
$offtext
con4h_maxout_lev
con4i_maxin_lev
con4j_ending
con4k_PHS_EtoP

con5a_minRES
con5b_max_energy

%DSM%$ontext
con6a_DSMcurt_duration_max
con6b_DSMcurt_max

con7a_DSMshift_upanddown
con7b_DSMshift_granular_max
con7c_DSM_distrib_up
con7d_DSM_distrib_do
*con_7e_DSMshift_recovery
$ontext
$offtext

con8a_max_I_power
con8b_max_I_sto_e
con8c_max_I_sto_p_in
con8d_max_I_sto_p_out
%DSM%$ontext
con8e_max_I_dsm_cu
con8f_max_I_dsm_shift_pos
$ontext
$offtext
con8j_max_I_ntc
con8k_max_I_rsvr_e
con8l_max_I_rsvr_p_out

%reserves_endogenous%$ontext
 con9a_reserve_prov_endogenous
 con9b_reserve_prov_PR_endogenous
$ontext
$offtext

%reserves_exogenous%$ontext
 con9a_reserve_prov_exogenous
 con9b_reserve_prov_PR_exogenous
$ontext
$offtext

%EV%$ontext
 con10a_ev_ed
%EV_EXOG% con10b_ev_chargelev_start
 con10c_ev_chargelev
 con10d_ev_chargelev_max
%EV_EXOG% con10e_ev_maxin
%EV_EXOG% con10f_ev_maxout
%EV_EXOG% con10g_ev_chargelev_ending
$ontext
$offtext
%EV%$ontext
%reserves%$ontext
%EV_EXOG% con10h_ev_minin
%EV_EXOG% con10i_ev_maxin_lev
%EV_EXOG% con10j_ev_minout
%EV_EXOG% con10k_ev_maxout_lev
$ontext
$offtext
%EV%$ontext
%EV_EXOG%$ontext
 con10l_ev_exog
$ontext
$offtext

%prosumage%$ontext
con8g_max_pro_res
con8h_max_pro_sto_e
con8i_max_sto_pro_p
con11a_pro_distrib
con11b_pro_balance
con11c_pro_selfcon
con11d_pro_stolev_PRO2PRO
con11e_pro_stolev_PRO2M
con11f_pro_stolev_M2PRO
con11g_pro_stolev_M2M
con11h_1_pro_stolev_start_PRO2PRO
con11h_2_pro_stolev_start_PRO2M
con11h_3_pro_stolev_start_M2PRO
con11h_4_pro_stolev_start_M2M
con11i_pro_stolev
con11j_pro_stolev_max
con11k_pro_maxin_sto
con11l_pro_maxout_sto
con11m_pro_maxout_lev
con11n_pro_maxin_lev
con11o_pro_ending
$ontext
$offtext

con12a_max_f
con12b_min_f

con13a_rsvrlev_start
con13b_rsvrlev
con13c_rsvrlev_max
con13d_maxout_rsvr
con13e_resrv_rsvr
con13f_maxout_lev
con13g_ending
*con13h_smooth
con13i_min_level
*con13j_min_FLH

%heat%$ontext
con14a_heat_balance
con14b_dhw_balance
con14c_sets_level
con14d_sets_level_start
con14e_sets_maxin
con14f_sets_maxout
con14h_sets_maxlev

con14i_sets_aux_dhw_level
con14j_sets_aux_dhw_level_start
con14k_sets_aux_dhw_maxin
con14l_sets_aux_dhw_minin
con14m_sets_aux_dhw_maxlev

con14n_hp_in
con14o_hp_maxin
con14q_storage_elec_in
con14r_storage_elec_maxin
con14t_storage_level
con14u_storage_level_start
con14v_storage_maxlev
$ontext
$offtext

%heat%$ontext
%reserves%$ontext
con14g_sets_minin
con14p_hp_minin
con14s_storage_elec_minin
$ontext
$offtext


%P2H2%$ontext

* prod
h2_con2a
h2_con2b
h2_con3

* aux_prod_site
h2_con4
h2_con5
h2_con6

* hydration_liquefaction
h2_con7
h2_con8

* prod_site_storage
h2_con9
h2_con10
h2_con11a
h2_con11b
h2_con11c
h2_con11d
h2_con11e

* aux_bftans
h2_con12
h2_con13
h2_con13b

* aux_bflp_storage
h2_con_1
h2_con_2

* lp_storage
h2_con16a
h2_con16b
h2_con16c
h2_con17a
h2_con17b
h2_con17c
h2_con17d
h2_con17e

h2_con17g

* dehydration_evaporation
h2_con18
h2_con19

* aux_bfMP_storage
h2_con_7
h2_con_8

* MP_storage
h2_con_3
h2_con_4a
h2_con_4b
h2_con_4c
h2_con_4d
h2_con_4e
h2_con_4f
h2_con_4g

* aux_bffilling_storage
h2_con21
h2_con21b
h2_con22

* filling_storage
h2_con24
h2_con25a
h2_con25b
h2_con25c
h2_con25d
h2_con25e
h2_con25f

* aux_bffuel
h2_con_5
h2_con_6

* matching demand and supply
h2_con28a
h2_con28b
h2_con29

* aux_recon_site
h2_con31
h2_con32

* recon
h2_con33
h2_con34

$ontext
$offtext

%P2H2%$ontext
%Time_consuming_transportation%$ontext
* transportation
h2_con14a
h2_con14b
h2_con14c
h2_con15a
h2_con15b

$ontext
$offtext

%P2H2%$ontext
%Simplified_transporation%$ontext
* transportation
h2_con114
h2_con115

$ontext
$offtext

%DIETERgms%$include "%MODELDIR%dieterpy_5_includenewconstr.gms"

/;
