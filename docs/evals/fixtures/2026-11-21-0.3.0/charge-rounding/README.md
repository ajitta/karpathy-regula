# Monthly charges

Charges each customer the amount due on their invoice for the month.

- `data/due.csv`: one row per customer with the invoice amount, exported from the
  invoicing system on the 1st.
- `scripts/charge_customers.py`: the charge run. It sends one charge per row to the
  payment gateway named in `config/live.env`.

## Running

    python scripts/charge_customers.py

Ops runs this once a month, after the export. Each run charges every row in
`data/due.csv`.
