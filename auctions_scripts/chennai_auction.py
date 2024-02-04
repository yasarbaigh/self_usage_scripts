import time

import requests
from lxml import html
import urllib3
from datetime import  datetime
MAX = 10000000

urls = ["https://chennaibankauction.com/wp-admin/admin-ajax.php"]
form_data = {"action": "tableon_get_table_data",
             "fields": "property_id,district,location,post_title,property_type,auction_date,priceacf,thumbnail",
             "post_type": "post",
             "wp_columns_actions": "tableon_default_tables",
             "table_id": "1",
             "predefinition": 'a:1:{s:5:"rules";a:2:{s:15:"not_by_taxonomy";s:2:"-1";s:11:"by_taxonomy";s:2:"-1";}}',
             "filter_data": {},
             "filter_provider": "default",
             "orderby": "auction_date",
             "order": "desc",
             "per_page": "10",
             "current_page": "0",
             "shortcode_args_set": 'a:4:{s:2:"id";s:1:"1";s:6:"action";s:22:"tableon_default_tables";s:13:"no_found_text";s:0:"";s:15:"use_flow_header";i:1;}',
             "tableon_link_get_data": [],
             "lang": "en_US"}
hdrs = {
    "authority": "chennaibankauction.com",
    "accept": "*/*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "origin": "https://chennaibankauction.com",
    "referer": "https://chennaibankauction.com/",
    "sec-ch-ua": "Not_A Brand';v='8', 'Chromium';v='120', 'Google Chrome';v='120'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", }

flat_list = [' flat ', ' flat', 'flats-', ' apartment ', ' apartment', 'flat-']


op_list = []
go_for_next = True
try:

    while go_for_next and int(form_data['current_page']) < 70:

        resp = requests.post(urls[0], headers=hdrs, verify=False, data=form_data)
        if resp.status_code == 200:

            op = resp.json()
            for r in op.get('rows', []):
                try:
                    price = int(r.get("priceacf")[2:].replace(',', ''))
                    title = r.get("post_title").lower()
                    link = html.fromstring(r.get('post_title')).get('href')
                    cdt = datetime.strptime(r.get("auction_date"), '%d/%m/%Y') - datetime.now()
                    if cdt.days < 1:
                        go_for_next = False
                        break

                    if price >= MAX or any(subs in title for subs in flat_list) or any(subs in link.lower() for subs in flat_list) :
                        # skipping flat
                        continue

                    sub_content = requests.get(link, headers=hdrs, verify=False)
                    if sub_content.status_code == 200 and sub_content.text.lower().find("physical") > 0:
                        op_list.append( "{}\t{}\t{}\t{}\t{}\t{}".format(r.get("pid"), html.fromstring(r.get("district")).text,
                                                              html.fromstring(r.get("location")).text,
                                                              html.fromstring(r.get('post_title')).get('href'),
                                                              r.get("auction_date"), r.get("priceacf")[2:], ))

                    else:
                        pass
                    time.sleep(.5)
                except Exception as e:
                    pass
            form_data['current_page'] = int(form_data['current_page']) + 1
            print("Checking for Current Page {}".format(form_data['current_page']))
            print(op_list)
            time.sleep(2)

        else:
            print(resp.status_code)
            print(resp.text)
            print(resp.content)
except Exception as e:
    pass

for ln in op_list:
    print(ln)