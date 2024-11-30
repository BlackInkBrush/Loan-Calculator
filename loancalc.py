import math
import argparse

#configure the parser
parser = argparse.ArgumentParser()
parser.add_argument("--payment", type = float,default=None)
parser.add_argument("--type", type=str, default=None)
parser.add_argument("--principal", type = float, default=None)
parser.add_argument("--periods", type = float, default=None)
parser.add_argument("--interest", type=float, default=None)
args = parser.parse_args()

nominal_interest = (args.interest / 12) / 100 if args.interest else None

def calculate_monthly_payment(loan_principal, num_payments, interest):
    if interest == 0:
        payment = loan_principal / num_payments
    else:
        payment = loan_principal * (
            (interest * (1 + interest) ** num_payments) /
            ((1 + interest) ** num_payments - 1)
        )
    return payment

def calculate_principal(annuity_payment, interest, num_payments):
    loan_principal = annuity_payment / ((interest * (1 + interest)**num_payments) /
                                        ((1 + interest)**num_payments - 1))
    return loan_principal

def number_of_payments(annuity_payment, interest, loan_principal):
    if interest <= 0:
        raise ValueError("Interest must be greater than 0 for this calculation.")
    numerator = math.log(annuity_payment / (annuity_payment - interest * loan_principal))
    
    denominator = math.log(1 + interest)
    
    num_of_payments = numerator / denominator
    
    return num_of_payments

def diff_payment(loan_principal, num_payments, interest):
    payments = {}
    for m in range(1, int(num_payments) + 1):
        payment = (loan_principal / num_payments) + (loan_principal - (loan_principal * (m - 1) / num_payments)) * interest
        payments[m] = math.ceil(payment)
    return payments


def validate_parser(args):
    provided_args = sum(1 for arg in vars(args).values() if arg is not None)
    if args.type != "annuity" and args.type != "diff":
        return False
    elif args.type == "diff" and args.payment is not None:
        return False
    elif args.interest is None:
        return False
    elif provided_args < 4:
        return False
    elif any(arg is not None and arg < 0 for arg in [args.payment, args.periods, args.principal, args.interest]):
        return False
    return True
        
    


def main(args):
    validation = validate_parser(args)
    
    if not validation:
        return "Incorrect parameters"
        
    if args.payment is None:
        if args.type == "annuity":
            payment = math.ceil(calculate_monthly_payment(args.principal, args.periods, nominal_interest))
            overpayment = (payment * args.periods) - args.principal
            return f"Your monthly payment = {str(payment)}!"
        payments = diff_payment(args.principal, args.periods, nominal_interest)
        overpayment = sum(payments.values()) - args.principal
        for m, payment in payments.items():
            print(f"Month {m}: payment is {math.ceil(payment)}")
        print(f"Overpayment = {math.ceil(overpayment)}")      
        
    elif args.principal is None:
        principal = calculate_principal(args.payment, nominal_interest, args.periods)
        return f"Your loan principal = {str(principal)}!"
    elif args.periods is None:
        num_payments = number_of_payments(args.payment, nominal_interest, args.principal)
        rounded_months = int(num_payments) + (1 if num_payments % 1 != 0 else 0)
        overpayment = (args.payment * rounded_months) - args.principal
        if rounded_months <= 11:
            return f"It will take {str(rounded_months)} months to repay this loan! \n Overpayment = {str(overpayment)}"
        years = rounded_months // 12
        remaining_months = rounded_months % 12
        if remaining_months == 0:
            return f"It will take {str(years)} years to repay this loan! \n Overpayment = {str(overpayment)}"
        return f"It will take {str(years)} years and {str(remaining_months)} months to repay this loan! \n Overpayment = {str(overpayment)}"
        
            
print(main(args))
