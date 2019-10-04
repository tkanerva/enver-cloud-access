from __future__ import print_function
from pprint import pprint
from twisted.internet.task import react
import treq

from enver_config import CONFIG


url_ = 'http://www.envertecportal.com/ApiInverters/QueryTerminalReal'
hdrs = [
 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8'
, 'Content-Length: 0'
, 'Referer: http://www.envertecportal.com/terminal/systemreal' 
, 'Accept: application/json, text/javascript, */*; q=0.01' 
, 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8' 
, 'Origin: http://www.envertecportal.com' 
, 'X-Requested-With: XMLHttpRequest' 
]
data="""
page=1&perPage=50&orderBy=GATEWAYSN&whereCondition=%7B%22STATIONID%22%3A%22{stationid}%22%7D
"""


def main(*args):
    hdrs_ = dict(map(str.strip, x.split(':', 1)) for x in hdrs)  # morph headers to dict
    # get stationid from CONFIG
    stationid = CONFIG.get('station_id') or 0
    base = CONFIG.get('current_base_url') or url_
    uri = base + '?' + data.format(stationid=stationid).strip()
    print(uri, hdrs_)
    dfr = treq.post(uri, headers=hdrs_)

    def getTotalPower(r):
        data = r['Data']
        queryResults = data.get("QueryResults")
        power = sum(float(i.get("POWER", -1)) for i in queryResults)
        return power

    def getPowerArray(r):
        data = r['Data']
        queryResults = data.get("QueryResults")
        all_power = list(float(i.get("POWER", -1)) for i in queryResults)
        return all_power

    def getTemperatures(r):
        data = r['Data']
        queryResults = data.get("QueryResults")
        all_temps = list(float(i.get("TEMPERATURE", 0)) for i in queryResults)
        return all_temps

    dfr.addCallback(treq.json_content)
    #dfr.addCallback(getTotalPower)
    #dfr.addCallback(getPowerArray)
    dfr.addCallback(getTemperatures)
    return dfr


def _main(*args):
    dfr = main([])
    dfr.addCallback(print)
    return dfr


if __name__=="__main__":
    react(_main, [])
