from sympy.physics.vector import dynamicsymbols
import sympy as sym
import numpy as np

# See instructions after the NHL_Eqn class for running this as a stand alone module.


class NHL_Eqn:

    """
        NHL_Eqn object

        Methods
        -------
        nh_lagranges_equations:
        This method uses attributes defined in the __init__ method to perform the operations associated with nonholonomic Lagranges equations.

        make_states:
        This method uses attributes to reduce the order of the equations of motion from second order to first order for each coordinate. This method relies on 
        sympy and it's derivative function. 

        get_alpha:
        This method is used to obtain the alpha_hk terms shown in the nonholonomic lagrange equations.
        the constraint attribute is used in the .coeff() method.

        Attributes
        ----------
        Lagrangian: The Lagragian, L, defined as L=T-V. Where T is the total kinetic energy and V is the total potential energy. This must be entered into the constructor.

        Coordinates: These are the coordinates of the system. Example: x,y,z. These must be entered into the constructor

        Coordinate Derivatives: The derivatives of the coordinates mentioned above. Example: x'(t), y'(t), z'(t). These must be entered into the constructor.

        Optional Attributes
        -------------------

        State Variables: The varibles the user chooses to use for state space representation. This attribute is set to none by default. If there are no states defined, the get_states
                          method will not apply. An error will be raised.

        Constraint Equations: The nonholonomic constraints of the system or model. These equations are optional and the default is none. If there are no constraints defined,
        the get_alpha method will raise an error

    """

    def __init__(self, lagrangian: sym.core.add.Add, coordinates: tuple, coordinate_derivatives: tuple,
                 state_variables: list = None, constraint_equations: list = None, *, k: int = 0, m: int = 0) -> None:

        self.lagrangian = lagrangian
        self.coordinates = coordinates
        self.coordinate_derivatives = coordinate_derivatives
        self.constraint_equations = constraint_equations
        self.state_variables = state_variables
        self.k = k
        self.m = m

        if not type(lagrangian) is sym.core.add.Add:
            raise TypeError('Verify the Lagrangian is of the proper type.')

        if not type(coordinates) is tuple:
            raise TypeError('Coordinates must be a tuple.')

        if not type(coordinate_derivatives) is tuple:
            raise TypeError('Coordinate_derivatives must be a tuple.')

        if state_variables != None and not type(state_variables) is list:
            raise TypeError('State_variables must be a tuple.')

        if constraint_equations != None and not type(constraint_equations) is tuple:
            raise TypeError('Constraint_equations must be a tuple.')

        if not type(k) is int:
            raise TypeError('k must be an integer.')

        if k <= 0:
            raise ValueError('k must be positive.')

        if not type(m) is int:
            raise TypeError('m must be an integer.')

        if m <= 0:
            raise ValueError('m must be positive.')

    def nh_lagranges_equations(self):
        """
            lagranges_equations will produce a system of equations, given in a list, by evaluating Lagrange's equations. There are no inputs other than the self. 

        """
        # This is applies when there are no nonholonomic constraints effectivly resulting in the normal Lagranges equations.
        try:
            if self.constraint_equations == None:
                eoms = []
                for i, qk in enumerate(self.coordinates):
                    qkd = self.coordinate_derivatives[i]

                    # below is the Lagrange equation to be iterated for each coordinate. The bit of code below evaluates Lagrange's equation for each coordinate and
                    # appends it to a list in step.
                    eoms.append(sym.diff(sym.diff(self.lagrangian, qkd), sym.Symbol(
                        't'))-sym.diff(self.lagrangian, qk))
                return eoms
        except:
            print('Error: Please verify the Lagrangian, coordinates and their derivatives. They should all be symbols')

        # If nonholonomic constraints are present, this step will apply.
        else:
            eoms = []
            for k in range(self.k):
                holonomic = sym.diff(sym.diff(self.lagrangian, self.coordinate_derivatives[k]), sym.Symbol(
                    't'))-sym.diff(self.lagrangian, self.coordinates[k])
                nonholonomic = []
                for h in range(self.m):
                    nonholonomic.append(sym.diff(sym.diff(self.lagrangian, self.coordinate_derivatives[k+h+1]), sym.Symbol(
                        't'))-sym.diff(self.lagrangian, self.coordinates[k+h+1]))
                for i in range(len(nonholonomic)-1):
                    holonomic+nonholonomic[i]+nonholonomic[i+1]
                    eoms.append(
                        holonomic+nonholonomic[i]*self.get_alpha()[i]+nonholonomic[i+1]*self.get_alpha()[i+1])
            return eoms

    def make_states(self):
        """
            make_states method will take the equations of motion produced from the lagranges_equation method and express them as a system of first order ODEs.
            There are no inputs other than the self.
        """

        equations = []
        for i, expression in enumerate(self.lagranges_equations()):

            # denom is the coefficient of the second order dervative of the current coordinate.
            denom = expression.coeff(sym.Derivative(
                self.coordinates[i], (sym.var('t'), 2)))

            # The operation below extracts the right hand side of the equation by solving the expression for the second order derivative and setting the output
            # to the rhs. The denom expression is used to ensure the integrity of the equation is held by dividing the coefficient of the second order derivative
            # into every term. This is important if there is any non-conservative work in the system.

            # rhs is the right hand side of the equation of motion after isolating the
            rhs = sym.solve(
                expression/denom, sym.Derivative(self.coordinates[i], (sym.var('t'), 2)))[0]
            # second order derivative of the current coordinate.

            # lhs is the left hand side of the equation of motion after isolating the
            lhs = sym.simplify((expression/denom)+rhs)
            # second order derivative of the current coordinate. This is the second order derivative of the current coordinate.

            for k in range(len(self.coordinates)):
                # This operation equates lhs to rhs and performs variable substituion to reduce the order of the
                # ODEs by 1. The output is a list that contains a system of equations.

                rhs = rhs.subs(sym.Derivative(self.coordinates[k], sym.var(
                    't'), 1), self.state_variables[k+len(self.coordinates)]).subs(self.coordinates[k], self.state_variables[k])
                lhs = lhs.subs(sym.Derivative(self.coordinates[k], sym.var(
                    't'), 1), self.state_variables[k+len(self.coordinates)]).subs(self.coordinates[k], self.state_variables[k])

            # here we are simplitfing the equation so it shows a clean equation.
            eq1 = sym.Eq(lhs, rhs).simplify()

            eq2 = sym.Eq(sym.Derivative(self.state_variables[i], sym.var(
                't'), 1), self.state_variables[i+len(self.coordinates)])

            equations.append(eq1)
            equations.append(eq2)

        return equations

    def get_alpha(self):
        """
            This function will examine the constraint equation for the alphas found in the nonholonomic Lagranges equations.
        """
        try:
            alphas = []
            for h in range(self.m):
                for k in range(self.k):
                    alphas.append(self.constraint_equations[h].coeff(
                        self.coordinate_derivatives[k]))
            self.alphas = alphas
            return alphas
        except:
            print(
                'No constraints have been defined. Enter constraint equations into constuctor to obtain alphas.')


