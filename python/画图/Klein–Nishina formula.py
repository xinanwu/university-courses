import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import e, h, hbar, alpha, c, m_e
DPI = 100

# A bunch of constants factored into a single variable.
f = (hbar * alpha / m_e / c)**2 / 2
# A grid of scattering angles in rad.
theta = np.arange(0, 2*np.pi, 0.01)
n = len(theta)


def plot_diff_xsec(E):
    """Plot the differential cross section for incoming photon energy, E."""

    # Incoming photon frequency (s-1) and wavelength (m).
    nu = E * 1.e6 * e / h
    lam = c / nu

    # Scattered photon wavelength (m).
    lamp = lam + h / m_e / c * (1 - np.cos(theta))
    P = lam / lamp
    # Differential cross section given by the Klein-Nishina formula.
    dsigma_dOmega = f * P**2 * (P + 1/P - np.sin(theta)**2)

    # Plot the polar and Cartesian plots.
    ax1.plot(theta, dsigma_dOmega, label=str(E) + r' MeV')
    # Because of the symmetry, we only really need angles 0 -> 180 deg.
    ax2.plot(np.degrees(theta[:n//2]), dsigma_dOmega[:n//2],
             label=str(E) + r' MeV')

# A Matplotlib figure with a polar Axes above a Cartesian one.
fig = plt.figure(figsize=(800/DPI, 1000/DPI))
ax1 = fig.add_subplot(211, projection='polar')
ax2 = fig.add_subplot(212)

# Our grid of photon energies (in MeV).
Egrid = 0.001, 0.01, 0.1, 1, 10
for E in Egrid:
    plot_diff_xsec(E)
ax2.set_xlabel(r'$\theta\;/\mathrm{deg}$')
ax2.set_ylabel(r'$\mathrm{d}\sigma/\mathrm{d}\Omega\;/\mathrm{m^2\,sr^{-1}}$')
# Set the Cartesian x-axis ticks to sensible values (in degrees).
ax2.set_xticks([0, 45, 90, 135, 180])

plt.legend()
plt.show()