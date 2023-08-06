$setglobal end_hour %py_end_hour%
$setglobal h_set %py_h_set%
$setglobal data_input_gdx %py_data_input_gdx%
$setglobal iter_countries_switch_on   %py_iter_countries_switch_on%
$setglobal iter_countries_switch_off  %py_iter_countries_switch_off%
$setglobal net_transfer %py_network_transfer%

Sets

t "All tech gen and sto"
n "nodes"
s(t) "storage"
g(t) "tech"
h "Hours"
l "Lines"
;

alias (s,sto);

Parameters
c_i_tech(n,g)
c_i_sto_p(n,s)
c_i_sto_e(n,s)
c_m_tech(n,g)
c_m_sto(n,s)
c_fix_tech(n,g)
c_fix_sto(n,s)
c_fix_pros(n)
d(n,h)
eta_sto(n,s)
max_tech_p(n,g)
min_tech_p(n,g)
max_sto_p(n,s)
max_sto_e(n,s)
min_sto_p(n,s)
min_sto_e(n,s)
phi_tech(n,g,h)
eta_ntc(l)
max_flow(l)
incidence_matrix(l,n)
;

scalar
ms
ss
;

*----------------------------------
*------- Definition end_hour ------
*----------------------------------
%end_hour%$ontext

Set h "Hours" / %h_set% / ;

$ontext
$offtext

*----------------------------------
*--------- Import data gdx --------
*----------------------------------
Sets
tech_headers
sto_headers
nodes_headers
lines_headers
;

Parameters
tech_data(n,g,tech_headers)
sto_data(n,s,sto_headers)
nodes_data(n,nodes_headers)
lines_data(l,lines_headers)
dem(h,n)
phi_t(h,n,g)
;

* with iteration
%iter_countries_switch_on%$ontext

$include "%py_modeldir%countries-lines.gms"
$ontext
$offtext

* without iteration
%iter_countries_switch_off%$ontext
$GDXin "%data_input_gdx%"
$load n l
;

$ontext
$offtext

$GDXin "%data_input_gdx%"
%end_hour%$load h
$load t g s
$load tech_headers sto_headers nodes_headers lines_headers
$load tech_data sto_data nodes_data lines_data dem phi_t incidence_matrix
;

c_i_tech(n,g) = tech_data(n,g,'c_i_tech');
c_m_tech(n,g) = tech_data(n,g,'c_m_tech');
max_tech_p(n,g) = tech_data(n,g,'max_tech_p');
min_tech_p(n,g) = tech_data(n,g,'min_tech_p');
c_fix_tech(n,g) = tech_data(n,g,'c_fix_tech');
c_i_sto_p(n,s) = sto_data(n,s,'c_i_sto_p');
c_i_sto_e(n,s) = sto_data(n,s,'c_i_sto_e');
c_m_sto(n,s) = sto_data(n,s,'c_m_sto');
c_fix_sto(n,s) = sto_data(n,s,'c_fix_sto');
eta_sto(n,s) = sqrt(sto_data(n,s,'eta_sto'));
max_sto_p(n,s) = sto_data(n,s,'max_sto_p');
max_sto_e(n,s) = sto_data(n,s,'max_sto_e');
min_sto_p(n,s) = sto_data(n,s,'min_sto_p');
min_sto_e(n,s) = sto_data(n,s,'min_sto_e');

d(n,h) = dem(h,n);
phi_tech(n,g,h)  = phi_t(h,n,g);
max_flow(l) = lines_data(l,'max_flow');
eta_ntc(l) = lines_data(l,'eta_ntc');

*----------------------------------
*------------ MCP MODEL -----------
*----------------------------------

Variables
Z
F(l,h)
;

Positive Variables

G_L(n,g,h)             Generation level in hour h [MWh]
CU(n,g,h)              Thermal losses for fossil and Renewables curtailment technology for res in hour h [MWh]

