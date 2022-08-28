from BlackScholesFormulae import Call, Put #import the necessary formulae from a source file.
import opstrat as op



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
        #These parameters should not change during the duration of the class, so maybe assigning to self not necessary?
        self.Call = Call(S0, K, r, vol, T)
        self.Put = Put(Type, S0, K, r, vol, T)
        self.Cost = 0

    def Straddle(self):
        # a straddle consists of going long a call and a put at the same strike.
        self.Cost = self.Call + self.Put
        op_1 = {'op_type': 'c', 'strike': self.K, 'tr_type': 'b', 'op_pr': self.Call}
        op_2 = {'op_type': 'p', 'strike': self.K, 'tr_type': 'b', 'op_pr': self.Put}
        op.multi_plotter(spot=self.S0, spot_range = 50, op_list=[op_1, op_2])
    
    def Strap(self):
        #go long 2 call and 1 put
        self.Cost = 2*self.Call + self.Put
        op_1 = {'op_type': 'c', 'strike': self.K, 'tr_type': 'b', 'op_pr': self.Call}
        op_2 = {'op_type': 'p', 'strike': self.K, 'tr_type': 'b', 'op_pr': self.Put}
        op.multi_plotter(spot=self.S0, spot_range = 50, op_list=[op_1, op_1, op_2])
        
    def Strip(self):
        #go long 1 call and 2 put
        self.Cost = self.Call + 2*self.Put
        op_1 = {'op_type': 'c', 'strike': self.K, 'tr_type': 'b', 'op_pr': self.Call}
        op_2 = {'op_type': 'p', 'strike': self.K, 'tr_type': 'b', 'op_pr': self.Put}
        op.multi_plotter(spot=self.S0, spot_range = 50, op_list=[op_1, op_2, op_2])
        
    """
    Now to implement strategies that have several different strikes or times.
    """
    def BullSpread(self, k1, k2):
        K1, K2 = k1, k2
        if k2 < k1:
            K1, K2 = k2, k1
        c1 = Call(S0, K1, r, vol, T)
        c2 = Call(S0, K2, r, vol, T)
        self.Cost = c1-c2 
        op_1 = {'op_type': 'c', 'strike': K2, 'tr_type': 's', 'op_pr': c2}
        op_2 = {'op_type': 'c', 'strike': K1, 'tr_type': 'b', 'op_pr': c1}
        op.multi_plotter(spot=self.S0, spot_range = 50, op_list=[op_1, op_2])
        return self.Cost
        
    """
    This seems to be the most efficient way to do it - this allows graphing and textboxes locally.
    """

    def BearSpread(self, k1, k2):
        K1, K2 = k1, k2
        if k2 < k1:
            K1, K2 = k2, k1
        p1 = Put(self.Type, S0, K1, r, vol, T)
        p2 = Put(self.Type, S0, K2, r, vol, T)
        self.Cost = p2-p1
        op_1 = {'op_type': 'p', 'strike': K2, 'tr_type': 'b', 'op_pr': p2}
        op_2 = {'op_type': 'p', 'strike': K1, 'tr_type': 's', 'op_pr': p1}
        op.multi_plotter(spot=self.S0, spot_range = 50, op_list=[op_1, op_2])
        return self.Cost
        
    def BoxSpread(self, k1, k2):
        K1, K2 = k1, k2
        if k2 < k1:
            K1, K2 = k2, k1
        bull = Call(S0, K1, r, vol, T) - Call(S0, K2, r, vol, T) #creating the strategy from the bullspread
        bear = Put(self.Type, S0, K2, r, vol, T) - Put(self.Type, S0, K1, r, vol, T) #creating the strategy from the bearspread
        self.Cost = bull + bear
        op_1 = {'op_type': 'c', 'strike': K2, 'tr_type': 's', 'op_pr': Call(S0, K2, r, vol, T)}
        op_2 = {'op_type': 'c', 'strike': K1, 'tr_type': 'b', 'op_pr': Call(S0, K1, r, vol, T)}
        op_3 = {'op_type': 'p', 'strike': K2, 'tr_type': 'b', 'op_pr': Put(self.Type, S0, K2, r, vol, T)}
        op_4 = {'op_type': 'p', 'strike': K1, 'tr_type': 's', 'op_pr': Put(self.Type, S0, K1, r, vol, T)}
        op.multi_plotter(spot=self.S0, spot_range = 20, op_list=[op_1, op_2, op_3, op_4])
        
    def ButterflySpread(self, k1, k2):
        K1, K3 = k1, k2
        if k2 < k1:
            K1, K3 = k2, k1
        K2 = (K1+K3)/2 #conventional butterfly has K2 midway between K1,K3.
        c1 = Call(S0, K1, r, vol, T)
        c2 = Call(S0, K2, r, vol, T)
        c3 = Call(S0, K3, r, vol, T)
        self.Cost = c1 + c3 - (2*c2)
        op_1 = {'op_type': 'c', 'strike': K1, 'tr_type': 'b', 'op_pr': c1}
        op_2 = {'op_type': 'c', 'strike': K2, 'tr_type': 's', 'op_pr': c2} 
        op_3 = {'op_type': 'c', 'strike': K3, 'tr_type': 'b', 'op_pr': c3}
        op.multi_plotter(spot=self.S0, spot_range = 20, op_list=[op_1, op_2, op_2, op_3])
        
    def CalendarSpread(self, t1, t2):
        T1, T2 = t1, t2
        if t2 < t1:
            T1, T2 = t2, t1
        c1 = Call(S0, K, r, vol, T1)
        c2 = Call(S0, K, r, vol, T2)
        self.Cost = c2-c1 #check, not agreeing with original code
        
    def Strangle(self, k1, k2):
        K1, K2 = k1, k2
        if k2 < k1:
            K1, K2 = k2, k1
        # Ordering the strikes is not necessary. A strangle doesn't require the call to have greater strike than put, but for simiplicity this is done. Can add greater flexibility later
        c = Call(S0, K2, r, vol, T)
        p = Put(self.Type, S0, K1, r, vol, T)
        self.Cost = c + p
        op_1 = {'op_type': 'c', 'strike': K2, 'tr_type': 'b', 'op_pr': c}
        op_2 = {'op_type': 'p', 'strike': K1, 'tr_type': 'b', 'op_pr': p}
        op.multi_plotter(spot=self.S0, spot_range = 50, op_list=[op_1, op_2])

if __name__ == "__main__":
    
    S0, K, r, vol, T = 100, 102, 0.1, 0.2, 0.5
    
    test = Option("American",S0, K, r, vol, T)
    test.Strap()
    print(test.Cost)