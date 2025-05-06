import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

data = {
    'ISIN': ['US912828U816', 'US912828U473', 'US9128285M81'],
    'Purchase_Price': [980, 1015, 1000],
    'Market_Price': [990, 1020, 1010],
    'Coupon': [2.5, 3.0, 1.8],
    'Maturity_Date': ['2027-06-30', '2025-12-31', '2026-11-15'],
    'Face_Value': [1000, 1000, 1000],
    'Purchase_Date': ['2022-06-30', '2021-12-31', '2023-11-15']
}

df = pd.DataFrame(data)

df['Maturity_Date'] = pd.to_datetime(df['Maturity_Date'])
df['Purchase_Date'] = pd.to_datetime(df['Purchase_Date'])

today = pd.Timestamp(datetime.today().date())

df['Time_to_Maturity'] = (df['Maturity_Date'] - today).dt.days / 365.25

df['Current_Yield'] = (df['Coupon'] * df['Face_Value']) / df['Market_Price']

df['YTM'] = ((df['Coupon'] * df['Face_Value'] + (df['Face_Value'] - df['Market_Price']) / df['Time_to_Maturity']) /
             ((df['Market_Price'] + df['Face_Value']) / 2))

# Profit or Loss (PnL)
df['PnL'] = df['Market_Price'] - df['Purchase_Price']

# Print Portfolio Summary
print("Portfolio Summary:\n")
print(df[['ISIN', 'Market_Price', 'Current_Yield', 'YTM', 'PnL', 'Time_to_Maturity']])

# Save to Excel
df.to_excel("fixed_income_summary.xlsx", index=False)

# Plot PnL
plt.figure(figsize=(10, 6))
plt.bar(df['ISIN'], df['PnL'], color=['green' if x > 0 else 'red' for x in df['PnL']])
plt.title('Portfolio PnL by Security')
plt.xlabel('ISIN')
plt.ylabel('PnL ($)')
plt.grid(True)
plt.tight_layout()
plt.savefig("portfolio_pnl_plot.png")
plt.show()
