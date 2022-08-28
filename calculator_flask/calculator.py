from flask import Flask, render_template, request
from BlackScholesFormulae import Call, Put
from OptionsFlask import Option

"""
Flask application
"""
app = Flask(__name__) # Creating our Flask Instance

@app.route('/', methods=['GET'])
def index():
    """ Displays the index page accessible at '/' """

    return render_template('index.html')

@app.route('/result/', methods=['POST'])
def result():
    """Route where we send calculator form input"""

    error = None
    result = None

    S0 = request.form['spot']
    K = request.form['strike']
    K2 = request.form['addStrike']
    r = request.form['r']
    vol = request.form['vol']
    T = request.form['time']
    Type = request.form['type']
    strat = request.form['strat']

    try:
        """Convert inputs into floats"""
        S0 = float(S0)
        K = float(K)
        K2 = float(K2)
        r = float(r)
        vol = float(vol)
        T = float(T)
        """Create a derivative variable with necessary attributes for analysis"""
        derivative = Option(Type,S0,K,r,vol,T)
        
        # On default, the strategy on webpage is call
        if strat == "Call":
            cost = Call(S0, K, r, vol, T)
            desc = "This strategy is a standard {} call option.".format(Type)
        elif strat == "Put":
            cost = Put(Type,S0,K,r,vol,T)
            desc = "This strategy is a standard {} put option.".format(Type)
        elif strat == "Straddle":
            derivative.Straddle()
            cost = derivative.Cost
            desc = derivative.desc
        elif strat == "Strip":
            derivative.Strip()
            cost = derivative.Cost
            desc = derivative.desc
        elif strat == "Strap":
            derivative.Strap()
            cost = derivative.Cost
            desc = derivative.desc
        elif strat == "Bull Spread":
            derivative.BullSpread(K2)
            cost = derivative.Cost
            desc = derivative.desc
        elif strat == "Bear Spread":
            derivative.BearSpread(K2)
            cost = derivative.Cost
            desc = derivative.desc
        elif strat == "Box Spread":
            derivative.BoxSpread(K2)
            cost = derivative.Cost
            desc = derivative.desc
        elif strat == "Butterfly Spread":
            derivative.ButterflySpread(K2)
            cost = derivative.Cost
            desc = derivative.desc
        elif strat == "Strangle":
            derivative.Strangle(K2)
            cost = derivative.Cost
            desc = derivative.desc
            
        
        return render_template(
            'index.html',
            S0 = S0, #the new variables created are what we will refer to in the html
            K = K,
            K2 = K2,
            r = r,
            vol = vol,
            T = T,
            Type = Type,
            strat = strat,
            cost = cost,
            desc = desc,
            calculation_success=True
        )
        
    except ZeroDivisionError:
        return render_template(
            'index.html',
            S0 = S0,
            K = K,
            K2 = K2,
            r = r,
            vol = vol,
            T = T,
            Type = Type,
            strat = strat,
            result="Bad Input",
            calculation_success=False,
            error="You cannot divide by zero"
        )
        
    except ValueError:
        return render_template(
            'index.html',
            S0 = S0,
            K = K,
            K2 = K2,
            r = r,
            vol = vol,
            T = T,
            Type = Type,
            strat = strat,
            result="Bad Input",
            calculation_success=False,
            error="Please provide valid inputs"
        )

if __name__ == '__main__':
    app.debug = True
    app.run()