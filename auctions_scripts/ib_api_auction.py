import json
import time

import requests
from lxml import html
import urllib3
from datetime import datetime

MAX = 10000000


ibp_url = "https://ibapi.in/Sale_Info_Home.aspx/Button_search_Click"
prop_url = "https://ibapi.in/Sale_Info_Home.aspx/bind_modal_detail"
available_districts = set()
hdrs = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Type": "application/json; charset:utf8",
    "Cookie": "ASP.NET_SessionId=f5qgo5wvzokpezhxmjw5eoob; TS01211a4c=01e1feefea434466611382403ecb238ac1d272fb5f9a146e093feedf6ea61a2b62321f007ab707e638a52bf66a093889393341a62afcc7417cab23fa3f9c66340e2aad878e",
    "Origin": "https://ibapi.in",
    "Referer": "https://ibapi.in/sale_info_home.aspx",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": 'Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows"
}


my_districts = ['CHENNAI', 'KANCHEEPURAM', 'VELLORE', 'THIRUVALLUR', 'TIRUVANNAMALAI', ]
flat_list = [' flat ', ',flat ', '-flat-', 'flats-', ' apartment ', ' apartment-', 'flat-']

monthly_dts = [{"key_val": [["State", "'TN'"], ["period", "'202402'"]]},
               {"key_val": [["State", "'TN'"], ["period", "'202403'"]]}]

monthly_dts = [{"key_val": [["State", "'TN'"], ["period", "'202402'"]]}]




op_list = []
go_for_next = True
try:

    for item in monthly_dts:

        resp = requests.post(ibp_url, headers=hdrs, verify=False, data=json.dumps(item))
        if resp.status_code == 200:

            op = resp.json().get('d')

            op = (op.replace('\\"', '"').replace(' id="btn_view" style="', " id='btn_view' style='")
                  .replace(':bold"', ":bold'").replace("\\'", "'"))

            op = json.loads(op)
            price = ''
            for r in op:
                try:
                    p_id = r.get('Property ID')
                    p_id = p_id[1 + p_id.find('>'): -4]

                    price = r.get('Reserve Price (Rs)')
                    available_districts.add(r.get('District'))

                    if float(price.strip().replace(',', '')) < MAX and r.get('District') in my_districts:
                        time.sleep(.5)
                        sub_content = requests.post(prop_url, headers=hdrs, data='{"prop_id":"' + p_id + '"}',
                                                    verify=False)
                        if sub_content.status_code == 200 and sub_content.text.lower().find("physical") > 0:
                            lwr = sub_content.text.lower()
                            if any(subs in lwr for subs in flat_list):
                                print("Flat {}  {}".format(p_id, price))
                                pass
                            else:
                                op_list.append(
                                    "{}\t{}\t{}\t{}\t{}\t{}".format(p_id, r.get('Bank Name'), r.get('District'),
                                                                    r.get('City'),
                                                                    price,
                                                                    r.get("Auction Start Date & Time")[0:12]))

                        elif sub_content.status_code > 399 :
                            print("Sub-check Failed {}  {}".format(p_id, price))

                except Exception as e:
                    print("Error for {} {}".format(r.get('Property ID'), price))

        else:
            print(resp.status_code)
            print(resp.text)
            print(resp.content)

        go_for_next = False

except Exception as e:
    print(e)

print(available_districts)


print()
print()
print()
print()
for ln in op_list:
    print(ln)
