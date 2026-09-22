<h1 align="center">
<a href="https://arkanis.cc/overlay" target="_blank">Arkanis Overlay</a>
简体中文便携版（非官方）
</h1>

<p align="center">
<a href="../../releases/latest"><img alt="GitHub 最新 Release" src="https://img.shields.io/github/v/release/NightGhost961/arkanis-overlay-simplified-chinese?display_name=tag&label=Release&logo=github" /></a>
<img alt="许可证" src="https://img.shields.io/badge/license-PolyForm%20Noncommercial%201.0.0-blue" />
<a href="https://github.com/ArkanisCorporation/ArkanisOverlay" target="_blank"><img alt="上游项目" src="https://img.shields.io/badge/upstream-ArkanisOverlay-181717?logo=github" /></a>
</p>

<h3 align="center">
为《星际公民》打造的新一代游戏内辅助悬浮层<br>
</h3>

<h6 align="center">
上游项目由 <a href="https://discord.com/users/174617873182883841" target="_blank"><b>FatalMerlin</b></a>
和 <a href="https://discord.com/users/224580858432978944" target="_blank"><b>TheKronnY</b></a> 创建；<br/>
本仓库为独立维护的非官方简体中文适配与便携构建。
</h6>

> [!WARNING]
> 本仓库不是 Arkanis Corporation、Cloud Imperium Games 或 UEX Corporation 的官方产品、官方翻译或获得背书的项目。完整上游署名、术语来源和商标说明见 [ATTRIBUTIONS.md](ATTRIBUTIONS.md)。

---

## 🚀 Arkanis Overlay 是什么？

**Arkanis Overlay** 是一款以易用性为核心、面向 **《星际公民》** 的游戏内辅助悬浮层。它让玩家无需频繁切出游戏或在多个网页之间切换，也能快速获得常用工具和信息。

