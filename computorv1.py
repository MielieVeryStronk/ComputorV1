from sys import argv
import re


class Term:
    power = 0
    coeff = 1

    def __init__(self, degree):
        self.coeff = 0.0
        self.power = degree

    def __init__(self, expression, side):
        terms = expression.split(" ")
        for item in terms:
            if item == "-":
                self.coeff *= -1
            elif "^" in item:
                self.power = item.split("^")[1]
            elif re.search(r"([0-9]*\.?[0-9])", item):
                self.coeff *= float(item)
        if side == "rhs":
            self.coeff *= -1


class Polynomial:

    terms = []
    degree = 0

    def __init__(self, expression):
        self.terms = self.parsePoly(expression)
        if int(self.degree) > 2:
            print("Polynomial degree = " + str(self.degree))
            print("The polynomial degree is strictly greater than 2, I can't solve.")
            exit(0)

    def parsePoly(self, poly):
        terms_lhs = []
        terms_rhs = []
        final = []
        regex = "([+-]?\s?[0-9]*\.?[0-9]*\s\*\s[xX]\^\d)"

        lhs = poly.split("=")[0]
        rhs = poly.split("=")[1]
        lhs = re.findall(regex, lhs)
        rhs = re.findall(regex, rhs)
        for exp in lhs:
            terms_lhs.append(Term(exp, "lhs"))
        for exp in rhs:
            terms_rhs.append(Term(exp, "rhs"))
        for left in terms_lhs:
            if int(left.power) > self.degree:
                self.degree = int(left.power)
        for right in terms_rhs:
            if int(right.power) > self.degree:
                self.degree = int(right.power)
        final.append(Term("+ 0 * X^0", "lhs"))
        final.append(Term("+ 0 * X^1", "lhs"))
        final.append(Term("+ 0 * X^2", "lhs"))
        for f in final:
            for left in terms_lhs:
                if f.power == left.power:
                    f.coeff += left.coeff
        for f in final:
            for right in terms_rhs:
                if f.power == right.power:
                    f.coeff += right.coeff
        return final


def to_whole(float):
    if float.is_integer():
        return int(float)
    return float


def print_sign(coeff):
    if coeff < 0:
        print("- " + str(to_whole(coeff * -1)), end="")
    else:
        print("+ " + str(to_whole(coeff)), end="")


def print_reduced(poly):
    print("Reduced form: ", end="")
    for item in poly.terms:
        print_sign(item.coeff)
        print(" * X^" + str(item.power), end=" ")
    print("= 0")


def solve_polynomial(poly):
    a = 1.0
    b = 1.0
    c = 1.0
    degree = 0

    for term in poly.terms:
        if int(term.power) == 0:
            c = term.coeff
        elif int(term.power) == 1:
            b = term.coeff
        elif int(term.power) == 2:
            a = term.coeff
    print("Polynomial degree = " + str(poly.degree))
    d = (b**2) - (4*a*c)
    if d == 0.0:
        print("Discriminant is zero. One real solution:")
        print(str(round((-b+d**(1/2))/(2*a), 6)))
    elif d > 0.0:
        print("Discriminant is strictly positive. Two real solutions:")
        print(str(round((-b-d**(1/2))/(2*a), 6)))
        print(str(round((-b+d**(1/2))/(2*a), 6)))
    elif d < 0.0:
        print("There are no real solutions:")
        exit(0)
    if poly.degree == 1:
        print("The solution is:")
        print(str(round(-(c/b), 6)))
    elif poly.degree == 0:
        sol = True
        for term in poly.terms:
            if term.coeff != 0.0:
                sol = False
                break
        if (sol):
            print("All real numbers are a solution.")
        else:
            print("There are no solutions.")


# Entry point for running with command
if len(argv) <= 1:
    print("No arguments...")
elif len(argv) > 2:
    print("Too many arguments...")
else:
    poly = Polynomial(argv[1])
    print_reduced(poly)
    solve_polynomial(poly)


# Entry point for example.py
def run_example(example):
    poly = Polynomial(example)
    print_reduced(poly)
    solve_polynomial(poly)