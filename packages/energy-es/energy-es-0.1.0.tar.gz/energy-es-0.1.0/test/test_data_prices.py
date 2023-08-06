"""Energy-ES - Tests - Data - Prices - Unit tests."""

import unittest
from unittest.mock import MagicMock, patch

# We import "paths" to include the "src" directory in "sys.path" so that we can
# import "userconf".
import paths
from mocks import get_mock, SettingsManagerMock

from energy_es.data.prices import PricesManager


class DataPricesTestCase(unittest.TestCase):
    """Unit tests of the "energy_es.data.prices" module."""

    @patch("requests.get", get_mock)
    @patch("userconf.SettingsManager")
    def test_initial_data(self, sm_mock: MagicMock):
        """Test the initial values of `PricesManager._prices`."""
        # Mock
        sm_mock.return_value = SettingsManagerMock()

        pm = PricesManager()
        self.assertIs(pm._prices, None)

    @patch("requests.get", get_mock)
    @patch("userconf.SettingsManager")
    def test_is_data_valid(self, sm_mock: MagicMock):
        """Test `PricesManager._is_data_valid`."""
        # Mock
        sm_mock.return_value = SettingsManagerMock()

        pm = PricesManager()
        self.assertFalse(pm._is_data_valid())

        pm.get_prices()
        self.assertTrue(pm._is_data_valid())

    @patch("requests.get", get_mock)
    @patch("userconf.SettingsManager")
    def test_get_prices(self, sm_mock: MagicMock):
        """Test `PricesManager.get_prices`."""
        # Mock
        sm_mock.return_value = SettingsManagerMock()

        pm = PricesManager()
        prices = pm.get_prices()

        self.assertEqual(type(prices), dict)
        self.assertEqual(len(prices), 3)

        self.assertIn("updated", prices)
        self.assertEqual(type(prices["updated"]), float)

        self.assertIn("price_unit", prices)
        self.assertEqual(type(prices["price_unit"]), str)

        self.assertIn("data", prices)
        data = prices["data"]
        self.assertEqual(type(data), list)
        self.assertEqual(len(data), 24)

        for i, v in enumerate(data):
            self.assertEqual(type(v), dict)
            self.assertEqual(len(v), 4)

            self.assertIn("time", v)
            t = v["time"]
            self.assertEqual(type(t), str)
            self.assertEqual(t, str.zfill(str(i), 2) + ":00")

            self.assertIn("spot_market", v)
            self.assertEqual(type(v["spot_market"]), float)

            self.assertIn("pvpc_pcb", v)
            self.assertEqual(type(v["pvpc_pcb"]), float)

            self.assertIn("pvpc_cm", v)
            self.assertEqual(type(v["pvpc_cm"]), float)

    @patch("requests.get", get_mock)
    @patch("userconf.SettingsManager")
    def test_prices_units(self, sm_mock: MagicMock):
        """Test `PricesManager.get_prices` with different units."""
        # Mock
        sm_mock.return_value = SettingsManagerMock()

        pm = PricesManager()

        data_k = pm.get_prices("k")["data"]  # Prices in €/kWh
        data_m = pm.get_prices("m")["data"]  # Prices in €/MWh

        k_count = len(data_k)
        m_count = len(data_m)

        self.assertEqual(k_count, 24)
        self.assertEqual(m_count, 24)

        # Check that each price in €/kWh is equal to the price in €/MWh divided
        # by 1000.
        for i in ("spot_market", "pvpc_pcb", "pvpc_cm"):
            for j in range(k_count):
                act = data_k[j][i]
                exp = round(data_m[j][i] / 1000, 5)

                self.assertEqual(act, exp)
