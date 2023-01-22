from skyfield.api import load, Star
from skyfield.positionlib import position_of_radec, ICRF
from skyfield.data import hipparcos
import pandas as pd
from astroquery.simbad import Simbad
import numpy as np
import matplotlib.pyplot as plt
import math
from datetime import datetime
from matplotlib.widgets import Slider

def update_data():
    ts = load.timescale()
    t = ts.now()

    planets = load('de421.bsp')
    earth = planets['earth']

    planet_names = ['MERCURY BARYCENTER', 'VENUS BARYCENTER', 'MARS BARYCENTER', 'JUPITER BARYCENTER',
    'SATURN BARYCENTER', 'URANUS BARYCENTER', 'NEPTUNE BARYCENTER', 'PLUTO BARYCENTER',
    'SUN', 'MOON']

    selected_planets = []
    for i, v in enumerate(planet_names):
        pl = planets[v]
        astrometric_pl = earth.at(t).observe(pl)
        ra, dec, distance = astrometric_pl.radec()
        selected_planets.append([v,ra.hours,dec.degrees])

    with load.open(hipparcos.URL) as f:
        df = hipparcos.load_dataframe(f)

    star_pass = df[df.magnitude <= 3]
    # bright_stars = Star.from_dataframe(star_pass)
    # astrometric_stars = earth.at(t).observe(bright_stars)
    # ra, dec, distance = astrometric_stars.radec()
    # Simbad.add_votable_fields('typed_id')
    # sr = Simbad.query_objectids(f"HIP32349")
    # k = []
    # for i, v in enumerate(star_pass.index.tolist()):
    #     sr = Simbad.query_objectids(f"HIP{v}")
    #     t = 0
    #     for p in sr['ID']:
    #         if '*' in p:
    #             k.append(" ".join(p.split()[1:]))
    #             t += 1
    #             break

    # star_pass.to_json('stars.json')
    selected_planets = pd.DataFrame.from_records(selected_planets, columns = ['name','ra','dec'], index = 'name')
    selected_planets.to_json('planets.json')


    # starra = star_pass.ra_degrees
    # stardec = star_pass.dec_degrees
    # # print(star_pass)
    # dec_0 = star_pass.loc[27989].dec_degrees
    # ra_0 = star_pass.loc[27989].ra_degrees
    # # dec_0 = np.arccos(normal[2]/np.sqrt(np.sum(np.array(normal)**2)))
    # # ra_0 = np.sign(normal[1])*np.arccos(normal[0]/np.sqrt(normal[0]**2+normal[1]**2))

    # denom = np.cos(dec_0)*np.cos(stardec*np.pi/180)*np.cos(starra*np.pi/180 - ra_0)\
    #      + np.sin(stardec*np.pi/180)*np.sin(dec_0)
    # X = np.cos(stardec*np.pi/180)*np.sin(starra*np.pi/180 - ra_0)/denom
    # Y = (np.sin(dec_0)*np.cos(stardec*np.pi/180)*np.cos(starra*np.pi/180 - ra_0)\
    #     - np.cos(dec_0)*np.sin(stardec*np.pi/180))/denom
    # final = pd.concat([X,Y], axis = 1)
    # final = final[(abs(final[0]) < 1) & (abs(final[1]) < 1)]

    final = pd.concat([star_pass.dec_degrees, star_pass.ra_degrees], axis = 1)
    final.to_json('stars.json')
    return 0

update_data()

def normalise_stars(normal):
    star_pass = pd.read_json('stars.json')
    starra = star_pass.ra_degrees
    stardec = star_pass.dec_degrees

    vec = ICRF(normal).radec()
    # dec_0 = np.arccos(normal[2]/np.sqrt(np.sum(np.array(normal)**2)))
    # ra_0 = np.sign(normal[1])*np.arccos(normal[0]/np.sqrt(normal[0]**2+normal[1]**2))
    dec_0 = vec[1]._degrees
    ra_0 = vec[0]._degrees

    denom = np.cos(dec_0*np.pi/180)*np.cos(stardec*np.pi/180)*np.cos(starra*np.pi/180 - ra_0*np.pi/180)\
         + np.sin(stardec*np.pi/180)*np.sin(dec_0*np.pi/180)
    X = np.cos(stardec*np.pi/180)*np.sin(starra*np.pi/180 - ra_0*np.pi/180)/denom
    Y = (np.sin(dec_0*np.pi/180)*np.cos(stardec*np.pi/180)*np.cos(starra*np.pi/180 - ra_0*np.pi/180)\
        - np.cos(dec_0*np.pi/180)*np.sin(stardec*np.pi/180))/denom
    final = pd.concat([X,Y], axis = 1)
    final = final[(abs(final[0]) < 1.5) & (abs(final[1]) < 1.5)]
    # plt.scatter(final[0],final[1])
    # plt.show()
    return final.to_json()

# fig,ax = plt.subplots()
# normal = [1,0.0,0.0]
# v = normalise_stars(normal)
# # print(v)
# ax.set_facecolor('black')
# ax.scatter(v[0],v[1], c = 'white', s=0.5)

# ax_slider = plt.axes((0.20, 0.01, 0.65, 0.03), facecolor='yellow')
# slider = Slider(ax_slider, 'normalx', valmin=-1, valmax=1, valinit = normal[0])
# ax_slider = plt.axes((0.20, 0.04, 0.65, 0.03), facecolor='yellow')
# slider1 = Slider(ax_slider, 'normaly', valmin=-1, valmax=1, valinit = normal[1])
# ax_slider = plt.axes((0.20, 0.07, 0.65, 0.03), facecolor='yellow')
# slider2 = Slider(ax_slider, 'normalz', valmin=-1, valmax=1, valinit = normal[2])

# def update(val):
#     normal[0] = val
#     ax.clear()
#     v = pd.read_json(normalise_stars(normal))
#     ax.scatter(v[0],v[1], c = 'white', s=0.5)
#     fig.canvas.draw_idle()

# def update1(val):
#     normal[1] = val
#     ax.clear()
#     v = pd.read_json(normalise_stars(normal))
#     ax.scatter(v[0],v[1], c = 'white', s=0.5)
#     fig.canvas.draw_idle()

# def update2(val):
#     normal[2] = val
#     ax.clear()
#     v = pd.read_json(normalise_stars(normal))
#     ax.scatter(v[0],v[1], c = 'white', s=0.5)
#     fig.canvas.draw_idle()

# slider.on_changed(update)
# slider1.on_changed(update1)
# slider2.on_changed(update2)

# plt.show()