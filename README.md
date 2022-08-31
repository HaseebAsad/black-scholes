# Black-Scholes Options Pricing
## About
This app is an educational options tool based on the Black-Scholes-Merton model for the value of a European Call with a non-dividend paying underlying:
Investors often use sophisticated strategies when trading options in the market and this page offers the user to be construct a few of these strategies given inputs, and to see how these strategies may be constructed, their payoffs and their costs. The tool also allows the user to compare different strategies and hence pick the most suitable strategy for their risk profile.

## Theory

The Black-Scholes-Merton Model, and by extension the calculator, take inputs in to calculate the value of a given option and its related strategies. These are:
- Spot price  : The spot price is the price of the underlying at a given time .
- Strike price  : The strike price or the exercise price is the price at which the underlying may be bought or sold in the options contract.
- Risk-free interest rate  : This is used to represent the return of a risk-free asset. In practice, models often use annualised treasury interest rates.
- Volatility  : Volatility is a measure of the return realised on the underlying asset. Usually, implied volatility (forward-looking) is used by investors.
- Time to expiry : This is the time remaining from the time of spot price until maturity/exercise of the option.
It is possible to translate both the spot price and the time to expiry so that they are situated around . This is used in the calculator.
Black-Scholes-Merton Model
As aforementioned, this calculator is based on the Nobel prize-winning Black-Scholes-Merton (BSM) model, of which we use the derived pricing formulas for a European call and European Put. 

Importantly, key assumptions used to construct the BSM model, and thus must be assumed in the usage of this calculator are:

- No dividends: An important assumption is that the underlying offers no dividends during the life of the derivative. There is an alternate model if there are dividend payments.
- Brownian Motion: The underlying price is a Wiener Process, with stock drift and volatility constant.
- Risk-free interest: The risk-free rate of interest  is constant and same for all maturities.
- Frictionless market: There are no transaction costs or taxes. All securities are perfectly divisible (i.e. decimal divisions of a security are valid).
- No early exercise: European-style options do not allow for the early exercise of the option contract - they may only be exercised at maturity.
