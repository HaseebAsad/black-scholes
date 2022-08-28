from BlackScholesFormulae import Call, Put #import the necessary formulae from a source file.



"""
The following class gives us an object with the attributes assigned for an option. This allows us to have
a single object which has all the necessary information needed to create strategies.
"""

class Option:
    def __init__(self, Type, S0, K, r, vol, T):
        self.Type = Type
        self.S0 = S0
        self.K = K
        self.r = r
        self.vol = vol
        self.T = T
        self.Call = Call(S0, K, r, vol, T)
        self.Put = Put(Type, S0, K, r, vol, T)
        self.Cost = 0

    def Straddle(self):
        # a straddle consists of going long a call and a put at the same strike.
        self.Cost = self.Call + self.Put
        self.desc = "A straddle consists of going long a call and a put, at {} and {} respectively, with both the same\
            strike price and expiry date. The idea of a straddle is that the investor \
            is expecting a significant move of the price in the underlying away from the strike price, \
            upwards or downwards. However, if there is insufficient movement, the investor \
            will incur a loss. \
            This strategy is similar to a strangle with a reduced need for movement in the underlying, but with greater downside risk.\
            ".format(self.Call,self.Put)
    
    def Strap(self):
        #go long 2 call and 1 put
        self.Cost = 2*self.Call + self.Put
        self.desc = "A strap consists of going long two calls, in this case at {}, and one put at {}.\
            In a strap, the investor is betting that there will be a big move in stock price,\
            speculating a bigger upwards movement than downwards.\
            ".format(self.Call,self.Put)
        
    def Strip(self):
        #go long 1 call and 2 put
        self.Cost = self.Call + 2*self.Put
        self.desc = "A strip consists of going long one call, in this case at {}, and two puts at {}.\
            In a strip, the investor is betting that there will be a big move in stock price,\
            speculating a bigger downwards movement than upwards.\
            ".format(self.Call,self.Put)
        
    """
    Now to implement strategies that have several different strikes or times.
    """
    
    def BullSpread(self, k2):
        K1, K2 = self.K, k2
        if k2 < self.K:
            K1, K2 = k2, self.K
        c1 = Call(self.S0, K1, self.r, self.vol, self.T)
        c2 = Call(self.S0, K2, self.r, self.vol, self.T)
        self.Cost = c1-c2
        self.desc = "A bull spread consists of going long one call of strike {} at {} \
            and shorting a call of higher strike {} at {} with same expiry date.\
            A bull spread reduces the downwards exposure of the investor, at the cost of limiting upside potential.\
            ".format(K1, c1, K2, c2)
        
    def BearSpread(self, k2):
        K1, K2 = self.K, k2
        if k2 < self.K:
            K1, K2 = k2, self.K
        p1 = Put(self.Type, self.S0, K1, self.r, self.vol, self.T)
        p2 = Put(self.Type, self.S0, K2, self.r, self.vol, self.T)
        self.Cost = p2-p1
        self.desc = "A bear spread consists of going long one put of strike {} at {} \
            and shorting a put of lower strike {} at {} with same expiry date.\
            A bear spread reduces the upwards exposure of the investor, at the cost of limiting downside potential.\
            ".format(K1, p1, K2, p2)
        
    def BoxSpread(self, k2):
        K1, K2 = self.K, k2
        if k2 < self.K:
            K1, K2 = k2, self.K
        bull = Call(self.S0, K1, self.r, self.vol, self.T) - Call(self.S0, K2, self.r, self.vol, self.T) #creating the strategy from the bullspread
        bear = Put(self.Type, self.S0, K2, self.r, self.vol, self.T) - Put(self.Type, self.S0, K1, self.r, self.vol, self.T) #creating the strategy from the bearspread
        self.Cost = bull + bear
        self.desc = "A box spread is a combination of a bull (call) spread at {} and a bear \
            (put) spread at {}. \
            The payoff a bear spread is always K1 - K2, in this case {}-{}={}.\
            Hence, the value of a box spread is always the value of this payoff, factoring in the time value.\
            ".format(bull, bear, K1, K2, K1 - K2)
        
    def ButterflySpread(self, k2):
        K1, K3 = self.K, k2
        if k2 < self.K:
            K1, K3 = k2, self.K
        K2 = (K1+K3)/2 #conventional butterfly has K2 midway between K1,K3.
        c1 = Call(self.S0, K1, self.r, self.vol, self.T)
        c2 = Call(self.S0, K2, self.r, self.vol, self.T)
        c3 = Call(self.S0, K3, self.r, self.vol, self.T)
        self.Cost = c1 + c3 - (2*c2)
        self.desc = "A butterfly spread involves positions with options with three different strike prices. \
            It consists of going long a call of a low strike {} at {}, going long of a call of a high strike {} at {}\
            and shorting two calls with a strike {} halfway between {} and {} at {}. \
            A butterfly spread leads to a profit if the underlying remains close to the strike \
            but gives rise to a small loss if there is a signficant price move in either direction.\
            ".format(K1, c1, K3, c3, K2, K1, K3, c2)

    def Strangle(self, k2):
        K1, K2 = self.K, k2
        if k2 < self.K:
            K1, K2 = k2, self.K
        c = Call(self.S0, K2, self.r, self.vol, self.T)
        p = Put(self.Type, self.S0, K1, self.r, self.vol, self.T)
        self.Cost = c + p
        self.desc = "A strangle consists of a longing a call of higher strike {} at {}\
            and longing a put of lower strike {} at {}. The investor is expecting a large movement \
            in the underlying, but without certainty in which direction this will be. \
            If there is insufficient movement, the investor will incur a loss. \
            This strategy is similar to a straddle with a lower downside risk, but the underlying has to make a greater move to yield a profit. \
            ".format(K2, c, K1, p)
        
    def CalendarSpread(self, t1, t2):
        T1, T2 = t1, t2
        if t2 < t1:
            T1, T2 = t2, t1
        c1 = Call(self.S0, self.K, self.r, self.vol, T1)
        c2 = Call(self.S0, self.K, self.r, self.vol, T2)
        self.Cost = c2-c1 #check, not agreeing with original code

if __name__ == "__main__":
    
    S0, K, r, vol, T = 100, 102, 0.1, 0.2, 0.5
    
    test = Option("American",S0, K, r, vol, T)
    test.Strap()
    print(test.desc)
    
    