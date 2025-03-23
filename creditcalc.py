import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--principal")
parser.add_argument("--payment")
parser.add_argument("--periods")
parser.add_argument("--interest")
parser.add_argument("--type")

args = parser.parse_args()


def calculate_nominal_interest_rate(interest):
    interest = float(interest)
    i = interest / 100 / 12
    return i


def calculate_overpayment(payment, months, principal):
    return math.ceil(payment * months - principal)


def calculate_monthly_payment(principal, interest, periods):

    principal = float(principal)
    periods = float(periods)
    interest_rate = calculate_nominal_interest_rate(interest)

    to_div_1 = interest_rate * math.pow((1 + interest_rate), periods)
    to_div_2 = math.pow((1 + interest_rate), periods) - 1
    to_multiple = to_div_1 / to_div_2
    monthly_payment = math.ceil(principal * to_multiple)

    overpayment = calculate_overpayment(payment=monthly_payment, months=periods, principal=principal)

    return monthly_payment, overpayment


def calculate_months(principal, payment, interest):

    principal = float(principal)
    payment = float(payment)

    interest_rate = calculate_nominal_interest_rate(interest)
    months = math.log(payment / (payment - interest_rate * principal)) / math.log(1 + interest_rate)
    months = math.ceil(months)

    overpayment = calculate_overpayment(payment=payment, months=months, principal=principal)

    return months, overpayment


def calculate_loan_principal(payment, interest, periods):

    payment = float(payment)
    periods = float(periods)
    interest_rate = calculate_nominal_interest_rate(interest)

    lp = int((payment * (1 - (1 + interest_rate) ** (-periods))) / interest_rate)
    overpayment = calculate_monthly_payment(lp, interest, periods)[1]

    return lp, overpayment


def months_message(base_months):
    msg = "It will take "
    years = base_months // 12
    if years == 0:
        msg += f"{base_months} months "
    elif base_months % 12 == 0:
        msg += f"{years} years "
    else:
        msg += f"{years} years and {base_months % 12} months "

    msg += "to repay this loan!"

    return msg


def cal_single_differentiated_payment(principal, periods, interest, m):
    differentiated_payment =  principal / periods + interest * (principal - (principal * (m - 1)/periods))
    return math.ceil(differentiated_payment)


def calculate_differentiated_payments(principal, periods, interest):
    principal = float(principal)
    periods = int(periods)
    interest = float(interest)
    interest = calculate_nominal_interest_rate(interest)

    d_payments = [cal_single_differentiated_payment(principal, periods, interest, m) for m in range(1, periods + 1)]
    text_msg = ""
    month = 1
    for payment in d_payments:
        text_msg += f"Month {month}: payment is {payment}\n"
        month += 1

    overpayment = round(sum(d_payments) - principal)
    print(text_msg)
    print(f"Overpayment = {overpayment}")


def args_validation(args_obj):
    if (not args.type or args.type not in ("annuity", "diff")
            or (args.type == "diff" and args.payment is not None)
            or args.interest is None):
        raise ValueError

    if ((args_obj.principal is not None and float(args_obj.principal) < 0) or
            (args_obj.periods is not None and float(args_obj.periods) < 0) or
            (args_obj.payment is not None and float(args_obj.payment) < 0) or
            (args_obj.interest is not None and float(args_obj.interest) < 0)):
        raise ValueError


def main(args_obj):
    args_validation(args_obj)

    if args_obj.principal and args_obj.payment and args_obj.interest and (args_obj.type == "annuity"):
        months, overpayment = calculate_months(principal=args_obj.principal, payment=args_obj.payment, interest=args_obj.interest)
        print(months_message(months))
        print(f"Overpayment = {overpayment}")
    elif args_obj.principal and args_obj.periods and args_obj.interest and (args_obj.type == "annuity"):
        payment, overpayment = calculate_monthly_payment(principal=args_obj.principal,
                                                         interest=args_obj.interest, periods=args_obj.periods)
        print(f"Your monthly payment = {payment}!")
        print(f"Overpayment = {overpayment}")
    elif args_obj.payment and args_obj.periods and args_obj.interest and (args_obj.type == "annuity"):
        loan_principal, overpayment = calculate_loan_principal(payment=args_obj.payment, interest=args_obj.interest,
                                                               periods=args_obj.periods)
        print(f"Your loan principal = {loan_principal}!")
        print(f"Overpayment = {overpayment}")
    elif args_obj.principal and args_obj.periods and args_obj.interest and (args_obj.type == "diff"):
        calculate_differentiated_payments(principal=args_obj.principal, periods=args_obj.periods, interest=args_obj.interest)
    else:
        raise ValueError

try:
    main(args)
except ValueError:
    print("Incorrect parameters")
