from bs4 import BeautifulSoup
import requests


class BahnScrapper:
    def get_conn_details(self, origin, destination, time):
        result = requests.get(self._get_uri(origin, destination, time))
        self.soup = BeautifulSoup(result.content, "lxml")

        times = self._get_times()
        d = self._get_station("station stationDest ")
        o = self._get_station("station first ")

        return [{"from": {"name": o, "time": i[0]},
                 "to": {"name": d, "time": i[1]}}
                for i in times]

    def _get_uri(self, origin, destination, time):
        date = f'{time.day}.{time.month}.{time.year}'
        time = f'{time.hour}%3A{time.minute}'
        uri = f'https://reiseauskunft.bahn.de/bin/query.exe/dn?revia=yes&existOptimizePrice=1&country=DEU&dbkanal_007=L01_S01_D001_KIN0001_qf-bahn-svb-kl2_lz03&start=1&protocol=https%3A&REQ0JourneyStopsS0A=1&S=Kurhessenstra%C3%9Fe%2C+Frankfurt+a.M.&REQ0JourneyStopsSID={origin}&Z={destination}&REQ0JourneyStopsZID=&date={date}&time={time}&timesel=depart&returnDate=&returnTime=&returnTimesel=depart&optimize=0&auskunft_travelers_number=1&tariffTravellerType.1=E&tariffTravellerReductionClass.1=0&tariffClass=2&rtMode=DB-HYBRID&externRequest=yes&HWAI=JS%21js%3Dyes%21ajax%3Dyes%21'
        print(uri)
        return uri

    def _get_times(self):
        times = self.soup.find_all("td", {"class": "time"})
        times = self._trim_texts(times)
        times = [(i, j) for i, j in zip(times[:-1], times[1:])]
        times = self._remove_delay_time(times)
        return times

    def _remove_delay_time(self, times):
        result = []
        for i in times:
            if len(i) > 5:
                result.append(i[5:0])
            else:
                result.append(i)
        return result

    def _get_station(self, css_class):
        station_names = self.soup.find_all("td", {"class": css_class})
        station_names = self._trim_texts(station_names)
        return station_names[0]

    def _trim_texts(self, leaving_times: list):
        leaving_times = [i.getText().replace('\xa0', '').replace('\n', '') for i in leaving_times]
        leaving_times = [i.strip() for i in leaving_times if i is not ""]
        return leaving_times
