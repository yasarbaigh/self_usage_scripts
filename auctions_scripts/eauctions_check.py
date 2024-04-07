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

        crnt = "{}{}{}".format(u, "?page=", pg)
        resp = requests.get(crnt, verify=False)
        if resp.status_code == 200:

            tree = html.fromstring(resp.content)

            items = tree.xpath("//div[@class= 'col-md-9']//div[@class = 'col-sm-12 col-lg-12 col-md-12']")

            if len(items) < 1:
                break
            a = items[0]
            prices = a.xpath("//div[@class = 'image-tag']/text()")
            links = a.xpath("//a[@class = 'text-light text-decoration-none linkhover']/@href")
            timings = a.xpath("//div[@class = 'col-sm-12 col-lg-6 text-light p-1']/text()")
            desc1 = a.xpath("//a[@class = 'text-light text-decoration-none linkhover']/text()")
            desc2 = a.xpath("//p[@class = 'card-text  text-light']/text()")

            for x in range(len(items)):
                if any(subs in desc1[x].lower() for subs in flat_list) or any(subs in desc2[x].lower()  for subs in flat_list):
                    break
                try:

                    p = int(prices[x].strip().replace(",", "").replace("₹ ", ""))
                    if p >= MAX:
                        continue
                except Exception as e:
                    continue

                dt = datetime.strptime(timings[x].replace(" AM", "").replace(" PM", ""), '%d-%m-%Y %H:%M')
                now = datetime.now()
                if dt < now:
                    i = 1000000
                    break
                print("{}\t{}\t{}\t{}".format(timings[x], links[x], prices[x], desc1[x]))
                op_list.append("{}\t{}\t{}\t{}".format(timings[x], links[x], prices[x], desc1[x]))

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