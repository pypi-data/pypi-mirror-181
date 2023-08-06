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

***************  SETS  *********************************************************

***** Sets used in the model *****
Sets

i /0*23/                 Set defining the 24 hours of a day
tech                     Generation technologies
 dis(tech)               Dispatchable generation technologies
 nondis(tech)            Nondispatchable generation technologies
 con(tech)               Conventional generation technologies
 res(tech)               Renewable generation technologies
sto                      Storage technologies
rsvr                     Reservoir technologies
dsm                      DSM technologies
 dsm_shift(dsm)          DSM load shifting technologies
 dsm_curt(dsm)           DSM load curtailment technologies
h                        Hours
n                        Nodes
l                        Lines
ev                       EV types
reserves                         Reserve qualities
 reserves_up(reserves)           Positive reserves
 reserves_do(reserves)           Negative reserves
 reserves_spin(reserves)         Spinning reserves
 reserves_nonspin(reserves)      Nonspinning reserves
 reserves_prim(reserves)         Primary reserves
 reserves_nonprim(reserves)      Nonprimary reserves
 reserves_prim_up(reserves)      Primary positive reserves
 reserves_nonprim_up(reserves)   Nonprimary positive reserves
 reserves_prim_do(reserves)      Primary negative reserves
 reserves_nonprim_do(reserves)   Nonprimary negative reserves
bu                       Building archtypes
ch                       Heating combination type
 hst(ch)                 Heating technology that feeds to storage
 hp(ch)                  Heat pump technologies
 hel(ch)                 Hybrid electric heating technologies - electric part
 hfo(ch)                 Hybrid electric heating technologies - fossil part
h2_tech                          Set for the production technology for H2
h2_channel                       Set for the distribution channel for H2
h2_tech_recon                    Set for the reconversion technology for H2

h2_prod_aux_set(n,h2_tech,h2_channel)           Subset for auxiliary process at production site
h2_hyd_liq_set(n,h2_channel)                    Subset for hydrogenation or liquefaction
h2_sto_p_set(n,h2_channel)                      Subset for production site storage
h2_lp_sto_set(n,h2_channel)                     Subset for LP storage
h2_aux_pretrans_set(n,h2_channel)               Subset for pre-transportation auxiliaries
h2_aux_bfhp_sto_set(n,h2_channel)               Subset for HP storage auxiliaries
h2_hp_sto_set(n,h2_channel)                     Subset for HP storage
h2_dehyd_evap_set(n,h2_channel)                 Subset for dehydration or evaporation
h2_trans_set(n,h2_channel)                      Subset for transportation
h2_aux_bflp_sto_set(n,h2_channel)               Subset for LP storage auxiliaries
h2_aux_bfMP_sto_set(n,h2_channel)               Subset for MP storage auxiliaries
h2_MP_sto_set(n,h2_channel)                     Subset for MP storage
h2_aux_bffuel_set(n,h2_channel)                 Subset for pre-fueling auxiliaries
h2_channel_wo_decent_set(h2_channel)            Subset for those technologies that are not decentralized
h2_tech_avail_set (n,h2_tech)                   Subset for those production technologies that are actually available in a country
h2_channel_avail_set(n,h2_channel)              Subset for those distribution channels that are actually available in a country
h2_tech_recon_avail_set                         Subset for those reconversion technologies that are actually available in a country
h2_recon_set                                    Subset for those channels that can also be used for re-conversion
h2_mobility_set                                 Subset for those channels that can also be used for h2 mobility
h2_p2x_set                                      Subset for those channels that can also be used for p2x other than hydrogen for mobility
h2_recon_aux_set                                Subset for auxiliaries at re-conversion site
* h2_bi_recon_set(n,h2_tech_recon)                Subset for bidirection re-convertion technologies

***** Sets used for data upload *****
headers_tech                     Generation technologies - upload headers
 tech_dispatch                   Generation technologies - dispatchable or nondispatchable
 tech_res_con                    Generation technologies - renewable or "conventional"
headers_sto                      Storage technologies - upload headers
headers_reservoir                Reservoir technologies - upload headers
headers_dsm                      DSM technologies - upload headers
 dsm_type                        DSM technologies - shifting or curtailment
headers_time                     Temporal data - upload headers
headers_topology                 Spatial data - upload headers
headers_ev                       EV data - upload headers
headers_time_ev                  EV temporal data - upload headers
headers_prosumage_generation     Prosumage generation data - upload headers
headers_prosumage_storage        Prosumage storage data - upload headers
headers_reserves                 Reserve data - upload headers
 reserves_up_down                Reserve data - positive and neagtive reserves
 reserves_spin_nonspin           Reserve data - spinning and nonspinning reserves
 reserves_prim_nonprim           Reserve data - primary and nonprimary reserves
headers_heat                     Heat data - upload headers
 heat_storage                    Heat data - storage technologies
 heat_hp                         Heat data - heat pump technologies
 heat_elec                       Heat data - hybrid heating technologies - electric part
 heat_fossil                     Heat data - hybrid heating technologies - fossil part
headers_h2_parameters_table1     H2 input data - upload headers
headers_h2_parameters_table2     H2 input data - upload headers
headers_h2_parameters_table3     H2 input data - upload headers
headers_h2_parameters_table4     H2 input data - upload headers
headers_h2_parameters_table5     H2 input data - upload headers
headers_h2_parameters_table6     H2 input data - upload headers
headers_h2_parameters_table7     H2 input data - upload headers
headers_h2_parameters_table8     H2 input data - upload headers
headers_h2_parameters_table9     H2 input data - upload headers
headers_h2_parameters_table10    H2 input data - upload headers

headers_nodes                    parameters per nodes - upload headers
headers_scalar                   parameters as scalar - upload headers
;

***************  PARAMETERS  ***************************************************

Parameters

***** Generation technologies *****
*--- Variable and fixed costs ---*
eta(n,tech)              Efficiency of conventional technologies [0 1]
carbon_content(n,tech)   CO2 emissions per fuel unit used [tons per MWh thermal]
c_up(n,tech)             Load change costs UP [EUR per MWh]
c_do(n,tech)             Load change costs DOWN [EUR per MWh]
c_fix(n,tech)            Annual fixed costs [EUR per MW per year]
c_vom(n,tech)            Variable O&M costs [EUR per MWh]
CO2price(n,tech)         CO2 price in [EUR per ton]
avail(n,tech)            Power plant availability - temporally flat [0 1]

*--- Investment ---*
c_inv_overnight(n,tech)  Investment costs: Overnight [EUR per MW]
lifetime_tech(n,tech)      Investment costs: technical lifetime [a]
recovery(n,tech)         Investment costs: Recovery period according to depreciation tables [a]
interest_rate_tech(n,tech)    Investment costs: Interest rate [%]
m_p(n,tech)              Investment: maximum installable capacity per technology [MW]
m_e(n,tech)              Investment: maximum installable energy [TWh per a]

*--- Flexibility ---*
grad_per_min(n,tech)     Maximum load change relative to installed capacity [% of installed capacity per minute]

***** Fuel and CO2 costs *****
fuelprice(n,tech)        Fuel price conventionals [EUR per MWh thermal]

***** Renewables *****
c_cu(n,tech)             Hourly Curtailment costs for renewables [Euro per MW]
phi_min_res(n)      Minimum renewables share [0 1]

