import numpy as np
import numpy.testing as npt
import sys
import pandas as pd
import json

sys.path.append(r'C:\Users\vikra\starview\backend')

import testing

def test_fetching():
    testing.update_data()
    stars = pd.read_json('stars.json')
    planets = pd.read_json('planets.json')

    npt.assert_equal((0 < stars['ra_degrees'].all() < 360), True)
    npt.assert_array_equal((-90 < planets['ra'].all() < 90), True)
    npt.assert_array_less(stars.magnitude, 4.001)

    orion_hip_id = [24436, 27989, 25336,26311, 27366, 25930]
    orion_stars = stars.loc[orion_hip_id]
    orion_mags = [0.18, 0.44, 1.64, 1.69, 2.07, 2.24]

    npt.assert_array_less(abs(np.array(orion_stars.magnitude.tolist())
     - np.array(orion_mags)), 0.1)

def test_normalise():
    normal = [1,1,1]
    pl = json.loads(testing.normalise_planets(normal))
    st = json.loads(testing.normalise_stars(normal))

    npt.assert_array_less(np.abs(list(pl['0'].values())), 1)
    npt.assert_array_less(np.abs(list(st['0'].values())), 1)
    npt.assert_array_less(np.abs(list(pl['1'].values())), 1)
    npt.assert_array_less(np.abs(list(st['1'].values())), 1)

test_normalise()