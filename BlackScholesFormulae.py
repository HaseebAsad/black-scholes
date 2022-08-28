import numpy as np
from scipy.stats import norm as N
import math
"""
The function below aims to output the BSM cost of a European call option, with the assumptions given in Hull page 309.
Most important assumption is no dividends during the life of the derivative, which is true for futures.
Remember that the value of an American Call is the same as a European call under these assumptions (mainly no dividend).
Otherwise, with dividends, early exercise brings value to American options.
"""


def Call(S0 , K, r, vol, T):
    d1 = (np.log(S0/K)+(r+(vol**2)/2)*T)/(vol*np.sqrt(T)) #conditional probability for the gain of the buyer
    d2 = d1-vol*np.sqrt(T) #probability option will expire in the money
    c = S0*N.cdf(d1)-(K*math.exp(-r*T)*N.cdf(d2)) #value of call option
    return c

def europeanPut(S0,K,r,vol,T):
    d1 = (np.log(S0/K)+(r+(vol**2)/2)*T)/(vol*np.sqrt(T)) #conditional probability for the gain of the buyer
    d2 = d1-vol*np.sqrt(T) #probability option will expire in the money
    p = K*math.exp(-r*T)*N.cdf(-d2)-S0*N.cdf(-d1) #value of a European put
    return p


    

def Put(Type, S0, K, r, vol, T):
    p = europeanPut(S0, K, r, vol, T)
    if Type == "A": #if put is american
        d4 = (np.log(S0/K)-(1/2*vol**2*T))/(vol*np.sqrt(T))
        Pa = (europeanPut(S0,K*math.exp(r*T),r,vol,T)*N.cdf(-d4)) + \
                 +max(p,K-S0)*N.cdf(d4)
        return Pa
    return p

"""
Important things to consider when using these is what the time to expiry is as a fraction of the time interval used for interest rate/vol.
So if the time to expiry is 6 months, interest rate and vol are given per annum, then T=0.5
The next function gives the cost of a European put given the cost of a European call (i.e. put call parity). Benefit of this is that
you do not need to know vol, this is given in the value of the call. That said, will likely not be used in this project since vol
will be needed at some point anyway.
"""

def putParity(c,S0,K,r,T):
    p = c-S0+K*math.exp(-r*T) #value of put given value of call. Proved by no arbitrage condition.
    return p

"""
Test for both functions below.
"""
Type = "E"
S0 = 42
K = 40
r = 0.1
vol = 0.2
T = 0.5
c = Call( S0, K, r, vol, T)
p = Put(Type, S0, K, r, vol, T)

#print(c, p)

"""
Valuation for American Put - there exists no closed form of the valuation for an American Put. Merton gave one for perpetual put options,
but these are not traded anywhere and are traded OTC if they are.
https://www.jstor.org/stable/2326779

NOTE: W. Xiadong offers a closed form solution of an American put on a non-dividend paying underlying.
http://aeconf.com/articles/may2007/aef080111.pdf
The mathematics needs to be checked for this.
"""

# def AmericanPut(S0,K,r,vol,T):
#     Pe = Put(S0,K,r,vol,T) #Value of corresponding European Call with the given information.
#     d4 = (np.log(S0/K)-(1/2*vol**2*T))/(vol*np.sqrt(T)) #probabilities given in Xiao's paper
#     Pa = (Put(S0,K*math.exp(r*T),r,vol,T)*N.cdf(-d4)) + \
#         +max(Pe,K-S0)*N.cdf(d4)
#     return Pa

"""
This is now integrated into the Put function
Alternative for first term given in paper: K*N.cdf(-d4)-S0*N.cdf(-d3)
Test given below to confirm that the American put costs more than the European put.
"""

#print(AmericanPut(S0,K,r,vol,T),p)

