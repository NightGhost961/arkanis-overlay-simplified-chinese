namespace Arkanis.Overlay.Components.Helpers;

using System.Text.Json;
using System.Text.RegularExpressions;

/// <summary>
///     Reads the community Star Citizen language file supplied with the Chinese patch and exposes a small,
///     safe name-translation index for the live UEX data used by the overlay.
/// </summary>
public static partial class CommunityTranslationIndex
{
    private const string TranslationFileName = "社区翻译对照.ini";
    private static readonly string[] UexTranslationFileNames =
    [
        "UEX专有名词中英对照.json",
        "UEX专有名词补充汉化.json",
    ];

    [GeneratedRegex(
        @"^(?<zh>[\u3400-\u9fff0-9][\u3400-\u9fffA-Za-z0-9·\-\s]{0,80}?)\s*\((?<en>[A-Za-z][A-Za-z0-9 .,'’&/\-]{1,80})\)\s*$",
        RegexOptions.CultureInvariant
    )]
    private static partial Regex ParenthesizedName();

    [GeneratedRegex(
        @"^(?<zh>[\u3400-\u9fff][\u3400-\u9fff0-9·\-\s]{0,80}?)(?<en>[A-Z][A-Za-z0-9 .,'’&/\-]{1,80})\s*$",
        RegexOptions.CultureInvariant
    )]
    private static partial Regex InlineName();

    private static readonly Lazy<TranslationIndex> Index = new(CreateIndex);

    private static readonly IReadOnlyDictionary<string, string> CuratedFallbacks =
        new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
        {
            ["Stanton"] = "斯坦顿",
            ["Pyro"] = "派罗",
            ["Nyx"] = "尼克斯",
            ["Terra"] = "泰拉",
            ["Area18"] = "18区",
            ["Orison"] = "奥里森",
            ["Everus Harbor"] = "埃弗勒斯空间站",
            ["Port Tressler"] = "特雷斯勒空间站",
            ["Baijini Point"] = "拜吉尼角",
            ["Seraphim Station"] = "炽天使空间站",
            ["HUR-L1"] = "赫斯顿 L1",
            ["HUR-L2"] = "赫斯顿 L2",
            ["HUR-L3"] = "赫斯顿 L3",
            ["HUR-L4"] = "赫斯顿 L4",
            ["HUR-L5"] = "赫斯顿 L5",
            ["ARC-L1"] = "弧光 L1",
            ["ARC-L2"] = "弧光 L2",
            ["ARC-L3"] = "弧光 L3",
            ["ARC-L4"] = "弧光 L4",
            ["ARC-L5"] = "弧光 L5",
            ["MIC-L1"] = "微科 L1",
            ["MIC-L2"] = "微科 L2",
            ["MIC-L3"] = "微科 L3",
            ["MIC-L4"] = "微科 L4",
            ["MIC-L5"] = "微科 L5",
            ["Hadanite"] = "哈丹水晶",
            ["Aphorite"] = "紫钠水晶",
            ["Dolivine"] = "暗橄榄石",
            ["Agricium"] = "艾格瑞金属",
            ["Laranite"] = "砬兰石",
            ["Taranite"] = "塔兰导电石",
            ["Quantanium"] = "量子矿物",
            ["Quantainium"] = "量子矿物",
            ["Bexalite"] = "贝沙电气石",
            ["Titanium"] = "钛",
            ["Tungsten"] = "钨",
            ["Gold"] = "金",
            ["Copper"] = "铜",
            ["Iron"] = "铁",
        };

    /// <summary>
    ///     Returns a bilingual display value for an English game name. Keeping the original name in parentheses
    ///     preserves recognition and makes the first Chinese-patch release safe to use with English UEX data.
    /// </summary>
    public static string Display(string value)
    {
        if (string.IsNullOrWhiteSpace(value) || ContainsChinese(value))
        {
            return value;
        }

        var translated = Index.Value.FindChinese(value);
        return translated is null ? value : $"{translated} ({value})";
    }

    /// <summary>
    ///     Adds matching English names to a Chinese query so the existing UEX-backed search can find translated
    ///     commodities and locations without changing its database schema.
    /// </summary>
    public static IEnumerable<string> ExpandSearch(string value)
        => Index.Value.FindEnglish(value).Prepend(value).Distinct(StringComparer.OrdinalIgnoreCase);

    private static TranslationIndex CreateIndex()
    {
        var translations = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);

