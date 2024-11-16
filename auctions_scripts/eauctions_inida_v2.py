import time
from lxml import html
from datetime import datetime
import requests

urls = ['https://www.eauctionsindia.com/house-auctions-in-chengalpattu',
        'https://www.eauctionsindia.com/house-auctions-in-chennai', 'https://www.eauctionsindia.com/house-auctions-in-kanchipuram', 'https://www.eauctionsindia.com/house-auctions-in-thiruvallur']
# urls = ['https://www.eauctionsindia.com/house-auctions-in-chengalpattu']
flat_list = [' flat ', ' flat ', ' flat:', ' apartment ']
symbolic_list = [' Symbolic ']

op_list = []
MAX = 9000000
for u in urls:
    pg = 1
    i = 1
    print("\n\n Checking for " + u + "\n\n")
    while i < 500:

        # crnt = "{}{}{}".format(u, "?page=", pg)   # Old-url
        crnt = "{}{}{}".format(u, "/", pg)
        resp = requests.get(crnt, verify=False)
        if resp.status_code == 200:

            tree = html.fromstring(resp.content)

            white_rows = tree.xpath("//tr[@class= ' text-white bg-pc2 ']")

            if len(white_rows) > 0:               

                for row in white_rows:
                    try:
                        tds = row.xpath(".//td")

                        a_id = tds[0].text.strip()
                        desc = tds[1].text.strip()
                        a_date = tds[2].text.strip()
                    
                        price = tds[4].text.strip()
                        lnk = tds[5].xpath('.//a/@href')[0]

                        dt = datetime.strptime(a_date.replace(" AM", "").replace(" PM", ""), '%d-%m-%Y %H:%M')
                        now = datetime.now()
                        if dt < now:
                            i = 1000000  # old-auction item
                            continue

                        p = int(price.strip().replace(",", "").replace("₹ ", ""))
                        if p >= MAX:
                            print('skipping {} {}'.format(a_id, price))
                            continue

                        if any(subs in desc.lower() for subs in flat_list) or any(subs in a_id.lower()  for subs in flat_list):
                            print('skipping {} {}'.format(a_id, price))
                            continue

                        op_list.append([a_id, a_date, price, lnk,  desc])
                    except Exception as ex:
                        print("Error in TD {}".format( ex))

            
            dark_rows = tree.xpath("//tr[@class= ' text-white bg-pc2 ']")

            if len(dark_rows) > 0:               

                for row in dark_rows:
                    try:
                        tds = row.xpath(".//td")

                        a_id = tds[0].text.strip()
                        desc = tds[1].text.strip()
                        a_date = tds[2].text.strip()
                    
                        price = tds[4].text.strip()
                        lnk = tds[5].xpath('.//a/@href')[0]

                        dt = datetime.strptime(a_date.replace(" AM", "").replace(" PM", ""), '%d-%m-%Y %H:%M')
                        now = datetime.now()
                        if dt < now:
                            i = 1000000  # old-auction item
                            continue

                        p = int(price.strip().replace(",", "").replace("₹ ", ""))
                        if p >= MAX:
                            print('skipping {} {}'.format(a_id, price))
                            break

                        if any(subs in desc.lower() for subs in flat_list) or any(subs in a_id.lower()  for subs in flat_list):
                            print('skipping {} {}'.format(a_id, price))
                            continue

                        op_list.append([a_id, a_date, price, lnk,  desc])
                    except Exception as ex:
                        print("Error in TD {}".format( ex))

        else:
            break

        pg += 1
        i += 1
        time.sleep(5)


for ln in op_list:
    print(ln)

print("eaucitons_check")
print(datetime.now())

print("\n\n\n\n")
print("===================================================")