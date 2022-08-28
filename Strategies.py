import numpy as np
from scipy.stats import norm as N
import math
from BlackScholesFormulae import Call, Put
import opstrat as op

"""
These strategies are all taken from "Trading strategies involving options", Ch11 - Hull.
"""
"""
First strategy attempt to program is a Bull Spread. The inputs will be the usual for finding an option, but also the other two strikes.
The call with the higher strike price is shorted, whilst the call with the lower strike price is held long.
"""
# An idea is to also create payoff diagrams? Will need classes for this. Can use the opstrat module above.
# Test data
Type = "E"
S0 = 100
k1, k2 = 95, 105
r = 0.1
vol = 0.2
T = 0.5
"""
BULL SPREAD (requires initial investment)
A bull spread can also be created by puts, by longing the put with the lower strike and shorting put with higher strike.
This requires a positive up-front cash flow to the investor!
"""


def BullSpread(S0, k1, k2, r, vol, T):
    K1, K2 = k1, k2
    if k2 < k1:
        # this ensures that K2 is always the greater strike price. Probably inefficient, check.
        K1, K2 = k2, k1
    c1 = Call(S0, K1, r, vol, T)  # long a call with the lower strike
    c2 = Call(S0, K2, r, vol, T)  # short a call with the higher strike
    cost = c1-c2
    print("This Bull spread strategy consists of going long a call of strike", K1, "at a cost of", c1,
          "and going short a call of strike", K2, "with return", c2, "for a total cost of", cost)
    # Below plots the bullspread also. Make code look neater.
    op_1 = {'op_type': 'c', 'strike': K2, 'tr_type': 's', 'op_pr': c2}
    op_2 = {'op_type': 'c', 'strike': K1, 'tr_type': 'b', 'op_pr': c1}
    op.multi_plotter(spot=S0, op_list=[op_1, op_2])

    # this outputs the relevant data, starting with cost of strategy and then ascending in order of strike.
    data = [cost, c1, c2]
    return data


#BullSpread(S0, k1, k2, r, vol, T)

"""
BEAR SPREAD (requires initial cash outflow)
Investor hopes/speculates the stock price will decline. Bear spreads created with calls require initial cash flow INFLOW.
"""


def BearSpread(S0, k1, k2, r, vol, T):
    K1, K2 = k1, k2
    if k2 < k1:
        K1, K2 = k2, k1
    p1 = Put(Type ,S0, K1, r, vol, T)
    p2 = Put(Type ,S0, K2, r, vol, T)
    cost = p2-p1
    print("This Bear spread strategy consists of going long a put of strike", K2, "at a cost of", p2,
          "and going short a put of strike", K1, "with return", p1, "for a total cost of", cost)
    op_1 = {'op_type': 'p', 'strike': K2, 'tr_type': 'b', 'op_pr': p2}
    op_2 = {'op_type': 'p', 'strike': K1, 'tr_type': 's', 'op_pr': p1}
    op.multi_plotter(spot=S0, op_list=[op_1, op_2])
    data = [cost, p1, p2]
    return data

#BearSpread(S0, k1, k2, r, vol, T)

"""
BOX SPREAD
A box spread is created from longing a bull spread (calls) with strikes K1,K2
and longing a bear spread (puts) of the same strike. Hence payoff is always present value of K1-K2, i.e.
payoff = (K1-K2)*e^(rT)
"""


def BoxSpread(S0, k1, k2, r, vol, T):
    K1, K2 = k1, k2
    if k2 < k1:
        K1, K2 = k2, k1
    bull = BullSpread(S0, K1, K2, r, vol, T)
    bear = BearSpread(S0, K1, K2, r, vol, T)
    cost = bear[0] + bull[0]
    
    op_1 = {'op_type': 'c', 'strike': K2, 'tr_type': 's', 'op_pr': bull[2]}
    op_2 = {'op_type': 'c', 'strike': K1, 'tr_type': 'b', 'op_pr': bull[1]}
    
    op_3 = {'op_type': 'p', 'strike': K2, 'tr_type': 'b', 'op_pr': bear[2]}
    op_4 = {'op_type': 'p', 'strike': K1, 'tr_type': 's', 'op_pr': bear[1]}
    op.multi_plotter(spot=S0, op_list=[op_1, op_2, op_3, op_4])
    return cost

#BoxSpread(S0, k1, k2, r, vol, T)

"""
BUTTERFLY SPREAD
A butterfly spread is characteristic for its use of positions in options of three different strikes.
A butterfly spread from calls is created from longing a call with a low strike, longing one with a high strike
and shorting two calls with strike halfway between the first
A butterfly spread using put options gives the exact same pay off with the exact same cost, this is due to PC
parity and the symmetry of the strikes.
"""

def ButterflySpread(S0, k1, k2, r, vol, T):
    K1, K3 = k1, k2
    if k2 < k1:
        K1, K3 = k2, k1
    K2 = (K1+K3)/2 #conventional butterfly has K2 midway between K1,K3.
    c1 = Call(S0,K1, r, vol, T)
    c2 = Call(S0,K2, r, vol, T)
    c3 = Call(S0,K3, r, vol, T)
    cost = c1 + c3 - (2*c2)
    data = [cost, c1, c2, c3]
    
    print("This Butterfly spread strategy consists of going long a call of strike", K1, "at a cost of", c1,
          "going long a call of strike", K3, "at a cost of", c3,"and going short two calls of strike", K2,
          "with return",c2 ,"for a total cost of", cost)
    
    op_1 = {'op_type': 'c', 'strike': K1, 'tr_type': 'b', 'op_pr': c1}
    op_2 = {'op_type': 'c', 'strike': K2, 'tr_type': 's', 'op_pr': c2} 
    op_3 = {'op_type': 'c', 'strike': K3, 'tr_type': 'b', 'op_pr': c3}
    op.multi_plotter(spot=S0, op_list=[op_1, op_2, op_2, op_3]) #is there a more fficient way to do this graph?
    return data

