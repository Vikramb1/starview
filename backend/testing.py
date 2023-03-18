from skyfield.api import load, Star, Angle
from skyfield.positionlib import position_of_radec, ICRF, Barycentric
from skyfield.data import hipparcos
import pandas as pd
from astroquery.simbad import Simbad
import numpy as np
import matplotlib.pyplot as plt
import math, json
from datetime import datetime
from matplotlib.widgets import Slider
pd.options.mode.chained_assignment = None  # default='warn'

def update_data():
    ts = load.timescale()
    t = ts.now()

    planets = load('de421.bsp')
    earth = planets['earth']

    planet_names = ['MERCURY BARYCENTER', 'VENUS BARYCENTER', 'MARS BARYCENTER', 'JUPITER BARYCENTER',
    'SATURN BARYCENTER', 'URANUS BARYCENTER', 'NEPTUNE BARYCENTER', 'MOON']

    selected_planets = []
    for i, v in enumerate(planet_names):
        pl = planets[v]
        astrometric_pl = earth.at(t).observe(pl)
        ra, dec, distance = astrometric_pl.radec()
        selected_planets.append([v.split(' ')[0][0] + v.split(' ')[0][1:].lower() ,ra.hours,dec.degrees])

    with load.open(hipparcos.URL) as f:
        df = hipparcos.load_dataframe(f)

    star_pass = df[df.magnitude <= 4]
    # bright_stars = Star.from_dataframe(star_pass)
    # astrometric_stars = earth.at(t).observe(bright_stars)
    # ra, dec, distance = astrometric_stars.radec()
    Simbad.add_votable_fields('typed_id')
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
            k.append(sr['ID'][0])
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

def normalise_planets(normal, planet_pass):
    normal /= np.sqrt(np.sum(np.array(normal)**2))
    planetra = np.radians(planet_pass.ra)
    planetdec = np.radians(planet_pass.dec)
    planet_pass['Name'] = planet_pass.index
    planetname = planet_pass.Name

    vec = ICRF(normal).radec()
    # dec_0 = np.arccos(normal[2]/np.sqrt(np.sum(np.array(normal)**2)))
    # ra_0 = np.sign(normal[1])*np.arccos(normal[0]/np.sqrt(normal[0]**2+normal[1]**2))
    dec_0 = np.radians(vec[1]._degrees)
    ra_0 = np.radians(vec[0]._degrees)

    denom = np.cos(dec_0)*np.cos(planetdec)*np.cos(planetra - ra_0)\
        + np.sin(planetdec)*np.sin(dec_0)
    X = np.cos(planetdec)*np.sin(planetra - ra_0)/denom
    Y = (np.sin(dec_0)*np.cos(planetdec)*np.cos(planetra - ra_0)\
        - np.cos(dec_0)*np.sin(planetdec))/denom
    final = pd.concat([X,Y, planetname], axis = 1)
    final = final[(abs(final[0]) < 1) & (abs(final[1]) < 1)]
    return final.to_json()

def normalise_stars(normal, star_pass):
    # normal = np.array(normal)
    # normal = normal + min(normal)
    # normal /= np.sqrt(np.sum(np.array(normal)**2))
    starra = np.radians(star_pass.ra_degrees)
    stardec = np.radians(star_pass.dec_degrees)
    starname = star_pass.Name
    starmag = star_pass.magnitude

    ts = load.timescale()
    vec = ICRF(normal, t=ts).radec()    
    dec_0 = np.radians(vec[1].degrees)
    ra_0 = np.radians(vec[0]._degrees)
    # ra, dec = Angle(hours=5.5877286), Angle(degrees=-5.38731536)
    # print(ra,dec)
    # dec_0 = np.radians(dec.degrees)
    # ra_0 = np.radians(ra._degrees)
    # dec_0 = np.arctan2(normal[1],normal[0])
    # ra_0 = np.arccos(normal[2]/np.sqrt(np.sum(np.array(normal)**2)))

    # print(dec_0, ra_0)
    # dec_0 = np.arctan(normal[1]/normal[0])
    # ra_0 = np.arctan(normal[2]/np.sqrt(np.sum(np.array(normal)**2)))
    # print(dec_0, ra_0)
    # dec_0 = np.radians(normal[0])
    # ra_0 = np.radians(normal[1])
    # field_rotation = -268 *np.pi/180
    # field_rotation = np.pi

    denom = np.cos(dec_0)*np.cos(stardec)*np.cos(starra - ra_0)\
        + np.sin(stardec)*np.sin(dec_0)
    X = np.cos(stardec)*np.sin(starra - ra_0)/denom
    Y = (np.sin(dec_0)*np.cos(stardec)*np.cos(starra - ra_0)\
        - np.cos(dec_0)*np.sin(stardec))/denom
    # X = np.cos(field_rotation)*X - np.sin(field_rotation)*Y
    # Y = np.sin(field_rotation)*X + np.cos(field_rotation)*Y
    final = pd.concat([X,Y, starname, starmag], axis = 1)
    final = final[(abs(final[0]) < 1) & (abs(final[1]) < 1)]
    # final = final.query('(abs("0") < 1) & (abs("1") < 1)')
    # plt.scatter(final[0],final[1])
    # plt.show()
    # return final
    # c = final.columns
    # data = [{'id' : x, 'data' : dict(zip(c, y))} 
    #             for x, *y in zip(final.index, final.values.tolist())]
    # return json.dumps(data)
    # return final
    return final.to_json()