STO_IN(n,s,t,h)        Storage inflow technology sto hour h [MWh]
STO_OUT(n,s,h)         Storage outflow technology sto hour h [MWh]
STO_L(n,s,h)           Storage level technology sto hour h [MWh]

N_TECH(n,g)            Technology tech built [MW]
N_STO_E(n,s)           Storage technology built - Energy [MWh]
N_STO_P(n,s)           Storage loading and discharging capacity built - Capacity [MW]

STO_L0(n,s)

STO_OUT_GRID(n,s,h)
STO_OUTgoIN(n,s,sto,h)
G_GRID(n,g,h)
;

Equations
OF
eq_nodalbalance(n,h)
eq_tech_level(n,g,h)
eq_sto_level(n,s,h)
eq_stolfinal(n,s)

eq_stoout_divide(n,s,h)
eq_stooutgoin_nosame(n,s,sto,h)
eq_stoin_nosame(n,s,sto,h)
eq_stoin_with_stooutgoin(n,s,sto,h)
eq_gtotal(n,g,h)

eq_mutech_lo(n,g,h)
eq_mutech_up(n,g,h)
eq_musto_lo(n,s,h)
eq_musto_up(n,s,h)
eq_mustoin_lo(n,s,h)
eq_mustoin_up(n,s,h)
eq_mustoout_lo(n,s,h)
eq_mustoout_up(n,s,h)
eq_mutechpmin(n,g)
eq_mutechpmax(n,g)
eq_mustopmin(n,s)
eq_mustopmax(n,s)
eq_mustoemin(n,s)
eq_mustoemax(n,s)

eq_mustol0_up(n,s)
eq_mustol0_lo(n,s)
eq_mumaxflowi(l,h)
eq_mumaxflowo(l,h)
;

OF..
    Z =e= 

Sum(n, 
    + sum(g, c_i_tech(n,g)*N_TECH(n,g)*card(h)/8760)
    + sum(g, c_fix_tech(n,g)*N_TECH(n,g)*card(h)/8760)
    + sum(s, c_i_sto_e(n,s)*N_STO_E(n,s)*card(h)/8760)
    + sum(s, c_i_sto_p(n,s)*N_STO_P(n,s)*card(h)/8760)
    + sum(s, c_fix_sto(n,s)/2*(N_STO_P(n,s) + N_STO_E(n,s))*card(h)/8760)
    + sum(h, 
        + sum(g, G_L(n,g,h)*c_m_tech(n,g))
        + sum(s, (sum(t, STO_IN(n,s,t,h)) + STO_OUT(n,s,h))*c_m_sto(n,s))
        )
    )
;
* Balances
eq_nodalbalance(n,h)..
    d(n,h) + sum((s,g), STO_IN(n,s,g,h)) - sum(g, G_L(n,g,h)) - sum(s, STO_OUT_GRID(n,s,h)) +  sum( l , incidence_matrix(l,n) * eta_ntc(l) * F(l,h)) =e= EPS
;
eq_tech_level(n,g,h)..
    (G_L(n,g,h) + CU(n,g,h) - phi_tech(n,g,h)*N_TECH(n,g)) =e= EPS
;
eq_sto_level(n,s,h)..
    (STO_L(n,s,h) - STO_L(n,s,h-1)$(ord(h)>1) - STO_L0(n,s)$(ord(h)=1) - sum(t, STO_IN(n,s,t,h))*eta_sto(n,s) + STO_OUT(n,s,h)/eta_sto(n,s)) =e= EPS
;
eq_stolfinal(n,s)..
    sum(h, STO_L(n,s,h)$(card(h)=ord(h))) - STO_L0(n,s) =e= EPS
;
eq_stoout_divide(n,s,h)..
    STO_OUT(n,s,h) - (STO_OUT_GRID(n,s,h) + sum(sto, STO_OUTgoIN(n,s,sto,h))) =e= EPS
;
eq_stooutgoin_nosame(n,s,sto,h)$(ord(s)=ord(sto))..
    STO_OUTgoIN(n,s,sto,h) =E= EPS
