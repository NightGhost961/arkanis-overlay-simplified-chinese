# Arkanis Overlay 简体中文非官方便携版

这是基于 [ArkanisCorporation/ArkanisOverlay](https://github.com/ArkanisCorporation/ArkanisOverlay)
制作的**非官方**简体中文适配版，面向《星际公民》玩家使用。它不是 Arkanis Corporation、Cloud Imperium Games 或 UEX Corporation 的官方产品或官方翻译。

本仓库公开源代码以便审计和复现构建，但继承上游的 **PolyForm Noncommercial 1.0.0** 许可证：允许非商业使用、修改与分发；不授予商业使用权。完整条款见 [LICENSE.md](LICENSE.md)，署名和第三方来源见 [ATTRIBUTIONS.md](ATTRIBUTIONS.md)。

## 下载与运行

请在仓库的 [Releases](../../releases) 页面下载最新的 `zh-CN` 便携 ZIP。

该 ZIP 的 SHA-256 为 `4CC0145BD9EC96259C00FA4B20DBDCD9BEC68696B200A5E0FC6FF95764DEB628`。GitHub 自动生成的 `Source code (zip/tar.gz)` 仅是源码快照，并不是可直接运行的便携包。

1. 下载 ZIP。
2. 将 ZIP 解压到**新建的独立文件夹**。
3. 运行 `ArkanisOverlay.exe`。

这是自带 .NET 运行时的 `win-x64` 便携版，不需要覆盖官方安装目录，也不会修改《星际公民》客户端。请不要与官方自动更新目录混用；官方更新会替换自定义版本。

## 这一版的内容

- 将常用界面、导航、搜索、贸易、库存、机库和设置控件翻译为简体中文。
- 修复设置窗口可能停在 `Loading` 的脚本观察循环问题。
- 游戏实体显示为“中文（English）”，保留英文原名以便查找、核对和报告问题。
- 支持中文搜索：输入中文地点、商品或载具名时会扩展为相应的 UEX 英文实体名，并以同义词匹配而非错误地要求中英文同时命中。
- 包含主术语表、社区术语对照、以及基于本机只读 UEX 缓存生成的补充术语表。

此次发布审计的本机缓存覆盖为 **1,747 / 1,747** 个实体名称：205 个商品、560 个载具名称/全称、3 个星系、11 个行星、18 个月球、5 座城市、59 个空间站、115 个前哨站和 771 个终端。

## 验证边界

- 已通过 8 项单元测试，并验证 ZIP 内含 `ArkanisOverlay.exe`、`hostfxr.dll`、中文界面脚本和三份术语资源。
- 已核对 Release ZIP 中的主术语 JSON 与本仓库源文件哈希一致。
- 上述实体覆盖针对构建时本机缓存；UEX 日后新增或重命名的实体需要重新生成补充词表。
- 尚未在每一台 Windows 环境实际点击 Preferences 做 GUI 冒烟测试。若仍出现 `Loading`，请附上日志和复现步骤后报告问题。

## 从源码构建

项目要求 .NET SDK `10.0.301`。在 PowerShell 中：

```powershell
$env:PATH = "$PWD\.dotnet;$env:PATH"
dotnet test .\tests\Arkanis.Overlay.Host.Desktop.UnitTests\Arkanis.Overlay.Host.Desktop.UnitTests.csproj --configuration Release --no-restore
dotnet publish .\src\Arkanis.Overlay.Host.Desktop\Arkanis.Overlay.Host.Desktop.csproj --runtime win-x64 --configuration Release --self-contained true --output .\publish-zh-cn
```

`tools/generate_uex_supplement.py` 以只读模式读取本机 Overlay 缓存，并从根目录主术语表生成 `UEX专有名词补充汉化.json`。运行生成器前请先关闭 Overlay，且仅在你有权使用相关术语数据时再分发生成结果。

## 贡献与报告问题

欢迎提交可核对的术语修正、搜索复现步骤或构建问题。请不要提交《星际公民》游戏文件、账户信息、日志中的令牌或其他个人数据。提交贡献即表示你有权依据本仓库的非商业许可分发该贡献。

## 修改与 AI 协助声明

本适配版由维护者主导，使用 **OpenAI GPT-5 Codex** 协助完成代码修改、术语补全脚本、测试和文档草拟。AI 不是本项目、上游项目或任何术语数据的权利主体；发布者仍应负责审核准确性、第三方权利和许可证合规性。

## 商标与免责声明

`Star Citizen`、`Cloud Imperium Games`、`UEX` 及相关名称可能是各自权利人的商标。本仓库与上述权利人没有隶属或背书关系。软件按许可证所述“按现状”提供，不提供任何保证。
