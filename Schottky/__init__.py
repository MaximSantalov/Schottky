from scipy.constants import c, N_A, k, e, m_e, epsilon_0

# Units for the experiments are cm for length, g for mass, s fot time, and eV for energy
constants = {
    'c': c * 100,  # m/s
    'Avogadro': N_A,
    'q': e,  # C
    'm_e': m_e * 1000,  # g
    'A_R': 1.20173e2,  # A*cm-2*K-2
    'k': k / e,  # eV/K
    'epsilon_0': epsilon_0 * 1e-2,  # F/cm
}
