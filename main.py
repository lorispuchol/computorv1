import sys
from collections import defaultdict

def parse_terms(s):
    s = s.replace('-', '+-')
    terms = s.split('+')
    return [t.strip() for t in terms if t.strip()]

def parse_term(term_str):
    parts = term_str.split('*')
    if len(parts) != 2:
        raise ValueError(f"Invalid term: {term_str}")
    coeff_str, x_part = parts[0].strip(), parts[1].strip()
    coeff = float(coeff_str)
    if not x_part.startswith('X^'):
        raise ValueError(f"Invalid X part: {x_part}")
    exponent = int(x_part[2:])
    return coeff, exponent

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py \"equation\"")
        return

    equation = sys.argv[1]
    try:
        left_part, right_part = equation.split('=')
    except ValueError:
        print("Invalid equation format")
        return

    left_terms = parse_terms(left_part)
    right_terms = parse_terms(right_part)

    coefficients = defaultdict(float)
    try:
        for term in left_terms:
            coeff, exp = parse_term(term)
            coefficients[exp] += coeff
        for term in right_terms:
            coeff, exp = parse_term(term)
            coefficients[exp] -= coeff
    except ValueError as e:
        print(f"Error parsing terms: {e}")
        return

    sorted_exponents = sorted(coefficients.keys())
    terms_list = []
    for exp in sorted_exponents:
        coeff = coefficients[exp]
        if coeff < 0:
            sign = '-'
            abs_coeff = -coeff
        else:
            sign = '+'
            abs_coeff = coeff
        term_str = f"{sign}{abs_coeff:.6g} * X^{exp}"
        terms_list.append(term_str)

    if not terms_list:
        reduced_str = "0 * X^0 = 0"
    else:
        reduced_str = ' '.join(terms_list)
        if reduced_str.startswith('+'):
            reduced_str = reduced_str[1:].lstrip()
        reduced_str += " = 0"

    print(f"Reduced form: {reduced_str}")

    all_zero = all(v == 0 for v in coefficients.values())
    if all_zero:
        degree = 0
    else:
        non_zero_exponents = [exp for exp, coeff in coefficients.items() if coeff != 0]
        degree = max(non_zero_exponents) if non_zero_exponents else 0

    print(f"Polynomial degree: {degree}")

    if degree > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        return

    if degree == 0:
        if all_zero:
            print("Any real number is a solution.")
        else:
            print("No solution.")
        return

    if degree == 1:
        a = coefficients.get(1, 0.0)
        b = coefficients.get(0, 0.0)
        if a == 0:
            print("No solution.")
            return
        solution = -b / a
        print("The solution is:")
        print(f"{solution:.6g}")
        return

    if degree == 2:
        a = coefficients.get(2, 0.0)
        b = coefficients.get(1, 0.0)
        c = coefficients.get(0, 0.0)
        discriminant = b**2 - 4 * a * c
        epsilon = 1e-10

        if discriminant > 0:
            sqrt_d = discriminant ** 0.5
            x1 = (-b + sqrt_d) / (2 * a)
            x2 = (-b - sqrt_d) / (2 * a)
            print("Discriminant is strictly positive, the two solutions are:")
            print(f"{x1:.6g}")
            print(f"{x2:.6g}")
        elif discriminant == 0:
            x = -b / (2 * a)
            print("Discriminant is zero, the solution is:")
            print(f"{x:.6g}")
        else:
            sqrt_d_abs = (-discriminant) ** 0.5
            real_part = -b / (2 * a)
            imaginary_part = sqrt_d_abs / (2 * a)
            real_part_str = f"{real_part:.6g}" if abs(real_part) >= epsilon else '0'
            imaginary_str = f"{imaginary_part:.6g}" if abs(imaginary_part) >= epsilon else '0'
            if real_part_str == '0':
                sol1 = f"{imaginary_str}i"
                sol2 = f"-{imaginary_str}i"
            else:
                sol1 = f"{real_part_str} + {imaginary_str}i"
                sol2 = f"{real_part_str} - {imaginary_str}i"
            print("Discriminant is strictly negative, the two complex solutions are:")
            print(sol1)
            print(sol2)

if __name__ == "__main__":
    main()