from json import load, loads, dumps
from re import search
from time import time
from hashlib import md5
from pandas import read_excel
from requests import get
from tkinter import Tk, filedialog
import os


def get_time_zone(uid):  # 根据uid映射得到时区
    uid_first = str(uid)[0]
    if uid_first == "6":
        return -5
    elif uid_first == "7":
        return 1
    else:
        return 8


def check_md5():  # 联网校对物品id字典是否有更新
    is_latest = False
    try:
        with open("zh-cn.json", "r") as f:
            file = f.read().encode("utf-8")
            file_md5 = md5(file).hexdigest()
            md5_list = loads(get("https://api.uigf.org/md5/genshin").text)
            latest_md5 = md5_list["chs"]
            is_latest = (file_md5 == latest_md5)
    except IOError:  # 检查字典是否存在
        is_latest = False
    if not is_latest:  # 如果字典有更新或不存在，则更新id字典
        print("正在更新字典……")
        new_json = get("https://api.uigf.org/dict/genshin/chs.json").text
        with open("zh-cn.json", "w", encoding="gbk") as f0:
            f0.write(new_json)


def read(gatcha_type, uid, excel_name, sheet_name, dictionary, uigf_list):  # dictionary:字典列表
    sheet = read_excel(excel_name, sheet_name=sheet_name)
    for row in sheet.index.values:
        data = {
            "uigf_gacha_type": gatcha_type,
            "uid": uid,
            "gacha_type": gatcha_type,
            "item_id": str(dictionary[str(sheet.iloc[row, 1])]),
            "count": "1",
            "time": str(sheet.iloc[row, 0]),
            "name": str(sheet.iloc[row, 1]),
            "lang": "zh-cn",
            "item_type": str(sheet.iloc[row, 2]),
            "rank_type": str(sheet.iloc[row, 3]),
            "id": str(sheet.iloc[row, 6])
        }
        uigf_list.append(data)


def get_excels(path):  # 获取文件夹中的抽卡记录表
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path) and file_path.endswith(".xlsx") and "非小酋抽卡记录" in file:
            yield file_path


def output_uigf(excel, dictionary):  # 输出uigf
    lists = []
    read_uid = search(r"[0-9]{9}", excel).group()
    info = {
        "uid": read_uid,
        "lang": "zh-cn",
        "export_timestamp": int(time()),
        "export_app": "非小酋",
        "export_app_version": "v1.0",
        "uigf_version": "v2.4",
        "region_time_zone": get_time_zone(read_uid)
    }
    read("100", read_uid, excel, "新手祈愿", dictionary, lists)
    read("200", read_uid, excel, "常驻祈愿", dictionary, lists)
    read("301", read_uid, excel, "角色活动祈愿", dictionary, lists)
    read("302", read_uid, excel, "武器活动祈愿", dictionary, lists)
    output = {"info": info, "list": lists}
    with open(read_uid + '.json', 'w', encoding="gbk") as f2:
        f2.write(dumps(output, ensure_ascii=False, indent=4))
        print(read_uid + "导出完成")


if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    with open("zh-cn.json", "r", encoding="gbk") as f1:
        trans_list = load(f1)
    excels = get_excels(filedialog.askdirectory(title="请选择抽卡记录表所在的文件夹"))
    xl_list = []
    for i in excels:
        xl_list.append(i)
    if not xl_list:
        print("未在文件夹中发现可用的抽卡记录表，请确认有没有将非小酋记录表重命名！")
    for xl in xl_list:
        output_uigf(xl, trans_list)
