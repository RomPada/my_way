import numpy as np
import matplotlib.pyplot as plt

# Визначення функції для інтегрування
def f(x):
    return x**2

a = 0
b = 2

# Метод Монте-Карло з використанням середнього значення
def monte_carlo_integral_mean(func, a, b, n_samples=200_000, seed=42):
    rng = np.random.default_rng(seed)
    x = rng.uniform(a, b, size=n_samples)
    y = func(x)
    estimate = (b - a) * np.mean(y) 
    return estimate

# Обчислення інтегралу за допомогою методу Монте-Карло (середнє значення)
mc_est = monte_carlo_integral_mean(f, a, b, n_samples=200_000, seed=42)

# Аналітичне значення інтегралу
analytic = (b**3 - a**3) / 3

# Імпорт SciPy та обчислення інтегралу за допомогою quad
try:
    import scipy.integrate as spi
    quad_res, quad_err = spi.quad(f, a, b)
except Exception as e:
    quad_res, quad_err = None, None
    print("SciPy недоступний або помилка імпорту:", e)

# Обчислення похибок
abs_err = abs(mc_est - analytic)
rel_err = abs_err / abs(analytic)

print("=== Результати інтегрування ===")
print(f"Монте-Карло (mean): {mc_est:.10f}")
print(f"Аналітично:         {analytic:.10f}  (8/3)")
print(f"Абс. похибка:       {abs_err:.10f}")
print(f"Відн. похибка:      {rel_err:.6%}")

# Порівняння з результатом SciPy quad
if quad_res is not None:
    print("\n=== SciPy quad ===")
    print(f"quad:               {quad_res:.10f}")
    print(f"оцінка помилки:     {quad_err:.3e}")
    print(f"|MC - quad|:        {abs(mc_est - quad_res):.10f}")

# Візуалізація результатів інтегрування
x_plot = np.linspace(-0.5, 2.5, 400)
y_plot = f(x_plot)

fig, ax = plt.subplots()
ax.plot(x_plot, y_plot, "r", linewidth=2)

ix = np.linspace(a, b, 200)
ax.fill_between(ix, f(ix), color="gray", alpha=0.3)

ax.axvline(x=a, color="gray", linestyle="--")
ax.axvline(x=b, color="gray", linestyle="--")
ax.set_xlim([x_plot[0], x_plot[-1]])
ax.set_ylim([0, max(y_plot) + 0.1])
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.set_title(f"Графік інтегрування f(x)=x^2 від {a} до {b}")
ax.grid(True)
plt.show()
