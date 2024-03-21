

# url = 'http://192.168.10.159/v1/'+str(id)
# url = "http://192.168.1.3:7078/501"

import requests
import json
import datetime

for i in range(500, 505):
    re = requests.get('http://192.168.1.3:7078/'+str(i)).json()
    print(re)
    d = datetime.datetime.strptime(re[0]['w_date'].split("T")[0], "%Y-%m-%d")


    print(d.year)
    print(d.day)
    print(d.month)





    data_j = {
        #แยกเวลา,วันที่
        
            "name": "test"+str(i),
            "year": d.year,
            "date": d.day,
            "month": d.month,
            "waterfront": re[0]["w_height"],
            "waterback": 0,
            "waterdrain": re[0]["w_height"]+ re[0]["w_cubic"]
            }


    requests.post('http://localhost/water/', json=data_j)
    # print(data_j)









