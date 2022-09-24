from math import log10, pi
import astropy.units as u
from astropy.constants import c, k_B
from astropy.units import Quantity


def to_db(x, reference: Quantity | int | float = 1 * u.W) -> Quantity[u.dB]:
    """Converts a quantity to dB against a reference value.

    Arguments:
        x -- quantity to convert to dB

    Keyword Arguments:
        reference -- reference value with units (default: {1*u.W})

    Returns:
        quantity in dB
    """
    return 10 * log10(x) * u.dB


def wavelength_to_frequency(λ: Quantity[u.m]) -> Quantity[u.Hz]:
    """Frequency of an electromagnetic wave given the wavelength.

    Arguments:
        λ -- wavelength

    Returns:
        frequency
    """
    return (c / λ).decompose()


def frequency_to_wavelength(f: Quantity[u.Hz]) -> Quantity[u.m]:
    """Wavelength of an electromagnetic wave given the frequency.

    Arguments:
        f -- frequency

    Returns:
        wavelength
    """
    return (c / f).decompose()


def L_s(d: Quantity[u.m], λ: Quantity[u.m]) -> Quantity[u.dB]:
    """Free space loss due to the transmitted power spreading over a wider area.

    Arguments:
        d -- distance
        λ -- wavelength

    Returns:
        loss in dB
    """
    return 20 * log10(4 * pi * d / λ) * u.dB


def N_0(T_s: Quantity[u.K]) -> Quantity[u.W / u.Hz]:
    """Noise spectral density (N_0) from the system noise temperature.

    Arguments:
        T_s -- system noise temperature

    Returns:
        noise spectral density
    """
    return (T_s * k_B).to(u.W / u.Hz)


def total_white_noise_power(T_s: Quantity[u.K], B: Quantity[u.Hz]) -> Quantity[u.W]:
    """Total white noise spectral power over a bandwidth.

    Arguments:
        T_s -- system noise temperature
        B -- bandwidth

    Returns:
        total spectral power
    """
    return (T_s * k_B * B).to(u.W)


def T_sys(T_ant: Quantity[u.K], L: Quantity[u.dimensionless_unscaled], F: Quantity[u.dimensionless_unscaled],
          T_0: Quantity[u.dimensionless_unscaled] = 290 * u.K) -> Quantity[u.K]:
    """Recieving ground station system noise temperature.

    Arguments:
        T_ant -- antenna noise temperature
        L -- cable loss factor, L <= 1
        F -- amplifier noise figure, F >= 1

    Keyword Arguments:
        T_0 -- reference noise temperature (default: {290*u.K})

    Returns:
        system noise temperature
    """
    return T_ant + T_0 * (1 - L) / L + T_0 * (F - 1)


def EIRP(G_ant: Quantity[u.dimensionless_unscaled], L_cable: Quantity[u.dimensionless_unscaled],
         P_tx: Quantity[u.W]) -> Quantity[u.W]:
    """Transmitting ground station equivalent isotropic radiated power.

    Arguments:
        G_ant -- antenna gain
        L_cable -- cable attenuation
        P_tx -- transmission amplifier power

    Returns:
        _description_
    """
    return G_ant * L_cable * P_tx
