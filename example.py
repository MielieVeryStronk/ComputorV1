import computorv1

computorv1.run_example("-35 * X^0 - 2 * X^1 + 1 * X^2 = 0")             # X = -5 OR 7
computorv1.run_example("0 = 1 * X^2 + 1 * X^1 - 2 * X^0")               # X = 1 OR -2
computorv1.run_example("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")       # X = 0.905239 OR -0.475131
computorv1.run_example("12 * X^0 = - 4 * X^1 + 1 * X^2")                # X = -2 OR 6
computorv1.run_example("12 * X^0 = - 4 * X^1 + 1 * X^3")                # err degree bigger than 2
