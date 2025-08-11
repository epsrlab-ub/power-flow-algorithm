# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 15:17:18 2024

@author: USER!
"""

import numpy as np

def build_inexact_Jacobian(Y_bus, num_buses):
    """
    Constructs the Jacobian matrix for power flow analysis.

    Parameters:
    v : ndarray
        Voltage at each bus (complex values).
    Y_bus : ndarray
        Admittance matrix (Y_bus).
    num_buses : int
        The number of buses in the system.

    Returns:
    Jacobian : ndarray
        The constructed Jacobian matrix.
    """

    # Initialize the Jacobian sub-matrices J1, J2, J3, and J4 as zero matrices
    J1 = np.zeros((num_buses - 1, num_buses - 1))
    J2 = np.zeros((num_buses - 1, num_buses - 1))
    J3 = np.zeros((num_buses - 1, num_buses - 1))
    J4 = np.zeros((num_buses - 1, num_buses - 1))
    
    # Loop over buses from 2 to N (ignoring the slack bus at index 1)
    for i in range(1, num_buses):
        Gii = np.real(Y_bus[i, i])  # Real part (conductance) for bus i
        Bii = np.imag(Y_bus[i, i])  # Imaginary part (susceptance) for bus i
        
        # Diagonal Jacobian elements (excluding bus 1)
        J1[i-1, i-1] = np.sum(np.imag(Y_bus[i, :])) - Bii
        J2[i-1, i-1] = 2 * Gii + np.sum(np.real(Y_bus[i, :])) - Gii
        J3[i-1, i-1] = np.sum(np.real(Y_bus[i, :])) - Gii
        J4[i-1, i-1] = -2 * Bii - np.sum(np.imag(Y_bus[i, :])) + Bii
        
        # Off-diagonal Jacobian elements
        for j in range(1, num_buses):  # Excluding bus 1 (slack bus)
            if i != j:
                Gij = np.real(Y_bus[i, j])  # Real part (off-diagonal)
                Bij = np.imag(Y_bus[i, j])  # Imaginary part (off-diagonal)
                
                J1[i-1, j-1] = -Bij  # Off-diagonal elements
                J2[i-1, j-1] = Gij
                J3[i-1, j-1] = -Gij
                J4[i-1, j-1] = -Bij
    
    # Combine submatrices to form the complete Jacobian
    Jacobian = np.block([[J1, J2], [J3, J4]])


    return Jacobian
