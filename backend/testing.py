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
pd.options.mode.chained_assignment = None  # default='warn'

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
        selected_planets.append([v.split(' ')[0],ra.hours,dec.degrees])

    with load.open(hipparcos.URL) as f:
        df = hipparcos.load_dataframe(f)

    star_pass = df[df.magnitude <= 4]
    # bright_stars = Star.from_dataframe(star_pass)
    # astrometric_stars = earth.at(t).observe(bright_stars)
    # ra, dec, distance = astrometric_stars.radec()
    Simbad.add_votable_fields('typed_id')
    # sr = Simbad.query_objectids(f"HIP32349")
    k = []
    for i, v in enumerate(star_pass.index.tolist()):
        t = 1
        sr = Simbad.query_objectids(f"HIP{v}")
        for y in sr['ID']:
            if 'NAME' in y:
                k.append(y.split(' ')[1:][0])
                t = 0
                break
        if t == 1:
            k.append(' ')
    # print(len(star_pass), len(k))
    star_pass['Name'] = pd.Series(k).values
    # star_pass.set_index('Name', inplace=True)
    # print(star_pass)

    # star_pass.to_json('stars.json')
    selected_planets = pd.DataFrame.from_records(selected_planets, columns = ['name','ra','dec'], index = 'name')
    selected_planets.to_json('planets.json')

    final = pd.concat([star_pass.dec_degrees, star_pass.ra_degrees, star_pass.Name, star_pass.magnitude], axis = 1)
    final.to_json('stars.json')

    return 0

def normalise_planets(normal):
    planet_pass = pd.read_json('planets.json')
    planetra = planet_pass.ra
    planetdec = planet_pass.dec
    planet_pass['Name'] = planet_pass.index
    planetname = planet_pass.Name

    vec = ICRF(normal).radec()
    # dec_0 = np.arccos(normal[2]/np.sqrt(np.sum(np.array(normal)**2)))
    # ra_0 = np.sign(normal[1])*np.arccos(normal[0]/np.sqrt(normal[0]**2+normal[1]**2))
    dec_0 = vec[1]._degrees
    ra_0 = vec[0]._degrees

    denom = np.cos(dec_0*np.pi/180)*np.cos(planetdec*np.pi/180)*np.cos(planetra*np.pi/180 - ra_0*np.pi/180)\
         + np.sin(planetdec*np.pi/180)*np.sin(dec_0*np.pi/180)
    X = np.cos(planetdec*np.pi/180)*np.sin(planetra*np.pi/180 - ra_0*np.pi/180)/denom
    Y = (np.sin(dec_0*np.pi/180)*np.cos(planetdec*np.pi/180)*np.cos(planetra*np.pi/180 - ra_0*np.pi/180)\
        - np.cos(dec_0*np.pi/180)*np.sin(planetdec*np.pi/180))/denom
    final = pd.concat([X,Y, planetname], axis = 1)
    final = final[(abs(final[0]) < 1.5) & (abs(final[1]) < 1.5)]
    # plt.scatter(final[0],final[1])
    # plt.show()
    return final.to_json()

star_pass = pd.read_json('stars.json')
def normalise_stars(normal):
    # normal = np.array(normal)
    # normal = normal + min(normal)
    # normal /= sum(normal)
    starra = star_pass.ra_degrees
    stardec = star_pass.dec_degrees
    starname = star_pass.Name
    starmag = star_pass.magnitude

    # vec = ICRF(normal).radec()
    # print(normal)
    # r = np.arctan(normal[1]/normal[0])
    # d = np.arctan(normal[2]/np.sqrt(np.sum(np.array(normal)**2)))
    # print(vec, [r,d])
    # dec_0 = np.arccos(normal[2]/np.sqrt(np.sum(np.array(normal)**2)))
    # ra_0 = np.sign(normal[1])*np.arccos(normal[0]/np.sqrt(normal[0]**2+normal[1]**2))
    # dec_0 = vec[1]._degrees
    # ra_0 = vec[0]._degrees
    dec_0 = normal[0]
    ra_0 = normal[1]

    denom = np.cos(dec_0*np.pi/180)*np.cos(stardec*np.pi/180)*np.cos(starra*np.pi/180 - ra_0*np.pi/180)\
         + np.sin(stardec*np.pi/180)*np.sin(dec_0*np.pi/180)
    X = np.cos(stardec*np.pi/180)*np.sin(starra*np.pi/180 - ra_0*np.pi/180)/denom
    Y = (np.sin(dec_0*np.pi/180)*np.cos(stardec*np.pi/180)*np.cos(starra*np.pi/180 - ra_0*np.pi/180)\
        - np.cos(dec_0*np.pi/180)*np.sin(stardec*np.pi/180))/denom
    final = pd.concat([X,Y, starname, starmag], axis = 1)
    final = final[(abs(final[0]) < 1) & (abs(final[1]) < 1)]
    # plt.scatter(final[0],final[1])
    # plt.show()
    return final
    return final.to_json()


