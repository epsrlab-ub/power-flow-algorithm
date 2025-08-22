# Power Flow Algorithm Repository

This repository contains a collection of **MATLAB** and **Python** codes that solve **AC power flow problems** using five conventional methods.  
The algorithms have been validated on the **33-bus distribution test system** for users’ convenience, and they are capable of being applied to various types of system networks, including radial and mesh configurations.

## Contents
- **Backward/Forward Sweep Method**
- **Newton–Raphson Power Method**
- **Newton–Raphson Current Method**
- **Z-Bus Method**
- **Decoupled Power Flow Method**

## Contributions

This work is the result of collaborative efforts:

| Name                 | Role                      | Contact                |
|----------------------|---------------------------|------------------------|
| **Morufdeen Atilola** | Developed the set of codes | 📧 morufdee@buffalo.edu |
| **Adedoyin Inaolaji** | Supervised the work        | 📧 ainaolaj@buffalo.edu |


**Note:**  
The algorithms provided in this repository are designed and validated for **single-phase** power flow analysis.  
They do not currently support three-phase or unbalanced system modeling.  
Modifications are required to extend the algorithms for multi-phase applications.

## DataFiles Reference
- **33-node:** M. E. Baran and F. F. Wu, "Network reconfiguration in distribution systems for loss reduction and load balancing," in IEEE Transactions on Power Delivery, vol. 4, no. 2, pp. 1401-1407, Apr 1989.
- **730-node:** H. K. Vemprala, M. A. I. Khan, and S. Paudyal, “Open-source polyphase distribution system power flow analysis tool (DxFlow),” in Proc. IEEE International Conference on Electro Information Technology (EIT), pp. 1–6, IEEE, 2019.

## Usage
Clone the repository:
```bash
git clone https://github.com/epsrlab-ub/power-flow-algorithm.git