***** Storage *****
*--- Variable and fixed costs ---*
c_m_sto_in(n,sto)       Marginal costs of storing in [EUR per MWh]
c_m_sto_out(n,sto)      Marginal costs of storing out [EUR per MWh]
eta_sto_in(n,sto)       Storage efficiency storing in [0 1]
eta_sto_out(n,sto)      Storage efficiency storing out [0 1]
eta_sto_self(n,sto)     Stroage self discharge per hour [0 1]
phi_sto_ini(n,sto)      Initial storage level [0 1]
etop_max(n,sto)         Maximum E to P ratio of storage types [#]
c_fix_sto_p_in(n,sto)   Annual fixed costs storage power in [EUR per MW]
c_fix_sto_p_out(n,sto)  Annual fixed costs storage power out [EUR per MW]
c_fix_sto_e(n,sto)      Annual fixed costs storage energy [EUR per MWh]
avail_sto(n,sto)        Storage availability - temporally flat [0 1]

*--- Investment ---*
c_inv_overnight_sto_e(n,sto)       Investment costs for storage energy: Overnight [EUR per MWh]
c_inv_overnight_sto_p_in(n,sto)    Investment costs for storage capacity storing in: Overnight [EUR per MW]
c_inv_overnight_sto_p_out(n,sto)   Investment costs for storage capacity storing out: Overnight [EUR per MW]
m_sto_e(n,sto)                     Investment into storage: maximum installable energy [MWh]
m_sto_p_in(n,sto)                  Investment into storage: maximum installable power [MW]
m_sto_p_out(n,sto)                 Investment into storage: maximum installable power [MW]
lifetime_sto(n,sto)
interest_rate_sto(n,sto) 

***** Reservoir*****
*--- Variable and fixed costs ---*
c_m_rsvr(n,rsvr)                 Marginal costs of generating energy from reservoir [EUR per MWh]
eta_rsvr_out(n,rsvr)             Generation efficiency [0 1]
phi_rsvr_ini(n,rsvr)             Initial reservoir level [0 1]
c_fix_rsvr_p_in(n,rsvr)          Annual fixed costs inflow [EUR per MW per a]
c_fix_rsvr_p_out(n,rsvr)         Annual fixed costs generation [EUR per MW per a]
c_fix_rsvr_e(n,rsvr)             Annual fixed costs energy [EUR per MWh per a]
phi_rsvr_min(n)             Minimum hourly reservoir outflow as fraction of annual energy [0 1]
phi_rsvr_lev_min(n,rsvr)         Minimum filling level [0 1]
avail_rsvr(n,rsvr)               Reservoir availability - temporally flat [0 1]
min_flh(n,rsvr)

*--- Investment ---*
c_inv_overnight_rsvr_p_in(n,rsvr)        Investment costs for reservoir capacity in: Overnight [EUR per MW]
c_inv_overnight_rsvr_p_out(n,rsvr)       Investment costs for reservoir capacity out: Overnight [EUR per MW]
c_inv_overnight_rsvr_e(n,rsvr)           Investment costs for reservoir energy: Overnight [EUR per MWh]
inv_lifetime_rsvr(n,rsvr)                Investment costs for reservoir: technical lifetime [a]
inv_interest_rsvr(n,rsvr)                Investment costs for reservoir: Interest rate [%]
m_rsvr_e(n,rsvr)                         Investment into reservoir: maximum installable energy [MWh]
* m_rsvr_p_in                              Investment into reservoir: maximum installable capacity [MW]
m_rsvr_p_out(n,rsvr)                     Investment into reservoir: maximum installable capacity [MW]

***** DSM *****
*--- Variable and fixed costs ---*
c_m_dsm_cu(n,dsm)       DSM: hourly costs of load curtailment [EUR per MWh]
c_m_dsm_shift(n,dsm)     DSM: costs for load shifting [EUR per MWh]
c_fix_dsm_cu(n,dsm)      Annual fixed costs load curtailment capacity [EUR per MW per a]
c_fix_dsm_shift(n,dsm)   Annual fixed costs load shifting capacity [EUR per MW per a]

*--- Flexibility, efficiency, recovery ---*
t_dur_dsm_cu(n,dsm)      DSM: Maximum duration load curtailment [h]
t_off_dsm_cu(n,dsm)      DSM: Minimum recovery time between two load curtailment instances [h]

t_dur_dsm_shift(n,dsm)   DSM: Maximum duration load shifting [h]
t_off_dsm_shift(n,dsm)   DSM: Minimum recovery time between two granular load upshift instances [h]
eta_dsm_shift(n,dsm)     DSM: Efficiency of load shifting technologies [0 1]

*--- Investment ---*
c_inv_overnight_dsm_cu(n,dsm)            Investment costs for DSM load curtailment: Overnight [EUR per MW]
c_inv_overnight_dsm_shift(n,dsm)         Investment costs for DSM load shifting: Overnight [EUR per MW]
inv_lifetime_dsm_cu(n,dsm)               Investment costs for DSM load curtailment: lifetime [a]
inv_lifetime_dsm_shift(n,dsm)            Investment costs for DSM load shifting: liefetime [a]
inv_interest_dsm_cu(n,dsm)               Investment costs for DSM load curtailment: Interest rate [%]
inv_interest_dsm_shift(n,dsm)            Investment costs for DSM load shifting: Interest rate [%]
m_dsm_cu(n,dsm)                          DSM: Maximum installable capacity load curtailment [MW]
m_dsm_shift(n,dsm)                       DSM: Maximum installable capacity load shifting [MW]

***** Time Data *****
d(n,h)                        Demand hour h [MWh]
phi_res(n,tech,h)                  Renewables availability technology res in hour h [0 1]
* phi_ror                  Run-of-river availability technology ror in hour h [0 1]
rsvr_in(n,rsvr,h)                  Reservoir inflow in hour h [0 1]
* n_ev_p_upload            Power rating of the charging connection in hour h [MW - 0 when car is in use or parked without grid connection]
* ev_ed_upload             Electricity demand for mobility vehicle profile ev in hour h [MW]
* ev_ged_exog_upload       Electricity demand for mobility in case of uncontrolled charging vehicle profile ev in hour h [MW]
phi_reserves_call(n,reserves,h)        Hourly share of reserve provision that is actually activated [0 1]
reserves_exogenous(n,reserves,h)       Hourly reserve provision [MW]

***** Transmission *****
*--- Investment ---*
c_inv_overnight_ntc(l)       Investment costs in: overnight [EUR per MW and km]
c_fix_ntc_per_km(l)          Fixed costs [EUR per MW and km per a]
inv_lifetime_ntc(l)          Investment costs: technical lifetime [a]
inv_recovery_ntc(l)          Investment costs: Recovery period in [a]
inv_interest_ntc(l)          Investment costs: Interest rate [%]
m_ntc(l)                     Investment into NTC: maximum installable capacity [MW]
c_m_ntc(l)                   Variable O&M costs for line use [EUR per MWh]

*--- Topology and distance ---*
inc(l,n)              Incidence index of link l on node n
dist(l)             Distance covered by link l [km]
loss_ntc(l)         Cross-border transmission losses [% per 100km]

***** Electric vehicles *****
*--- Costs and attributes ---*
c_m_ev_dis(n,ev)       Marginal costs of discharging V2G [EUR per MWh]
c_m_ev_cha(n,ev)       Marginal costs of discharging V2G [EUR per MWh]
pen_phevfuel(n,ev)     Penalty for non-electric PHEV operation mode [EUR per MWh]
eta_ev_in(n,ev)        Electric vehicle efficiency of charging (G2V) [0 1]
eta_ev_out(n,ev)       Electric vehicle efficiency of discharging (V2G) [0 1]
phi_ev_ini(n,ev)       Electric vehicle charging level in initial period [0 1]

n_ev_e(n,ev)           Electric vehicle battery capacity [MWh]
ev_quant(n)         Overall number of electirc vehicles [#]
phi_ev(n,ev)           Share of electric vehicles per load profile in actual scenario [0 1]
ev_phev(n,ev)          Defines whether an electric vehicle is a PHEV REEV [1 if yes 0 otherwise]

*--- Temporal data ---*
n_ev_p(n,ev,h)           Electric vehicle power rating [MWh]
ev_ed(n,ev,h)            Electric vehicle electricity demand [MWh]
ev_ged_exog(n,ev,h)      Electric vehicle grid electricity demand for exogenous charging pattern [MWh]

***** Prosumage *****
phi_pro_load(n)             Share of prosumagers among total load [0 1]
phi_pro_self(n)             Minimum self-generation shares for prosumagers [0 1]
m_res_pro(n,tech)                Maximum installable: renewables capacity [MW]
m_sto_pro_e(n,sto)              Maximum installable: storage energy [MWh]
m_sto_pro_p(n,sto)              Maximum installable: storage capacity [MW]
phi_sto_pro_ini(n,sto)          Prosumagers initial storage loading [0 1]

***** Reserves *****
phi_reserves_share(n,reserves)       Shares of SRL and MRL up and down [0 1]
reserves_intercept(n,reserves)       Intercept of regression line determining reserves demand
reserves_slope(n,reserves,tech)           Slope of regression line determining reserves demand
reserves_reaction(n,reserves)        Activation reaction time for reserves qualities [min]
phi_reserves_pr_up(n)       Positive primary reserves fraction of total nonprimary reserves demand [0 1]
phi_reserves_pr_do(n)       Negative primary reserves fraction of total nonprimary reserves demand [0 1]
*reserves_exog

***** Heat *****
*--- Time data ---*
dh(n,bu,ch,h)                       Hourly heat demand [MWh per m2]
temp_source(n,bu,ch,h)              Heat pumps - source temperature [�Celsius]
d_dhw(n,bu,ch,h)                    Hourly DHW demand [MWh per m2]
nets_profile(h)          Hourly exogenous heat demand by nonsmart night-time storage heaters [MWh per m2]

*--- Technololgy attributes ---*
phi_heat_type(n,bu,ch)            Share of heating type ch per building archetype bu [0 1]
eta_heat_stat(n,bu,ch)            Static efficiency for heating technologies [0 1]
eta_heat_dyn(n,bu,ch)             Static efficiency for heating technologies [0 1]
eta_dhw_aux_stat(n,bu,ch)         Static efficiency for auxiliary DHW technologies [0 1]
n_heat_p_in(n,bu,ch)              Maximum power inflow into heating technologies [MW]
n_heat_p_out(n,bu,ch)             Maximum power outflow from heating technologies [MW]
n_heat_e(n,bu,ch)                 Maximum energy level of heating storage technologies [MWh]
n_sets_p_in(n,bu,ch)              SETS - Power rating - electricity intake [MW]
n_sets_p_out(n,bu,ch)             SETS - Power rating - heat output [MW]
n_sets_e(n,bu,ch)                 SETS - Energy storage capacity [MWh]
n_sets_dhw_p_in(n,bu,ch)          SETS auxiliary DHW module - power rating - electricity intake [MW]
n_sets_dhw_p_out(n,bu,ch)         SETS auxiliary DHW module - power rating - DHW output [MW]
n_sets_dhw_e(n,bu,ch)             SETS auxiliary DHW module - energy storage capacity [MWh]
phi_heat_ini(n,bu,ch)             Inititial storage level of heating technologies [0 1]
temp_sink(n,bu,ch)                Heat pumps - sink temperature [�Celsius]
pen_heat_fuel(n,bu,ch)            Penalty term for non-electric fuel usage for hybrid heating technologies [EUR per MWh]
area_floor(n,bu,ch)               Floor area subject to specific heating technology in specific building type [m2]
* theta_night                       Indicator for night hours {0 1}

***** P2H2 *****

*--- Switches ---*
h2_tech_avail_sw(n,h2_tech)                    Switch for production technologie
h2_channel_avail_sw(n,h2_channel)                 Switch for distribution channels
h2_tech_recon_sw(n,h2_tech_recon)                    Switch for reconversion technologie

h2_recon_sw(n,h2_channel)                         Switch for re-convertion process
h2_mobility_sw(n,h2_channel)                      Switch for p2h2 for mobility
h2_p2x_sw(n,h2_channel)                           Switch for p2x process other than h2 for mobility

h2_prod_aux_sw(n,h2_tech,h2_channel)                      Switch for production auxiliaries
h2_hyd_liq_sw(n,h2_channel)                       Switch for hydrogenation and liquefaction
h2_sto_p_sw(n,h2_channel)                         Switch for storage at production sites
h2_lp_sto_sw(n,h2_channel)                        Switch for LP storage
h2_aux_pretrans_sw(n,h2_channel)                  Switch for pre-transportation auxiliaries
h2_aux_bfhp_sto_sw(n,h2_channel)                  Switch for HP storage auxiliaries
h2_hp_sto_sw(n,h2_channel)                        Switch for HP storage
h2_dehyd_evap_sw(n,h2_channel)                    Switch for dehydration and evaporation
h2_trans_sw(n,h2_channel)                         Switch for transportation
h2_dehyd_evap_gas_sw(n,h2_channel)                Switch for dehydration and evaporation gas
h2_aux_bflp_sto_sw(n,h2_channel)                  Switch for LP storage auxiliaries
h2_aux_bfMP_sto_sw(n,h2_channel)                  Switch for MP storage auxiliaries
h2_aux_bffuel_sw(n,h2_channel)                    Switch for pre-fueling auxiliaries
h2_recon_aux_sw(n,h2_channel,h2_tech_recon)                     Switch for re-conversion auxiliaries
h2_MP_sto_sw(n,h2_channel)                        Switch for MP storage
h2_bypass_1_sw(n,h2_tech,h2_channel)                      Switch for bypass 1
h2_bypass_2_sw(n,h2_channel)                      Switch for bypass 2
* h2_bidirect_sw                      Switch for bidirect technologies

*--- Technological Parameters---
h2_efficiency(n,h2_tech)                                   See excel sheet (data_input.xlsx)
h2_prod_scale(n,h2_tech)                                   See excel sheet (data_input.xlsx)
h2_prod_lifetime(n,h2_tech)                                See excel sheet (data_input.xlsx)
h2_prod_aux_lifetime(n,h2_tech,h2_channel)                            See excel sheet (data_input.xlsx)
h2_hyd_liq_lifetime(n,h2_channel)                             See excel sheet (data_input.xlsx)
h2_sto_p_lifetime(n,h2_channel)                               See excel sheet (data_input.xlsx)
h2_sto_p_lifetime_alt                           See excel sheet (data_input.xlsx)
h2_lp_sto_lifetime(n,h2_channel)                              See excel sheet (data_input.xlsx)
h2_aux_pretrans_lifetime(n,h2_channel)                        See excel sheet (data_input.xlsx)
h2_trans_lifetime(n,h2_channel)                               See excel sheet (data_input.xlsx)
h2_aux_bfhp_sto_lifetime(n,h2_channel)                        See excel sheet (data_input.xlsx)
h2_hp_sto_lifetime(n,h2_channel)                              See excel sheet (data_input.xlsx)
h2_dehyd_evap_lifetime(n,h2_channel)                          See excel sheet (data_input.xlsx)
h2_aux_bflp_sto_lifetime(n,h2_channel)                        See excel sheet (data_input.xlsx)
h2_aux_bfMP_sto_lifetime(n,h2_channel)                        See excel sheet (data_input.xlsx)
h2_MP_sto_lifetime(n,h2_channel)                              See excel sheet (data_input.xlsx)
h2_aux_bffuel_lifetime(n,h2_channel)                          See excel sheet (data_input.xlsx)
h2_sto_p_type(n,h2_channel)                                   See excel sheet (data_input.xlsx)
h2_prod_aux_ed(n,h2_tech,h2_channel)                                  See excel sheet (data_input.xlsx)
h2_hyd_liq_ed(n,h2_channel)                                    See excel sheet (data_input.xlsx)
h2_sto_p_ed(n,h2_channel)                                      See excel sheet (data_input.xlsx)
h2_sto_p_ed_alt                                 See excel sheet (data_input.xlsx)
h2_lp_sto_ed(n,h2_channel)                                     See excel sheet (data_input.xlsx)
h2_aux_pretrans_ed(n,h2_channel)                               See excel sheet (data_input.xlsx)
h2_trans_eta(n,h2_channel)                                     See excel sheet (data_input.xlsx)
h2_aux_bfhp_sto_ed(n,h2_channel)                               See excel sheet (data_input.xlsx)
h2_hp_sto_ed(n,h2_channel)                                     See excel sheet (data_input.xlsx)
h2_dehyd_evap_ed(n,h2_channel)                                 See excel sheet (data_input.xlsx)
h2_dehyd_evap_gas(n,h2_channel)                                See excel sheet (data_input.xlsx)
h2_sto_p_eta_stat(n,h2_channel)                                See excel sheet (data_input.xlsx)
h2_sto_p_eta_stat_alt                           See excel sheet (data_input.xlsx)
h2_hp_sto_eta_stat(n,h2_channel)                               See excel sheet (data_input.xlsx)
h2_lp_sto_eta_stat(n,h2_channel)                               See excel sheet (data_input.xlsx)
h2_hp_sto_phi_ini(n,h2_channel)                                See excel sheet (data_input.xlsx)
h2_sto_p_phi_ini(n,h2_channel)                                 See excel sheet (data_input.xlsx)
h2_sto_p_phi_min(n,h2_channel)                                 See excel sheet (data_input.xlsx)
h2_sto_p_phi_ini_alt                            See excel sheet (data_input.xlsx)
h2_lp_sto_phi_ini(n,h2_channel)                                See excel sheet (data_input.xlsx)
h2_lp_sto_phi_min(n,h2_channel)                                See excel sheet (data_input.xlsx)
h2_hp_sto_phi_min(n,h2_channel)                                See excel sheet (data_input.xlsx)
h2_recon_aux_lifetime(n,h2_channel,h2_tech_recon)                           See excel sheet (data_input.xlsx)
h2_recon_aux_ed(n,h2_channel,h2_tech_recon)                                 See excel sheet (data_input.xlsx)
h2_recon_lifetime(n,h2_tech_recon)                               See excel sheet (data_input.xlsx)
h2_recon_efficiency(n,h2_tech_recon)                             See excel sheet (data_input.xlsx)
h2_eta_prod_aux(n,h2_tech,h2_channel)                                 See excel sheet (data_input.xlsx)
h2_eta_hyd(n,h2_channel)                                      See excel sheet (data_input.xlsx)
h2_eta_aux_pretrans(n,h2_channel)                             See excel sheet (data_input.xlsx)
h2_eta_dehyd_evap(n,h2_channel)                               See excel sheet (data_input.xlsx)
h2_eta_aux_bfhp_sto(n,h2_channel)                             See excel sheet (data_input.xlsx)
h2_eta_recon_aux(n,h2_channel,h2_tech_recon)                                See excel sheet (data_input.xlsx)
h2_lp_sto_station_cap(n,h2_channel)                           See excel sheet (data_input.xlsx)
h2_MP_sto_station_cap(n,h2_channel)                           See excel sheet (data_input.xlsx)
h2_hp_sto_station_cap(n,h2_channel)                           See excel sheet (data_input.xlsx)
h2_fill_station_cap(n)                             See excel sheet (data_input.xlsx)
h2_fill_station_nb(n)                              Endogenous
h2_fill_station_nb_p2x(n,h2_channel)                          Endogenous
h2_aux_bflp_sto_ed(n,h2_channel)                              See excel sheet (data_input.xlsx)
h2_eta_aux_bflp_sto(n,h2_channel)                             See excel sheet (data_input.xlsx)
h2_aux_bfMP_sto_ed(n,h2_channel)                              See excel sheet (data_input.xlsx)
h2_eta_aux_bfMP_sto(n,h2_channel)                             See excel sheet (data_input.xlsx)
h2_MP_sto_ed(n,h2_channel)                                    See excel sheet (data_input.xlsx)
h2_MP_sto_eta_stat(n,h2_channel)                              See excel sheet (data_input.xlsx)
h2_MP_sto_phi_ini(n,h2_channel)                               See excel sheet (data_input.xlsx)
h2_MP_sto_phi_min(n,h2_channel)                               See excel sheet (data_input.xlsx)
h2_aux_bffuel_ed(n,h2_channel)                                See excel sheet (data_input.xlsx)
h2_eta_aux_bffuel(n,h2_channel)                               See excel sheet (data_input.xlsx)
h2_trans_load_time(n,h2_channel)                              See excel sheet (data_input.xlsx)
h2_trans_unload_time(n,h2_channel)                            See excel sheet (data_input.xlsx)

max_d_h2(n)                                        Endogenous parameter
max_d_p2x(n,h2_channel)                                       Endogenous parameter

*--- Cost Parameters ---
h2_interest_rate(n)                               See excel sheet (data_input.xlsx)
h2_trans_dist(n,h2_channel)                                  See excel sheet (data_input.xlsx)
h2_prod_c_overnight(n,h2_tech)                            See excel sheet (data_input.xlsx)
h2_prod_c_fix(n,h2_tech)                                  See excel sheet (data_input.xlsx)
h2_prod_c_fix2(n,h2_tech)                                 See excel sheet (data_input.xlsx)
h2_prod_aux_c_overnight(n,h2_tech,h2_channel)                        See excel sheet (data_input.xlsx)
h2_prod_aux_c_fix(n,h2_tech,h2_channel)                              See excel sheet (data_input.xlsx)
h2_prod_aux_c_fix2(n,h2_tech,h2_channel)                             See excel sheet (data_input.xlsx)
h2_hyd_liq_c_overnight(n,h2_channel)                         See excel sheet (data_input.xlsx)
h2_hyd_liq_c_fix(n,h2_channel)                               See excel sheet (data_input.xlsx)
h2_hyd_liq_c_fix2(n,h2_channel)                              See excel sheet (data_input.xlsx)
h2_hyd_liq_c_vom(n,h2_channel)                               See excel sheet (data_input.xlsx)
h2_sto_p_c_overnight(n,h2_channel)                           See excel sheet (data_input.xlsx)
h2_sto_p_c_fix(n,h2_channel)                                 See excel sheet (data_input.xlsx)
h2_sto_p_c_fix2(n,h2_channel)                                See excel sheet (data_input.xlsx)
h2_sto_p_c_overnight_alt                       See excel sheet (data_input.xlsx)
h2_sto_p_c_fix_alt                             See excel sheet (data_input.xlsx)
h2_sto_p_c_fix2_alt                            See excel sheet (data_input.xlsx)
h2_lp_sto_c_overnight(n,h2_channel)                          See excel sheet (data_input.xlsx)
h2_lp_sto_c_fix(n,h2_channel)                                See excel sheet (data_input.xlsx)
h2_lp_sto_c_fix2(n,h2_channel)                               See excel sheet (data_input.xlsx)
h2_aux_pretrans_c_overnight(n,h2_channel)                    See excel sheet (data_input.xlsx)
h2_aux_pretrans_c_fix(n,h2_channel)                          See excel sheet (data_input.xlsx)
h2_aux_pretrans_c_fix2(n,h2_channel)                         See excel sheet (data_input.xlsx)
h2_trans_c_overnight(n,h2_channel)                           See excel sheet (data_input.xlsx)
h2_trans_c_var(n,h2_channel)                                 See excel sheet (data_input.xlsx)
h2_trans_c_fix(n,h2_channel)                                 See excel sheet (data_input.xlsx)
h2_trans_c_fuel(n,h2_channel)                                See excel sheet (data_input.xlsx)
h2_trans_c_driver(n,h2_channel)                              See excel sheet (data_input.xlsx)
h2_LKW_cap(n,h2_channel)                                     See excel sheet (data_input.xlsx)
h2_aux_bfhp_sto_c_overnight(n,h2_channel)                    See excel sheet (data_input.xlsx)
h2_aux_bfhp_sto_c_fix(n,h2_channel)                          See excel sheet (data_input.xlsx)
h2_aux_bfhp_sto_c_fix2(n,h2_channel)                         See excel sheet (data_input.xlsx)
h2_hp_sto_c_overnight(n,h2_channel)                          See excel sheet (data_input.xlsx)
h2_hp_sto_c_fix(n,h2_channel)                                See excel sheet (data_input.xlsx)
h2_hp_sto_c_fix2                               See excel sheet (data_input.xlsx)
h2_dehyd_evap_c_overnight(n,h2_channel)                      See excel sheet (data_input.xlsx)
h2_dehyd_evap_c_fix(n,h2_channel)                            See excel sheet (data_input.xlsx)
h2_dehyd_evap_c_fix2(n,h2_channel)                           See excel sheet (data_input.xlsx)
h2_aux_bflp_sto_c_overnight(n,h2_channel)                    See excel sheet (data_input.xlsx)
h2_aux_bflp_sto_c_fix(n,h2_channel)                          See excel sheet (data_input.xlsx)
h2_aux_bflp_sto_c_fix2(n,h2_channel)                         See excel sheet (data_input.xlsx)
h2_aux_bfMP_sto_c_overnight(n,h2_channel)                    See excel sheet (data_input.xlsx)
h2_aux_bfMP_sto_c_fix(n,h2_channel)                          See excel sheet (data_input.xlsx)
h2_aux_bfMP_sto_c_fix2(n,h2_channel)                         See excel sheet (data_input.xlsx)
h2_MP_sto_c_overnight(n,h2_channel)                          See excel sheet (data_input.xlsx)
h2_MP_sto_c_fix(n,h2_channel)                                See excel sheet (data_input.xlsx)
h2_MP_sto_c_fix2(n,h2_channel)                               See excel sheet (data_input.xlsx)
h2_aux_bffuel_c_overnight(n,h2_channel)                      See excel sheet (data_input.xlsx)
h2_aux_bffuel_c_fix(n,h2_channel)                            See excel sheet (data_input.xlsx)
h2_aux_bffuel_c_fix2(n,h2_channel)                           See excel sheet (data_input.xlsx)
h2_recon_aux_c_overnight(n,h2_channel,h2_tech_recon)                       See excel sheet (data_input.xlsx)
h2_recon_aux_c_fix(n,h2_channel,h2_tech_recon)                             See excel sheet (data_input.xlsx)
h2_recon_aux_c_fix2(n,h2_channel,h2_tech_recon)                            See excel sheet (data_input.xlsx)
h2_recon_c_overnight(n,h2_tech_recon)                           See excel sheet (data_input.xlsx)
h2_recon_c_fix(n,h2_tech_recon)                                 See excel sheet (data_input.xlsx)
h2_recon_c_vom(n,h2_tech_recon)                                 See excel sheet (data_input.xlsx)
* h2_bidirect_ratio                              See excel sheet (data_input.xlsx)
h2_c_gas(n)                                       See excel sheet (data_input.xlsx)

*--- Temporal H2 data ---
d_h2(n,h)                                           See excel sheet (time_series.xlsx)
d_p2x(n,h,h2_channel)                                          See excel sheet (time_series.xlsx)

***************  DERIVED PARAMETERS  *******************************************

c_fuel(n,tech)   Fuel costs for conventional plants [EUR per MWh]
c_co2(n,tech)    CO2 costs for conventional plants [EUR per MWh]
c_m(n,tech)              Marginal production costs for conventional plants including fuel and CO2 and variable O and M costs [EUR per MWh]
c_i(n,tech)              Annualized investment costs by conventioanl plant [EUR per MW]

c_i_res(n,tech)          Annualized investment costs by renewable plant [EUR per MW]
c_fix_res(n,tech)        Annualized fixed costs by renewable plant [EUR per MW per a]

c_i_sto_e(n,sto)        Annualized investment costs storage energy [EUR per MWh]
c_i_sto_p_in(n,sto)     Annualized investment costs storage capacity in [EUR per MW]
c_i_sto_p_out(n,sto)    Annualized investment costs storage capacity in [EUR per MW]

c_i_rsvr_e(n,rsvr)       Annualized investment costs storage energy [EUR per MWh]
c_i_rsvr_p_in(n,rsvr)    Annualized investment costs storage capacity [EUR per MW]
c_i_rsvr_p_out(n,rsvr)   Annualized investment costs storage capacity [EUR per MW]

c_i_dsm_cu(n,dsm)       DSM: Annualized investment costs load curtailment [EUR per MW]
c_i_dsm_shift(n,dsm)     DSM: Annualized investment costs load shifting [EUR per MW]

c_i_ntc(l)          Investment for net transfer capacity [EUR per MW]
c_fix_ntc(l)        Fixed costs [EUR per MW per a]
eta_ntc(l)          Lump-sum reduction of cross-border NTC based on distance aka TRL [0 1]

phi_mean_reserves_call(n,reserves)           Hourly mean of share reserves called [0 1]

theta_dir(n,bu,ch)        Dummy equal to 1 if building type bu has direct heating type ch [0 1]
theta_sets(n,bu,ch)        Dummy equal to 1 if building type bu has SETS heating type ch [0 1]
theta_hp(n,bu,ch)          Dummy equal to 1 if building type bu has heat pump heating type ch [0 1]
theta_elec(n,bu,ch)        Dummy equal to 1 if building type bu has hybrif electric heating - electric part [0 1]
theta_fossil(n,bu,ch)      Dummy equal to 1 if building type bu has hybrif electric heating - fossil part [0 1]
theta_storage(n,bu,ch)     Dummy equal to 1 if building type ch has storage heating type ch [0 1]

*--- Cost Parameters Annualized ---
h2_prod_c_a_overnight(n,h2_tech)
h2_prod_c_a_fix(n,h2_tech)                              See excel sheet (data_input.xlsx)
h2_prod_c_a_fix2(n,h2_tech)                             See excel sheet (data_input.xlsx)
h2_prod_c_ad_fix(n,h2_tech)                             See excel sheet (data_input.xlsx)
h2_prod_c_ad_fix2(n,h2_tech)                            See excel sheet (data_input.xlsx)
h2_prod_c_ad_a_fix(n,h2_tech)                           See excel sheet (data_input.xlsx)
h2_prod_c_ad_a_fix2(n,h2_tech)                          See excel sheet (data_input.xlsx)
h2_prod_aux_c_a_overnight(n,h2_tech,h2_channel)                    See excel sheet (data_input.xlsx)
h2_hyd_liq_c_a_overnight(n,h2_channel)                     See excel sheet (data_input.xlsx)
h2_sto_p_c_a_overnight(n,h2_channel)                       See excel sheet (data_input.xlsx)
h2_lp_sto_c_a_overnight(n,h2_channel)                      See excel sheet (data_input.xlsx)
h2_aux_pretrans_c_a_overnight(n,h2_channel)                See excel sheet (data_input.xlsx)
h2_trans_c_a_overnight(n,h2_channel)                       See excel sheet (data_input.xlsx)
aux_bfhp_sto_c_a_overnight(n,h2_channel)                   See excel sheet (data_input.xlsx)
h2_hp_sto_c_a_overnight(n,h2_channel)                      See excel sheet (data_input.xlsx)
h2_dehyd_evap_c_a_overnight(n,h2_channel)                  See excel sheet (data_input.xlsx)
h2_prod_c_ad_overnight(n,h2_tech)                       See excel sheet (data_input.xlsx)
h2_prod_c_ad_a_overnight(n,h2_tech)                     See excel sheet (data_input.xlsx)
h2_aux_bflp_sto_c_a_overnight(n,h2_channel)                See excel sheet (data_input.xlsx)
h2_aux_bfMP_sto_c_a_overnight(n,h2_channel)                See excel sheet (data_input.xlsx)
h2_MP_sto_c_a_overnight(n,h2_channel)                      See excel sheet (data_input.xlsx)
h2_aux_bffuel_c_a_overnight(n,h2_channel)                  See excel sheet (data_input.xlsx)
h2_recon_aux_c_a_overnight(n,h2_channel,h2_tech_recon)                   See excel sheet (data_input.xlsx)
h2_recon_c_a_overnight(n,h2_tech_recon)                       See excel sheet (data_input.xlsx)
h2_recon_c_a_fix                             See excel sheet (data_input.xlsx)
h2_recon_c_a_fix2                            See excel sheet (data_input.xlsx)

c_infes   
c_h_infes   
c_h_dhw_infes

***************  PARAMETERS FOR DATA UPLOAD  ***********************************

technology_data_upload(n,tech,tech_res_con,tech_dispatch,headers_tech)
technology_data(n,tech,headers_tech)
storage_data(n,sto,headers_sto)
reservoir_data(n,rsvr,headers_reservoir)
time_data_upload(h,n,headers_time)
dsm_data_upload(n,dsm,dsm_type,headers_dsm)
dsm_data(n,dsm,headers_dsm)
topology_data(l,headers_topology)
ev_data(n,ev,headers_ev)
ev_time_data_upload(h,n,headers_time_ev,ev)
prosumage_data_generation(n,tech,headers_prosumage_generation)
prosumage_data_storage(n,sto,headers_prosumage_storage)
reserves_time_data_activation(h,n,reserves)
reserves_time_data_provision(h,n,reserves)
reserves_data_upload(n,reserves,reserves_up_down,reserves_spin_nonspin,reserves_prim_nonprim,headers_reserves)
reserves_data(n,reserves,headers_reserves)
heat_data_upload(n,bu,ch,heat_storage,heat_hp,heat_elec,heat_fossil,headers_heat)
heat_data(n,bu,ch,headers_heat)
dh_upload(h,n,bu)
d_dhw_upload(h,n,bu)
temp_source_upload(h,n,ch)

h2_parameter_data_table1
h2_parameter_data_table2
h2_parameter_data_table3
h2_parameter_data_table4
h2_parameter_data_table5
h2_parameter_data_table6
h2_parameter_data_table7
h2_parameter_data_table8
h2_parameter_data_table9
h2_parameter_data_table10

h2_time_data(h,n)
h2_p2x_time_data(h,n,h2_channel)

nodes_data_upload(n,headers_nodes)
scalar_data_upload(headers_scalar)
;

%DIETERgms%$include "%MODELDIR%dieterpy_2_nodesandparsload.gms"

%DIETERgms%$ontext

***************  UPLOAD TIME-CONSTANT SETS AND PARAMETERS  *********************

$onecho >temp.tmp
se=0

dset=n                                   rng=spatial!N5                  rdim=0 cdim=1

dset=tech                                rng=Technologies!B6             rdim=1 cdim=0
dset=headers_tech                        rng=Technologies!E5             rdim=0 cdim=1
dset=tech_dispatch                       rng=Technologies!D6             rdim=1 cdim=0
dset=tech_res_con                        rng=Technologies!C6             rdim=1 cdim=0

dset=sto                                 rng=storage!B6                  rdim=1 cdim=0
dset=headers_sto                         rng=storage!C5                  rdim=0 cdim=1

dset=rsvr                                rng=reservoir!B6                rdim=1 cdim=0
dset=headers_reservoir                   rng=reservoir!C5                rdim=0 cdim=1

dset=dsm                                 rng=DSM!B6                      rdim=1 cdim=0
dset=headers_dsm                         rng=DSM!D5                      rdim=0 cdim=1
dset=dsm_type                            rng=DSM!C6                      rdim=1 cdim=0

dset=l                                   rng=spatial!A6                  rdim=1 cdim=0
dset=headers_topology                    rng=spatial!B5                  rdim=0 cdim=1

dset=ev                                  rng=ev!B6                       rdim=1 cdim=0
dset=headers_ev                          rng=ev!C5                       rdim=0 cdim=1

dset=headers_prosumage_generation        rng=prosumage!C5                rdim=0 cdim=1
dset=headers_prosumage_storage           rng=prosumage!I5                rdim=0 cdim=1

dset=reserves                            rng=reserves!B6                 rdim=1 cdim=0
dset=headers_reserves                    rng=reserves!F5                 rdim=0 cdim=1
dset=reserves_up_down                    rng=reserves!C6                 rdim=1 cdim=0
dset=reserves_spin_nonspin               rng=reserves!D6                 rdim=1 cdim=0
dset=reserves_prim_nonprim               rng=reserves!E6                 rdim=1 cdim=0

dset=bu                                  rng=heat!B6                     rdim=1 cdim=0
dset=ch                                  rng=heat!C6                     rdim=1 cdim=0
dset=heat_storage                        rng=heat!D6                     rdim=1 cdim=0
dset=heat_hp                             rng=heat!E6                     rdim=1 cdim=0


dset=heat_elec                           rng=heat!F6                     rdim=1 cdim=0
dset=heat_fossil                         rng=heat!G6                     rdim=1 cdim=0

dset=headers_heat                        rng=heat!H5                     rdim=0 cdim=1

dset=h2_tech                             rng=P2H2!B6                     rdim=1 cdim=0
dset=h2_channel                          rng=P2H2!H6                     rdim=1 cdim=0
dset=h2_tech_recon                       rng=P2H2!Q6                     rdim=1 cdim=0
dset=headers_h2_parameters_table1        rng=P2H2!C5                     rdim=0 cdim=1
dset=headers_h2_parameters_table2        rng=P2H2!I5                     rdim=0 cdim=1
dset=headers_h2_parameters_table3        rng=P2H2!R5                     rdim=0 cdim=1
dset=headers_h2_parameters_table4        rng=P2H2!Y5                     rdim=0 cdim=1
dset=headers_h2_parameters_table5        rng=P2H2!AK5                    rdim=0 cdim=1
dset=headers_h2_parameters_table6        rng=P2H2!AX5                    rdim=0 cdim=1
dset=headers_h2_parameters_table7        rng=P2H2!FC5                    rdim=0 cdim=1
dset=headers_h2_parameters_table8        rng=P2H2!FO5                    rdim=0 cdim=1
dset=headers_h2_parameters_table9        rng=P2H2!FX5                    rdim=0 cdim=1
dset=headers_h2_parameters_table10       rng=P2H2!GC5                    rdim=0 cdim=1


par=technology_data_upload               rng=Technologies!A5             rdim=4 cdim=1
par=storage_data                         rng=storage!A5                  rdim=2 cdim=1
par=reservoir_data                       rng=reservoir!A5                rdim=2 cdim=1
par=dsm_data_upload                      rng=DSM!A5                      rdim=3 cdim=1
par=topology_data                        rng=spatial!A5                  rdim=1 cdim=1
%GER_only%par=inc                        rng=spatial!M5                  rdim=1 cdim=1
par=ev_data                              rng=ev!A5                       rdim=2 cdim=1
par=prosumage_data_generation            rng=prosumage!A5                rdim=2 cdim=1
par=prosumage_data_storage               rng=prosumage!G5                rdim=2 cdim=1
par=reserves_data_upload                 rng=reserves!A5                 rdim=5 cdim=1
par=heat_data_upload                     rng=heat!A5                     rdim=7 cdim=1
par=h2_parameter_data_table1             rng=P2H2!A5                     rdim=2 cdim=1
par=h2_parameter_data_table2             rng=P2H2!G5                     rdim=2 cdim=1
par=h2_parameter_data_table3             rng=P2H2!P5                     rdim=2 cdim=1
par=h2_parameter_data_table4             rng=P2H2!W5                     rdim=2 cdim=1
par=h2_parameter_data_table5             rng=P2H2!AH5                    rdim=3 cdim=1
par=h2_parameter_data_table6             rng=P2H2!AV5                    rdim=2 cdim=1
par=h2_parameter_data_table7             rng=P2H2!EZ5                    rdim=3 cdim=1
par=h2_parameter_data_table8             rng=P2H2!FM5                    rdim=2 cdim=1
par=h2_parameter_data_table9             rng=P2H2!FW5                    rdim=1 cdim=1
par=h2_parameter_data_table10            rng=P2H2!GB5                    rdim=1 cdim=1


dset=headers_nodes                       rng=nodes!B3                    rdim=0 cdim=1
dset=headers_scalar                      rng=scalar!A4                   rdim=1 cdim=0
par=nodes_data_upload                    rng=nodes!A3                    rdim=1 cdim=1
par=scalar_data_upload                   rng=scalar!A4                   rdim=1 cdim=0

$offecho

%skip_Excel%$call "gdxxrw static_input.xlsx @temp.tmp o=Data_input maxdupeerrors=100";

$GDXin Data_input.gdx
$load n tech headers_tech tech_dispatch tech_res_con
$load sto headers_sto rsvr headers_reservoir reservoir_data dsm headers_dsm dsm_type
$load technology_data_upload storage_data dsm_data_upload
$load headers_nodes, headers_scalar, nodes_data_upload, scalar_data_upload
%GER_only%$load l headers_topology topology_data inc
%GER_only%$ontext
$load l headers_topology topology_data
$ontext
$offtext
%DIETERgms%$ontext
$load ev headers_ev ev_data
$load headers_prosumage_generation headers_prosumage_storage prosumage_data_generation prosumage_data_storage
$load reserves reserves_up_down reserves_spin_nonspin reserves_prim_nonprim headers_reserves reserves_data_upload
$load bu ch heat_storage heat_hp heat_elec heat_fossil headers_heat heat_data_upload
$load h2_tech h2_channel h2_tech_recon headers_h2_parameters_table1 headers_h2_parameters_table2 headers_h2_parameters_table3 headers_h2_parameters_table4 headers_h2_parameters_table5 headers_h2_parameters_table6 headers_h2_parameters_table7 headers_h2_parameters_table8 headers_h2_parameters_table9 headers_h2_parameters_table10 h2_parameter_data_table1 h2_parameter_data_table2 h2_parameter_data_table3 h2_parameter_data_table4 h2_parameter_data_table5 h2_parameter_data_table6 h2_parameter_data_table7 h2_parameter_data_table8 h2_parameter_data_table9 h2_parameter_data_table10
;

%GER_only%$ontext
parameter inc ;
inc(l,n) = 1 ;
$ontext
$offtext
%DIETERgms%$ontext

***************  UPLOAD TIME-SERIES SETS AND PARAMETERS  ***********************

$onecho >temp2.tmp
se=0

dset=h                           rng=basic!A8            rdim=1 cdim=0
dset=headers_time                rng=basic!B7            rdim=0 cdim=1
par=time_data_upload             rng=basic!A6            rdim=1 cdim=2

dset=headers_time_ev             rng=EV!B7               rdim=0 cdim=1
par=ev_time_data_upload          rng=EV!A6               rdim=1 cdim=3

par=reserves_time_data_provision         rng=reserves_provision!A6       rdim=1 cdim=2
par=reserves_time_data_activation        rng=reserves_activation!A6      rdim=1 cdim=2

par=dh_upload                    rng=heat!C7             rdim=1 cdim=2
* par=theta_night                  rng=heat!A9            rdim=1 cdim=0

par=d_dhw_upload                 rng=heat_dhw!A6         rdim=1 cdim=2

par=nets_profile                 rng=NETS!A7             rdim=1 cdim=0

par=temp_source_upload           rng=heat_pump!A7        rdim=1 cdim=2

par=h2_time_data                 rng=P2H2!A2             rdim=1 cdim=1
par=h2_p2x_time_data             rng=P2X!A2              rdim=1 cdim=2
$offecho

%skip_Excel%$call "gdxxrw timeseries_input.xlsx @temp2.tmp o=time_series";

$GDXin time_series.gdx
$load h headers_time time_data_upload
$load headers_time_ev ev_time_data_upload
$load reserves_time_data_activation
$load reserves_time_data_provision
$load dh_upload
* $load theta_night
$load temp_source_upload
$load d_dhw_upload nets_profile
$load h2_time_data
$load h2_p2x_time_data
;

$ontext
$offtext
* This closes the DIETERgms



***************  ASSIGNMENTS  **************************************************

***** Aliases *****
alias (h,hh) ;
alias (res,resres) ;
alias (reserves,reservesreserves) ;
alias (nondis,nondisnondis) ;
alias (h2_channel,h2_channel_alias)  ;

***** Derived sets *****
dis(tech)$sum( (n,tech_res_con,headers_tech), technology_data_upload(n,tech,tech_res_con,'dis',headers_tech)) = yes;
nondis(tech)$sum( (n,tech_res_con,headers_tech), technology_data_upload(n,tech,tech_res_con,'nondis',headers_tech)) = yes;

con(tech)$sum( (n,tech_dispatch,headers_tech), technology_data_upload(n,tech,'con',tech_dispatch,headers_tech)) = yes;
res(tech)$sum( (n,tech_dispatch,headers_tech), technology_data_upload(n,tech,'res',tech_dispatch,headers_tech)) = yes;

reserves_up(reserves)$sum( (n,reserves_spin_nonspin,reserves_prim_nonprim,headers_reserves), reserves_data_upload(n,reserves,'up',reserves_spin_nonspin,reserves_prim_nonprim,headers_reserves)) = yes;
reserves_do(reserves)$sum( (n,reserves_spin_nonspin,reserves_prim_nonprim,headers_reserves), reserves_data_upload(n,reserves,'do',reserves_spin_nonspin,reserves_prim_nonprim,headers_reserves)) = yes;

reserves_spin(reserves)$sum( (n,reserves_up_down,reserves_prim_nonprim,headers_reserves), reserves_data_upload(n,reserves,reserves_up_down,'spin',reserves_prim_nonprim,headers_reserves)) = yes;
reserves_nonspin(reserves)$sum( (n,reserves_up_down,reserves_prim_nonprim,headers_reserves), reserves_data_upload(n,reserves,reserves_up_down,'nonspin',reserves_prim_nonprim,headers_reserves)) = yes;

reserves_prim(reserves)$sum( (n,reserves_up_down,reserves_spin_nonspin,headers_reserves), reserves_data_upload(n,reserves,reserves_up_down,reserves_spin_nonspin,'prim',headers_reserves)) = yes;
reserves_nonprim(reserves)$sum( (n,reserves_up_down,reserves_spin_nonspin,headers_reserves), reserves_data_upload(n,reserves,reserves_up_down,reserves_spin_nonspin,'nonprim',headers_reserves)) = yes;

reserves_prim_up(reserves)$sum( (n,reserves_spin_nonspin,headers_reserves), reserves_data_upload(n,reserves,'up',reserves_spin_nonspin,'prim',headers_reserves)) = yes;
reserves_prim_do(reserves)$sum( (n,reserves_spin_nonspin,headers_reserves), reserves_data_upload(n,reserves,'do',reserves_spin_nonspin,'prim',headers_reserves)) = yes;
reserves_nonprim_up(reserves)$sum( (n,reserves_spin_nonspin,headers_reserves), reserves_data_upload(n,reserves,'up',reserves_spin_nonspin,'nonprim',headers_reserves)) = yes;
reserves_nonprim_do(reserves)$sum( (n,reserves_spin_nonspin,headers_reserves), reserves_data_upload(n,reserves,'do',reserves_spin_nonspin,'nonprim',headers_reserves)) = yes;

hst(ch)$sum( (n,bu,heat_hp,heat_elec,heat_fossil,headers_heat), heat_data_upload(n,bu,ch,'yes',heat_hp,heat_elec,heat_fossil,headers_heat)) = yes;
hp(ch)$sum( (n,bu,heat_storage,heat_elec,heat_fossil,headers_heat), heat_data_upload(n,bu,ch,heat_storage,'yes',heat_elec,heat_fossil,headers_heat)) = yes;

hel(ch)$sum( (n,bu,heat_storage,heat_hp,heat_fossil,headers_heat), heat_data_upload(n,bu,ch,heat_storage,heat_hp,'yes',heat_fossil,headers_heat)) = yes;
hfo(ch)$sum( (n,bu,heat_storage,heat_hp,heat_elec,headers_heat), heat_data_upload(n,bu,ch,heat_storage,heat_hp,heat_elec,'yes',headers_heat)) = yes;

***** Parameters *****

*--- Generation technologies ---*
technology_data(n,tech,headers_tech) = sum((tech_res_con,tech_dispatch), technology_data_upload(n,tech,tech_res_con,tech_dispatch,headers_tech)) ;
eta(n,tech) = technology_data(n,tech,'eta_con') ;
carbon_content(n,tech) = technology_data(n,tech,'carbon_content') ;
c_up(n,dis) =technology_data(n,dis,'load change costs up') ;
c_do(n,dis) = technology_data(n,dis,'load change costs down') ;
c_fix(n,tech) = technology_data(n,tech,'fixed_costs') ;
c_vom(n,tech) = technology_data(n,tech,'variable_om') ;
avail(n,tech) = technology_data(n,tech,'availability') ;
CO2price(n,tech) = technology_data(n,tech,'CO2_price') ;

c_inv_overnight(n,tech) = technology_data(n,tech,'oc') ;
lifetime_tech(n,tech) = technology_data(n,tech,'lifetime') ;
recovery(n,tech) = technology_data(n,tech,'recovery_period') ;
interest_rate_tech(n,tech) = technology_data(n,tech,'interest_rate') ;
m_p(n,tech) = technology_data(n,tech,'max_installable') ;
m_e(n,tech) = technology_data(n,tech,'max_energy') ;
grad_per_min(n,dis) = technology_data(n,dis,'load change flexibility') ;
fuelprice(n,tech) = technology_data(n,tech,'fuel costs') ;

c_cu(n,res) = technology_data(n,res,'curtailment_costs') ;

*--- Storage technologies ---*
c_m_sto_in(n,sto) = storage_data(n,sto,'mc_in');
c_m_sto_out(n,sto) = storage_data(n,sto,'mc_out');
eta_sto_in(n,sto) = storage_data(n,sto,'efficiency_in');
eta_sto_out(n,sto) = storage_data(n,sto,'efficiency_out');
eta_sto_self(n,sto) = storage_data(n,sto,'efficiency_self');
c_fix_sto_e(n,sto) = storage_data(n,sto,'fixed_costs_energy');
c_fix_sto_p_in(n,sto) = storage_data(n,sto,'fixed_costs_power_in');
c_fix_sto_p_out(n,sto) = storage_data(n,sto,'fixed_costs_power_out');
phi_sto_ini(n,sto) = storage_data(n,sto,'level_start');
etop_max(n,sto) = storage_data(n,sto,'etop_max') ;
avail_sto(n,sto) = storage_data(n,sto,'availability') ;

c_inv_overnight_sto_e(n,sto) = storage_data(n,sto,'oc_energy');
c_inv_overnight_sto_p_in(n,sto) = storage_data(n,sto,'oc_capacity_in');
c_inv_overnight_sto_p_out(n,sto) = storage_data(n,sto,'oc_capacity_out');
lifetime_sto(n,sto) = storage_data(n,sto,'lifetime');
interest_rate_sto(n,sto) = storage_data(n,sto,'interest_rate');
m_sto_e(n,sto) = storage_data(n,sto,'max_energy');
m_sto_p_in(n,sto) = storage_data(n,sto,'max_power_in');
m_sto_p_out(n,sto) = storage_data(n,sto,'max_power_out');

*--- Reservoir technologies ---*
c_m_rsvr(n,rsvr) = reservoir_data(n,rsvr,'mc');
eta_rsvr_out(n,rsvr) = reservoir_data(n,rsvr,'efficiency_out');
c_fix_rsvr_p_in(n,rsvr) = reservoir_data(n,rsvr,'fixed_costs_power_in');
c_fix_rsvr_p_out(n,rsvr) = reservoir_data(n,rsvr,'fixed_costs_power_out');
c_fix_rsvr_e(n,rsvr) = reservoir_data(n,rsvr,'fixed_costs_energy');
phi_rsvr_ini(n,rsvr) = reservoir_data(n,rsvr,'level_start');
phi_rsvr_lev_min(n,rsvr) = reservoir_data(n,rsvr,'level_min');
avail_rsvr(n,rsvr) = reservoir_data(n,rsvr,'availability') ;

c_inv_overnight_rsvr_p_in(n,rsvr) = reservoir_data(n,rsvr,'oc_capacity_in');
c_inv_overnight_rsvr_p_out(n,rsvr) = reservoir_data(n,rsvr,'oc_capacity_out');
c_inv_overnight_rsvr_e(n,rsvr) = reservoir_data(n,rsvr,'oc_energy');
inv_lifetime_rsvr(n,rsvr) = reservoir_data(n,rsvr,'lifetime');
inv_interest_rsvr(n,rsvr) = reservoir_data(n,rsvr,'interest_rate');
m_rsvr_e(n,rsvr) = reservoir_data(n,rsvr,'max_energy');
m_rsvr_p_out(n,rsvr) = reservoir_data(n,rsvr,'max_power');
min_flh(n,rsvr) = reservoir_data(n,rsvr,'min_flh');

*--- DSM technologies ---*
dsm_curt(dsm)$sum( (n,dsm_type,headers_dsm), dsm_data_upload(n,dsm,'curt',headers_dsm)) = yes;
dsm_shift(dsm)$sum( (n,dsm_type,headers_dsm), dsm_data_upload(n,dsm,'shift',headers_dsm)) = yes;
dsm_data(n,dsm,headers_dsm) = sum(dsm_type, dsm_data_upload(n,dsm,dsm_type,headers_dsm) ) ;

c_m_dsm_cu(n,dsm_curt) = dsm_data(n,dsm_curt,'mc')     ;
c_m_dsm_shift(n,dsm_shift) = dsm_data(n,dsm_shift,'mc')  ;
c_fix_dsm_cu(n,dsm_curt) = dsm_data(n,dsm_curt,'fc')  ;
c_fix_dsm_shift(n,dsm_shift) = dsm_data(n,dsm_shift,'fc') ;

t_dur_dsm_cu(n,dsm_curt) = dsm_data(n,dsm_curt,'max_duration')   ;
t_off_dsm_cu(n,dsm_curt) = dsm_data(n,dsm_curt,'recovery_time')   ;
t_dur_dsm_shift(n,dsm_shift) = dsm_data(n,dsm_shift,'max_duration')   ;
t_off_dsm_shift(n,dsm_shift) = dsm_data(n,dsm_shift,'recovery_time')   ;
eta_dsm_shift(n,dsm_shift)  = dsm_data(n,dsm_shift,'efficiency')   ;

c_inv_overnight_dsm_cu(n,dsm_curt) =  dsm_data(n,dsm_curt,'oc')   ;
c_inv_overnight_dsm_shift(n,dsm_shift)  =  dsm_data(n,dsm_shift,'oc')   ;
inv_lifetime_dsm_cu(n,dsm_curt)  =  dsm_data(n,dsm_curt,'lifetime')   ;
inv_lifetime_dsm_shift(n,dsm_shift)   =  dsm_data(n,dsm_shift,'lifetime')   ;
inv_interest_dsm_cu(n,dsm_curt)   =  dsm_data(n,dsm_curt,'interest_rate')   ;
inv_interest_dsm_shift(n,dsm_shift)  =  dsm_data(n,dsm_shift,'interest_rate')   ;
m_dsm_cu(n,dsm_curt) =  dsm_data(n,dsm_curt,'max_installable')   ;
m_dsm_shift(n,dsm_shift) =  dsm_data(n,dsm_shift,'max_installable')   ;

*--- Temporal data ---*
d(n,h) = time_data_upload(h,n,'demand')  ;
phi_res(n,res,h) = sum(headers_time$(sameas(res,headers_time)), time_data_upload(h,n,headers_time));
rsvr_in(n,rsvr,h) = sum(headers_time$(sameas(rsvr,headers_time)), time_data_upload(h,n,headers_time));
phi_reserves_call(n,reserves,h) = reserves_time_data_activation(h,n,reserves) ;
reserves_exogenous(n,reserves,h) = reserves_time_data_provision(h,n,reserves) ;

*--- Spatial data ---*
inv_lifetime_ntc(l) = topology_data(l,'lifetime') ;
inv_recovery_ntc(l) = topology_data(l,'recovery_period') ;
inv_interest_ntc(l) = topology_data(l,'interest_rate') ;
c_inv_overnight_ntc(l) = topology_data(l,'overnight_costs') ;
c_fix_ntc_per_km(l) = topology_data(l,'fixed_costs') ;
m_ntc(l) = topology_data(l,'max_installable') ;
dist(l) = topology_data(l,'distance') ;
loss_ntc(l) = topology_data(l,'loss_transmission') ;
c_m_ntc(l) = topology_data(l,'variable_om') ;

*--- Electric vehicles ---*
c_m_ev_cha(n,ev) = ev_data(n,ev,'mc_charge') ;
c_m_ev_dis(n,ev) = ev_data(n,ev,'mc_discharge') ;
pen_phevfuel(n,ev) = ev_data(n,ev,'penalty_fuel') ;
eta_ev_in(n,ev) = ev_data(n,ev,'efficiency_charge') ;
eta_ev_out(n,ev) = ev_data(n,ev,'efficiency_discharge') ;
phi_ev_ini(n,ev) = ev_data(n,ev,'ev_start') ;

n_ev_e(n,ev) = ev_data(n,ev,'ev_capacity') ;
phi_ev(n,ev) = ev_data(n,ev,'share_ev') ;
ev_phev(n,ev) = ev_data(n,ev,'ev_type') ;

n_ev_p(n,ev,h) = ev_time_data_upload(h,n,'n_ev_p',ev) ;
ev_ed(n,ev,h) = ev_time_data_upload(h,n,'ev_ed',ev) ;
ev_ged_exog(n,ev,h) = ev_time_data_upload(h,n,'ev_ged_exog',ev) ;


*--- Prosumage ---*
m_res_pro(n,res) = prosumage_data_generation(n,res,'max_power') ;
m_sto_pro_e(n,sto) = prosumage_data_storage(n,sto,'max_energy') ;
m_sto_pro_p(n,sto) = prosumage_data_storage(n,sto,'max_power') ;
phi_sto_pro_ini(n,sto) = prosumage_data_storage(n,sto,'level_start') ;


*--- Reserves ---*
reserves_data(n,reserves,headers_reserves) = sum((reserves_up_down,reserves_spin_nonspin,reserves_prim_nonprim), reserves_data_upload(n,reserves,reserves_up_down,reserves_spin_nonspin,reserves_prim_nonprim,headers_reserves)) ;
phi_reserves_share(n,reserves) = reserves_data(n,reserves,'share_sr_mr') ;
reserves_intercept(n,reserves) = reserves_data(n,reserves,'intercept') ;
reserves_slope(n,reserves,'wind_on') = reserves_data(n,reserves,'slope_wind_on') ;
reserves_slope(n,reserves,'wind_off') = reserves_data(n,reserves,'slope_wind_off') ;
reserves_slope(n,reserves,'pv') = reserves_data(n,reserves,'slope_pv') ;
reserves_reaction(n,reserves) = reserves_data(n,reserves,'reaction_time') ;
phi_reserves_pr_up(n) = reserves_data(n,'PR_up','fraction_pr') ;
phi_reserves_pr_do(n) = reserves_data(n,'PR_do','fraction_pr') ;


*--- Heat ---*
heat_data(n,bu,ch,headers_heat) = sum((heat_storage,heat_hp,heat_elec,heat_fossil), heat_data_upload(n,bu,ch,heat_storage,heat_hp,heat_elec,heat_fossil,headers_heat)) ;
phi_heat_type(n,bu,ch) = heat_data(n,bu,ch,'share') ;
area_floor(n,bu,ch) = heat_data(n,bu,ch,'area_floor') ;
dh(n,bu,ch,h) = area_floor(n,bu,ch) * phi_heat_type(n,bu,ch) * dh_upload(h,n,bu) ;
d_dhw(n,bu,ch,h) = area_floor(n,bu,ch) * phi_heat_type(n,bu,ch) * d_dhw_upload(h,n,bu) ;
eta_heat_stat(n,bu,ch) = heat_data(n,bu,ch,'static_efficiency') ;
eta_heat_dyn(n,bu,ch) = heat_data(n,bu,ch,'dynamic_efficiency') ;
eta_dhw_aux_stat(n,bu,ch) = heat_data(n,bu,ch,'static_efficiency_sets_aux_dhw') ;
* currently not used
n_heat_p_in(n,bu,ch) = heat_data(n,bu,ch,'max_power') ;
n_heat_p_out(n,bu,ch) = heat_data(n,bu,ch,'max_outflow') ;
n_heat_e(n,bu,ch) = heat_data(n,bu,ch,'max_level') ;
n_sets_p_in(n,bu,ch) = heat_data(n,bu,ch,'max_power') ;
n_sets_p_out(n,bu,ch) = heat_data(n,bu,ch,'max_outflow') ;
n_sets_e(n,bu,ch) = heat_data(n,bu,ch,'max_level') ;
n_sets_dhw_p_in(n,bu,ch) = heat_data(n,bu,ch,'max_power_in_sets_aux_dhw') ;
n_sets_dhw_p_out(n,bu,ch) = heat_data(n,bu,ch,'max_power_out_sets_aux_dhw') ;
n_sets_dhw_e(n,bu,ch) = heat_data(n,bu,ch,'max_energy_sets_aux_dhw') ;
phi_heat_ini(n,bu,ch) = heat_data(n,bu,ch,'level_ini') ;
temp_sink(n,bu,ch) = heat_data(n,bu,ch,'temperature_sink') ;
temp_source(n,bu,'hp_as',h) = temp_source_upload(h,n,'hp_as') ;
temp_source(n,bu,'hp_gs',h) = heat_data(n,bu,'hp_gs','temperature_source') ;
temp_source(n,bu,'gas_hp_gs',h) = heat_data(n,bu,'gas_hp_gs','temperature_source') ;
temp_source(n,bu,'hp_gs_elec',h) = heat_data(n,bu,'hp_gs_elec','temperature_source') ;
pen_heat_fuel(n,bu,ch) = heat_data(n,bu,ch,'penalty_non-electric_heat_supply') ;

*--- P2H2 ---*

*--- Switches ---*
h2_tech_avail_sw(n,h2_tech) = h2_parameter_data_table1(n,h2_tech,'tech_avail_sw');
h2_channel_avail_sw(n,h2_channel) = h2_parameter_data_table2(n,h2_channel,'channel_avail_sw');
h2_tech_recon_sw(n,h2_tech_recon) = h2_parameter_data_table3(n,h2_tech_recon,'tech_recon_sw');

h2_recon_sw(n,h2_channel) = h2_parameter_data_table2(n,h2_channel,'recon_sw');
h2_mobility_sw(n,h2_channel) = h2_parameter_data_table2(n,h2_channel,'h2_mobility_sw');
h2_p2x_sw(n,h2_channel) = h2_parameter_data_table2(n,h2_channel,'p2x_sw');

h2_prod_aux_sw(n,h2_tech,h2_channel) = h2_parameter_data_table5(n,h2_tech,h2_channel,'prod_aux_sw');
h2_hyd_liq_sw(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hyd_liq_sw');
h2_sto_p_sw(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'sto_p_sw');
h2_lp_sto_sw(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'lp_sto_sw');
h2_aux_pretrans_sw(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_pretrans_sw');
h2_aux_bfhp_sto_sw(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bfhp_sto_sw');
h2_hp_sto_sw(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hp_sto_sw');
h2_dehyd_evap_sw(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'dehyd_evap_sw');
h2_trans_sw(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'trans_sw');
h2_aux_bflp_sto_sw(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bflp_sto_sw');
h2_aux_bfMP_sto_sw(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bfMP_sto_sw');
h2_MP_sto_sw(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'MP_sto_sw');
h2_aux_bffuel_sw(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bffuel_sw');
h2_dehyd_evap_gas_sw(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'dehyd_evap_gas_sw');

h2_recon_aux_sw(n,h2_channel,h2_tech_recon) = h2_parameter_data_table7(n,h2_channel,h2_tech_recon,'recon_aux_sw');
h2_bypass_1_sw(n,h2_tech,h2_channel)=h2_parameter_data_table5(n,h2_tech,h2_channel,'bypass_1_sw');
h2_bypass_2_sw(n,h2_channel)=h2_parameter_data_table6(n,h2_channel,'bypass_2_sw');
* h2_bidirect_sw(n,h2_tech_recon) = h2_parameter_data_table3(n,h2_tech_recon,'bidirect_sw');

*--- Technological Parameters---
h2_efficiency(n,h2_tech) = h2_parameter_data_table4(n,h2_tech,'efficiency');
h2_prod_scale(n,h2_tech) = h2_parameter_data_table4(n,h2_tech,'prod_scale');
h2_prod_lifetime(n,h2_tech) = h2_parameter_data_table4(n,h2_tech,'prod_lifetime');
h2_prod_aux_lifetime(n,h2_tech,h2_channel) = h2_parameter_data_table5(n,h2_tech,h2_channel,'prod_aux_lifetime');
h2_eta_prod_aux(n,h2_tech,h2_channel) = h2_parameter_data_table5(n,h2_tech,h2_channel,'eta_prod_aux');
h2_hyd_liq_lifetime(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hyd_liq_lifetime');
h2_eta_hyd(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'eta_hyd_liq');
h2_sto_p_lifetime(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'sto_p_lifetime');
h2_aux_bflp_sto_lifetime(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bflp_sto_lifetime');

h2_lp_sto_lifetime(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'lp_sto_lifetime');
h2_aux_bfMP_sto_lifetime(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bfMP_sto_lifetime');
h2_MP_sto_lifetime(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'MP_sto_lifetime');
h2_aux_bffuel_lifetime(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bffuel_lifetime');

h2_aux_pretrans_lifetime(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_pretrans_lifetime');
h2_eta_aux_pretrans(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'eta_aux_pretrans');
h2_trans_lifetime(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'trans_lifetime');
h2_aux_bfhp_sto_lifetime(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bfhp_sto_lifetime');
h2_eta_aux_bfhp_sto(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'eta_aux_bfhp_sto');
h2_hp_sto_lifetime(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hp_sto_lifetime');
h2_dehyd_evap_lifetime(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'dehyd_evap_lifetime');
h2_eta_dehyd_evap(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'eta_dehyd_evap');

h2_sto_p_type(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'sto_p_type');

h2_prod_aux_ed(n,h2_tech,h2_channel) = h2_parameter_data_table5(n,h2_tech,h2_channel,'prod_aux_ed');
h2_hyd_liq_ed(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hyd_liq_ed');
h2_sto_p_ed(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'sto_p_ed');

h2_lp_sto_ed(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'lp_sto_ed');
h2_aux_pretrans_ed(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_pretrans_ed');
h2_trans_eta(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'trans_eta');
h2_aux_bfhp_sto_ed(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bfhp_sto_ed');
h2_hp_sto_ed(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hp_sto_ed');
h2_dehyd_evap_ed(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'dehyd_evap_ed');
h2_sto_p_eta_stat(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'sto_p_eta_stat');

h2_hp_sto_eta_stat(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hp_sto_eta_stat') ;
h2_hp_sto_phi_min(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hp_sto_phi_min') ;
h2_lp_sto_eta_stat(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'lp_sto_eta_stat');
h2_hp_sto_phi_ini(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hp_sto_phi_ini');
h2_hp_sto_phi_min(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hp_sto_phi_min');
h2_sto_p_phi_ini(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'sto_p_phi_ini');
h2_sto_p_phi_min(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'sto_p_phi_min');

h2_lp_sto_phi_ini(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'lp_sto_phi_ini');
h2_lp_sto_phi_min(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'lp_sto_phi_min');

h2_aux_bflp_sto_ed(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bflp_sto_ed');
h2_eta_aux_bflp_sto(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'eta_aux_bflp_sto');
h2_aux_bfMP_sto_ed(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bfMP_sto_ed');
h2_eta_aux_bfMP_sto (n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'eta_aux_bfMP_sto');
h2_MP_sto_ed(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'MP_sto_ed');
h2_MP_sto_eta_stat(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'MP_sto_eta_stat');
h2_MP_sto_phi_ini(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'MP_sto_phi_ini');
h2_MP_sto_phi_min(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'MP_sto_phi_min');
h2_aux_bffuel_ed(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bffuel_ed');
h2_eta_aux_bffuel(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'eta_aux_bffuel');

h2_recon_aux_lifetime(n,h2_channel,h2_tech_recon) = h2_parameter_data_table7(n,h2_channel,h2_tech_recon,'recon_aux_lifetime');
h2_eta_recon_aux(n,h2_channel,h2_tech_recon) = h2_parameter_data_table7(n,h2_channel,h2_tech_recon,'eta_recon_aux');
h2_recon_aux_ed(n,h2_channel,h2_tech_recon) = h2_parameter_data_table7(n,h2_channel,h2_tech_recon,'recon_aux_ed');

h2_recon_lifetime(n,h2_tech_recon) = h2_parameter_data_table8(n,h2_tech_recon,'recon_lifetime');
h2_recon_efficiency(n,h2_tech_recon) = h2_parameter_data_table8(n,h2_tech_recon,'recon_efficiency');

*--- Cost Parameters ---
h2_interest_rate(n) = h2_parameter_data_table10(n,'interest_rate');
h2_trans_dist(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'trans_dist');
h2_trans_load_time(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'Load_time');
h2_trans_unload_time(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'Unload_time');
h2_prod_c_overnight(n,h2_tech) = h2_parameter_data_table4(n,h2_tech,'prod_c_overnight');
h2_prod_c_fix(n,h2_tech) = h2_parameter_data_table4(n,h2_tech,'prod_c_fix');
h2_prod_c_fix2(n,h2_tech) = h2_parameter_data_table4(n,h2_tech,'prod_c_fix2');
h2_prod_aux_c_overnight(n,h2_tech,h2_channel) = h2_parameter_data_table5(n,h2_tech,h2_channel,'prod_aux_c_overnight');
h2_prod_aux_c_fix(n,h2_tech,h2_channel) = h2_parameter_data_table5(n,h2_tech,h2_channel,'prod_aux_c_fix');
h2_prod_aux_c_fix2(n,h2_tech,h2_channel) = h2_parameter_data_table5(n,h2_tech,h2_channel,'prod_aux_c_fix2');
h2_hyd_liq_c_overnight(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hyd_liq_c_overnight');
h2_hyd_liq_c_fix(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hyd_liq_c_fix');
h2_hyd_liq_c_fix2(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hyd_liq_c_fix2');
h2_hyd_liq_c_vom(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hyd_liq_c_vom');
h2_sto_p_c_overnight(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'sto_p_c_overnight');
h2_sto_p_c_fix(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'sto_p_c_fix');
h2_sto_p_c_fix2(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'sto_p_c_fix2');

h2_lp_sto_c_overnight(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'lp_sto_c_overnight');
h2_lp_sto_c_fix(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'lp_sto_c_fix');
h2_lp_sto_c_fix2(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'lp_sto_c_fix2');
h2_aux_pretrans_c_overnight(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_pretrans_c_overnight');
h2_aux_pretrans_c_fix(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_pretrans_c_fix');
h2_aux_pretrans_c_fix2(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_pretrans_c_fix2');
h2_trans_c_fix(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'trans_c_fix');
h2_LKW_cap(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'LKW_cap');
h2_trans_c_overnight(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'trans_c_overnight');
h2_trans_c_fuel(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'fuel_costs');
h2_trans_c_driver(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'driver_wage');
h2_aux_bfhp_sto_c_overnight(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bfhp_sto_c_overnight');
h2_aux_bfhp_sto_c_fix(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bfhp_sto_c_fix');
h2_aux_bfhp_sto_c_fix2(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bfhp_sto_c_fix2');
h2_hp_sto_c_overnight(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hp_sto_c_overnight');
h2_hp_sto_c_fix(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hp_sto_c_fix');
h2_dehyd_evap_c_overnight(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'dehyd_evap_c_overnight');
h2_dehyd_evap_c_fix(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'dehyd_evap_c_fix');
h2_dehyd_evap_c_fix2(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'dehyd_evap_c_fix2');
h2_dehyd_evap_gas(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'dehyd_evap_gas');
h2_lp_sto_station_cap(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'lp_sto_station_cap');
h2_fill_station_cap(n) = h2_parameter_data_table9(n,'fill_station_cap');
h2_MP_sto_station_cap(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'MP_sto_station_cap');
h2_hp_sto_station_cap(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'hp_sto_station_cap');

h2_aux_bflp_sto_c_overnight(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bflp_sto_c_overnight');
h2_aux_bflp_sto_c_fix(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bflp_sto_c_fix');
h2_aux_bflp_sto_c_fix2(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bflp_sto_c_fix2');
h2_aux_bfMP_sto_c_overnight(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bfMP_sto_c_overnight');
h2_aux_bfMP_sto_c_fix(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bfMP_sto_c_fix');
h2_aux_bfMP_sto_c_fix2(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bfMP_sto_c_fix2');
h2_MP_sto_c_overnight(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'MP_sto_c_overnight');
h2_MP_sto_c_fix(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'MP_sto_c_fix');
h2_MP_sto_c_fix2(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'MP_sto_c_fix2');
h2_aux_bffuel_c_overnight(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bffuel_c_overnight');
h2_aux_bffuel_c_fix(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bffuel_c_fix');
h2_aux_bffuel_c_fix2(n,h2_channel) = h2_parameter_data_table6(n,h2_channel,'aux_bffuel_c_fix2');

h2_c_gas(n) = h2_parameter_data_table10(n,'c_gas');

h2_recon_aux_c_overnight(n,h2_channel,h2_tech_recon) = h2_parameter_data_table7(n,h2_channel,h2_tech_recon,'recon_aux_c_overnight');
h2_recon_aux_c_fix(n,h2_channel,h2_tech_recon) = h2_parameter_data_table7(n,h2_channel,h2_tech_recon,'recon_aux_c_fix');
h2_recon_aux_c_fix2(n,h2_channel,h2_tech_recon) = h2_parameter_data_table7(n,h2_channel,h2_tech_recon,'recon_aux_c_fix2');

h2_recon_c_overnight(n,h2_tech_recon) = h2_parameter_data_table8(n,h2_tech_recon,'recon_c_overnight');
h2_recon_c_fix(n,h2_tech_recon) = h2_parameter_data_table8(n,h2_tech_recon,'recon_c_fix');
h2_recon_c_vom(n,h2_tech_recon) = h2_parameter_data_table8(n,h2_tech_recon,'recon_c_vom');
* h2_bidirect_ratio(n,h2_tech_recon) = h2_parameter_data_table8(n,h2_tech_recon,'bidirect_ratio');

*-----nodes parameters and scalars-------------

phi_min_res(n) = nodes_data_upload(n,'phi_min_res');
ev_quant(n) = nodes_data_upload(n,'ev_quant');
phi_pro_self(n) = nodes_data_upload(n,'phi_pro_self');
phi_pro_load(n) = nodes_data_upload(n,'phi_pro_load');
phi_rsvr_min(n) = nodes_data_upload(n,'phi_rsvr_min');

c_infes = scalar_data_upload('c_infes');
c_h_infes = scalar_data_upload('c_h_infes');
c_h_dhw_infes = scalar_data_upload('c_h_dhw_infes');

*--- Temporal H2 data ---

%P2H2%$ontext

d_h2(n,h) = h2_time_data(h,n);
max_d_h2(n) = smax(h,sum(i, d_h2(n,h - ord(i))$(mod(ord(h),24)=0)));
h2_fill_station_nb(n)  = max_d_h2(n) / h2_fill_station_cap(n) ;

d_p2x(n,h,h2_channel) = h2_p2x_time_data(h,n,h2_channel);
max_d_p2x(n,h2_channel) = smax(h,sum(i, d_p2x(n,h - ord(i),h2_channel)$(mod(ord(h),24)=0)));
h2_fill_station_nb_p2x(n,h2_channel)  =  max_d_p2x(n,h2_channel) / h2_fill_station_cap(n) ;

$ontext
$offtext

***************  CALCULATE DERIVED PARAMETERS  *********************************

c_fuel(n,tech)$eta(n,tech) = fuelprice(n,tech)/eta(n,tech) ;
c_co2(n,tech)$eta(n,tech) = carbon_content(n,tech)/eta(n,tech)*CO2price(n,tech);
c_m(n,tech)$eta(n,tech) = c_vom(n,tech) + c_fuel(n,tech) + c_co2(n,tech) ;

c_i(n,tech)$lifetime_tech(n,tech) = c_inv_overnight(n,tech)*( interest_rate_tech(n,tech) * (1+interest_rate_tech(n,tech))**(lifetime_tech(n,tech)) )
                  / ( (1+interest_rate_tech(n,tech))**(lifetime_tech(n,tech))-1 )       ;

c_i_res(n,res) = c_i(n,res) ;
c_fix_res(n,res) = c_fix(n,res) ;

c_i_sto_e(n,sto)$lifetime_sto(n,sto) = c_inv_overnight_sto_e(n,sto)*( interest_rate_sto(n,sto) * (1+interest_rate_sto(n,sto))**(lifetime_sto(n,sto)) )
                 / ( (1+interest_rate_sto(n,sto))**(lifetime_sto(n,sto))-1 )       ;

c_i_sto_p_in(n,sto)$lifetime_sto(n,sto) = c_inv_overnight_sto_p_in(n,sto)*( interest_rate_sto(n,sto) * (1+interest_rate_sto(n,sto))**(lifetime_sto(n,sto)) )
                 / ( (1+interest_rate_sto(n,sto))**(lifetime_sto(n,sto))-1 )       ;

c_i_sto_p_out(n,sto)$lifetime_sto(n,sto) = c_inv_overnight_sto_p_out(n,sto)*( interest_rate_sto(n,sto) * (1+interest_rate_sto(n,sto))**(lifetime_sto(n,sto)) )
                 / ( (1+interest_rate_sto(n,sto))**(lifetime_sto(n,sto))-1 )       ;

c_i_rsvr_p_in(n,rsvr) = c_inv_overnight_rsvr_p_in(n,rsvr)*( inv_interest_rsvr(n,rsvr) * (1+inv_interest_rsvr(n,rsvr))**(inv_lifetime_rsvr(n,rsvr)) )
                 / ( (1+inv_interest_rsvr(n,rsvr))**(inv_lifetime_rsvr(n,rsvr))-1 )       ;

c_i_rsvr_p_out(n,rsvr) = c_inv_overnight_rsvr_p_out(n,rsvr)*( inv_interest_rsvr(n,rsvr) * (1+inv_interest_rsvr(n,rsvr))**(inv_lifetime_rsvr(n,rsvr)) )
                 / ( (1+inv_interest_rsvr(n,rsvr))**(inv_lifetime_rsvr(n,rsvr))-1 )       ;

c_i_rsvr_e(n,rsvr) = c_inv_overnight_rsvr_e(n,rsvr)*( inv_interest_rsvr(n,rsvr) * (1+inv_interest_rsvr(n,rsvr))**(inv_lifetime_rsvr(n,rsvr)) )
                 / ( (1+inv_interest_rsvr(n,rsvr))**(inv_lifetime_rsvr(n,rsvr))-1 )       ;

c_i_dsm_cu(n,dsm_curt)$inv_lifetime_dsm_cu(n,dsm_curt) =c_inv_overnight_dsm_cu(n,dsm_curt)*( inv_interest_dsm_cu(n,dsm_curt) * (1+inv_interest_dsm_cu(n,dsm_curt))**(inv_lifetime_dsm_cu(n,dsm_curt)) )
                 / ( (1+inv_interest_dsm_cu(n,dsm_curt))**(inv_lifetime_dsm_cu(n,dsm_curt))-1 )       ;

c_i_dsm_shift(n,dsm_shift)$inv_lifetime_dsm_shift(n,dsm_shift) = c_inv_overnight_dsm_shift(n,dsm_shift)*( inv_interest_dsm_shift(n,dsm_shift) * (1+inv_interest_dsm_shift(n,dsm_shift))**(inv_lifetime_dsm_shift(n,dsm_shift)) )
                 / ( (1+inv_interest_dsm_shift(n,dsm_shift))**(inv_lifetime_dsm_shift(n,dsm_shift))-1 )       ;

c_i_ntc(l)$inv_lifetime_ntc(l) = dist(l) * (c_inv_overnight_ntc(l) * (inv_interest_ntc(l) * (1 + inv_interest_ntc(l))**(inv_lifetime_ntc(l)) )
                 / ((1 + inv_interest_ntc(l)) ** (inv_lifetime_ntc(l))-1 ) ) ;

c_fix_ntc(l) = c_fix_ntc_per_km(l) * dist(l) ;

eta_ntc(l) = 1 - loss_ntc(l) * dist(l)/100 ;

phi_mean_reserves_call(n,reserves) = sum(h, phi_reserves_call(n,reserves,h) ) / card(h) + eps ;


theta_sets(n,bu,'setsh')$(smax( (heat_storage,heat_hp,heat_elec,heat_fossil,headers_heat) , heat_data_upload(n,bu,'setsh',heat_storage,heat_hp,heat_elec,heat_fossil,headers_heat)) > 0 AND phi_heat_type(n,bu,'setsh')) = 1;
theta_dir(n,bu,'dir')$(smax((heat_storage,heat_hp,heat_elec,heat_fossil,headers_heat) , heat_data_upload(n,bu,'dir',heat_storage,heat_hp,heat_elec,heat_fossil,headers_heat)) > 0 AND phi_heat_type(n,bu,'dir')) = 1;

theta_storage(n,bu,ch)$(sum((heat_hp,heat_elec,heat_fossil,headers_heat), heat_data_upload(n,bu,ch,'yes',heat_hp,heat_elec,heat_fossil,headers_heat)) AND phi_heat_type(n,bu,ch)) = 1;
theta_hp(n,bu,ch)$sum( (heat_storage,heat_elec,heat_fossil,headers_heat), heat_data_upload(n,bu,ch,heat_storage,'yes',heat_elec,heat_fossil,headers_heat) AND phi_heat_type(n,bu,ch)) = 1;

theta_elec(n,bu,ch)$sum( (heat_storage,heat_hp,heat_fossil,headers_heat), heat_data_upload(n,bu,ch,heat_storage,heat_hp,'yes',heat_fossil,headers_heat) AND phi_heat_type(n,bu,ch)) = 1;
theta_fossil(n,bu,ch)$sum( (heat_storage,heat_hp,heat_elec,headers_heat), heat_data_upload(n,bu,ch,heat_storage,heat_hp,heat_elec,'yes',headers_heat) AND phi_heat_type(n,bu,ch)) = 1;

*--- Cost Parameters - Annualized ---

%P2H2%$ontext

h2_prod_c_a_overnight(n,h2_tech) = h2_prod_c_overnight(n,h2_tech)*( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_prod_lifetime(n,h2_tech)) ) / ( (1+h2_interest_rate(n))**(h2_prod_lifetime(n,h2_tech))-1 );
h2_prod_c_a_fix(n,h2_tech) =  h2_prod_c_fix(n,h2_tech);
h2_prod_c_a_fix2(n,h2_tech) = h2_prod_c_fix2(n,h2_tech);

h2_prod_aux_c_a_overnight(n,h2_tech,h2_channel) = h2_prod_aux_c_overnight(n,h2_tech,h2_channel)*( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_prod_aux_lifetime(n,h2_tech,h2_channel)) ) / ( (1+h2_interest_rate(n))**(h2_prod_aux_lifetime(n,h2_tech,h2_channel))-1 )  + h2_prod_aux_c_fix(n,h2_tech,h2_channel) + h2_prod_aux_c_fix2(n,h2_tech,h2_channel)     ;
h2_hyd_liq_c_a_overnight(n,h2_channel) = h2_hyd_liq_c_overnight(n,h2_channel)*( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_hyd_liq_lifetime(n,h2_channel)) ) / ( (1+h2_interest_rate(n))**(h2_hyd_liq_lifetime(n,h2_channel))-1 ) + h2_hyd_liq_c_fix(n,h2_channel) + h2_hyd_liq_c_fix2(n,h2_channel)      ;
h2_sto_p_c_a_overnight(n,h2_channel) = h2_sto_p_c_overnight(n,h2_channel)*( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_sto_p_lifetime(n,h2_channel)) ) / ( (1+h2_interest_rate(n))**(h2_sto_p_lifetime(n,h2_channel))-1 )   + h2_sto_p_c_fix(n,h2_channel) + h2_sto_p_c_fix2(n,h2_channel)    ;
h2_lp_sto_c_a_overnight(n,h2_channel) = h2_lp_sto_c_overnight(n,h2_channel)*( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_lp_sto_lifetime(n,h2_channel)) ) / ( (1+h2_interest_rate(n))**(h2_lp_sto_lifetime(n,h2_channel))-1 )  + h2_lp_sto_c_fix(n,h2_channel) + h2_lp_sto_c_fix2(n,h2_channel)     ;
h2_aux_pretrans_c_a_overnight(n,h2_channel) = h2_aux_pretrans_c_overnight(n,h2_channel)*( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_aux_pretrans_lifetime(n,h2_channel)) ) / ( (1+h2_interest_rate(n))**(h2_aux_pretrans_lifetime(n,h2_channel))-1 )  + h2_aux_pretrans_c_fix(n,h2_channel) + h2_aux_pretrans_c_fix2(n,h2_channel)     ;
h2_trans_c_a_overnight(n,h2_channel) = h2_trans_c_overnight(n,h2_channel)*( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_trans_lifetime(n,h2_channel)) ) / ( (1+h2_interest_rate(n))**(h2_trans_lifetime(n,h2_channel))-1 ) + h2_trans_c_fix(n,h2_channel)   ;
aux_bfhp_sto_c_a_overnight(n,h2_channel) = h2_aux_bfhp_sto_c_overnight(n,h2_channel)*( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_aux_bfhp_sto_lifetime(n,h2_channel)) ) / ( (1+h2_interest_rate(n))**(h2_aux_bfhp_sto_lifetime(n,h2_channel))-1 )  + h2_aux_bfhp_sto_c_fix(n,h2_channel)  + h2_aux_bfhp_sto_c_fix2(n,h2_channel)  ;


h2_hp_sto_c_a_overnight(n,h2_channel) = h2_hp_sto_c_overnight(n,h2_channel)*( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_hp_sto_lifetime(n,h2_channel)) ) / ( (1+h2_interest_rate(n))**(h2_hp_sto_lifetime(n,h2_channel))-1 )   + h2_hp_sto_c_fix(n,h2_channel)  ;
h2_dehyd_evap_c_a_overnight(n,h2_channel) = h2_dehyd_evap_c_overnight(n,h2_channel)*( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_dehyd_evap_lifetime(n,h2_channel)) ) / ( (1+h2_interest_rate(n))**(h2_dehyd_evap_lifetime(n,h2_channel))-1 )  + h2_dehyd_evap_c_fix(n,h2_channel) + h2_dehyd_evap_c_fix2(n,h2_channel)     ;

h2_aux_bflp_sto_c_a_overnight(n,h2_channel) = h2_aux_bflp_sto_c_overnight(n,h2_channel)*( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_aux_bflp_sto_lifetime(n,h2_channel)) ) / ( (1+h2_interest_rate(n))**(h2_aux_bflp_sto_lifetime(n,h2_channel))-1 ) + h2_aux_bflp_sto_c_fix(n,h2_channel) + h2_aux_bflp_sto_c_fix2(n,h2_channel)      ;
h2_aux_bfMP_sto_c_a_overnight(n,h2_channel) = h2_aux_bfMP_sto_c_overnight(n,h2_channel)*( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_aux_bfMP_sto_lifetime(n,h2_channel)) ) / ( (1+h2_interest_rate(n))**(h2_aux_bfMP_sto_lifetime(n,h2_channel))-1 ) + h2_aux_bfMP_sto_c_fix(n,h2_channel) + h2_aux_bfMP_sto_c_fix2(n,h2_channel)      ;
h2_MP_sto_c_a_overnight(n,h2_channel) = h2_MP_sto_c_overnight(n,h2_channel)*( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_MP_sto_lifetime(n,h2_channel)) ) / ( (1+h2_interest_rate(n))**(h2_MP_sto_lifetime(n,h2_channel))-1 ) + h2_MP_sto_c_fix(n,h2_channel) + h2_MP_sto_c_fix2(n,h2_channel)      ;
h2_aux_bffuel_c_a_overnight(n,h2_channel) = h2_aux_bffuel_c_overnight(n,h2_channel)*( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_aux_bffuel_lifetime(n,h2_channel)) ) / ( (1+h2_interest_rate(n))**(h2_aux_bffuel_lifetime(n,h2_channel))-1 ) + h2_aux_bffuel_c_fix(n,h2_channel) + h2_aux_bffuel_c_fix2(n,h2_channel)      ;


h2_recon_aux_c_a_overnight(n,h2_channel,h2_tech_recon) = h2_recon_aux_c_overnight(n,h2_channel,h2_tech_recon)*( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_recon_aux_lifetime(n,h2_channel,h2_tech_recon)) ) /( (1+h2_interest_rate(n))**(h2_recon_aux_lifetime(n,h2_channel,h2_tech_recon))-1 ) + h2_recon_aux_c_fix(n,h2_channel,h2_tech_recon) + h2_recon_aux_c_fix2(n,h2_channel,h2_tech_recon)      ;

h2_recon_c_a_overnight(n,h2_tech_recon) = h2_recon_c_overnight(n,h2_tech_recon) * ( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_recon_lifetime(n,h2_tech_recon)) ) / ( (1+h2_interest_rate(n))**(h2_recon_lifetime(n,h2_tech_recon))-1 ) + h2_recon_c_fix(n,h2_tech_recon)      ;

h2_prod_c_ad_overnight(n,h2_tech) = h2_prod_c_overnight(n,h2_tech) * h2_prod_scale(n,h2_tech) ;
h2_prod_c_ad_a_overnight(n,h2_tech) = h2_prod_c_ad_overnight (n,h2_tech)*( h2_interest_rate(n) * (1+h2_interest_rate(n))**(h2_prod_lifetime(n,h2_tech)) ) / ( (1+h2_interest_rate(n))**(h2_prod_lifetime(n,h2_tech))-1 ) ;

h2_prod_c_ad_fix(n,h2_tech) = h2_prod_c_fix(n,h2_tech) *  h2_prod_scale(n,h2_tech) ;
h2_prod_c_ad_a_fix(n,h2_tech) = h2_prod_c_fix(n,h2_tech) *  h2_prod_scale(n,h2_tech) ;

h2_prod_c_ad_fix2(n,h2_tech) = h2_prod_c_fix2(n,h2_tech) *  h2_prod_scale(n,h2_tech) ;
h2_prod_c_ad_a_fix2(n,h2_tech) = h2_prod_c_fix2(n,h2_tech) *  h2_prod_scale(n,h2_tech) ;

h2_trans_c_var(n,h2_channel) = ( h2_trans_c_fuel(n,h2_channel) * h2_trans_c_driver(n,h2_channel)/100  + h2_trans_c_driver(n,h2_channel)/50 ) / max(1,h2_LKW_cap(n,h2_channel)) ;


*--- Derived Sets ---
h2_prod_aux_set(n,h2_tech,h2_channel)=yes$h2_prod_aux_sw(n,h2_tech,h2_channel) ;
h2_hyd_liq_set(n,h2_channel)=yes$h2_hyd_liq_sw(n,h2_channel) ;
h2_sto_p_set(n,h2_channel)=yes$h2_sto_p_sw(n,h2_channel) ;
h2_lp_sto_set(n,h2_channel)=yes$h2_lp_sto_sw(n,h2_channel) ;
h2_aux_pretrans_set(n,h2_channel)=yes$h2_aux_pretrans_sw(n,h2_channel) ;
h2_aux_bfhp_sto_set(n,h2_channel)=yes$h2_aux_bfhp_sto_sw(n,h2_channel) ;
h2_hp_sto_set(n,h2_channel)=yes$h2_hp_sto_sw(n,h2_channel) ;
h2_dehyd_evap_set(n,h2_channel)=yes$h2_dehyd_evap_sw(n,h2_channel) ;
h2_trans_set(n,h2_channel)=yes$h2_trans_sw(n,h2_channel) ;
h2_channel_wo_decent_set(h2_channel) = yes ;

h2_channel_wo_decent_set('fuel_decent') = no ;

* h2_bi_recon_set(n,h2_tech_recon)=no;
* h2_bi_recon_set(n,h2_tech_recon)=yes$h2_bidirect_sw(n,h2_tech_recon) ;


h2_tech_avail_set(n,h2_tech)=yes$h2_tech_avail_sw(n,h2_tech) ;
h2_channel_avail_set(n,h2_channel)=yes$h2_channel_avail_sw(n,h2_channel) ;

h2_tech_recon_avail_set(n,h2_tech_recon)=yes$h2_tech_recon_sw(n,h2_tech_recon) ;
h2_recon_set(n,h2_channel)=yes$h2_recon_sw(n,h2_channel) ;
h2_mobility_set(n,h2_channel)=yes$h2_mobility_sw(n,h2_channel) ;
h2_p2x_set(n,h2_channel)=yes$h2_p2x_sw(n,h2_channel) ;


h2_recon_aux_set(n,h2_channel,h2_tech_recon)=yes$h2_recon_aux_sw(n,h2_channel,h2_tech_recon) ;
h2_aux_bflp_sto_set(n,h2_channel)=yes$h2_aux_bflp_sto_sw(n,h2_channel) ;
h2_aux_bfMP_sto_set(n,h2_channel)=yes$h2_aux_bfMP_sto_sw(n,h2_channel) ;
h2_MP_sto_set(n,h2_channel)=yes$h2_MP_sto_sw(n,h2_channel) ;
h2_aux_bffuel_set(n,h2_channel)=yes$h2_aux_bffuel_sw(n,h2_channel) ;

$ontext
$offtext

***************  Adjust costs to model's hourly basis **************************

c_i(n,tech) = c_i(n,tech)*card(h)/8760 ;
c_i_res(n,tech) = c_i_res(n,tech)*card(h)/8760 ;
c_i_sto_p_in(n,sto) = c_i_sto_p_in(n,sto)*card(h)/8760 ;
c_i_sto_p_out(n,sto) = c_i_sto_p_out(n,sto)*card(h)/8760 ;
c_i_sto_e(n,sto) = c_i_sto_e(n,sto)*card(h)/8760 ;
c_i_rsvr_p_in(n,rsvr) = c_i_rsvr_p_in(n,rsvr)*card(h)/8760 ;
c_i_rsvr_p_out(n,rsvr) = c_i_rsvr_p_out(n,rsvr)*card(h)/8760 ;
c_i_rsvr_e(n,rsvr) = c_i_rsvr_e(n,rsvr)*card(h)/8760 ;
c_i_dsm_cu(n,dsm_curt) = c_i_dsm_cu(n,dsm_curt)*card(h)/8760 ;
c_i_dsm_shift(n,dsm_shift) = c_i_dsm_shift(n,dsm_shift)*card(h)/8760 ;

c_fix(n,tech) = c_fix(n,tech)*card(h)/8760 ;
c_fix_sto_p_in(n,sto) = c_fix_sto_p_in(n,sto)*card(h)/8760 ;
c_fix_sto_p_out(n,sto) = c_fix_sto_p_out(n,sto)*card(h)/8760 ;
c_fix_sto_e(n,sto) = c_fix_sto_e(n,sto)*card(h)/8760 ;
c_fix_dsm_cu(n,dsm_curt) = c_fix_dsm_cu(n,dsm_curt)*card(h)/8760 ;
c_fix_dsm_shift(n,dsm_shift) = c_fix_dsm_shift(n,dsm_shift)*card(h)/8760 ;
c_fix_rsvr_p_in(n,rsvr) = c_fix_rsvr_p_in(n,rsvr)*card(h)/8760 ;
c_fix_rsvr_p_out(n,rsvr) = c_fix_rsvr_p_out(n,rsvr)*card(h)/8760 ;
c_fix_rsvr_e(n,rsvr) = c_fix_rsvr_e(n,rsvr)*card(h)/8760 ;

m_e(n,'bio') = m_e(n,'bio')*card(h)/8760 ;

c_i_ntc(l) = c_i_ntc(l) * card(h)/8760 ;

%P2H2%$ontext

h2_prod_c_a_overnight(n,h2_tech) = h2_prod_c_a_overnight(n,h2_tech)*card(h)/8760 ;
h2_prod_c_ad_a_overnight(n,h2_tech) = h2_prod_c_ad_a_overnight(n,h2_tech)*card(h)/8760 ;
h2_prod_c_a_fix(n,h2_tech) = h2_prod_c_a_fix(n,h2_tech)*card(h)/8760 ;
h2_prod_c_a_fix2(n,h2_tech) = h2_prod_c_a_fix2(n,h2_tech)*card(h)/8760 ;
h2_prod_c_ad_a_fix(n,h2_tech) = h2_prod_c_ad_a_fix(n,h2_tech)*card(h)/8760 ;
h2_prod_c_ad_a_fix2(n,h2_tech) = h2_prod_c_ad_a_fix2(n,h2_tech)*card(h)/8760 ;
h2_prod_aux_c_a_overnight(n,h2_tech,h2_channel) = h2_prod_aux_c_a_overnight(n,h2_tech,h2_channel)*card(h)/8760 ;
h2_hyd_liq_c_a_overnight(n,h2_channel) = h2_hyd_liq_c_a_overnight(n,h2_channel)*card(h)/8760 ;
h2_sto_p_c_a_overnight(n,h2_channel) = h2_sto_p_c_a_overnight(n,h2_channel)*card(h)/8760 ;
h2_lp_sto_c_a_overnight(n,h2_channel) = h2_lp_sto_c_a_overnight(n,h2_channel)*card(h)/8760 ;
h2_aux_pretrans_c_a_overnight(n,h2_channel) = h2_aux_pretrans_c_a_overnight(n,h2_channel)*card(h)/8760 ;
h2_trans_c_a_overnight(n,h2_channel) = h2_trans_c_a_overnight(n,h2_channel)*card(h)/8760 ;
aux_bfhp_sto_c_a_overnight(n,h2_channel) = aux_bfhp_sto_c_a_overnight(n,h2_channel)*card(h)/8760 ;
h2_hp_sto_c_a_overnight(n,h2_channel) = h2_hp_sto_c_a_overnight(n,h2_channel)*card(h)/8760 ;
h2_dehyd_evap_c_a_overnight(n,h2_channel) = h2_dehyd_evap_c_a_overnight(n,h2_channel)*card(h)/8760 ;
h2_aux_bflp_sto_c_a_overnight(n,h2_channel) = h2_aux_bflp_sto_c_a_overnight(n,h2_channel)*card(h)/8760;
h2_aux_bfMP_sto_c_a_overnight(n,h2_channel) = h2_aux_bfMP_sto_c_a_overnight(n,h2_channel)*card(h)/8760;
h2_MP_sto_c_a_overnight(n,h2_channel) = h2_MP_sto_c_a_overnight(n,h2_channel)*card(h)/8760;
h2_aux_bffuel_c_a_overnight(n,h2_channel) = h2_aux_bffuel_c_a_overnight(n,h2_channel)*card(h)/8760;

h2_recon_aux_c_a_overnight(n,h2_channel,h2_tech_recon) = h2_recon_aux_c_a_overnight(n,h2_channel,h2_tech_recon)*card(h)/8760 ;

h2_recon_c_a_overnight(n,h2_tech_recon) = h2_recon_c_a_overnight(n,h2_tech_recon)*card(h)/8760 ;

h2_recon_c_fix(n,h2_tech_recon) = h2_recon_c_fix(n,h2_tech_recon)*card(h)/8760 ;

$ontext
$offtext

***************  Check for parameter sanity ************************************

Parameter
check_heat
check_heat_agg ;
check_heat(n,bu) = sum( ch , phi_heat_type(n,bu,ch)) ;
check_heat_agg = smax( (n,bu) , check_heat(n,bu) ) ;
*abort$(check_heat_agg > 1) "DATA: heating technologies for a building type do not add up to 100 percent" ;

%P2H2%$ontext

* sanity checks
abort$( sum( (n,h2_channel) , h2_recon_sw(n,h2_channel) + h2_mobility_sw(n,h2_channel) + h2_p2x_sw(n,h2_channel) ) / ( card(n) * card(h2_channel) ) > 1 ) "Only 'h2_mobility_sw' or 'recon_sw' or 'p2x_sw' can be chosen, but not two or more of them at the same time."
abort$( sum ( n , 1$( h2_tech_avail_sw(n,'PEM') = 0 AND h2_channel_avail_sw(n,'fuel_decent') = 1  ) ) > 0 ) "Using the channel 'fuel_decent' requires the electrolysis technology 'PEM'."
abort$( sum ( n , 1$( h2_channel_avail_sw(n,'fuel_decent') = 1 AND ( h2_recon_sw(n,'fuel_decent') = 1 OR h2_p2x_sw(n,'fuel_decent') ) ) ) > 0 ) "The channel 'fuel_decent' cannot be used for reconversion or p2x."
abort$( sum ( n , sum( h2_channel_wo_decent_set , 1$( h2_sto_p_type(n,h2_channel_wo_decent_set) = h2_sto_p_type(n,'fuel_decent') ) ) ) > 0 ) "The channel 'fuel_decent' must use a different storage type (number-identifier) as storage cannot be shared with other supply chains."

$ontext
$offtext


***************  Infeasibility *************************************************

Positive variable
G_INFES(n,h)
H_INFES(n,bu,ch,h)
H_DHW_INFES(n,bu,ch,h)
;

Scalar ms 'model status', ss 'solve status';
