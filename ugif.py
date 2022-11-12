import pandas
import json
import time 
import os

lists=[]
def read(types,uid,excel_name,sheet_name):
    sheet=pandas.read_excel(excel_name,sheet_name=sheet_name)
    for row in sheet.index.values :
        data={
            "uigf_gacha_type": types,
            "uid": uid,
            "gacha_type": types,
            "item_id": "",
            "count": "1",
            "time": str(sheet.iloc[row, 0]),
            "name": str(sheet.iloc[row, 1]),
            "lang": "zh-cn",
            "item_type": str(sheet.iloc[row, 2]),
            "rank_type": str(sheet.iloc[row, 3]),
            "id": str(sheet.iloc[row, 6])
        }
        lists.append(data)

name = [i for i in os.listdir() if '非小酋抽卡记录' in i]
for excel_name in name:
    lists=[]
    uid=excel_name[7:16]
    info={
        "uid": uid,
        "lang": "zh-cn",
        "export_time": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))),
        "export_timestamp": int(time.time()),
        "export_app": "export feixiaoqiu",
        "export_app_version": "v1.0",
        "uigf_version": "v2.2"
    }
    lists=[]
    read("100",uid,excel_name,"新手祈愿")
    read("200",uid,excel_name,"常驻祈愿")
    read("301",uid,excel_name,"角色活动祈愿")
    read("302",uid,excel_name,"武器活动祈愿")
    output={"info":info,"list":lists}
    f2 = open(uid+'.json', 'w',encoding="utf8")
    f2.write(json.dumps(output,ensure_ascii=False,indent=4))
    print(uid+"导出完成")
    f2.close()