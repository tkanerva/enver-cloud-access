from pprint import pprint
import requests
import json

try:
    from enver_config import CONFIG
except ImportError:
    CONFIG = {}


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


def get_enver(station_id=None):
    hdrs_ = dict(map(str.strip, x.split(':', 1)) for x in hdrs)  # morph headers to dict
    # if not given, get stationid from CONFIG
    stationid = station_id or CONFIG.get('station_id', 0)
    base = CONFIG.get('current_base_url') or url_
    uri = base + '?' + data.format(stationid=stationid).strip()
    r = requests.post(uri, headers=hdrs_)

    d = json.loads(r.text)

    def getPower(r, func=list, item="POWER"):
        data = r['Data']
        queryResults = data.get("QueryResults")
        return func(float(i.get(item, -1)) for i in queryResults)

    r = getPower(d, func=sum)  # get Total power, sum up all values.
    return r


def _main(*args):
    res = get_enver()
    print(res)


if __name__=="__main__":
    _main()
