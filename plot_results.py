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
electricity_bus = views.node(results, "bel")
gas_bus = views.node(results, "gas")
thermal_bus = views.node(results, "bth")
pp_chp_bus = views.node(results, "pp_chp")
pth = views.node(results, "pth")


fig, ax = plt.subplots(figsize=(10, 5))
electricity_bus["sequences"].plot(
    ax=ax, kind="line", drawstyle="steps-post"
)
plt.legend(
    loc="upper center", prop={"size": 8}, bbox_to_anchor=(0.5, 1.3), ncol=2
)
fig.subplots_adjust(top=0.8)
plt.show()

fig, ax = plt.subplots(figsize=(10, 5))
gas_bus["sequences"].plot(
    ax=ax, kind="line", drawstyle="steps-post"
)
plt.legend(
    loc="upper center", prop={"size": 8}, bbox_to_anchor=(0.5, 1.3), ncol=2
)
fig.subplots_adjust(top=0.8)
plt.show()

fig, ax = plt.subplots(figsize=(10, 5))
thermal_bus["sequences"].plot(
    ax=ax, kind="line", drawstyle="steps-post"
)
plt.legend(
    loc="upper center", prop={"size": 8}, bbox_to_anchor=(0.5, 1.3), ncol=2
)
fig.subplots_adjust(top=0.8)
plt.show()

fig, ax = plt.subplots(figsize=(10, 5))
pp_chp_bus["sequences"].plot(
    ax=ax, kind="line", drawstyle="steps-post"
)
plt.legend(
    loc="upper center", prop={"size": 8}, bbox_to_anchor=(0.5, 1.3), ncol=2
)
fig.subplots_adjust(top=0.8)
plt.show()

fig, ax = plt.subplots(figsize=(10, 5))
pth["sequences"].plot(
    ax=ax, kind="line", drawstyle="steps-post"
)
plt.legend(
    loc="upper center", prop={"size": 8}, bbox_to_anchor=(0.5, 1.3), ncol=2
)
fig.subplots_adjust(top=0.8)
plt.show()