# h = pd.read_json('stars.json')
# k = normalise_stars([3,3,3], h)
# print(k.columns)
# print(k[abs(k[0]) < 0.1])
# h = pd.read_json('stars.json')
# # import cProfile
# # cProfile.run("normalise_stars([3,3,3], h)")
# fig,ax = plt.subplots()
# # ax.set_autoscale_on(False)
# plt.axis('equal')

# # # print(star_pass.loc[24436])
# normal = np.array([0.1,0.1,0.1])
# v = normalise_stars([0.1,0.1,0.1], h)
# # print(normal)
# # normal /= sum(normal)
# # print(normal) 
# # exit()
# ax.set_facecolor('black')
# # ax.scatter(v[0],v[1], c = 'white', s=max(v['magnitude']*2)-v['magnitude']*2)
# # for i, txt in enumerate(v['Name']):
# #     ax.annotate(txt, (v[0].iloc[i],v[1].iloc[i]), c = 'white', size = max(v['magnitude']*2)-v['magnitude'].iloc[i]*2 - 3)
# ax.set_ylim([-1,1])
# ax.set_xlim([-1,1])
# # e = v.loc[[24436, 27989, 25336]]
# # ax.scatter(e[0], e[1], c = 'red', s = 0.5)
# # ax.set_ylim([-1,1])
# # ax.set_xlim([-1,1])

# ax_slider = plt.axes((0.20, 0.01, 0.65, 0.03), facecolor='yellow')
# slider = Slider(ax_slider, 'normalx', valmin=-1, valmax=1, valinit = normal[0])
# ax_slider1 = plt.axes((0.20, 0.04, 0.65, 0.03), facecolor='yellow')
# slider1 = Slider(ax_slider1, 'normaly', valmin=-1, valmax=1, valinit = normal[1])
# ax_slider2 = plt.axes((0.20, 0.07, 0.65, 0.03), facecolor='yellow')
# slider2 = Slider(ax_slider2, 'normalz', valmin=-1, valmax=1, valinit = normal[2])
# # ax_slider2 = plt.axes((0.20, 0.07, 0.65, 0.03), facecolor='yellow')
# # slider2 = Slider(ax_slider2, 'normalz', valmin=-1, valmax=1, valinit = normal[2])
# def update(val):
#     normal[0] = val
#     ax.clear()
#     v = normalise_stars(normal, h)
#     ax.scatter(v[0],v[1], c = 'white', s=max(v['magnitude']*5)-v['magnitude']*5)
#     ax.set_ylim([-1,1])
#     ax.set_xlim([-1,1])
#     fig.canvas.draw_idle()

# def update1(val):
#     normal[1] = val
#     ax.clear()
#     v = normalise_stars(normal, h)
#     ax.scatter(v[0],v[1], c = 'white', s=max(v['magnitude']*5)-v['magnitude']*5)
#     ax.set_ylim([-1,1])
#     ax.set_xlim([-1,1])
#     fig.canvas.draw_idle()  

# def update2(val):
#     normal[2] = val
#     ax.clear()
#     v = normalise_stars(normal, h)
#     ax.scatter(v[0],v[1], c = 'white', s=max(v['magnitude']*5)-v['magnitude']*5)
#     ax.set_ylim([-1,1])
#     ax.set_xlim([-1,1])
#     fig.canvas.draw_idle()  

# # def update2(val):
# #     normal[2] = val
# #     ax.clear()
# #     v = normalise_stars(normal)
# #     ax.scatter(v[0],v[1], c = 'white', s=0.5)
# #     fig.canvas.draw_idle()


# slider.on_changed(update)
# slider1.on_changed(update1)
# slider2.on_changed(update2)
# # slider2.on_changed(update2)
# # ax.set_ylim([-1,1])
# # ax.set_xlim([-1,1])
# plt.show()