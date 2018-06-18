import unittest

from app.rest_server import get_coords_list, coords_to_tuples_list

class ServerTestCase(unittest.TestCase):
    """Tests for rest_server.py"""

    def test_coords_to_tuples_list(self):
        self.assertIsNotNone(coords_to_tuples_list([[4,3],[0,0],[2,7]]))
        self.assertEqual([(4,3),(0,0),(2,7)], coords_to_tuples_list([[4,3],[0,0],[2,7]]))
        self.assertEqual([(0,0)], coords_to_tuples_list([[0,0]]))
    
    def test_get_coords_list(self):
        simple_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[1,2], [8,6], [0,0]]]
                    }
                }
            ]
        }

        self.assertEqual([[1,2], [8,6], [0,0]], get_coords_list(simple_geojson, 0))

if __name__ == '__main__':
    unittest.main()