该项目受到《逃离塔科夫》社区工具 [RatScanner](https://ratscanner.com/) 的启发，强调可靠性、可扩展性和社区协作。它仍在积极开发中，核心目标是：

> **减少操作阻力，保持沉浸体验。**

本仓库在上游源码基础上加入简体中文界面、中文实体显示、中文同义词搜索和 UEX 术语补充资源，并发布自带运行时的 Windows 便携包。

---

## 📦 下载与运行本便携版

在 [Releases 页面](../../releases/latest) 下载最新的 `zh-CN` 便携 ZIP。当前包的 SHA-256：

```text
4CC0145BD9EC96259C00FA4B20DBDCD9BEC68696B200A5E0FC6FF95764DEB628
```

它是自带 .NET 运行时的 `win-x64` 包，而不是上游安装器：

1. 下载 Release 中的 ZIP。
2. 解压到一个新建的独立文件夹。
3. 运行 `ArkanisOverlay.exe`。

请勿将文件覆盖到官方安装目录，也不要与官方自动更新目录混用。本适配版不会修改《星际公民》客户端。GitHub 自动生成的 `Source code (zip/tar.gz)` 仅是源码快照，不能替代便携包。

---

## ✨ 核心功能

- **游戏内搜索工具**
  — 快速检索常用游戏信息，减少在网页之间切换的次数。

- **社区数据整合**
  — 对接 [UEX Corporation][uex] 数据，并为后续社区工具整合预留扩展空间。

- **简体中文界面与实体显示**
  — 常用导航、搜索、贸易、库存、机库和设置控件显示为简体中文；商品、载具、地点和终端等实体以“中文（English）”显示，便于核对原名。

- **中文同义词搜索**
  — 输入中文地点、商品或载具名时，会扩展为对应 UEX 英文实体名进行匹配，而不是要求中英文同时命中。

- **Windows 托盘与悬浮层体验**
  — 程序通常驻留在系统托盘，可通过默认快捷键 `左 Alt + 左 Shift + S` 打开悬浮层；快捷键可在设置中调整。

- **设置窗口修复**
  — 修复中文脚本重复写入 DOM 属性导致 Preferences 可能持续停在 `Loading` 的问题。

本版构建时对本机 UEX 缓存的术语审计为 **1,747 / 1,747** 个实体名称具备中文主译名：205 个商品、560 个载具名称/全称、3 个星系、11 个行星、18 个月球、5 座城市、59 个空间站、115 个前哨站和 771 个终端。

## 🤝 社区与公开源码

本仓库公开源码，用于审计、复现构建、提交术语修正和报告问题。欢迎任何可核对的贡献：翻译修订、中文搜索复现步骤、测试结果和构建改进都很有价值。

请不要提交《星际公民》游戏文件、账户信息、访问令牌或含个人信息的原始日志。上游项目与贡献方式见 [ArkanisCorporation/ArkanisOverlay](https://github.com/ArkanisCorporation/ArkanisOverlay)；本适配版的问题请优先在本仓库提交。

## 🖥️ 技术栈

- Microsoft **.NET 10**
  — 本构建使用项目要求的 .NET SDK `10.0.301`。

- **WPF 承载的 Blazor Windows 应用**
  — 以 C#、WPF、WebView2 和 Blazor 构建客户端界面。

- **ASP.NET Core 服务端**
  — 为后续服务端和数据整合能力提供基础。

> [!TIP]
> 上游的浏览器演示可在 [overlay.arkanis.cc][overlay-demo] 查看。它不代表本仓库的简体中文脚本、术语资源或便携包版本。

---

## 🛠️ 从源码构建

项目要求 .NET SDK `10.0.301`。PowerShell 示例：

```powershell
$env:PATH = "$PWD\.dotnet;$env:PATH"
dotnet test .\tests\Arkanis.Overlay.Host.Desktop.UnitTests\Arkanis.Overlay.Host.Desktop.UnitTests.csproj --configuration Release --no-restore
dotnet publish .\src\Arkanis.Overlay.Host.Desktop\Arkanis.Overlay.Host.Desktop.csproj --runtime win-x64 --configuration Release --self-contained true --output .\publish-zh-cn
```

`tools/generate_uex_supplement.py` 以只读模式读取本机 Overlay 缓存，并从 `UEX专有名词中英对照.json` 生成 `UEX专有名词补充汉化.json`。仅在你有权使用相关术语数据时再分发生成结果。

### 程序行为与设置

程序启动后通常驻留在 **Windows 系统托盘**，不会默认显示主窗口。可从托盘菜单打开设置窗口或退出程序。

设置中可调整的项目包括：

- 是否随 Windows 自动启动；
- 星战关闭时是否自动退出 Overlay；
- 打开悬浮层的快捷键；
- 其他与外观和行为相关的应用选项。

---

## 🔮 上游路线图与规划

以下内容来自上游项目规划，不代表本适配版承诺在特定时间实现。

### 🧩 核心改进

- [x] 无缝自更新安装器与更新流程（上游功能）
- [x] 用于快速打开和导航的快捷键
- [ ] 更高的可靠性与易用性
- [ ] 可配置的布局、主题与行为
- [ ] 更完善的本地化

### 🔎 更智能的搜索

- [x] 覆盖实体数据库（商品、地点、物品等）的全文搜索
- [ ] 改进模糊搜索和结果排序

### 🔗 集成与工具

- [x] 基于 [UEX Corporation][uex] 的游戏实体搜索
- [ ] [UEX CLI](https://github.com/UEXCorp/UEX-CLI) 与 MFD 屏幕整合
- [ ] 内嵌工具与服务（需要相应权限）
  - [ ] [SPViewer](https://www.spviewer.eu/)
  - [ ] [Erkul](https://www.erkul.games/)
  - [ ] [Regolith Co.](https://regolith.rocks/)
- [ ] 基于社区数据源（Wiki、JSON 导出等）的信息扩充
- [ ] Discord、组织等社交功能

### 🔍 OCR 驱动的信息能力

- [ ] UEX 数据提取（商品、物品、燃料、矿石等价格）
- [ ] [Regolith Co.](https://regolith.rocks/) 整合
- [ ] 基于玩家位置的地图感知与上下文推荐

### 🧭 长期愿景

- 玩法辅助工具：任务与进度跟踪、队伍/会话/组织管理、库存管理、笔记与规划。
- 面向第三方扩展的 **插件支持**（探索阶段）。

---

## 💡 项目理念

《星际公民》的世界很庞大，也难免令人沮丧，尤其对刚刚踏入斯坦顿及更远星系的新公民而言。**Arkanis Overlay** 不试图改变游戏，而是希望让游戏过程更顺畅。

核心原则：

- **可靠的体验**：悬浮层必须稳定，游戏本身已经有足够多的问题。
- **渐进式成长**：尽早发布，经常改进。
- **不做外挂**：项目不会包含作弊、自动化或破坏游戏平衡的功能。

## 🧑‍💻 开发状态

上游项目由 [FatalMerlin](https://github.com/FatalMerlin) 牵头，主要使用 C#、WPF、WebView2 和 Blazor 开发。本仓库的重点是维护简体中文适配、术语资源、中文搜索和便携构建。

若发现问题或想贡献功能，请在本仓库提交 Issue 或 Pull Request，并附上可复现的说明。我们尤其欢迎应用测试、翻译校对和 UI/UX 反馈。

## 🙌 社区与支持

感谢 UEX 开发团队、Arkanis Corporation 成员以及更广泛的《星际公民》社区提供的数据、测试、反馈和想法。

## 🧭 为什么叫 “Arkanis”？

这个名字致敬 **Arkanis Sector**：一片属于勇敢探索者的边疆区域。它代表了这个工具希望体现的精神——探索、实用与前沿创新。

---

## 📜 许可证、引用与 AI 协助

本项目继承上游 **PolyForm Noncommercial License 1.0.0**：

- <span style="color: green">可以</span> 在非商业用途下使用、修改和分发软件；
- <span style="color: red">不可以</span> 将软件用于商业目的，包括出售、商业业务或以金钱回报为目标的活动。

完整条款见 [LICENSE.md](LICENSE.md)。这是公开源码仓库，但并非 MIT、GPL 或其他 OSI 批准的开源许可证。

上游必需版权声明、UEX/社区术语引用和商标声明见 [ATTRIBUTIONS.md](ATTRIBUTIONS.md)。本适配版由维护者主导，使用 **OpenAI GPT-5 Codex** 协助完成代码修改、术语补全脚本、测试和文档草拟；AI 不是本项目、上游项目或术语数据的权利主体。

---

## 🌌 结语

这只是开始。Arkanis Overlay 希望与游戏和社区一同成长，让《星际公民》的旅程顺畅一点。

> *“一艘船的好坏，取决于它的船员。”*
> — 佚名

[overlay-demo]: https://overlay.arkanis.cc
[arkanis-discord]: https://join.arkanis.cc
[uex]: https://uexcorp.space