fig,ax = plt.subplots()
# ax.set_autoscale_on(False)
plt.axis('equal')

# print(star_pass.loc[24436])
normal = np.array([-8.201639, 78.634464])
v = normalise_stars(normal)
# print(normal)
# normal /= sum(normal)
# print(normal) 
# exit()
ax.set_facecolor('black')
ax.scatter(v[0],v[1], c = 'white', s=max(v['magnitude']*5)-v['magnitude']*5)
for i, txt in enumerate(v['Name']):
    ax.annotate(txt, (v[0].iloc[i],v[1].iloc[i]), c = 'white', size = max(v['magnitude']*5)-v['magnitude'].iloc[i]*5 - 5)
ax.set_ylim([-1,1])
ax.set_xlim([-1,1])
e = v.loc[[24436, 27989, 25336]]
# ax.scatter(e[0], e[1], c = 'red', s = 0.5)
# ax.set_ylim([-1,1])
# ax.set_xlim([-1,1])

ax_slider = plt.axes((0.20, 0.01, 0.65, 0.03), facecolor='yellow')
slider = Slider(ax_slider, 'normalx', valmin=-180, valmax=180, valinit = normal[0])
ax_slider1 = plt.axes((0.20, 0.04, 0.65, 0.03), facecolor='yellow')
slider1 = Slider(ax_slider1, 'normaly', valmin=-180, valmax=180, valinit = normal[1])
# ax_slider2 = plt.axes((0.20, 0.07, 0.65, 0.03), facecolor='yellow')
# slider2 = Slider(ax_slider2, 'normalz', valmin=-1, valmax=1, valinit = normal[2])

def update(val):
    normal[0] = val
    ax.clear()
    v = normalise_stars(normal)
    ax.scatter(v[0],v[1], c = 'white', s=max(v['magnitude']*5)-v['magnitude']*5)
    ax.set_ylim([-1,1])
    ax.set_xlim([-1,1])
    fig.canvas.draw_idle()

def update1(val):
    normal[1] = val
    ax.clear()
    v = normalise_stars(normal)
    ax.scatter(v[0],v[1], c = 'white', s=max(v['magnitude']*5)-v['magnitude']*5)
    ax.set_ylim([-1,1])
    ax.set_xlim([-1,1])
    fig.canvas.draw_idle()  

# def update2(val):
#     normal[2] = val
#     ax.clear()
#     v = normalise_stars(normal)
#     ax.scatter(v[0],v[1], c = 'white', s=0.5)
#     fig.canvas.draw_idle()


slider.on_changed(update)
slider1.on_changed(update1)
# slider2.on_changed(update2)
# ax.set_ylim([-1,1])
# ax.set_xlim([-1,1])
plt.show()



# pxSize = 3.8e-6
# widthPx = 4656
# heightPx = 3520
# c_ra = 194.464
# c_dec = 71.217
# bin = 1
# fLen = 24e-3
# r = -268

# s_ra = star_pass.ra_degrees
# s_dec = star_pass.dec_degrees

# imageWidthRad = 2 * np.arctan((pxSize * bin * widthPx / 1000.0) / (2 * fLen))
# imageHeightRad = 2  * np.arctan((pxSize * bin * heightPx / 1000.0) / (2 * fLen))

# pixelsPerRadW = widthPx / imageWidthRad
# pixelsPerRadH = heightPx / imageHeightRad

# imageCenterX = widthPx / 2
# imageCenterY = heightPx / 2

# stdX = np.cos(s_dec) * np.sin(s_ra - c_ra) / (np.cos(c_dec) * np.cos(s_dec) * np.cos(s_ra - c_ra) + np.sin(c_dec) * np.sin(s_dec))
# stdY = (np.sin(c_dec) * np.cos(s_dec) * np.cos(s_ra - c_ra) - np.cos(c_dec) * np.sin(s_dec)) / (np.cos(c_dec) * np.cos(s_dec) * np.cos(s_ra - c_ra) + np.sin(c_dec) * np.sin(s_dec))

# starPixelX = pixelsPerRadW * stdX + imageCenterX
# starPixelY = pixelsPerRadH * stdY + imageCenterY
# starPixelX = widthPx - starPixelX

# # print(starPixelX,starPixelY)

# fig,ax = plt.subplots()
# plt.scatter(starPixelX, starPixelY, c = 'white', s=0.5)
# ax.set_facecolor('black')
# plt.show()