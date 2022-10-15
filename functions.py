from math import cos, degrees, log10, pi, radians, sin, sqrt, asin, tan


# constants
c = 299792458           # m/s
k_B = 1.380649e-23      # J/K

# planets
earth_gm = 398600.436   # km^3 s^-2
earth_R = 6371          # km
earth_d = 149598023000  # m
moon_gm = 4902.800      # km^3 s^-2
moon_R = 1737.4         # km
moon_d = 384399000      # km
mercury_gm = 22032.09   # km^3 s^-2
mercury_R = 2439.7      # km
mercury_d = 46001195642 # m
mars_gm = 42828.37362   # km^3 s^-2
mars_R = 3389.5         # km
mars_d = 227939366000   # m
saturn_gm = 37931206.23 # km^3 s^-2
saturn_R = 58232        # km
saturn_d = 4.335e11     # m


def db(x, inverse=False):
    ans = 10 * log10(x)
    return -ans if inverse else ans


def freq_to_wavelength(f):
    return c / f


def g_ant_db(wavelength, d, eta):
    return db(pi ** 2 * d ** 2 / wavelength ** 2 * eta)


def s_leo(h_km, elev):
    if elev == 0:
        return sqrt((earth_R + h_km) ** 2 - earth_R ** 2) * 1000
    if elev == 90:
        return h_km * 1000
    theta = radians(elev)
    alpha = asin(earth_R * sin(pi/2 + theta) / (earth_R + h_km))
    beta = pi/2 - theta - alpha
    s = (earth_R + h_km) * sin(beta) / sin(pi/2 + theta)
    return s * 1000


def l_s_db(h_km, elev, wavelength, planet, elongation):
    if planet == 'Earth':
        s = s_leo(h_km, elev)
        return db((wavelength / (4 * pi * s)) ** 2)
    if planet == 'Moon':
        s = moon_d
        return db((wavelength / (4 * pi * s)) ** 2)
    if planet == 'Mercury':
        ds = mercury_d
    if planet == 'Mars':
        ds = mars_d
    if planet == 'Saturn':
        ds = saturn_d
    s = sqrt(earth_d ** 2 + ds ** 2 - 2 * earth_d * ds * cos(radians(elongation)))
    return db((wavelength / (4 * pi * s)) ** 2)


def l_pr_db(f_ghz, d, e_tt, e_t_alpha_1_2_r):
    alpha_1_2_t = 21 / (f_ghz * d)
    return -12 * ((e_tt/alpha_1_2_t) ** 2 + e_t_alpha_1_2_r ** 2)


def one_over_r_db(swath_width, pixel_size, bits_per_px, h_km, planet, d_c_percent, t_dl):
    if planet == 'Earth':
        gm, r = earth_gm, earth_R
    if planet == 'Moon':
        gm, r = moon_gm, moon_R
    if planet == 'Mercury':
        gm, r = mercury_gm, mercury_R
    if planet == 'Mars':
        gm, r = mars_gm, mars_R
    if planet == 'Saturn':
        gm, r = saturn_gm, saturn_R
    h = h_km * 1000
    v = sqrt(gm / (h_km + r)) * 1000
    swath_width_m = h * tan(radians(swath_width))
    pixel_size_m = h * tan(radians(pixel_size / 60))
    r_g = bits_per_px * swath_width_m * v / pixel_size_m ** 2
    r = r_g * (d_c_percent / 100) / (t_dl / 24)
    """px_per_row = swath_width / (pixel_size / 60)
    bits_per_row = px_per_row * bits_per_px
    row_height_deg = pixel_size / 60
    sc_time_per_row = h * tan(radians(row_height_deg)) / v
    r_g_2 = bits_per_row / sc_time_per_row
    print(f'r_g with spreadsheet method =  {r_g_2}')
    print(f'r_g with formula from slides = {r_g}')
    print('ratio =', r_g / r_g_2)"""
    return db(r, inverse=True)


def one_over_k_b_db():
    return db(k_B, inverse=True)


def loss_factor_db(l):
    return db(l)


def p_db(p):
    return db(p)


def one_over_t_s_db(t_s):
    return db(t_s, inverse=True)