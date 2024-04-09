import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px



# CSS code with increased specificity (optional)
hide_menu = """
<style>
#root #MainMenu {
  visibility: hidden;
}

footer {
  visibility: visible;
}

footer:after {
  content:'Copyright @ 2021: Streamlit';
  display: block;
  position: relative;
  color: tomato;
  padding: 5px;
  top: 3px;
}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)

exurl="https://docs.google.com/spreadsheets/d/1cCvrf6drHcHTTPZhX1Fswmut7XPysyIv0Kil65UyiW4/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(spreadsheet=exurl)
df['Date of expense']=pd.to_datetime(df['Date of expense'],dayfirst=True)
df=df.set_index(df['Date of expense'],drop=True)
st.dataframe(df)

# Group the DataFrame by months and calculate the sum of values for each month
monthly_data = df['Amount'].resample('M').sum()
st.dataframe(monthly_data)

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

"""
# Identify positive balance and update the summary
positive_balances = {person: balance for person, balance in summary.items() if balance > 0}
for person, balance in positive_balances.items():
    for creditor, debt in summary.items():
        if debt < 0:
            st.write("# Final Balances:")
            st.write(f"## {person} owes {creditor} ¥{abs(debt)}")
"""

final_balances = {
  person: abs(summary[creditor]) if debt < 0 and summary[person] > 0 else "No Debts"
  for person, balance in summary.items() if balance > 0
  for creditor, debt in summary.items()
}

if final_balances:
  st.write("# Final Balances:")
  for person, balance in final_balances.items():
    if balance != "No Debts":
      st.write(f"## {person} owes {creditor} ¥{balance}")




# -- PLOT DATAFRAME
monthly_data=monthly_data.reset_index()
fig = px.bar(monthly_data,x='Date of expense',y='Amount',template='plotly_white',title='Mahine ka Hisab')
st.plotly_chart(fig)

