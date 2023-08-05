from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
# from NHL import *


def derivatives(z, time, parameters):
    m1, m2, k = parameters
    z1, z2, z3, z4 = z
    dz1dt = z3
    dz2dt = z4
    dz3dt = (k/m1)*(z2-2*z1)
    dz4dt = (k/m2)*(z1-z2)
    return dz1dt, dz2dt, dz3dt, dz4dt


def plot_state_vs_time(time: np.ndarray, state: int, initial_conditions):

    solution = odeint(derivatives, initial_conditions,
                      time, args=(parameters,))

    plt.figure(figsize=(15, 7.5))
    plt.plot(time, solution[:, state],
             label=f'$z_{state+1}$ Numerical')
    plt.title(f'$z_{state+1}$ Vs Time', fontsize=30)
    plt.xlabel('t', fontsize=30)
    plt.ylabel(f'$z_{state+1}$', fontsize=30)


def plot_phase_portrait(time: np.ndarray, state1: int, state2: int, initial_conditions: np.ndarray):

    solution = odeint(derivatives, initial_conditions,
                      time, args=(parameters,))

    plt.figure(figsize=(15, 7.5))
    plt.plot(solution[:, state1], solution[:, state2],
             label='$x_1$ Numerical')
    plt.title(f'$z_{state1+1}$ Vs $z_{state2+1}$', fontsize=30)
    plt.xlabel(f'$z_{state1+1}$', fontsize=30)
    plt.ylabel(f'$z_{state2+1}$', fontsize=30)


if __name__ == "__main__":
    tmax = 5
    dt = .0001
    time = np.arange(0, tmax+dt, dt)
    parameters = np.array([100, 100, 2000])
    intial_conditions = np.array(
        [.5, 0, 0, 0])

    plot_state_vs_time(time, 0, intial_conditions)
    plot_phase_portrait(time, 0, 2, intial_conditions)
    plt.show()
