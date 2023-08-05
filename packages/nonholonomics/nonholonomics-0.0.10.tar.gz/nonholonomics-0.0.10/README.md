In this project I aim to model carangiform fish swimming using nonholonomic constraints. Some of my approximations neglect various environmental effects. Because of this, my model can be reduced to a "landfish". The model consists of two rigid bodies: a head and tail, each with its own set of physical attribute parameters. The motion of the tail will be an imposed angular oscillation (to mimic neuromuscular activation) relative to the head. Nonholonomic constraints emulate the effects of dorsal and caudal "fins" on the landfish. In this model, the head and tail are constrained to move in the direction they are pointing. The tail is linked to the head by pins and springs. To ensure the forward motion has a bounded velocity, a nonlinear damping term is added to the equation of motion.

I will use nonholonomic Lagrange equations to produce the equations of motion. Which consist of one second-order nonlinear differential equation and two first-order nonholonomic constraint equations, representing a fourth-order forced dynamical system. I will analyze the behavior of the equations of motion to gain insight on possible parameter limitations, and roles.

Simulations will be done using Python. For various parameter values, examples of robust, smooth fish-like swimming should be obtainable. In which, the head oscillates slightly about a mean path as the landfish "swims" along a rigid, substrate. Parameters sets that show smooth, robust swimming will be analyzed in greater detail to see how the velocity builds from rest and to categorize the swimming motion.

If time permits, I would also like to use machine learning to perform systematic simulations for uncovering classes of behavior, small-parameter perturbation analyses may also be done for revealing roles of parameters in regular motion

evaluateNHL.py
    This file contatins a function that will symbolically evaluate the nonholonomic lagrange equation. The file will need to be give the unconstrained lagrangian, the nonholonomic constraints, and the dynamic varibles as a an array from 1-n with the independant variables being the first p entries and the dependant varibles occupying the n-p slots at the end.

nondimensionalization.py
    This program will nondimensionalize the output of evaluateNHL or any second order ode with some limitations.

harmonicbalance.py
    This program takes in the the EOM od nondimensionalized EOM and performs a harmonic balance to obtain the steady state solution of the independent variable. 

Simulation.py
    This program takes in the eom or the nondimensionalized eom and numerically solves the system of odes. Then runs a ploting routine to plot various phase portraits and in my personal case, will animate the solutions

Parameterstudy.py
    This program will examine the eom for import relationships between parameters in either the dimensional case or nondimensional case. The quatitavie results will presented qualitatively as expected outcomes based on some chosen parameters.