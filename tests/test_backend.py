import numpy as np
import numpy.testing as npt
import sys
import pandas as pd

sys.path.append(r'C:\Users\vikra\starview\backend')

import testing

def test_fetching():
    # testing.update_data()
    stars = pd.read_json('stars.json')
    planets = pd.read_json('planets.json')

    npt.assert_equal((0 < stars.ra_degrees.all() < 360), True)
    npt.assert_array_equal((-90 < planets.ra_degrees.all() < 90), True)

    npt.assert_array_less(stars.magnitude, 4)
    npt.assert_array_less(planets.magnitude, 4)

    orion_hip_id = [24436, 27989, 25336,26311, 26727, 27366, 25930]
    orion_stars = stars.loc[orion_hip_id]
    orion_mags = [0.18, 0.42, 1.64, 1.69, 1.88, 2.07, 2.20]

    npt.assert_approx_equal(orion_stars.mag, orion_mags)

test_fetching()