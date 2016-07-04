from __future__ import division, print_function

from ScientificProjects.Client import Client

from Schottky import Simulators

client = Client(config_file_name='config.ini')

client.user_manager.sign_in('bond_anton', 'secret_password')
client.user_manager.project_manager.open_project('Schottky diode')

#sim = Simulators.Simulator(client)

#print(sim)
#print(sim.equipment)

client.user_manager.sign_out()
