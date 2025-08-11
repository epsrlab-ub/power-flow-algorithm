# Inexact Constant Jacobian Method

This repository contains implementations of the **Inexact Constant Jacobian (ICJ)** method for performing power flow analysis on distribution systems in both MATLAB and Python. The method is developed based on the Newton Raphson (NR) Power Injection method, incorporating key assumptions for simplifying the analysis.

## Assumptions

The ICJ method is based on the following assumptions regarding the characteristics of the distribution network under normal operating conditions:

1. **Equal Voltage Magnitude**: The voltage magnitude is equal for all nodes in per unit (p.u.), i.e., \( V_i = 1 \, \text{p.u.} \).
2. **Small Voltage Angle Differences**: The voltage angle differences between neighboring nodes are small, i.e., \( \delta_i - \delta_j \) is minimal.

## Overview

The main function of the ICJ method computes the voltage profile of buses in a radial or mesh distribution system. It requires two primary inputs: load data and line data. The load data specifies the bus index along with the real and reactive power for each bus, while the line data includes information on the resistance and reactance of the lines connecting the buses.

### Functionality

The function includes the following features:

- **Data Input Requirements**: 
  - Load data must be structured with three columns: bus index, real power (P), and reactive power (Q).
  - Line data must have four columns: sending bus index, receiving bus index, resistance (R), and reactance (X).
  
- **Customizable Parameters**: Users can specify:
  - Slack bus voltage
  - Convergence tolerance for iteration
  - Maximum number of iterations allowed for calculations

  Default values for these parameters are provided, which can be overridden when calling the function.

### Guidance for Use

1. **Input Format**: Ensure that the input data (i.e., load and line data) is formatted correctly:
   - **Load Data**: 
     - Column 1: Bus index
     - Column 2: Real power (P)
     - Column 3: Reactive power (Q)
   - **Line Data**: 
     - Column 1: Sending bus index
     - Column 2: Receiving bus index
     - Column 3: Line resistance (R)
     - Column 4: Line reactance (X)

2. **Function Call**: To execute the function, provide the load and line data as arguments, along with optional parameters for slack bus voltage, tolerance, and maximum iterations. If you skip any of the optional parameters, the function will use the predefined default values.

3. **Example Usage**: The prompt provides an example of how to call the function. For instance:
   - **Python**:
     ```python
     v, iteration = icj_method(load_data, line_data, slack_bus_voltage=1.5, tolerance=1e-4)
     ```
   - **MATLAB**:
     ```matlab
     [v, iteration] = icj_method(load_data, line_data, 1.5, 1e-4);
     ```

4. **Exiting the Function**: Users are prompted to press Enter to continue or type 'quit' to exit the function, allowing for flexibility in user interaction.

### Expected Outputs

Upon successful execution, the function returns the following outputs:
- Voltage after each iteration
- Number of iterations
- Time taken for each iteration
- Average time taken for all runs
- Total active and reactive power loss
- Substation active and reactive power
- Graph of voltage magnitude and angle
- Single line diagram of the system model
- Graph of the relationship between maximum error and computational time
- .csv and .txt file of the voltage profile

This provides a comprehensive tool for conducting power flow analysis in distribution networks, supporting both MATLAB and Python users.

## Files

- `icj_method.py`: Python code for the Inexact Constant Jacobian Method for power flow analysis.
- `icj_method.m`: MATLAB code for the Inexact Constant Jacobian Method for power flow analysis.
