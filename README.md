# Arkanis Overlay 简体中文非官方便携版

[![GitHub Release](https://img.shields.io/github/v/release/NightGhost961/arkanis-overlay-simplified-chinese?display_name=tag&label=Release)](../../releases/latest)
[![License](https://img.shields.io/badge/license-PolyForm%20Noncommercial%201.0.0-blue)](LICENSE.md)

这是为《星际公民》玩家制作的 **Arkanis Overlay 非官方简体中文适配版**。项目提供可直接解压运行的 Windows x64 便携包，包含中文界面、中文实体显示与中文搜索支持。

它不是 Arkanis Corporation、Cloud Imperium Games 或 UEX Corporation 的官方产品、官方翻译或获得背书的项目。

## 下载

请到 [Releases 页面](../../releases/latest) 下载最新的 `ArkanisOverlay-zh-CN-portable-r4.zip`。

当前发布包的 SHA-256：

```text
4CC0145BD9EC96259C00FA4B20DBDCD9BEC68696B200A5E0FC6FF95764DEB628
```

这是自带 .NET 运行时的 `win-x64` 便携版：

1. 下载 ZIP。
2. 将 ZIP 解压到一个新建的独立文件夹。
3. 运行 `ArkanisOverlay.exe`。

请勿将它覆盖到官方安装目录，也不要与官方自动更新目录混用。该适配版不会修改《星际公民》客户端。

## 主要功能

- 常用界面、导航、搜索、贸易、库存、机库和设置控件的简体中文显示。
- 游戏商品、载具、地点、空间站、前哨站和终端以“中文（English）”形式显示，英文原名仍可用于核对和搜索。
- 中文同义词搜索：输入中文实体名时，会扩展为对应的 UEX 英文名进行匹配。
- 修复 Preferences 窗口可能持续停在 `Loading` 的 DOM 观察循环问题。
- 内置主术语表、社区术语参考和自动生成的 UEX 补充术语表。

构建时对本机 UEX 缓存进行的覆盖审计结果为 **1,747 / 1,747** 个实体名称：205 个商品、560 个载具名称/全称、3 个星系、11 个行星、18 个月球、5 座城市、59 个空间站、115 个前哨站和 771 个终端。

## 验证范围

- 8 项单元测试已通过。
- Release ZIP 已核验包含程序、`hostfxr.dll`、中文界面脚本和术语资源。
- 覆盖统计只对应构建时本机的 UEX 缓存；UEX 后续新增或改名的实体需要重新生成补充词表。
- 尚未替代所有 Windows 环境的人工 GUI 冒烟测试。若 Preferences 仍显示 `Loading`，请提交复现步骤和已脱敏日志。

## 从源码构建

项目要求 .NET SDK `10.0.301`。PowerShell 示例：

```powershell
$env:PATH = "$PWD\.dotnet;$env:PATH"
dotnet test .\tests\Arkanis.Overlay.Host.Desktop.UnitTests\Arkanis.Overlay.Host.Desktop.UnitTests.csproj --configuration Release --no-restore
dotnet publish .\src\Arkanis.Overlay.Host.Desktop\Arkanis.Overlay.Host.Desktop.csproj --runtime win-x64 --configuration Release --self-contained true --output .\publish-zh-cn
```

`tools/generate_uex_supplement.py` 以只读模式读取本机 Overlay 缓存，并从主术语表生成补充术语 JSON。仅在你有权使用相关术语数据时再分发生成结果。

## 许可、引用与 AI 协助

本适配版派生自 [ArkanisCorporation/ArkanisOverlay](https://github.com/ArkanisCorporation/ArkanisOverlay)，并继承上游的 **PolyForm Noncommercial 1.0.0** 许可证。仓库公开源代码以便审计和复现，但许可证仅允许非商业使用；它不是 MIT、GPL 或其他 OSI 批准的开源许可证。

完整的上游署名、UEX/社区术语来源、商标声明与 AI 协助披露见 [ATTRIBUTIONS.md](ATTRIBUTIONS.md)。本适配版由维护者主导，使用 **OpenAI GPT-5 Codex** 协助完成代码修改、术语补全脚本、测试和文档草拟。

## 贡献与问题反馈

欢迎提交可核对的术语修正、中文搜索复现步骤和构建问题。请不要提交游戏文件、账户信息、访问令牌或含个人信息的原始日志。

`Arkanis Overlay`、`Star Citizen`、`Cloud Imperium Games`、`UEX` 及相关名称可能是各自权利人的商标。本仓库与上述权利人没有隶属或背书关系。