;
eq_stoin_nosame(n,s,sto,h)$(ord(s)=ord(sto))..
    STO_IN(n,s,sto,h) =E= EPS
;
eq_stoin_with_stooutgoin(n,s,sto,h)..
    STO_OUTgoIN(n,s,sto,h) - STO_IN(n,sto,s,h) =E= EPS
;
eq_gtotal(n,g,h)..
    G_L(n,g,h) - G_GRID(n,g,h) - sum(s, STO_IN(n,s,g,h)) =E= EPS
;
eq_mutech_lo(n,g,h)..
    -1*(-G_L(n,g,h)) =G= EPS
;
eq_mutech_up(n,g,h)..
    -1*(G_L(n,g,h) - N_TECH(n,g)) =G= EPS
;
eq_musto_lo(n,s,h)..
    -1*(-STO_L(n,s,h)) =G= EPS
;
eq_musto_up(n,s,h)..
    -1*(STO_L(n,s,h) - N_STO_E(n,s)) =G= EPS
;
eq_mustoin_lo(n,s,h)..
    -1*(-sum(t, STO_IN(n,s,t,h))) =G= EPS
;
eq_mustoin_up(n,s,h)..
    -1*(sum(t, STO_IN(n,s,t,h)) - N_STO_P(n,s)) =G= EPS
;
eq_mustoout_lo(n,s,h)..
    -1*(-STO_OUT(n,s,h)) =G= EPS
;
eq_mustoout_up(n,s,h)..
    -1*(STO_OUT(n,s,h) - N_STO_P(n,s)) =G= EPS
;
eq_mutechpmin(n,g)..
    -1*(min_tech_p(n,g) - N_TECH(n,g)) =G= EPS
;
eq_mutechpmax(n,g)..
    -1*(N_TECH(n,g) - max_tech_p(n,g)) =G= EPS
;
eq_mustopmin(n,s)..
    -1*(min_sto_p(n,s) - N_STO_P(n,s)) =G= EPS
;
eq_mustopmax(n,s)..
    -1*(N_STO_P(n,s) - max_sto_p(n,s)) =G= EPS
;
eq_mustoemin(n,s)..
    -1*(min_sto_e(n,s) - N_STO_E(n,s)) =G= EPS
;
eq_mustoemax(n,s)..
    -1*(N_STO_E(n,s) - max_sto_e(n,s)) =G= EPS
;

eq_mustol0_up(n,s)..
    -1*(STO_L0(n,s) - N_STO_E(n,s)) =G= EPS
;
eq_mustol0_lo(n,s)..
    -1*(-STO_L0(n,s)) =G= EPS
;
eq_mumaxflowi(l,h)..
    F(l,h) - max_flow(l) =L= EPS
;
eq_mumaxflowo(l,h)..
    F(l,h) + max_flow(l) =G= EPS
;

model DEMO / 
OF
eq_nodalbalance
eq_tech_level
eq_sto_level
eq_stolfinal

eq_stoout_divide
eq_stooutgoin_nosame
eq_stoin_nosame
eq_stoin_with_stooutgoin
eq_gtotal

eq_mutech_lo
eq_mutech_up
eq_musto_lo
eq_musto_up
eq_mustoin_lo
eq_mustoin_up
eq_mustoout_lo
eq_mustoout_up
eq_mutechpmin
eq_mutechpmax
eq_mustopmin
eq_mustopmax
eq_mustoemin
eq_mustoemax

eq_mustol0_up
eq_mustol0_lo

eq_mumaxflowi
eq_mumaxflowo
/ 
;

$onecho > cplex.opt

lpmethod 4
threads 0
SolutionType 2
barepcomp 1e-8
datacheck 2
quality 1
predual -1

$offecho

$onecho > cplexd.opt

lpmethod 4
threads 1
SolutionType 2
barepcomp 1e-8
datacheck 2
quality 1
predual -1

$offecho

* In case only one node load exchanges are set to zero
%net_transfer%F.fx(l,h) = 0 ;

