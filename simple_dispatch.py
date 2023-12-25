# -*- coding: utf-8 -*-

import os
import warnings
import logging

import pandas as pd

from oemof.solph import Bus
from oemof.solph import EnergySystem
from oemof.solph import Flow
from oemof.solph import Model
from oemof.solph import create_time_index
from oemof.solph import processing

from oemof.solph.components import Sink
from oemof.solph.components import Source
from oemof.solph.components import Converter
from oemof.solph.components import GenericStorage

def main():
    # Read data file
    filename = os.path.join(os.getcwd(), "input_data.csv")
    try:
        data = pd.read_csv(filename)
    except FileNotFoundError:
        msg = "Data file not found: {0}. Only one value used!"
        warnings.warn(msg.format(filename), UserWarning)
        data = pd.DataFrame(
            {
                "DAA_price": [500, 400],
                "demand_th": [0.1, 0.3],
                "CO2_price": [300, 200],
                "Gas_price": [70, 80]
            }
        )

    solver = "cbc"
    solver_verbose = False
    debug = False

    # Create an energy system and optimize the dispatch at least costs.
    # ####################### initialize and provide data #####################
    datetimeindex = create_time_index(2022, number=len(data))
    energysystem = EnergySystem(
        timeindex=datetimeindex, infer_last_interval=False
    )

    # ######################### create energysystem components ################

    # electricity, heat and natural gas
    bel = Bus(label="bel")
    bth = Bus(label="bth")
    bgas = Bus(label="gas")

    energysystem.add(bgas, bel, bth)

    # an excess and a shortage variable can help to avoid infeasible problems
    energysystem.add(
        Sink(
            label="excess_el",
            inputs={bel: Flow(
                variable_costs=data["DAA_price"]*-1
            )}
        )
    )

    # sources
    energysystem.add(
        Source(
            label="rgas",
            outputs={bgas: Flow(
                variable_costs=data["Gas_price"]/1000
                               +data["CO2_price"]*0.000202
            )}
        )
    )
    energysystem.add(
        Source(
            label="belgrid",
            outputs={bel: Flow(
                variable_costs=data["DAA_price"]
            )}
        )
    )

    # demands (electricity/heat)
    energysystem.add(
        Sink(
            label="demand_th",
            inputs={bth: Flow(
                nominal_value=353e3,
                fix=data["demand_th"]
            )},
        )
    )

    # power plants: pth and combined heat and power plant (chp)
    energysystem.add(
        Converter(
            label="pth",
            inputs={bel: Flow()},
            outputs={bth: Flow(
                nominal_value=10e3,
                variable_costs=1
            )},
            conversion_factors={bel: 0.99},
        )
    )

    energysystem.add(
        Converter(
            label="pp_chp",
            inputs={bgas: Flow(nominal_value=475e3)},
            outputs={
                bel: Flow(variable_costs=5),
                bth: Flow(),
            },
            conversion_factors={bel: 0.421, bth: 0.474},
        )
    )

    # add thermal storage
    energysystem.add(
        GenericStorage(
            label="storage",
            nominal_storage_capacity=900e3,
            inputs={bth: Flow(nominal_value=50e3)},
            outputs={bth: Flow(nominal_value=50e3)},
            loss_rate=0.001,
            initial_storage_level=None,
            inflow_conversion_factor=1,
            outflow_conversion_factor=0.99,
            )
    )

    # ################################ optimization ###########################

    # create optimization model based on energy_system
    model = Model(energysystem)

    # if tee_switch is true solver messages will be displayed
    logging.info("Solve the optimization problem")
    model.solve(solver=solver, solve_kwargs={"tee": solver_verbose})

    logging.info("Store the energy system with the results.")

    # add results to the energy system to make it possible to store them.
    energysystem.results["main"] = processing.results(model)
    energysystem.results["meta"] = processing.meta_results(model)

    # Get the current working directory
    current_directory = os.getcwd()
    file_name = 'results.oemof'

    energysystem.dump(current_directory, file_name)

    logging.info("Results have been dumped.")


if __name__ == "__main__":
    main()