        // The UEX data set is maintained specifically for the names received from the Overlay's data provider.
        // It deliberately takes precedence over older, free-form community text.
        foreach (var fileName in UexTranslationFileNames)
        {
            foreach (var filePath in GetCandidatePaths(fileName).Distinct(StringComparer.OrdinalIgnoreCase))
            {
                if (!File.Exists(filePath))
                {
                    continue;
                }

                try
                {
                    LoadUexTranslations(filePath, translations);
                    break;
                }
                catch (JsonException)
                {
                    // Continue with the community file and curated terms when an optional JSON resource is invalid.
                }
                catch (IOException)
                {
                    // Continue with the community file and curated terms when an optional JSON resource is unavailable.
                }
                catch (UnauthorizedAccessException)
                {
                    // Continue with the community file and curated terms when an optional JSON resource cannot be read.
                }
            }
        }

        foreach (var (english, chinese) in CuratedFallbacks)
        {
            translations.TryAdd(english, chinese);
        }

        foreach (var filePath in GetCandidatePaths(TranslationFileName).Distinct(StringComparer.OrdinalIgnoreCase))
        {
            if (!File.Exists(filePath))
            {
                continue;
            }

            try
            {
                foreach (var line in File.ReadLines(filePath))
                {
                    var separatorIndex = line.IndexOf('=');
                    if (separatorIndex < 1)
                    {
                        continue;
                    }

                    var value = line[(separatorIndex + 1)..].Trim();
                    // Long descriptions can contain many unrelated bilingual terms. Only import compact display names.
                    if (value.Length is 0 or > 180 || value.Contains("\\n", StringComparison.Ordinal))
                    {
                        continue;
                    }

                    AddPair(ParenthesizedName().Match(value), translations);
                    AddPair(InlineName().Match(value), translations);
                }

                break;
            }
            catch (IOException)
            {
                // The fallback glossary still makes the patch usable when the optional resource is locked.
            }
            catch (UnauthorizedAccessException)
            {
                // The fallback glossary still makes the patch usable when the optional resource cannot be read.
            }
        }

        return new TranslationIndex(translations);
    }

    private static void LoadUexTranslations(string filePath, Dictionary<string, string> translations)
    {
        using var document = JsonDocument.Parse(File.ReadAllText(filePath));
        if (!document.RootElement.TryGetProperty("englishToChinese", out var categories)
            || categories.ValueKind is not JsonValueKind.Object)
        {
            return;
        }

        foreach (var category in categories.EnumerateObject())
        {
            if (category.Value.ValueKind is not JsonValueKind.Object)
            {
                continue;
            }

            foreach (var entry in category.Value.EnumerateObject())
            {
                var chinese = entry.Value.GetString()?.Trim();
                if (!string.IsNullOrWhiteSpace(chinese) && ContainsChinese(chinese))
                {
                    translations[entry.Name.Trim()] = chinese;
                }
            }
        }
    }

    private static void AddPair(Match match, IDictionary<string, string> translations)
    {
        if (!match.Success)
        {
            return;
        }

        var english = match.Groups["en"].Value.Trim();
        var chinese = match.Groups["zh"].Value.Trim();
        if (english.Length > 1 && chinese.Length > 0 && ContainsChinese(chinese))
        {
            translations.TryAdd(english, chinese);
        }
    }

    private static IEnumerable<string> GetCandidatePaths(string fileName)
    {
        yield return Path.Combine(AppContext.BaseDirectory, "localization", fileName);
        yield return Path.Combine(AppContext.BaseDirectory, fileName);
        yield return Path.Combine(Directory.GetCurrentDirectory(), "localization", fileName);
    }

    private static bool ContainsChinese(string value)
        => value.Any(character => character is >= '\u3400' and <= '\u9fff');

    private sealed class TranslationIndex(IReadOnlyDictionary<string, string> englishToChinese)
    {
        private readonly IReadOnlyDictionary<string, string> _englishToChinese = englishToChinese;

        public string? FindChinese(string english)
            => _englishToChinese.GetValueOrDefault(english);

        public IEnumerable<string> FindEnglish(string chineseQuery)
            => ContainsChinese(chineseQuery)
                ? _englishToChinese
                    .Where(pair => pair.Value.Contains(chineseQuery, StringComparison.OrdinalIgnoreCase))
                    // Prefer the named entity itself over a terminal whose longer translated label happens to
                    // contain the same location. Otherwise the first eight terminals can hide "New Babbage",
                    // "Everus Harbor", and other direct Chinese searches.
                    .OrderByDescending(pair => pair.Value.Equals(chineseQuery, StringComparison.OrdinalIgnoreCase))
                    .ThenBy(pair => pair.Key.Length)
                    .ThenBy(pair => pair.Key, StringComparer.OrdinalIgnoreCase)
                    .Select(pair => pair.Key)
                    .Take(8)
                : [];
    }
}
