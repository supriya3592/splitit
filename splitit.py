import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
exurl="https://docs.google.com/spreadsheets/d/1cCvrf6drHcHTTPZhX1Fswmut7XPysyIv0Kil65UyiW4/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(spreadsheet=exurl)
st.dataframe(df)

# Perform expense splitting and summarizing final balances
summary = {}
for index, row in df.iterrows():
    lender = row['Lender']
    borrowers = row['Borrowers'].split(', ')
    amount = float(row['Amount'])
    split_amount = amount / len(borrowers)
    for borrower in borrowers:
        summary.setdefault(lender, 0)
        summary.setdefault(borrower, 0)
        summary[lender] -= split_amount
        summary[borrower] += split_amount

# Identify positive balance and update the summary
positive_balances = {person: balance for person, balance in summary.items() if balance > 0}
for person, balance in positive_balances.items():
    for creditor, debt in summary.items():
        if debt < 0:
            st.write("# Final Balances:")
            st.write(f"## {person} owes {creditor} ¥{abs(debt)}")

# Display the summary of final balances
#st.write("Final Balances:")
#st.write(summary)
