"""Generate the checked-in UEX entity localization supplement from the local Overlay cache.

The source JSON supplied by the user remains unmodified. This generator adds translations for currently
uncovered UEX commodity, vehicle, location, station, outpost, and terminal names. Run it only while the
Overlay database is closed or through the read-only immutable SQLite URI used below.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_JSON = ROOT.parent / "UEX专有名词中英对照.json"
OUTPUT_JSON = ROOT / "src" / "Arkanis.Overlay.Host.Desktop" / "wwwroot" / "localization" / "UEX专有名词补充汉化.json"
DATABASE = Path(os.environ.get(
    "ARKANIS_OVERLAY_DB",
    r"C:\Users\77941\AppData\Local\ArkanisOverlay\data\Overlay.db",
))


COMMODITY_TRANSLATIONS = {
    "Atacamite": "氯铜矿",
    "CK13-GID Seed Blend": "CK13-GID 种子混合物",
    "Caranite": "卡拉奈特",
    "Caranite (Raw)": "卡拉奈特原矿",
    "Cobalt (Raw)": "钴原矿",
    "Construction Material Pebbles": "建筑材料碎石",
    "Construction Material Rubble": "建筑材料瓦砾",
    "Construction Material Salvage": "建筑材料回收料",
    "CryoPod": "冷冻舱",
    "DCSR2": "DCSR2 物资",
    "Ice (Raw)": "原冰",
    "Lastaphrene": "拉斯塔弗烯",
    "Luminalia Gift": "光明节礼物",
    "Ouratite (Raw)": "欧拉特烃原矿",
    "Partillium": "帕提利姆",
    "Redfin Energy Modulators": "红鳍能量调制器",
    "Ship Ammunition": "舰载弹药",
    "Ship Ammunition - Size 1": "舰载弹药 - 尺寸 1",
    "Ship Ammunition - Size 2": "舰载弹药 - 尺寸 2",
    "Ship Ammunition - Size 3": "舰载弹药 - 尺寸 3",
    "Ship Ammunition - Size 4": "舰载弹药 - 尺寸 4",
    "Ship Ammunition - Size 5": "舰载弹药 - 尺寸 5",
    "Ship Ammunition - Size 6": "舰载弹药 - 尺寸 6",
    "Ship Ammunition - Size 7": "舰载弹药 - 尺寸 7",
    "Silicon (Raw)": "硅原矿",
    "Stileron (Raw)": "稀钛铁原矿",
    "Sunset Berries": "日落浆果",
    "Year of the Dog Envelope": "狗年红包",
    "Year of the Monkey Envelope": "猴年红包",
    "Year of the Pig Envelope": "猪年红包",
    "Year of the Rat Envelope": "鼠年红包",
    "Year of the Rooster Envelope": "鸡年红包",
}


VEHICLE_TRANSLATIONS = {
    "600i Explorer": "起源 600i 探索版",
    "ATLS IKTI GEO": "南船座 ATLS IKTI 地质型",
    "ATLS IKTI GEO Rad": "南船座 ATLS IKTI 地质辐射型",
    "Ares Inferno Starfighter": "十字军 战神 炎魔星际战斗机",
    "Ares Ion Starfighter": "十字军 战神 离子星际战斗机",
    "Aurora Mk I CL": "RSI 极光 Mk I CL",
    "Aurora Mk I ES": "RSI 极光 Mk I ES",
    "Aurora Mk I LN": "RSI 极光 Mk I LN",
    "Aurora Mk I LX": "RSI 极光 Mk I LX",
    "Aurora Mk I MR": "RSI 极光 Mk I MR",
    "Auxilia": "辅助者",
    "CSV-FM": "阿格 CSV-FM",
    "Caterpillar Best In Show Edition": "德雷克 毛毛虫 最佳展示版",
    "Caterpillar Pirate Edition": "德雷克 毛毛虫 海盗版",
    "Cutlass Black Best In Show Edition": "德雷克 弯刀黑 最佳展示版",
    "Dragonfly Black": "德雷克 蜻蜓 黑色版",
    "Endeavor Fuel Bay Pod": "MISC 奋进 燃料舱模块",
    "Endeavor General Research Pod": "MISC 奋进 通用研究舱模块",
    "Endeavor Landing Bay Pod": "MISC 奋进 着陆舱模块",
    "Endeavor Medical Bay Pod": "MISC 奋进 医疗舱模块",
    "Endeavor Telescope Array Bay Pod": "MISC 奋进 望远镜阵列舱模块",
    "F7C-M Super Hornet Heartseeker Mk I": "铁砧 F7C-M 超级大黄蜂 寻心者 Mk I",
    "Galaxy Cargo Module": "RSI 银河 货运模块",
    "Galaxy Medical Module": "RSI 银河 医疗模块",
    "Galaxy Refinery Module": "RSI 银河 精炼模块",
    "Hammerhead Best In Show Edition": "圣盾 锤头鲨 最佳展示版",
    "MOLE Carbon Edition": "南船座 莫尔 碳素版",
    "MOLE Talus Edition": "南船座 莫尔 山岩版",
    "Mustang Alpha Vindicator": "起源 野马阿尔法 维京征服者版",
    "Nautilus Solstice Edition": "圣盾 鹦鹉螺 至日版",
    "Nova Tank": "腾博 新星坦克",
    "Orion": "RSI 猎户座",
    "Ranger CV": "腾博 游骑兵 CV",
    "Ranger RC": "腾博 游骑兵 RC",
    "Reclaimer Best In Show Edition": "圣盾 回收者 最佳展示版",
    "Retaliator Cargo Module - Bow": "圣盾 报复者 货运模块 - 前部",
    "Retaliator Cargo Module - Stern": "圣盾 报复者 货运模块 - 后部",
    "Retaliator Dropship Front Module": "圣盾 报复者 登陆艇前部模块",
    "Retaliator Living Front Module": "圣盾 报复者 生活前部模块",
    "Retaliator Living Rear Module": "圣盾 报复者 生活后部模块",
    "Retaliator Torpedo Module - Bow": "圣盾 报复者 鱼雷模块 - 前部",
    "Retaliator Torpedo Module - Stern": "圣盾 报复者 鱼雷模块 - 后部",
    "Retaliator Torpedo Module �C Bow": "圣盾 报复者 鱼雷模块 - 前部",
    "Retaliator Torpedo Module �C Stern": "圣盾 报复者 鱼雷模块 - 后部",
    "San'tok.yai": "异星 圣托凯",
    "San tok.Y��i": "阿欧泊亚 圣托凯",
    "Starlancer BLD": "MISC 星际枪骑兵 BLD",
    "Valkyrie Liberator Edition": "铁砧 女武神 解放者版",
}


LOCATION_TRANSLATIONS = {
    # Star systems, planets, moons, and cities.
    "Nyx": "尼克斯", "Pyro": "派罗", "Stanton": "斯坦顿",
    "ArcCorp": "弧光集团", "Bloom": "盛放星", "Crusader": "十字军星", "Delamar": "德拉玛",
    "Hurston": "赫斯顿", "MicroTech": "微科星", "Monox": "殁氧星", "Pyro I": "派罗 I",
    "Pyro IV": "派罗 IV", "Pyro V": "派罗 V", "Terminus": "端点星",
    "Aberdeen": "阿伯丁", "Adir": "阿迪尔", "Arial": "艾瑞尔", "Calliope": "卡利俄佩",
    "Cellin": "赛琳", "Clio": "克利俄", "Daymar": "戴玛尔", "Euterpe": "欧忒耳佩",
    "Fairo": "法伊罗", "Fuego": "弗果", "Ignis": "伊格尼斯", "Ita": "依塔", "Lyria": "莉瑞雅",
    "Magda": "玛格达", "Vatra": "瓦塔拉", "Vuur": "伏尔", "Wala": "瓦菈", "Yela": "耶拉",
    "Area 18": "18 区", "Levski": "列夫斯基", "Lorville": "罗威尔", "New Babbage": "新巴贝奇", "Orison": "奥里森",

    # Space stations.
    "ARC-L1 Wide Forest Station": "弧光 L1 广袤森林站",
    "ARC-L2 Lively Pathway Station": "弧光 L2 活力小径站",
    "ARC-L3 Modern Express Station": "弧光 L3 现代快线站",
    "ARC-L4 Faint Glen Station": "弧光 L4 淡幽谷站",
    "ARC-L5 Yellow Core Station": "弧光 L5 黄核站",
    "Baijini Point": "拜吉尼角", "CRU-L1 Ambitious Dream Station": "十字军 L1 雄心伟梦站",
    "CRU-L4 Shallow Fields Station": "十字军 L4 浅野站", "CRU-L5 Beautiful Glen Station": "十字军 L5 美丽幽谷站",
    "Checkmate Station": "将死站", "Dudley & Daughters": "达德利父女站", "Endgame": "终局站",
    "Everus Harbor": "埃弗勒斯空间站", "Gaslight": "煤气灯站", "Green Imperial Housing Exchange": "绿色帝国住房交易所",
    "HUR-L1 Green Glade Station": "赫斯顿 L1 绿色林地站", "HUR-L2 Faithful Dream Station": "赫斯顿 L2 忠诚之梦站",
    "HUR-L3 Thundering Express Station": "赫斯顿 L3 雷鸣快线站", "HUR-L4 Melodic Fields Station": "赫斯顿 L4 旋律田野站",
    "HUR-L5 High Course Station": "赫斯顿 L5 高阶航道站", "INS Jericho": "INS 杰里科",
    "MIC-L1 Shallow Frontier Station": "微科 L1 浅边站", "MIC-L2 Long Forest Station": "微科 L2 长林站",
    "MIC-L3 Endless Odyssey Station": "微科 L3 无尽奥德赛站", "MIC-L4 Red Crossroads Station": "微科 L4 红色十字路口站",
    "MIC-L5 Modern Icarus Station": "微科 L5 现代伊卡洛斯站", "Megumi Refueling": "惠美补给站",
    "Nyx Gateway (Pyro)": "尼克斯门户（派罗）", "Nyx Gateway (Stanton)": "尼克斯门户（斯坦顿）",
    "Orbituary": "轨道殡仪馆", "Patch City": "补丁城", "People's Service Station Alpha": "人民服务站阿尔法",
    "People's Service Station Delta": "人民服务站德尔塔", "People's Service Station Lambda": "人民服务站兰布达",
    "People's Service Station Theta": "人民服务站西塔", "Port Tressler": "特雷斯勒港",
    "Pyro Gateway (Nyx)": "派罗门户（尼克斯）", "Pyro Gateway (Stanton)": "派罗门户（斯坦顿）",
    "Rat's Nest": "鼠巢", "Rod's Fuel 'N Supplies": "罗德燃料与补给", "Ruin Station": "废墟站",
    "Seraphim Station": "炽天使站", "Stanton Gateway (Nyx)": "斯坦顿门户（尼克斯）",
    "Stanton Gateway (Pyro)": "斯坦顿门户（派罗）", "Starlight Service Station": "星光服务站",
    "Terra Gateway (Stanton)": "泰拉门户（斯坦顿）", "Wikelo Emporium Dasi Station": "维科洛商店达西站",
    "Wikelo Emporium Kinga Station": "维科洛商店金加站", "Wikelo Emporium Selo Station": "维科洛商店塞洛站",
    "PYAM-FARSTAT-1-2": "派罗远星站 1-2", "PYAM-FARSTAT-1-3": "派罗远星站 1-3",
    "PYAM-FARSTAT-1-5": "派罗远星站 1-5", "PYAM-FARSTAT-2-3": "派罗远星站 2-3",
    "PYAM-FARSTAT-3-5": "派罗远星站 3-5", "PYAM-FARSTAT-5-1": "派罗远星站 5-1",
    "PYAM-FARSTAT-5-3": "派罗远星站 5-3", "PYAM-FARSTAT-6-2": "派罗远星站 6-2",
    "PYAM-SUPVISR-3-4": "派罗监管站 3-4", "PYAM-SUPVISR-3-5": "派罗监管站 3-5",

    # Outposts and surface locations.
    "ArcCorp Mining Area 045": "弧光集团采矿区 045", "ArcCorp Mining Area 048": "弧光集团采矿区 048",
    "ArcCorp Mining Area 056": "弧光集团采矿区 056", "ArcCorp Mining Area 061": "弧光集团采矿区 061",
    "ArcCorp Mining Area 141": "弧光集团采矿区 141", "ArcCorp Mining Area 157": "弧光集团采矿区 157",
    "Arid Reach": "干旱地带", "Ashland": "灰烬之地", "Astor's Clearing": "阿斯特空地",
    "Benson Mining Outpost": "本森采矿前哨", "Blackrock Exchange": "黑岩交易所", "Bloodshot Ridge": "血眼山脊",
    "Bountiful Harvest Hydroponics": "丰收水培农场", "Brio's Breaker Yard": "布里奥拆船场", "Bud's Growery": "巴德种植园",
    "Bueno Ravine": "布埃诺峡谷", "Bullock's Reach": "布洛克地带", "Canard View": "卡纳德观景点",
    "Carver's Ridge": "卡弗山脊", "Chawla's Beach": "查瓦拉海滩", "Cutter's Rig": "卡特钻井平台",
    "Deakins Research": "迪金斯研究站", "Devlin Scrap & Salvage": "德夫林废料与打捞", "Dunboro": "邓伯勒",
    "Fallow Field": "休耕田", "Feo Canyon Depot": "费奥峡谷仓站", "Finn's Folly": "芬恩愚行地",
    "Frigid Knot": "寒霜结", "Frostbite": "冻伤", "Gallete Family Farms": "加莱特家族农场",
    "Ghost Hollow": "幽灵洼地", "Goner's Deal": "失意者交易", "Gray Gardens Depot": "灰色花园仓站",
    "HDMS-Anderson": "HDMS-安德森", "HDMS-Bezdek": "HDMS-贝兹德克", "HDMS-Edmond": "HDMS-埃德蒙",
    "HDMS-Hadley": "HDMS-哈德利", "HDMS-Hahn": "HDMS-哈恩", "HDMS-Lathan": "HDMS-莱森",
    "HDMS-Norgaard": "HDMS-诺高德", "HDMS-Oparei": "HDMS-奥帕雷", "HDMS-Perlman": "HDMS-珀尔曼",
    "HDMS-Pinewood": "HDMS-松林", "HDMS-Ryder": "HDMS-莱德", "HDMS-Stanhope": "HDMS-斯坦霍普",
    "HDMS-Thedus": "HDMS-西德斯", "HDMS-Woodruff": "HDMS-伍德拉夫", "Harper's Point": "哈珀角",
    "Hickes Research": "希克斯研究站", "Humboldt Mines": "洪堡矿场", "Jackson's Swap": "杰克逊交易点",
    "Jumptown": "跳跃镇", "Kabir's Post": "卡比尔哨站", "Kinder Plots": "金德农地", "Kudre Ore": "库德雷矿场",
    "Last Ditch": "最后一沟", "Last Landings": "最后着陆点", "Loveridge Mineral Reserve": "洛夫里奇矿藏",
    "Ludlow": "勒德洛", "Maker's Point": "梅克角", "Moreland Hills": "莫尔兰丘陵", "NT-999-XX": "NT-999-XX",
    "NT-999-XXII": "NT-999-XXII", "Narena's Rest": "纳雷娜休憩地", "Nuen Waste Management": "纽恩废物处理站",
    "Ostler's Claim": "奥斯特勒矿权", "Outpost 54": "前哨站 54", "Paradise Cove": "天堂湾",
    "Picker's Field": "采集者田地", "Private Property": "私人领地", "Prophet's Peak": "先知峰",
    "Prospect Depot": "勘探仓站", "Rappel": "绳降", "Raven's Roost": "渡鸦巢",
    "Rayari Anvik Research Outpost": "雷亚里安维克研究前哨", "Rayari Cantwell Research Outpost": "雷亚里坎特韦尔研究前哨",
    "Rayari Deltana Research Outpost": "雷亚里德尔塔娜研究前哨", "Rayari Kaltag Research Outpost": "雷亚里卡尔塔格研究前哨",
    "Rayari McGrath Research Outpost": "雷亚里麦格拉斯研究前哨", "Razor's Edge": "剃刀边缘",
    "Reclamation & Disposal Orinth": "回收与处理奥林斯", "Rough Landing": "粗暴着陆点", "Rustville": "锈镇",
    "Sacren's Plot": "萨克伦地块", "Sakura Sun Goldenrod Workcenter": "樱日金杆工作中心",
    "Sakura Sun Magnolia Workcenter": "樱日木兰工作中心", "Samson & Son's Salvage Center": "萨姆森父子打捞中心",
    "Scarper's Turn": "逃亡者转角", "Seer's Canyon": "先知峡谷", "Shadowfall": "暗影坠落",
    "Shady Glen": "阴影幽谷", "Shepherd's Rest": "牧羊人休息地", "Shubin Mining Facility SAL-2": "舒宾采矿设施 SAL-2",
    "Shubin Mining Facility SAL-5": "舒宾采矿设施 SAL-5", "Shubin Mining Facility SCD-1": "舒宾采矿设施 SCD-1",
    "Shubin Mining Facility SM0-10": "舒宾采矿设施 SM0-10", "Shubin Mining Facility SM0-13": "舒宾采矿设施 SM0-13",
    "Shubin Mining Facility SM0-18": "舒宾采矿设施 SM0-18", "Shubin Mining Facility SM0-22": "舒宾采矿设施 SM0-22",
    "Shubin Mining Facility SMCa-6": "舒宾采矿设施 SMCa-6", "Shubin Mining Facility SMCa-8": "舒宾采矿设施 SMCa-8",
    "Slowburn Depot": "慢燃仓站", "Stag's Rut": "雄鹿辙", "Stonetree": "石树", "Sunset Mesa": "日落台地",
    "Terra Mills HydroFarm": "泰拉磨坊水培农场", "The Golden Riviera": "黄金里维埃拉", "The Necropolis": "死城",
    "The Orphanage": "孤儿院", "The Yard": "堆场", "Tram & Myers Mining": "特拉姆与迈尔斯采矿",
    "Weeping Cove": "哭泣湾", "Windfall": "意外之财", "Yang's Place": "杨氏地点", "Zephyr": "和风",
}


# The UEX terminal endpoint composes service labels with the named places above. Translate the reusable labels
# separately, so newly added terminals remain readable even before a future supplemental-data refresh.
TERMINAL_PHRASES = {
    "Landing Services": "着陆服务", "Landing Service": "着陆服务", "Admin": "管理", "Administration": "管理处",
    "Cargo Center": "货运中心", "Cargo Deck": "货运甲板", "Cargo Elevator": "货运电梯", "Cargo Terminal": "货运终端",
    "Cargo": "货运", "Terminal": "终端", "Station": "空间站", "Gateway": "门户", "Service Station": "服务站",
    "Services": "服务", "Service": "服务", "Refinery": "精炼厂", "Refinement": "精炼", "Processing": "加工",
    "Mining Area": "采矿区", "Mining Facility": "采矿设施", "Mining Outpost": "采矿前哨", "Mining": "采矿",
    "Research Outpost": "研究前哨", "Research": "研究", "Medical": "医疗", "Pharmacy": "药房", "Hospital": "医院",
    "Weapons": "武器", "Weapon": "武器", "Armor": "护甲", "Clothing": "服装", "Parts": "零件", "Supplies": "补给",
    "Rentals": "租赁", "Rental": "租赁", "Sales": "销售", "Shop": "商店", "Outlet": "直营店", "Showroom": "展厅",
    "Bar": "酒吧", "Noodle": "面馆", "Noodles": "面馆", "Pizza": "披萨", "Burrito": "卷饼", "Coffee": "咖啡",
    "Juice": "果汁", "Beer": "啤酒", "Food": "餐饮", "Refreshments": "茶点", "Convenience": "便利店",
    "Fuel": "燃料", "Refueling": "补给", "Trade": "贸易", "Exchange": "交易所", "Deal": "交易",
    "Depot": "仓站", "Outpost": "前哨", "Facility": "设施", "Center": "中心", "Office": "办事处",
    "Residences": "住宅区", "Housing": "住房", "Metro Center": "地铁中心", "Spaceport": "太空港",
    "City": "城", "District": "区", "Platform": "平台", "Bay": "港湾", "Point": "角", "View": "观景点",
    "Canyon": "峡谷", "Ridge": "山脊", "Field": "田地", "Fields": "田野", "Forest": "森林", "Glen": "幽谷",
    "Hills": "丘陵", "Cove": "海湾", "Ravine": "峡谷", "Beach": "海滩", "Peak": "峰", "Mesa": "台地",
    "Nest": "巢", "Roost": "栖地", "Rest": "休憩地", "Reach": "地带", "Landing": "着陆点", "Landings": "着陆点",
    "Ruin": "废墟", "Rubble": "瓦砾", "Scrap": "废料", "Salvage": "打捞", "Disposal": "处理",
    "Waste": "废物", "HydroFarm": "水培农场", "Hydrofarm": "水培农场", "Growery": "种植园", "Farms": "农场",
    "Family": "家族", "Private": "私人", "Property": "领地", "Personal": "个人", "Imperial": "帝国",
    "People's": "人民", "Alpha": "阿尔法", "Delta": "德尔塔", "Lambda": "兰布达", "Theta": "西塔",
    "North": "北", "South": "南", "East": "东", "West": "西", "Front": "前部", "Rear": "后部", "Bow": "前部", "Stern": "后部",
    "General": "通用", "Living": "生活", "Dropship": "登陆艇", "Torpedo": "鱼雷", "Module": "模块",
    "Best In Show Edition": "最佳展示版", "Pirate Edition": "海盗版", "Liberator Edition": "解放者版",
    "Carbon Edition": "碳素版", "Talus Edition": "山岩版", "Solstice Edition": "至日版", "Explorer": "探索版",
    "Rad": "辐射型", "GEO": "地质型", "Starfighter": "星际战斗机", "Tank": "坦克",
    "Covalex": "科瓦莱克斯", "Casaba": "卡萨巴", "CenterMass": "中心质量", "Ellroy's": "埃尔罗伊的",
    "Dumper's": "倾倒者的", "Kel-To": "凯尔托", "Live": "活力", "Fire": "火焰", "Gaslight": "煤气灯",
    "Grubs": "幼虫", "Hot": "热辣", "Dogs": "热狗", "Platinum": "铂金", "Arkanis": "阿卡尼斯",
    "Rayari": "雷亚里", "Shubin": "舒宾", "TDD": "贸易发展部", "Tammany": "塔曼尼", "Teasa": "提萨",
    "Riker": "莱克", "Riker Memorial": "莱克纪念馆", "Nerena": "纳雷娜", "Narena": "纳雷娜",
    "Dunlow": "邓洛", "Dunboro": "邓伯勒", "Orinth": "奥林斯", "Makau": "马考", "Mills": "磨坊",
    "Kudre": "库德雷", "Pinewood": "松林", "Sakura": "樱花", "Magnolia": "木兰", "Goldenrod": "金杆",
    "Wikelo": "维科洛", "Emporium": "商店", "Dasi": "达西", "Kinga": "金加", "Selo": "塞洛",
    "Dudley": "达德利", "Daughters": "女儿们", "Rod's": "罗德的", "Rat's": "鼠的", "Endgame": "终局",
    "Checkmate": "将死", "Orbituary": "轨道殡仪馆", "Patch": "补丁", "Starlight": "星光", "Terra": "泰拉",
    "FARSTAT": "远星站", "SUPVISR": "监管站", "PYAM": "派罗", "HDMS": "HDMS", "INS": "INS",
}


REPOSITORIES = {
    "commodities": ("UexCommoditySyncRepository", ("name",)),
    "vehicles": ("UexSpaceShipSyncRepository", ("name", "name_full")),
    "locations": ("UexStarSystemSyncRepository", ("name",)),
    "locations_planets": ("UexPlanetSyncRepository", ("name",)),
    "locations_moons": ("UexMoonSyncRepository", ("name",)),
    "locations_cities": ("UexCitySyncRepository", ("name",)),
    "locations_stations": ("UexSpaceStationSyncRepository", ("name",)),
    "locations_outposts": ("UexOutpostSyncRepository", ("name",)),
    "terminals": ("UexTerminalSyncRepository", ("name",)),
}


def read_cache() -> dict[str, list[dict]]:
    uri = DATABASE.as_uri() + "?mode=ro&immutable=1"
    connection = sqlite3.connect(uri, uri=True)
    try:
        cursor = connection.cursor()
        data = {}
        for category, (prefix, _) in REPOSITORIES.items():
            content = cursor.execute(
                "select Content from ExternalSourceDataCache where Id like ?", (prefix + "%",)
            ).fetchone()[0]
            data[category] = json.loads(content)["Result"]
        return data
    finally:
        connection.close()


def flatten_translation_source() -> dict[str, str]:
    source = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    return {
        english: chinese
        for category in source["englishToChinese"].values()
        for english, chinese in category.items()
    }


def replace_phrase(text: str, source: str, target: str) -> str:
    pattern = rf"(?<![A-Za-z0-9]){re.escape(source)}(?![A-Za-z0-9])"
    return re.sub(pattern, target, text, flags=re.IGNORECASE)


def translate_terminal(name: str, known: dict[str, str]) -> str:
    translated = name
    for english, chinese in sorted(known.items(), key=lambda pair: len(pair[0]), reverse=True):
        translated = replace_phrase(translated, english, chinese)
    for english, chinese in sorted(TERMINAL_PHRASES.items(), key=lambda pair: len(pair[0]), reverse=True):
        translated = replace_phrase(translated, english, chinese)
    translated = translated.replace(" - ", " - ").replace("(", "（").replace(")", "）")
    return translated


def collect_names(records: list[dict], fields: tuple[str, ...]) -> set[str]:
    return {record[field] for record in records for field in fields if record.get(field)}


def main() -> None:
    source = flatten_translation_source()
    cache = read_cache()
    supplement: dict[str, dict[str, str]] = defaultdict(dict)

    known = source | COMMODITY_TRANSLATIONS | VEHICLE_TRANSLATIONS | LOCATION_TRANSLATIONS

    for name in collect_names(cache["commodities"], ("name",)):
        if name not in source:
            supplement["commodities"][name] = known.get(name, name)

    for vehicle in cache["vehicles"]:
        short_name = vehicle.get("name")
        full_name = vehicle.get("name_full")
        if not short_name:
            continue
        translated = known.get(short_name, short_name)
        if short_name not in source:
            supplement["vehicles"][short_name] = translated
        if full_name and full_name not in source:
            supplement["vehicles"][full_name] = translated

    for category in ("locations", "locations_planets", "locations_moons", "locations_cities", "locations_stations", "locations_outposts"):
        for name in collect_names(cache[category], ("name",)):
            if name not in source:
                supplement["locations"][name] = known.get(name, name)

    terminal_known = known | supplement["locations"] | source
    for name in collect_names(cache["terminals"], ("name",)):
        if name not in source:
            supplement["terminals"][name] = translate_terminal(name, terminal_known)

    unresolved = {
        category: sorted(name for name, translated in values.items() if not re.search(r"[\u3400-\u9fff]", translated))
        for category, values in supplement.items()
    }
    unresolved = {category: names for category, names in unresolved.items() if names}
    if unresolved:
        raise RuntimeError("Untranslated UEX entities:\n" + json.dumps(unresolved, ensure_ascii=False, indent=2))

    payload = {
        "schemaVersion": 1,
        "generatedAt": datetime.now(UTC).isoformat(),
        "source": {
            "primaryTerms": "UEX专有名词中英对照.json",
            "communityTranslation": "社区翻译对照.ini",
            "uexCache": "Overlay.db (read-only)",
            "selection": "补齐本机 UEX 缓存中的商品、载具、地点、终端；保留英文代码和型号。",
        },
        "englishToChinese": {category: dict(sorted(values.items())) for category, values in sorted(supplement.items())},
    }
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON}")
    for category, values in payload["englishToChinese"].items():
        print(f"{category}: {len(values)}")


if __name__ == "__main__":
    main()
