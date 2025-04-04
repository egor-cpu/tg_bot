import math
import sys




def fibonacci_method(func, a, b, tol):
    calls = 0

    fib = [sp.Rational(1), sp.Rational(1)] 
    while fib[-1] < (b - a) / tol:
        fib.append(fib[-1] + fib[-2])

    calls = 2

    step = 0
    lamda = sp.simplify( a + fib[-step-3] * (b - a) / fib[-step-1] )
    mu = sp.simplify( a + fib[-step-2] * (b - a) / fib[-step-1] )

    f_lamda = sp.simplify(func(lamda))
    f_mu = sp.simplify(func(mu))

    n = -int(sp.log(abs(f_lamda - f_mu), 10)) + 1
    print(f"\t\t\\item Вычисляем $\\lambda = {sp.latex(a)} + \\frac{{{fib[-step-3]}}}{{{fib[-step-1]}}}({sp.latex(b)} - {sp.latex(a)}) = {sp.latex(lamda)}$, $\\mu = {sp.latex(a)} + \\frac{{{fib[-step-2]}}}{{{fib[-step-1]}}}({sp.latex(b)} - {sp.latex(a)}) = {sp.latex(mu)}$")
    print(f"\t\t\\item Вычисляем $f(\\lambda) = f({sp.latex(lamda)}) = {sp.latex(f_lamda)}\\approx {float(f_lamda):.{n}f}$")
    print(f"\t\t\\item Вычисляем $f(\\mu) = f({sp.latex(mu)}) = {sp.latex(f_mu)}\\approx {float(f_mu):.{n}f}$")

    while (b - a) > tol:
        print(f"\t\t\\item $|b - a| = {sp.latex(b - a)} > {sp.latex(tol)}$")

        if f_lamda <= f_mu:
            a, b = a, mu
            mu = lamda
            f_mu = f_lamda

            lamda = sp.simplify( a + fib[-step-3] * (b - a) / fib[-step-1] )
            f_lamda = sp.simplify(func(lamda))
            n = -int(sp.ceiling(sp.log(abs(f_lamda - f_mu), 10)) )+ 1
            print(f"\t\t\\item Так как $f(\\mu) \\geq f(\\lambda)$, обновляем $b = {sp.latex(mu)}, f(\\mu) = f(\\lambda) \\approx {float(f_mu):.{n}f}$")
            print(f"\t\t\\item Вычисляем $\\lambda = {sp.latex(a)} + \\frac{{{fib[-step-3]}}}{{{fib[-step-1]}}}({sp.latex(b)} - {sp.latex(a)})  = {sp.latex(lamda)}$")
            print(f"\t\t\\item Вычисляем $f(\\lambda) = f({sp.latex(lamda)}) = {sp.latex(f_lamda)}\\approx {float(f_lamda):.{n}f}$")

        else:
            a, b = lamda, b
            lamda = mu
            f_lamda = f_mu

            mu = sp.simplify( a + fib[-step-2] * (b - a) / fib[-step-1] )
            f_mu = sp.simplify(func(mu))
            n = -int(sp.ceiling(sp.log(abs(f_lamda - f_mu), 10))) + 1
            print(f"\t\t\\item Так как $f(\\mu) < f(\\lambda)$, обновляем $a = {sp.latex(lamda)}, f(\\lambda) = f(\\mu) \\approx {float(f_lamda):.{n}f}$")
            print(f"\t\t\\item Вычисляем $\\mu = {sp.latex(a)} + \\frac{{{fib[-step-2]}}}{{{fib[-step-1]}}}({sp.latex(b)} - {sp.latex(a)}) = {sp.latex(mu)}$")
            print(f"\t\t\\item Вычисляем $f(\\mu) = f({sp.latex(mu)}) = {sp.latex(f_mu)}\\approx {float(f_mu):.{n}f}$")

        step += 1
        calls += 1
    print(f"\t\\item $|b - a| = |{sp.latex(b - a)}| < {sp.latex(tol)}$")

    return a, b, calls



