from fasthtml.common import *

app = FastHTML()
rt = app.route

@rt('/')
def get():
    return Body(
        H1('Mortgage Calculator'),
        Form(
            Div(
                Label('Home Price:'),
                Input(name='home_price', type='number', placeholder='Enter Home Price'),
            ),
            Div(
                Label('Down Payment (%):'),
                Input(name='down_payment', type='number', placeholder='Enter Down Payment Percentage'),
            ),
            Div(
                Label('Loan Term (years):'),
                Input(name='loan_term', type='number', placeholder='Enter Loan Term in Years'),
            ),
            Div(
                Label('Annual Interest Rate (%):'),
                Input(name='interest_rate', type='number', placeholder='Enter Interest Rate'),
            ),
            Button('Calculate', type='submit', hx_post='/calculate', hx_trigger='click', hx_target='#result'),
            Div(id='result', style='margin-top:20px; font-size: 20px; color: #005500;')
        ),
        Style("""
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f3f4f6;
        }
        input {
            margin: 5px;
            padding: 5px;
            width: calc(100% - 12px);
        }
        button {
            margin-top: 10px;
            padding: 10px 20px;
            font-size: 16px;
        }
        table {
            margin: 20px auto;
            border-collapse: collapse;
            width: 80%;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }
        th {
            background-color: #f2f2f2;
        }
        """)
    )

@rt('/calculate')
def post(home_price: float, down_payment: float, loan_term: float, interest_rate: float):
    loan_amount = home_price * (1 - down_payment / 100)
    monthly_rate = (interest_rate / 100) / 12
    num_payments = int(loan_term * 12)
    monthly_payment = loan_amount * monthly_rate / (1 - (1 + monthly_rate) ** -num_payments)
    
    result_text = f'Monthly Payment: ${monthly_payment:.2f}'

    # Calculating the breakdown of each payment
    remaining_balance = loan_amount
    payment_schedule = []

    for i in range(1, num_payments + 1):
        interest_payment = remaining_balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment
        payment_schedule.append((i, interest_payment, principal_payment, remaining_balance))

    # Creating data as a table
    schedule_table = Table(
        Tr(Th('Month'), Th('Interest'), Th('Principal'), Th('Balance')),
        *[Tr(Td(str(month)), Td(f"${interest:.2f}"), Td(f"${principal:.2f}"), Td(f"${balance:.2f}"))
          for month, interest, principal, balance in payment_schedule]
    )

    return Div(
        P(result_text, id='result'),
        H2('Payment Schedule:'),
        schedule_table
    )

serve()