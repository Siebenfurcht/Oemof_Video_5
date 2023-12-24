import matplotlib.pyplot as plt
import pandas as pd
import os
from oemof.solph import create_time_index

# Read data file
filename = os.path.join(os.getcwd(), "input_data.csv")
try:
    data = pd.read_csv(filename)
except FileNotFoundError:
    msg = "Data file not found: {0}. Only one value used!"
    data = pd.DataFrame(
        {
            "DAA_price": [500, 400],
            "demand_th": [0.1, 0.3],
            "CO2_price": [300, 200],
            "Gas_price": [70, 80]
        }
    )

datetimeindex = create_time_index(2022, number=len(data)-1)

data.insert(0,"datetime",datetimeindex,True)

data['datetime'] = pd.to_datetime(data['datetime'])
data.set_index('datetime')

fig, ax1 = plt.subplots(figsize=(10, 5))

ax2 = ax1.twinx()
ax1.plot(data['datetime'], data['DAA_price'], 'blue')
ax1.plot(data['datetime'], data['CO2_price'], 'orange')
ax1.plot(data['datetime'], data['Gas_price'], 'green')
ax2.plot(data['datetime'], data['demand_th'], 'brown')
ax1.set_xlabel('time')
ax1.set_ylabel('price in €/MWh')
ax2.set_ylabel('demand in % of nom. value')

plt.show()

fig, axs = plt.subplots(4)
fig.suptitle('Comparison of input data')
axs[0].plot(data['datetime'], data['Gas_price'], 'green')
axs[1].plot(data['datetime'], data['DAA_price'], 'blue')
axs[2].plot(data['datetime'], data['CO2_price'], 'orange')
axs[3].plot(data['datetime'], data['demand_th'], 'brown')

axs[0].set_ylabel('price in €/MWh')
axs[1].set_ylabel('price in €/MWh')
axs[2].set_ylabel('price in €/MWh')
axs[3].set_ylabel('demand in % of nom. value')


plt.show()