# To run this as a stand alone module, alter the main function to fit your system or model.
#
if __name__ == "__main__":
    def main():

        # This step establishes the variable names used for the coordinates used in the lagrangian.
        # coordinates must be entered with independent coords first.
        x, y, z = dynamicsymbols('x y z')
        # The right side of this equation must match the left side of the one above.
        coordinates = z, x, y

        # This step establishes the variable names we wish to use for the state space
        z1, z2, z3, z4, z5, = dynamicsymbols('z1 z2 z3 z4 z5')
        # The contents of the list must match the left side of the equation above
        state_variables = [z1, z2, z3, z4, z5]

        # This step assigns variable names fot coordinate derivatives
        xd, yd, zd = dynamicsymbols('x y z', 1)
        # The right side of this equation must match the left side of the one above.
        coordinate_derivatives = zd, xd,

        # This step makes the parameters into symbols.
        # Every parrameter in the system must appear here. If the value is known, enter it directly in the Lagrangian
        m, g = sym.symbols('m g')

        # The Lagrangian with parameters, coordinates, and coordinate derivatives as symbols and symbol functions.
        # This MUST be entered with the exact same coordinate and parameter names that were established above.
        lagrangian = sym.Rational(1/2)*m*(xd**2+yd**2+zd**2)-m*g*z

        # Enter the constraint equations here. They must be in derivative form, not Pfaffian form. Additionally,
        # the constraints must equal 0 on the right hand side.
        # Example: x'+y'+yz'=0. c1 and c2 are the consrtraint equations. If more are desired, follow the same naming convention.
        # If your system has 0 nonholonimic constraints, u
        c1 = xd+x*yd+y*zd
        c2 = y*xd+z*yd+zd
        constraint_equations = [c1, c2]
        # constraint_equations=None

        system = NHL_Eqn(lagrangian, coordinates, coordinate_derivatives,
                         state_variables, constraint_equations, k=1, m=2)
        return system

    system = main()
    print(system.nh_lagranges_equations())