#ButterflySpread(S0, k1, k2, r, vol, T)

"""
CALENDAR SPREAD
Calendar spreads are unique because the strategy by shorting a European call of a certain expiry date
and longing a call of the same strike but a later expiry date!
Of course a calendar spread can be created with puts (long the long-maturity, short the short-maturity)
"""

def CalendarSpread(S0,K,r,vol,t1,t2):
    T1, T2 = t1, t2
    if t2 < t1:
        T1, T2 = t2, t1
    c1 = Call(S0, K, r, vol, T1) #call with shorter time to maturity
    c2 = Call(S0, K, r, vol, T2) #call with longer time to maturity. This will almost always be more expensive
    cost = c2 - c1
    data = [cost, c1, c2]
    
    print("This Calendar spread strategy consists of shorting a call with time to maturity",T1, "with return", c1,
          "and going long a call with time to maturity", T2, "at a cost of", c2, "for a total cost of", cost)
    
    return data

#CalendarSpread(S0,102,r,vol,0.5,1)

"""
The payoff diagram for a calendar spread differs to that from traditional strategies (see fig 11.6 pg245)
so must be coded seperately to account for the different times to maturity.
"""

"""
DIAGONAL SPREADS
Diagonal spreads involve changing the strike price of the calls AND the expiration date,
i.e. a mix of all calendar spreads and bull/bear spreads.
These are omitted for the infinite flexibility you can have creating a strategy, but could be added at a later date?
"""
"""
COMBINATIONS are strategies that involve taking a position in both calls AND puts on the same stock
"""
"""
STRADDLE
A straddle is a key combination strategy. It involves buying a European call and put with same strike
"""

def Straddle(S0,K,r,vol,T):
    c = Call(S0,K,r,vol,T)
    p = Put(S0,K,r,vol,T)
    cost = c + p
    data = [cost, c, p]
    
    op_1 = {'op_type': 'c', 'strike': K, 'tr_type': 'b', 'op_pr': c}
    op_2 = {'op_type': 'p', 'strike': K, 'tr_type': 'b', 'op_pr': p}
    op.multi_plotter(spot=S0, op_list=[op_1, op_2]) #can make graph better by adding a greater range
    
    return data

#Straddle(S0,90,r,vol,T)

"""
STRIPS AND STRAPS
A strip involves long positions in one call and two puts (betting a big move in price, decrease more likely than increase)
A straph involves long positions in two calls and one put (same as strip, but betting on increase more so)
"""

def Strip(S0,K,r,vol,T):
    c = Call(S0,K,r,vol,T)
    p = Put(S0,K,r,vol,T)
    cost = c + 2*p
    data = [cost, c, p]
    
    op_1 = {'op_type': 'c', 'strike': K, 'tr_type': 'b', 'op_pr': c}
    op_2 = {'op_type': 'p', 'strike': K, 'tr_type': 'b', 'op_pr': p}
    op.multi_plotter(spot=S0, op_list=[op_1, op_2, op_2]) #can make graph better by adding a greater range
    
    return data

def Strap(S0,K,r,vol,T):
    c = Call(S0,K,r,vol,T)
    p = Put(S0,K,r,vol,T)
    cost = 2*c + p
    data = [cost, c, p]
    
    op_1 = {'op_type': 'c', 'strike': K, 'tr_type': 'b', 'op_pr': c}
    op_2 = {'op_type': 'p', 'strike': K, 'tr_type': 'b', 'op_pr': p}
    op.multi_plotter(spot=S0, op_list=[op_1, op_1, op_2]) #can make graph better by adding a greater range
    
    return data

#Strip(S0,100,r,vol,T)
#Strap(S0, 100, r, vol, T)
"""
Can add greater flexibility to both the strips and straps by adding inputs for number of puts and number of calls.
"""
"""
STRANGLE
A strangle involves going long a call and a put with same expiry but different strikes.
It is a very similar strategy as a straddle (investor bets on a move in stock, but unsure on direction)
It requires a greater movement in price than a straddle, but has smaller downside risk.
"""

def Strangle(S0, k1, k2, r, vol, T):
    K1, K2 = k1, k2
    if k2 < k1:
        K1, K2 = k2, k1
    # Ordering the strikes is not necessary. A strangle doesn't require the call to have greater strike than put, but for simiplicity this is done. Can add greater flexibility later
    c = Call(S0, k2, r, vol, T)
    p = Put(S0, k1, r, vol, T)
    cost = c + p
    data = [cost, c, p]
    
    op_1 = {'op_type': 'c', 'strike': K2, 'tr_type': 'b', 'op_pr': c}
    op_2 = {'op_type': 'p', 'strike': K1, 'tr_type': 'b', 'op_pr': p}
    op.multi_plotter(spot=S0, op_list=[op_1, op_2])
    
    return data

#Strangle(S0, k1, k2, r, vol, T)

"""
This rounds up all the strategies given in Hull's book. It's worth noting that
any (feasible) payoff diagram can be approximated using a large number of very small butterfly spikes.
"""