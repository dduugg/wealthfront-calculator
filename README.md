wealthfront-calculator
======================
Calculates a risk score based on proximity to a financial goal, and uses linear
interpolation to determine the corresponding
[Wealthfront](https://www.wealthfront.com/) portfolio.

###Usage
     $python wealthfront-calculator.py arg1 arg2 arg3 arg4

where:

- `arg1` is the amount held in taxable investment accounts
- `arg2` is the amount held in retirement investment accounts
- `arg3` is the total value of other holdings
- `arg4` is the financial goal

`arg1` and `arg2` are required, while `arg3` has a default value of `0` and
`arg4` has a default value of `1000000`. (`arg4` presumably changes infrequently
enough that it is worth hardcoding a default value.)

###Example
    $ python wealthfront-calculator.py 100000 200000 300000
    risk: 4.3
    VTI: $67,200
    LQD: $58,400
    VEA: $38,800
    VIG: $35,800
    MUB: $33,800
    VWO: $27,400
    EMB: $18,800
    VNQ: $14,400
    DJP: $ 5,400

###Notes
- Taxable and retirement account allocations are combined in the output. (It's
 an easy change to print each individually.)
- This is not investment advice.
