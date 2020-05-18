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
        for item in final:
            if int(item.power) > self.degree:
                self.degree = int(item.power)
        for item in final:
            if float(item.coeff) == 0.0:
                final.remove(item)
        for item in terms_lhs:
            if int(item.power) > self.degree:
                self.degree = int(item.power)
        for item in terms_rhs:
            if int(item.power) > self.degree:
                self.degree = int(item.power)
        if self.degree > 2:
            print("Degree larger than 2, unable to solve.")
            exit(0)
        else:
            self.degree = 0
        for item in final:
            if int(item.power) > self.degree:
                self.degree = int(item.power)
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
    poly.terms.sort(key=lambda x: x.power)
    for item in poly.terms:
        if int(item.power) == 0:
            print(str(to_whole(item.coeff)) + " * X^0", end=" ")
        else:
            print_sign(item.coeff)
            print(" * X^" + str(item.power), end=" ")
    print("= 0")


def solve_polynomial(poly):
    a = 0.0
    b = 0.0
    c = 0.0

    degree = 0

    for term in poly.terms:
        if int(term.power) == 0:
            c = float(term.coeff)
        elif int(term.power) == 1:
            b = float(term.coeff)
        elif int(term.power) == 2:
            a = float(term.coeff)
    print("Polynomial degree : " + str(poly.degree))
    if poly.degree == 0:
        if int(a) == 0:
            print("All real numbers are a solution.")
        else:
            print("There is no solution.")
    if poly.degree == 1:
        if len(poly.terms) > 1:
            b = float(poly.terms[0].coeff)
            a = float(poly.terms[1].coeff)
        else:
            b = 0
            a = float(poly.terms[0].coeff)
        print("The solution is:")
        print(str(round((-b/a), 6)))
    if poly.degree == 2:
        if len(poly.terms) > 2:
            c = float(poly.terms[0].coeff)
            b = float(poly.terms[1].coeff)
            a = float(poly.terms[2].coeff)
        elif len(poly.terms) > 1:
            c = 0
            b = float(poly.terms[0].coeff)
            a = float(poly.terms[1].coeff)
        else:
            c = 0
            b = 0
            a = float(poly.terms[0].coeff)
        d = b**2-(4*a*c)
        if d == 0.0:
            print("Discriminant is zero. One real solution:")
            print(str(round((-b/(2*a)), 6)))
        elif d > 0.0:
            print("Discriminant is strictly positive. Two real solutions:")
            print(str(round(((-b - (d ** 0.5)) / (2 * a)), 6)))
            print(str(round(((-b + (d ** 0.5)) / (2 * a)), 6)))
        elif d < 0.0:
            print("There are no real solutions, complex solution is:")
            print(str((-b - (d ** 0.5)) / (2 * a)))
            exit(0)
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