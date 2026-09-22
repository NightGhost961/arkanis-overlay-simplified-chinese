(() => {
    "use strict";

    // This patch deliberately translates only application chrome. Game names are translated in C# from the
    // community terminology file, so live UEX data remains searchable with its original English values.
    const terms = Object.freeze({
        "Search": "搜索",
        "Hub": "中心",
        "Close": "关闭",
        "Inventory": "库存",
        "Trade": "贸易",
        "Mining": "采矿",
        "Market": "市场",
        "Hangar": "机库",
        "Org": "组织",
        "Settings": "设置",
        "In Development": "开发中",
        "Disabled": "已禁用",
        "Find anything you're looking for.": "搜索你需要的任何内容。",
        "See what's going on around you.": "查看周边动态。",
        "Close the Overlay.": "关闭悬浮窗。",
        "Track and manage your Inventory.": "追踪并管理库存。",
        "Plan your next Haul.": "规划下一趟货运。",
        "Manage your Mining Operations.": "管理采矿作业。",
        "Trade with other players.": "与其他玩家交易。",
        "Manage your Fleet.": "管理舰队。",
        "Manage your Organization.": "管理组织。",
        "Configure the Overlay.": "配置悬浮窗。",
        "In Progress": "进行中",
        "Route Search": "路线搜索",
        "Ledger": "账本",
        "Transport vehicle": "运输载具",
        "Search for a game vehicle": "搜索游戏载具",
        "Capacity": "容量",
        "in SCUs": "单位：SCU",
        "Commodity": "商品",
        "Search for a game commodity": "搜索游戏商品",
        "Origin location": "起点位置",
        "Destination location": "终点位置",
        "Search for a game location": "搜索游戏位置",
        "Minimum origin stock": "起点最低库存",
        "Maximum destination stock": "终点最高库存",
        "Any stock status": "任意库存状态",
        "Cargo capacity": "货舱容量",
        "Create trade run": "创建贸易行程",
        "Application": "应用程序",
        "Overlay": "悬浮窗",
        "Locale": "区域与语言",
        "Preferences": "偏好设置",
        "Save": "保存",
        "Cancel": "取消",
        "Auto-start on system boot": "随系统启动",
        "Terminate on game exit": "游戏退出时关闭",
        "Update channel": "更新通道",
        "Configure the usage analytics options": "配置使用分析选项",
        "Blur overlay background": "模糊悬浮窗背景",
        "Overlay language": "悬浮窗语言",
        "Display format region": "显示格式区域",
        "Overlay toggle shortcut": "悬浮窗开关快捷键",
        "Cache management": "缓存管理",
        "Game entity": "游戏条目",
        "Search for game entity": "搜索游戏条目",
        "Unknown": "未知",
        "No matching game entities": "没有匹配的游戏条目",
        "Location": "位置",
        "Vehicle": "载具",
        "Item or commodity": "物品或商品",
        "Item or commodity name": "物品或商品名称",
        "Vehicle name": "载具名称",
        "Amount": "数量",
        "Unit": "单位",
        "Entity": "条目",
        "Manufacturer": "制造商",
        "Type": "类型",
        "Price": "价格",
        "Reported": "报告时间",
        "All available prices": "所有可用价格",
        "Max sell": "最高售价",
        "Min buy": "最低买价",
        "Min rent": "最低租赁价",
        "Manage inventory": "管理库存",
        "Unassigned inventory entries": "未分配库存条目",
        "Add new entry": "添加新条目",
        "Update": "更新",
        "Modify": "修改",
        "Remove": "移除",
        "Transfer": "转移",
        "Change Hangar": "更换机库",
        "Bulk remove": "批量移除",
        "Bulk transfer": "批量转移",
        "Bulk assign list": "批量分配清单",
        "All Inventory": "全部库存",
        "Inventory entries": "库存条目",
        "Equipped modules": "已装备组件",
        "Pledged": "已认领",
        "Loaner": "借用",
        "Custom name": "自定义名称",
        "List name": "清单名称",
        "Notes": "备注",
        "Inventory List": "库存清单",
        "Select an inventory list": "选择库存清单",
        "Secret Key": "密钥",
        "Success!": "成功！",
        "Shutdown": "关闭程序",
        "Error Details": "错误详情",
        "Application auto-update disabled.": "应用自动更新已禁用。",
        "Program version": "程序版本",
        "Copy result to clipboard": "复制结果到剪贴板",
        "The evaluation result": "计算结果",
        "within": "位于",
        "from": "从",
        "to": "到",
        "Missing": "缺失",
        "N/A": "不适用",
        "Item": "物品",
        "Items": "物品",
        "Commodity": "商品",
        "Commodities": "商品",
        "Location": "位置",
        "Locations": "位置",
        "Company": "公司",
        "Companies": "公司",
        "Space Ship": "飞船",
        "Space Ships": "飞船",
        "Ground Vehicle": "地面载具",
        "Ground Vehicles": "地面载具"
    });

    const attributes = ["aria-label", "placeholder", "title"];

    const translate = value => {
        if (!value) return value;
        const leading = value.match(/^\s*/)[0];
        const trailing = value.match(/\s*$/)[0];
        const trimmed = value.trim();
        if (terms[trimmed]) return `${leading}${terms[trimmed]}${trailing}`;

        const resultMatch = trimmed.match(/^Found (\d+) results in (.+)$/);
        return resultMatch ? `${leading}找到 ${resultMatch[1]} 个结果，用时 ${resultMatch[2]}${trailing}` : value;
    };

    const translateElement = element => {
        for (const attribute of attributes) {
            if (element.hasAttribute(attribute)) {
                const currentValue = element.getAttribute(attribute);
                const translatedValue = translate(currentValue);
                // Attribute changes are observed below. Writing the same value would queue another
                // mutation and create a self-sustaining WebView rendering loop.
                if (translatedValue !== currentValue) {
                    element.setAttribute(attribute, translatedValue);
                }
            }
        }
    };

    const translateTree = root => {
        if (root.nodeType === Node.TEXT_NODE) {
            const translatedValue = translate(root.nodeValue);
            if (translatedValue !== root.nodeValue) root.nodeValue = translatedValue;
            return;
        }
        if (root.nodeType !== Node.ELEMENT_NODE && root.nodeType !== Node.DOCUMENT_FRAGMENT_NODE) return;

        if (root.nodeType === Node.ELEMENT_NODE) translateElement(root);
        const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT);
        while (walker.nextNode()) {
            if (walker.currentNode.nodeType === Node.TEXT_NODE) {
                const currentValue = walker.currentNode.nodeValue;
                const translatedValue = translate(currentValue);
                if (translatedValue !== currentValue) walker.currentNode.nodeValue = translatedValue;
            } else {
                translateElement(walker.currentNode);
            }
        }
    };

    const start = () => {
        document.documentElement.lang = "zh-CN";
        document.documentElement.style.fontFamily = "Microsoft YaHei UI, Microsoft YaHei, Segoe UI, sans-serif";
        translateTree(document.body);
        new MutationObserver(records => {
            for (const record of records) {
                if (record.type === "attributes") translateElement(record.target);
                for (const node of record.addedNodes) translateTree(node);
            }
        }).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: attributes });
    };

    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start, { once: true });
    else start();
})();
