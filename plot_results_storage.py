# -*- coding: utf-8 -*-

import logging
import matplotlib.pyplot as plt

from oemof.solph import EnergySystem
from oemof.solph import views

logging.info("Restore the energy system and the results.")

# Read results file
energysystem = EnergySystem()
energysystem.restore('/home/michel/PycharmProjects/Oemof_Video5', filename='results.oemof')

# define an alias for shorter calls below (optional)
results = energysystem.results["main"]

# get all variables of a specific component/bus
storage = views.node(results, "storage")
keys = ((('bth', 'storage'), 'flow'),(('storage', 'bth'), 'flow'))
storage_flows = storage['sequences']
dictfilt = lambda x, y:dict([ (i,x[i]) for i in x if i in set(y) ])
storage_flows = dictfilt(storage_flows, keys)
storage_content = storage['sequences'][(('storage', 'None'), 'storage_content')]

Sum_Inflow = storage['sequences'][(('storage', 'bth'), 'flow')].sum()
print('storage-bth ',Sum_Inflow)
Sum_Outflow = storage['sequences'][(('bth', 'storage'), 'flow')].sum()
print('bth-storage ',Sum_Outflow)

print('Storage:\n\n',storage['sequences'].keys(),'\n\n',storage['sequences'])
print('Storage_flow:\n\n',storage_flows.keys(),'\n\n',storage_flows)
print('Storage_content:\n\n',storage_content.keys(),'\n\n',storage_content)

fig, ax = plt.subplots(figsize=(10, 5))
storage_flows[(('bth', 'storage'), 'flow')].plot(
    ax=ax, kind="line", drawstyle="steps-post",color="green"
)
plt.legend(
    loc="upper right"
)
fig.subplots_adjust(top=0.8)
fig.suptitle(f'Figure 1: Storage inflow, Sum = {int(Sum_Inflow/1000)} MWh')
plt.show()

fig, ax = plt.subplots(figsize=(10, 5))
storage_flows[(('storage', 'bth'), 'flow')].plot(
    ax=ax, kind="line", drawstyle="steps-post",color="blue"
)
plt.legend(
    loc="upper right"
)
fig.subplots_adjust(top=0.8)
fig.suptitle(f'Figure 2: Storage outflow Storage outflow, Sum = {int(Sum_Outflow/1000)} MWh')
plt.show()

fig, ax = plt.subplots(figsize=(10, 5))
storage_content.plot(
    ax=ax, kind="line", drawstyle="steps-post",color="orange"
)
plt.legend(
    loc="upper right"
)
fig.subplots_adjust(top=0.8)
fig.suptitle('Figure 3: Storage content')
plt.show()

fig, axs = plt.subplots(3)
fig.suptitle('Figure 4: Comparison of storage flows and content')
axs[0].plot(storage_flows[(('bth', 'storage'), 'flow')], 'green')
axs[0].set_title(f'Storage inflow, Sum = {int(Sum_Inflow/1000)} MWh')
axs[1].plot(storage_flows[(('storage', 'bth'), 'flow')], 'blue')
axs[1].set_title(f'Storage outflow, Sum = {int(Sum_Outflow/1000)} MWh')
axs[2].plot(storage_content, 'orange')
axs[2].set_title('Storage content')

axs[0].set_ylabel('Power in kW')
axs[1].set_ylabel('Power in kW')
axs[2].set_ylabel('Content in kWh')

plt.show()