def bisection_method(func, a, b, tol):
    calls = 0
    while (b - a) > tol:
        print(f"\t\\item $|b - a| = {sp.latex(b - a)} > {sp.latex(tol)}$")
        c = sp.simplify((a + b) / 2)
        eps = sp.simplify(tol / 1000)
        calls += 2
        c_minus = c - eps
        c_plus = c + eps
        f_minus = sp.simplify(func(c_minus))
        f_plus = sp.simplify(func(c_plus))
        n = -int(sp.ceiling(sp.log(abs(f_plus - f_minus), 10))) + 1
        if calls <= 2:
            print(f"\t\t\\item $\\epsilon = \\frac{{ {sp.latex(tol)} }}{{1000}} = {sp.latex(eps)}$")
        print(f"\t\t\\item $c = \\frac{{{sp.latex(a)} + {sp.latex(b)}}}{{2}} = {sp.latex(c)}$")
        print(f"\t\t\\item Вычисляем $f(c - \\epsilon) = f({sp.latex(c_minus)}) = {sp.latex(f_minus)} \\approx {float(f_minus):.{n}f}$")
        print(f"\t\t\\item Вычисляем $f(c + \\epsilon) = f({sp.latex(c_plus)}) = {sp.latex(f_plus)} \\approx {float(f_plus):.{n}f}$")
        if f_minus < f_plus:
            print(f"\t\t\\item Так как $f(c - \\epsilon) < f(c + \\epsilon)$, обновляем $b = {sp.latex(c)}$")
            b = c
        else:
            print(f"\t\t\\item Так как $f(c - \\epsilon) \\geq f(c + \\epsilon)$, обновляем $a = {sp.latex(c)}$")
            a = c

    print(f"\t\\item $|b - a| = |{sp.latex(b - a)}| < {sp.latex(tol)}$")
    return a, b, calls

def theoretical_evaluations_bisection(a, b, tol):
    N = 2 * sp.log((b - a) / tol, 2)
    print("$$N =  2 \\log_2\\left(\\frac{b - a}{\\text{tol}}\\right) =", end = "")
    print(f" 2 \\log_2\\left(\\frac{{{sp.latex(b)} - {sp.latex(a)}}}{{{sp.latex(tol)}}} \\right) = 2\\log_2\\left( {sp.latex((b - a) / tol)}\\right) \\approx {float(N):.1f} $$")
    return  N

def theoretical_evaluations_fibonacci(a, b, tol):
    phi = (1 + math.sqrt(5)) / 2
    N = math.log((b - a) / tol) / math.log(phi) + 2

    print("$$N = \\log_\\phi\\left(\\frac{b - a}{\\text{tol}}\\right)  + 2= ", end = "")
    print(f"\\log_\\phi\\left(\\frac{{{sp.latex(b)} - {sp.latex(a)}}}{{{sp.latex(tol)}}} \\right) + 2  = {float(N):.2f}$$")

    return N

func =  lambda x: sp.exp(x) - x**3/3 + 2 * x
a, b = sp.Rational(-2), sp.Rational(-1)
tolerances = [sp.Rational(1, 10), sp.Rational(1, 100), sp.Rational(1, 1000)]

with RedirectPrint('report/output.tex'):
    print(f"\\section{{Метод половинного деления}}")
    print(f"\t\\item Функция: $f(x) = e^x - \\frac{{x^3}}{{3}} + 2x$")
    print(f"\t\\item Начальные границы интервала: $a = {a}, b = {b}$")
    for tol in tolerances:
        print(f"\\subsection{{Точность: ${sp.latex(tol)}$}}")
        a_bis, b_bis, calls_bis = bisection_method(func, a, b, tol)
        theoretical = theoretical_evaluations_bisection(a, b, tol)
        n = -int(sp.ceiling(sp.log(tol, 10))) + 1
        print(f"Метод половинного деления:: $[{sp.latex(a_bis)}, {sp.latex(b_bis)}] \\approx [{float(a_bis):.{n}f}, {float(b_bis):.{n}f}]$, вызовы функции = ${calls_bis}$")

    print("\\newpage")
    print(f"\\section{{Метод Фибоначчи}}")
    print("\\begin{itemize}")
    print(f"\t\\item Функция: $f(x) = e^x - \\frac{{x^3}}{{3}} + 2x$")
    print(f"\t\\item Начальные границы интервала: $a = {a}, b = {b}$")
    print("\\end{itemize}")
    for tol in tolerances:
        print(f"\\subsection{{Точность: ${sp.latex(tol)}$}}")
        a_fib, b_fib, calls_fib = fibonacci_method(func, a, b, tol)
        theoretical = theoretical_evaluations_fibonacci(a, b, tol)
        n = -int(sp.ceiling(sp.log(tol, 10))) + 1
        print(f"Метод Фибоначчи:: $[{sp.latex(a_fib)}, {sp.latex(b_fib)}] \\approx [{float(a_fib):.{n}f}, {float(b_fib):.{n}f}]$, вызовы функции = ${calls_fib}$")


with open('report/output.tex', 'r', encoding='utf-8') as file:
    content = file.read()
content = content.replace('+ -', '-')
content = content.replace('- -', '+')
content = content.replace('--', '+')
with open('report/output.tex', 'w', encoding='utf-8') as file:
    file.write(content)