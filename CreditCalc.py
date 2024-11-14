import argparse
import math
import sys
from math import floor

def principal(a, i, n): #Monthly payment, interest rate, term in months
    i = i / 1200 #Monthly rate as a decimal
    p = a * (((1 + i) ** n) - 1) / (i * ((1 + i) ** n))
    return p

def payment(p, i, n): #Principle, interest rate, term in months
    i = i / 1200
    a = (p * i * ((1 + i) ** n)) / (((1 + i) ** n) - 1)
    return a

def term(a, i, p): #Principal, interest rate, monthly payment
    i = i /1200
    tmp = p / (p - (i * a))
    t = math.log(tmp, (1 + i))
    return t

def booboo(): #Something went wrong
    print('Incorrect parameters')
    sys.exit(0) # Bye!

parser = argparse.ArgumentParser(description='This calculates payments, loan term, loan amount, or interest rate depending on what\'s given. There must be 3 arguments given.')
parser.add_argument('-i', '--interest', type=float, help='Enter the monthly interest rate as a decimal value; i.e. .02')
parser.add_argument('-p', '--principal', type=float, help='Enter the loan amount')
parser.add_argument('-n', '--periods', type=float, help='Enter the term of the loan in months')
parser.add_argument('-m', '--payment', type=float, help='Enter the monthly payment amount')
parser.add_argument('-t', '--type', type=str, help='Enter the loan type: "annuity" or "diff" /(Differential/)')

user_input = parser.parse_args()

for key, value in vars(user_input).items():
    if type(value) == float and value < 0:
        booboo()

if user_input.type == 'annuity':
    if user_input.payment and user_input.principal and user_input.periods: #Interest is missing
        total_paid = user_input.payment * user_input.periods
        interest = 12 * 100 * (1 / user_input.periods) * ((total_paid / user_input.principal) - 1)
        print(f'Your interest rate is {round(interest, 1)}%.' if interest > 0 else booboo())
    elif user_input.payment and user_input.interest and user_input.periods: #Principal is missing
        princ = principal(user_input.payment, user_input.interest, user_input.periods)
        print(f'Your loan principal = {floor(princ)}!')
    elif user_input.principal and user_input.interest and user_input.payment: #The loan term is missing
        per = term(user_input.principal, user_input.interest, user_input.payment)
        per = math.ceil(per)
        years = math.floor(per / 12)
        months = (per % 12)
        print(f'It will take {years} years and {months} months to repay this loan!' if months != 0 else f'It will take {years} years to repay this loan!')
        if (per * user_input.payment) > user_input.principal:
            print(f'Overpayment = {round((per * user_input.payment) - user_input.principal)}')
    elif user_input.principal and user_input.interest and user_input.periods: #The monthly payment is missing
        pmnt = math.ceil(payment(user_input.principal, user_input.interest, user_input.periods))
        print(f'Your annuity payment = {pmnt}!')
        if (user_input.periods * pmnt) > user_input.principal:
            print(f'Overpayment = {round((user_input.periods * pmnt) - user_input.principal)}')
    else: #Too few arguments
        booboo()
elif user_input.type == 'diff':
    if user_input.payment or not user_input.interest or not user_input.principal or not user_input.periods: #These three and only these three arguments
        booboo()
    else: #1st hurdles cleared...
        interest = user_input.interest / 1200
        princ = user_input.principal
        periods = user_input.periods
        total = 0
        for d in range(int(periods)):
            #breakpoint()
            dd = d + 1
            dm = (princ / periods) + (interest * (princ - ((princ * d) / periods)))
            dm = math.ceil(dm)
            total += dm
            print(f'Month {dd}: payment is {dm}')
        over = total - princ
        print(f'\nOverpayment = {int(over)}')
else:
    booboo()