# -*- coding: utf-8 -*-

import os
import logging
import matplotlib.pyplot as plt

from oemof.solph import EnergySystem
from oemof.solph import views

logging.info("Restore the energy system and the results.")

# Get the current working directory
current_directory = os.getcwd()
file_name = 'results.oemof'

# Read results file
energysystem = EnergySystem()
energysystem.restore(current_directory, file_name)

# define an alias for shorter calls below (optional)
results = energysystem.results["main"]

# get all variables of a specific component/bus
thermal_bus = views.node(results, "bth")
storage = views.node(results, "storage")

# Analyse thermal node
Sum_th_demand = thermal_bus["sequences"][(('bth', 'demand_th'), 'flow')].sum()
Sum_th_prod_chp = thermal_bus["sequences"][(('pp_chp', 'bth'), 'flow')].sum()
Sum_th_prod_pth = thermal_bus["sequences"][(('pth', 'bth'), 'flow')].sum()

fig, axs = plt.subplots(3,figsize=(16, 9))
fig.suptitle('Thermal flows comparison', fontsize=24)
axs[0].plot(thermal_bus["sequences"][(('bth', 'demand_th'), 'flow')], 'blue')
axs[0].set_title(f'bth to demand_th, Sum = {int(Sum_th_demand/1000)} MWh')
axs[1].plot(thermal_bus["sequences"][(('pp_chp', 'bth'), 'flow')], 'green')
axs[1].set_title(f'pp_chp to bth, Sum = {int(Sum_th_prod_chp/1000)} MWh')
axs[2].plot(thermal_bus["sequences"][(('pth', 'bth'), 'flow')], 'orange')
axs[2].set_title(f'pth to bth, Sum = {int(Sum_th_prod_pth/1000)} MWh')

axs[0].set_ylabel('Power in kW')
axs[1].set_ylabel('Power in kW')
axs[2].set_ylabel('Power in kW')

plt.tight_layout()
plt.show()

# Analyse storage node
Sum_storage_Inflow = storage['sequences'][(('storage', 'bth'), 'flow')].sum()
Sum_storage_Outflow = storage['sequences'][(('bth', 'storage'), 'flow')].sum()

fig, ax = plt.subplots(figsize=(16, 9))
storage['sequences'][(('bth', 'storage'), 'flow')].plot(
    ax=ax, kind="line", drawstyle="steps-post",color="green"
)
plt.legend(
    loc="upper right"
)
fig.subplots_adjust(top=0.8)
fig.suptitle(f'Storage inflow, Sum = {int(Sum_storage_Inflow / 1000)} MWh', fontsize=24)
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(16, 9))
storage['sequences'][(('storage', 'bth'), 'flow')].plot(
    ax=ax, kind="line", drawstyle="steps-post",color="blue"
)
plt.legend(
    loc="upper right"
)
fig.subplots_adjust(top=0.8)
fig.suptitle(f'Storage outflow, Sum = {int(Sum_storage_Outflow / 1000)} MWh', fontsize=24)
plt.show()

fig, ax = plt.subplots(figsize=(16, 9))
storage['sequences'][(('storage', 'None'), 'storage_content')].plot(
    ax=ax, kind="line", drawstyle="steps-post",color="orange"
)
plt.legend(
    loc="upper right"
)
fig.subplots_adjust(top=0.8)
fig.suptitle('Storage content', fontsize=24)
plt.tight_layout()
plt.show()

fig, axs = plt.subplots(3,figsize=(16, 9))
fig.suptitle('Comparison of storage flows and content', fontsize=24)
axs[0].plot(storage['sequences'][(('bth', 'storage'), 'flow')], 'green')
axs[0].set_title(f'Storage inflow, Sum = {int(Sum_storage_Inflow / 1000)} MWh')
axs[1].plot(storage['sequences'][(('storage', 'bth'), 'flow')], 'blue')
axs[1].set_title(f'Storage outflow, Sum = {int(Sum_storage_Outflow / 1000)} MWh')
axs[2].plot(storage['sequences'][(('storage', 'None'), 'storage_content')], 'orange')
axs[2].set_title('Storage content')

axs[0].set_ylabel('Power in kW')
axs[1].set_ylabel('Power in kW')
axs[2].set_ylabel('Content in kWh')

plt.tight_layout()
plt.show()