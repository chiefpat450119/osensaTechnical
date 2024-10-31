from unittest import TestCase
from main import Main


class TestMain(TestCase):
	def test_get_args(self):
		self.main = Main([30, -110, 35, -120, 1, 1])
		self.assertTrue(self.main.get_args())

		self.main = Main([30, -110, 35, -120, 1])
		self.assertTrue(self.main.get_args())

		self.main = Main([30, -110, 35, -120])
		self.assertTrue(self.main.get_args())

		self.main = Main([30, -110, 35])
		self.assertFalse(self.main.get_args())

		self.main = Main([])
		self.assertFalse(self.main.get_args())

		self.main = Main([30, -110, 35, -120, 1, 1, 1])
		self.assertFalse(self.main.get_args())

		self.main = Main(["a", "b", "c", "d", "e", "f"])
		self.assertFalse(self.main.get_args())

		self.main = Main([1000, 39032, 32, 44449, 1, 1])
		self.assertFalse(self.main.get_args())

		self.main = Main([30, -110, 35, -120, -1, -1])
		self.assertFalse(self.main.get_args())



	def test_print_averages(self):
		self.main = Main([30, -110, 35, -120, 1, 1])
		self.main.station_dict = {
			"Station1": [1, 2, 3],
			"Station2": [4, 5, 6],
			"Station3": [7, 8, 9]
		}
		self.assertEqual(self.main.print_averages(), 5)

		self.main.station_dict = {
			"Station1": [],
			"Station2": [],
			"Station3": []
		}
		self.assertEqual(self.main.print_averages(), -1.0)

		self.main.station_dict = {
			"Station1": [],
			"Station2": [6, 7, 8],
			"Station3": [9, 10, 11]
		}
		self.assertEqual(self.main.print_averages(), 8.5)
