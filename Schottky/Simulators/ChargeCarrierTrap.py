from __future__ import division, print_function
# import timeit
import numpy as np

from Schottky.Samples.Trap import Trap
from Schottky.Simulators import Simulator
from Schottky.Simulators.Field import FieldSimulator
from Schottky import constants


class ChargeCarrierTrap(Simulator):

    def __init__(self, client, trap, description=None):
        assert isinstance(trap, Trap), 'Valid Trap Sample object expected'
        self.trap = trap
        samples = [self.trap]
        name = 'Charge Carrier Trap Simulator'
        category = {
            'name': 'Software',
            'description': 'Measurement, automation, control, simulation, and other software tools',
            'subcategory': {'name': 'Simulation',
                            'description': 'Simulation software',
                            'subcategory': None}}
        measurement_types = [{'name': 'Capture and Emission Kinetics',
                              'description': 'Measurement of charge carrier trap capture and emission kinetics',
                              'children': []}]
        measurements = [
            {'name': 'Capture rate',
             'description': 'measure charge carriers capture rate',
             'type': 'Capture and Emission Kinetics'},
            {'name': 'Emission rate',
             'description': 'measure charge carriers emission rate',
             'type': 'Capture and Emission Kinetics'},
        ]
        parts = None
        if trap.trap_potential:
            parts = [FieldSimulator(client=client, field=trap.trap_potential)]
        Simulator.__init__(
            self,
            client=client, name=name, description=description,
            samples=samples, parts=parts,
            category=category,
            measurement_types=measurement_types,
            measurements=measurements)

    def energy_level(self, band_gap):
        if self.trap.band == 'Ec':
            return self.trap.activation_energy
        else:
            return {'empty': band_gap - self.trap.activation_energy['empty'],
                    'full': band_gap - self.trap.activation_energy['full']}

    def capture_rate(self, temperature, f, n, p, v_n, v_p):
        sigma_n, sigma_p = self.trap.capture_cross_section(temperature)
        c_n = sigma_n * v_n * n
        c_p = sigma_p * v_p * p
        capture_n = c_n * (1 - f)
        capture_p = c_p * f
        return capture_n, capture_p

    def emission_rate(self, temperature, band_gap, f, v_n, v_p, n_c, n_v,
                      poole_frenkel_n=1.0, poole_frenkel_p=1.0):
        energy_scale = constants['k'] * temperature
        energy_level = self.energy_level(band_gap=band_gap)
        activation_energy_n = energy_level['full']
        activation_energy_p = energy_level['empty']
        sigma_n, sigma_p = self.trap.capture_cross_section(temperature)
        g_ratio_n = 1.0
        g_ratio_p = 1.0
        factor_n = sigma_n * v_n * n_c * g_ratio_n
        factor_n *= poole_frenkel_n
        factor_p = sigma_p * v_p * n_v * g_ratio_p
        factor_p *= poole_frenkel_p
        emission_rate_n = factor_n * np.exp(-activation_energy_n / energy_scale)
        emission_rate_p = factor_p * np.exp(-activation_energy_p / energy_scale)
        emission_n = emission_rate_n * f
        emission_p = emission_rate_p * (1 - f)
        return emission_n, emission_p
