"""Energy-ES - Data - Prices."""

from datetime import date, datetime
from zoneinfo import ZoneInfo

import requests
from userconf import UserConf


class PricesManager:
    """Prices manager.

    This class gets the hourly values of the Spot Market and PVPC energy prices
    of the current day in Spain. The data is cached in a configuration file
    inside the user's home directory. The data is provided by some APIs of "Red
    Eléctrica de España".

    The values are stored in €/MWh but can be returned in either €/kWh or
    €/MWh by the `get_prices` method.
    """

    # Red Eléctrica API for Spot Market prices. Prices are the same for whole
    # Spain.
    SPOT_API_URL = (
        "https://apidatos.ree.es/en/datos/mercados/precios-mercados-tiempo-"
        "real?start_date={}&end_date={}&time_trunc=hour"
    )

    # Red Eléctrica API for PVPC prices. Prices are different by system/area:
    #   1. Peninsula, Canarias and Baleares
    #   2. Ceuta y Melilla
    PVPC_API_URL = (
        "https://api.esios.ree.es/archives/70/download_json?locale=es&date={}"
    )

    def __init__(self):
        """Class initializer.

        When this method is called, the `_load_data` method is called. This
        method sets the `_prices` attribute. The following is an example of the
        `_prices` structure (the prices are in €/MWh):

        {
          "updated": 1671058800.0
          "price_unit": "€/MWh",
          "data": [
            {
              "hour": 14,
              "spot_market": 250.78,
              "pvpc_pcb": 127.97,
              "pvpc_cm": 120.5,
            }
          ]
        }
        """
        self._conf = UserConf("energy_es")
        self._prices = None

        self._load_data()

    def _load_data(self):
        """Load the data from the cache."""
        self._prices = self._conf.settings.get("prices")

    def _save_data(self):
        """Save the data to the cache."""
        self._conf.settings.set("prices", self._prices)

    def _is_data_valid(self) -> bool:
        """Check if the data is valid.

        :return: Whether the data is valid.
        """
        if self._prices is None:
            return False

        # We convert the "Updated" timestamp to a local datetime with time zone
        # information and we get the current datetime of the Europe/Madrid time
        # zone.

        # "Updated" datetime
        u = self._prices["updated"]
        d1 = datetime.fromtimestamp(u).astimezone()

        # Current datetime in Europe/Madrid
        d2 = datetime.now().astimezone(ZoneInfo("Europe/Madrid"))

        # Clear time
        d1 = d1.replace(hour=0, minute=0, second=0, microsecond=0)
        d2 = d2.replace(hour=0, minute=0, second=0, microsecond=0)

        # Compare datetimes/dates
        return d1 == d2

    def _format_hour(self, hour: int) -> str:
        """Return the HH:MM sring of an hour.

        :param hour: Hour (0-23).
        :return: HH:MM hour string.
        """
        return str.zfill(str(hour), 2) + ":00"

    def _get_updated_spot_market_data(self, today_em: date) -> list[dict]:
        """Get the Spot Market updated data.

        :param today_em: Current date in the Europe/Madrid time zone.
        :return: Sorted list of 24 dictionaries, each one for a different hour
        of the day. Each dictionary has a key named "spot_market" which value
        is the Spot Market price (for all Spain) (float) for a particular hour.
        """
        error = "Invalid Spot Market data"

        # Prepare URL
        dt = today_em.strftime("%Y-%m-%d")
        start = f"{dt}00:00"
        end = f"{dt}23:59"
        url = self.SPOT_API_URL.format(start, end)

        # Make request to the API
        res = requests.get(url)

        # Check response status
        if res.status_code != 200:
            raise Exception(res.reason)

        # Read response data to get the Spot Market prices (in €/MWh)
        data = res.json()["included"]

        spot = list(filter(lambda x: "spot" in x["type"].lower(), data))
        spot = spot[0]["attributes"]["values"]

        # Check data
        spot_count = len(spot)

        if spot_count != 24:
            raise Exception(
                f"{error}. 24 values expected but {spot_count} received."
            )

        # Transform data
        spot = list(map(
            lambda x: {
                "datetime":
                    datetime.fromisoformat(x["datetime"].replace(" ", "")),
                "value": x["value"]
            },
            spot
        ))

        # Sort data
        spot = sorted(spot, key=lambda x: x["datetime"])

        # Check data
        for i, v in enumerate(spot):
            vdt = v["datetime"]
            d = vdt.date()

            # Check date
            if d != today_em:
                raise Exception(
                    f"{error}. Data for {dt} expected but data for {str(d)} "
                    "received."
                )

            # Check hour
            if vdt.hour != i:
                exp = self._format_hour(i)
                act = vdt.strftime("%H:%M")

                raise Exception(
                    f"{error}. Data for {exp} expected but data for {act} "
                    "received."
                )

        # Transform and return data
        return list(map(
            lambda x: {"spot_market": x["value"]},
            spot
        ))

    def _get_updated_pvpc_data(self, today_em: date) -> list[dict]:
        """Get the PVPC updated data.

        :param today_em: Current date in the Europe/Madrid time zone.
        :return: Sorted list of 24 dictionaries, each one for a different hour
        of the day. Each dictionary has two keys named "pvpc_pcb" and
        "pvpc_cm", which values are, respectively, the PVPC price (for
        peninsula, Canarias and Baleares) (float) and the PVPC price (for Ceuta
        y Melilla) (float), for a particular hour.
        """
        error = "Invalid PVPC data"

        # Prepare URL
        dt = today_em.strftime("%Y-%m-%d")
        url = self.PVPC_API_URL.format(dt)

        # Make request to the API
        res = requests.get(url)

        # Check response status
        if res.status_code != 200:
            raise Exception(res.reason)

        # Read response data to get the PVPC prices (in €/MWh)
        data = res.json()["PVPC"]

        pvpc = list(map(
            lambda x: {
                "date": datetime.strptime(x["Dia"], "%d/%m/%Y").date(),
                "hour": int(x["Hora"][:2]),
                "pvpc_pcb": float(x["PCB"].replace(",", ".")),
                "pvpc_cm": float(x["CYM"].replace(",", "."))
            },
            data
        ))

        # Check data
        pvpc_count = len(pvpc)

        if pvpc_count != 24:
            raise Exception(
                f"{error}. 24 values expected but {pvpc_count} received."
            )

        # Sort data
        pvpc = sorted(pvpc, key=lambda x: x["hour"])

        # Check data
        for i, v in enumerate(pvpc):
            d = v["date"]
            h = v["hour"]

            # Check date
            if d != today_em:
                raise Exception(
                    f"{error}. Data for {dt} expected but data for {str(d)} "
                    "received."
                )

            # Check hour
            if h != i:
                exp = self._format_hour(i)
                act = self._format_hour(h)

                raise Exception(
                    f"{error}. Data for {exp} expected but data for {act} "
                    "received."
                )

        # Transform and return data
        return list(map(
            lambda x: {
                "pvpc_pcb": x["pvpc_pcb"],
                "pvpc_cm": x["pvpc_cm"]
            },
            pvpc
        ))

    def _update_data(self):
        """Update the data by calling the APIs."""
        # Current local datetime
        now = datetime.now()

        # Get the current datetime in the Europe/Madrid time zone
        today_em = now.astimezone(ZoneInfo("Europe/Madrid")).date()

        # Get updated data
        hour = list(range(24))
        spot = self._get_updated_spot_market_data(today_em)
        pvpc = self._get_updated_pvpc_data(today_em)

        # Prepare data
        data = list(map(
            lambda x: {
                "hour": x[0],
                "spot_market": x[1]["spot_market"],
                "pvpc_pcb": x[2]["pvpc_pcb"],
                "pvpc_cm": x[2]["pvpc_cm"]
            },
            zip(hour, spot, pvpc)
        ))

        # Update prices
        self._prices = {
            "updated": now.timestamp(),
            "price_unit": "€/MWh",
            "data": data
        }

        # Save data
        self._save_data()

    def get_prices(self, unit: str = "m") -> list[dict]:
        """Return the hourly energy prices (of either Spot Market or PVPC) of
        the current day in Spain.

        :param unit: Prices unit. It must be "k" to return the prices in €/kWh
        or "m" (default) to return them in €/MWh.
        :return: Sorted list of 24 dictionaries, each one for a different hour
        of the day. Each dictionary has four keys named "hour, "spot_market",
        "pvpc_pcb" and "pvpc_cm", which values are, respectively, the hour and
        the Spot Market price (for all Spain) (float), the PVPC price (for the
        peninsula, Canarias and Baleares) (float) and the PVPC price (for Ceuta
        y Melilla) (float) for a particular hour.
        """
        unit = unit.lower()

        # Check units
        if unit not in ("k", "m"):
            raise Exception(
                'Invalid unit. It must be "k" (€/kWh) or "m" (€/MWh)'
            )

        # Check whether data is valid and update it if not
        if not self._is_data_valid():
            self._update_data()

        if unit == "m":
            # Deep copy of "self._prices["data"]" with the prices in €/MWh
            price_unit = self._prices["price_unit"]

            data = list(map(
                lambda x: {
                    "time": self._format_hour(x["hour"]),
                    "spot_market": x["spot_market"],
                    "pvpc_pcb": x["pvpc_pcb"],
                    "pvpc_cm": x["pvpc_cm"],
                },
                self._prices["data"]
            ))
        else:
            # Deep copy of "self._prices["data"]" with the prices in €/kWh
            price_unit = "€/kWh"

            data = list(map(
                lambda x: {
                    "time": self._format_hour(x["hour"]),
                    "spot_market": round(x["spot_market"] / 1000, 5),
                    "pvpc_pcb": round(x["pvpc_pcb"] / 1000, 5),
                    "pvpc_cm": round(x["pvpc_cm"] / 1000, 5)
                },
                self._prices["data"]
            ))

        return {
            "updated": self._prices["updated"],
            "price_unit": price_unit,
            "data": data
        }
