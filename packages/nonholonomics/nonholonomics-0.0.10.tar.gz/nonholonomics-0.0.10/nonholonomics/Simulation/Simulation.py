import matplotlib.pyplot as plt
import numpy as np


def plot_state_vs_time(time: np.ndarray, state: int, *, solution: np.ndarray, figsize: tuple = (15, 7.5)):
    """
    Plot_state_vs_time will plot a chosen state against the time variable. 

    time: the times scale used to in the ODE solver

    state: The number coressponding to the state variable solution. 

            example: the state 'z1' has state=0. This is the index in the 'solution' array

    solution: This is the solution array provided by the ODE solver.

    figsize: the figure size given as a tuple.
    """

    if not type(time) is np.ndarray:
        raise TypeError('time needs to be in a numpy.ndarray')

    if not type(state) is int:
        raise TypeError('state needs to be of type int')

    if not type(solution) is np.ndarray:
        raise TypeError('solution needs to be in a numpy.ndarray')

    if not type(figsize) is tuple:
        raise TypeError('figsize needs to be in a tuple')

    plt.figure(figsize=figsize)
    plt.plot(time, solution[:, state],
             label=f'$z_{state+1}$ Numerical')
    plt.title(f'$z_{state+1}$ Vs Time', fontsize=30)
    plt.xlabel('t', fontsize=30)
    plt.ylabel(f'$z_{state+1}$', fontsize=30)


def plot_phase_portrait(state1: int, state2: int, *, solution: np.ndarray, figsize: tuple = (15, 7.5)):
    """
    Plot_phase_portrait will plot two state variables. With state2 as function of state1
    state1 and state2 are integers in the range of state variables of the system starting 0. 

    Example: for 'z1 vs z3' state1=0 and state2=2

    figsize: the figure size given as a tuple.

    state1: the state variable that appears on the horizontal axis

    state2: the state variable that appears on the vertical axis
    """

    if not type(state1) is int:
        raise TypeError('state1 needs to be of type int')

    if not type(state2) is int:
        raise TypeError('state2 needds to be of type int')

    if not type(solution) is np.ndarray:
        raise TypeError('solution needs to be in a numpy.ndarray')

    if not type(figsize) is tuple:
        raise TypeError('figsize needs to be in a tuple')

    plt.figure(figsize=figsize)
    plt.plot(solution[:, state1], solution[:, state2],
             label='$x_1$ Numerical')
    plt.title(f'$z_{state1+1}$ Vs $z_{state2+1}$', fontsize=30)
    plt.xlabel(f'$z_{state1+1}$', fontsize=30)
    plt.ylabel(f'$z_{state2+1}$', fontsize=30)


def plot_n_states(time: np.ndarray, *, kind: str, solution: np.ndarray, figsize: tuple = (15, 7.5)):
    """
    Plot_n_states will plot chosen states against the time variable. This generally used to plot all of the positions
    or all of the velocities.  

    time: the times scale used to in the ODE solver

    solution: The solution array comprised of solutions for the states wishe to be plotted.

    figsize: the figure size given as a tuple.
    """

    if not type(time) is np.ndarray:
        raise TypeError('time needs to be in a numpy.ndarray')

    if not type(solution) is np.ndarray:
        raise TypeError('solution needs to be in a numpy.ndarray')

    if not type(figsize) is tuple:
        raise TypeError('figsize needs to be in a tuple')

    if not type(kind) is str:
        raise TypeError(
            'kind needs to be a string. Common choices are velocity and position.')

    plt.figure(figsize=figsize)
    for i in range(solution.shape[1]):
        plt.plot(time, solution[:, i],
                 label=f'z{i+1}')
    plt.title(f'{kind} Vs Time', fontsize=30)
    plt.xlabel('t', fontsize=30)
    plt.ylabel(f'{kind}', fontsize=30)
    plt.legend()


if __name__ == "__main__":
    tmax = 5
    dt = .0001
    time = np.arange(0, tmax+dt, dt)

    x1 = 0.138197*np.cos(2.76393*time)+0.361803*np.cos(7.23606*time)
    x2 = 0.223607*np.cos(2.76393*time)-0.223607*np.cos(7.23606*time)

    solution = np.transpose(np.array([x1, x2]))

    plot_state_vs_time(time, 0, solution=solution,)
    plot_phase_portrait(0, 1, solution=solution,)
    plot_n_states(time, solution=solution)
    plt.show()
