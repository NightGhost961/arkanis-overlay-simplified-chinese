namespace Arkanis.Overlay.Host.Desktop.UnitTests;

using Components.Helpers;
using Domain.Models.Search;
using Shouldly;

public class CommunityTranslationIndexTests
{
    [Fact]
    public void Display_UsesCuratedStarCitizenTerminology()
        => CommunityTranslationIndex.Display("Hadanite")
            .ShouldBe("哈丹水晶 (Hadanite)");

    [Fact]
    public void Display_UsesTheProvidedUexTerminologyFileBeforeFallbacks()
        => CommunityTranslationIndex.Display("Arrow")
            .ShouldBe("铁砧 箭矢 (Arrow)");

    [Fact]
    public void Display_UsesTheSupplementForAFullUexVehicleName()
        => CommunityTranslationIndex.Display("Aegis Avenger Titan")
            .ShouldBe("圣盾 复仇者 泰坦 (Aegis Avenger Titan)");

    [Fact]
    public void ExpandSearch_MapsSupplementedChineseLocationsBackToUexNames()
        => CommunityTranslationIndex.ExpandSearch("新巴贝奇")
            .ShouldContain("New Babbage");

    [Fact]
    public void ExpandSearch_MapsChineseTermsBackToUexNames()
        => CommunityTranslationIndex.ExpandSearch("哈丹")
            .ShouldContain("Hadanite");

    [Fact]
    public void ChineseSearch_OrsTheChineseAndUexEnglishTerms()
    {
        var query = TextSearch.Fuzzy(CommunityTranslationIndex.ExpandSearch("哈丹"));

        query.Match(new SearchableName("Hadanite"))
            .Single()
            .ShouldBeOfType<ScoredMatch>();
    }

    [Fact]
    public void Display_ExtractsAnUncuratedNameFromTheCommunityFile()
        => CommunityTranslationIndex.Display("Astatine")
            .ShouldBe("砹 (Astatine)");
}
