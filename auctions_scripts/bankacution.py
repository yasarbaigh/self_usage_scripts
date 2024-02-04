import time

import requests


districts = ['', 'KANCHIPURAM', 'Chennai', 'Chennai-III', 'Ambattur', 'TIRUVALLUR', 'Thiruvallur', 'Chengalpattu']
url = "https://www.bankeauctions.com/home/liveAuctionDatatable//?reservePriceMaxRange=7000000&reservePriceMinRange=0&state=24&propertytype=0"
form_data = {'user': 'value', "sEcho":"", "iColumns":"", "sColumns":"", "iDisplayStart" :"0", "iDisplayLength":"200"}


all_districts = set()

count = 0
total_count = 10
while count <= total_count:
    server = requests.post(url, data=form_data)
    if server.status_code == 200:
        pass
        json_op = server.json()

        total_count = int(json_op.get('iTotalRecords'))
        props = json_op.get('aaData')
        for item in props:
            if ' flat ' in item[3] or ' Flat ' in item[3] or ' apartment  ' in item[3] or ' Apartment  ' in item[3]:
                continue
            elif item[4] in districts or 'hennai' in item[4] :
                print("{}\t{}\thttps://www.bankeauctions.com/{}\t{}\t{}".format(item[2], item[4], item[10], item[5], item[7])  )
            all_districts.add(item[4])
    else:
        pass
    count += 10
    form_data['iDisplayStart'] = count
    time.sleep(5)
    # print(count)
    pass

print("\n\n")
print(all_districts)