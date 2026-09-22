namespace Arkanis.Overlay.Domain.Models.Search;

using Abstractions;
using Abstractions.Game;
using Enums;
using Game;

/// <summary>
///     A prototype for any search query.
///     Matching queries against <see cref="ISearchable" /> subjects produces match results.
/// </summary>
public abstract record SearchQuery
{
    public virtual SearchMatchResult<T> Match<T>(T searchable) where T : ISearchable
        => SearchMatchResult.Create(searchable, Match(searchable.SearchableAttributes));

    public virtual SearchMatchResult Match(ISearchable searchable)
        => SearchMatchResult.Create(searchable, Match(searchable.SearchableAttributes));

    public virtual IEnumerable<SearchMatch> Match(IEnumerable<SearchableTrait> attributes, int depth = 0)
        => attributes.SelectMany(attribute => Match(attribute, depth));

    public abstract IEnumerable<SearchMatch> Match(SearchableTrait trait, int depth = 0);
}

public sealed record EmptySearch : SearchQuery
{
    private EmptySearch()
    {
    }

    public static SearchQuery Instance { get; } = new EmptySearch();

    public override IEnumerable<SearchMatch> Match(SearchableTrait trait, int depth = 0)
        => [];
}

public abstract record TextSearch(string Content) : SearchQuery
{
    protected string NormalizedContent { get; } = Content.ToLowerInvariant();

    public static FuzzyTextSearch Combine(IEnumerable<SearchQuery> queries)
        => new(string.Join(' ', queries.OfType<TextSearch>().Select(x => x.Content)));

    public static SearchQuery Fuzzy(string content)
        => FuzzyTextSearch.Create(content);

    /// <summary>
    ///     Creates one text query that matches any of the supplied alternatives. This is used for localized
    ///     search input, where a Chinese term and its UEX English name are synonyms rather than separate terms.
    /// </summary>
    public static SearchQuery Fuzzy(IEnumerable<string> alternatives)
    {
        var values = alternatives
            .Where(value => !string.IsNullOrWhiteSpace(value))
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .ToArray();

        return values.Length switch
        {
            0 => new FuzzyTextSearch(string.Empty),
            1 => new FuzzyTextSearch(values[0]),
            _ => new AlternativeFuzzyTextSearch(values),
        };
    }
}

public sealed record FuzzyTextSearch(string Content) : TextSearch(Content)
{
    private static int GetStringComparisonScore(string subject, string query, StringComparison comparison, Func<int>? fallback = null)
        => subject switch
        {
            _ when subject.Equals(query, comparison) => 100,
            _ when subject.StartsWith(query, comparison) => 99,
            _ when subject.EndsWith(query, comparison) => 98,
            _ when subject.Contains(query, comparison) => 97,
            _ => fallback?.Invoke() ?? 0,
        };

    public override IEnumerable<SearchMatch> Match(SearchableTrait trait, int depth = 0)
        => trait switch
        {
            SearchableCode data =>
            [
                GetStringComparisonScore(data.Code, Content, StringComparison.OrdinalIgnoreCase) is > 0 and var score
                    ? new ScoredMatch(score, depth, trait, this)
                    : new NoMatch(trait, this),
            ],
            SearchableName data =>
            [
                GetStringComparisonScore(data.Name, NormalizedContent, StringComparison.OrdinalIgnoreCase) is > 0 and var score
                    ? new ScoredMatch(score, depth, trait, this)
                    : new NoMatch(trait, this),
            ],
            _ => [new NoMatch(trait, this)],
        };

    public static SearchQuery Create(string content)
        => new FuzzyTextSearch(content);
}

/// <summary>
///     A fuzzy text search where each value is an alternative spelling/name for the same user-entered term.
/// </summary>
public sealed record AlternativeFuzzyTextSearch(IReadOnlyList<string> Alternatives)
    : TextSearch(string.Join(" | ", Alternatives))
{
    public override IEnumerable<SearchMatch> Match(SearchableTrait trait, int depth = 0)
    {
        var bestMatch = Alternatives
            .SelectMany(alternative => new FuzzyTextSearch(alternative).Match(trait, depth))
            .OfType<ScoredMatch>()
            .OrderByDescending(match => match.NormalizedScore)
            .FirstOrDefault();

        return bestMatch is null
            ? [new NoMatch(trait, this)]
            : [new ScoredMatch(bestMatch.Score, bestMatch.Depth, trait, this)];
    }
}

public sealed record LocationSearch(IGameLocation Location) : SearchQuery
{
    public override IEnumerable<SearchMatch> Match(SearchableTrait trait, int depth = 0)
        => trait switch
        {
            SearchableLocation data => Location.IsOrContains(data.Location)
                ? [new SoftMatch(trait, this)]
                : [new ExcludeMatch(trait, this)],
            _ => [new NoMatch(trait, this)],
        };
}

public sealed record EntityCategorySearch(params HashSet<GameEntityCategory> Categories) : SearchQuery
{
    public bool ExcludeOnMismatch { get; init; } = true;

    public override IEnumerable<SearchMatch> Match(SearchableTrait trait, int depth = 0)
        => trait switch
        {
            SearchableEntityCategory data => Categories.Contains(data.Category)
                ? [new SoftMatch(trait, this)]
                : ExcludeOnMismatch
                    ? [new ExcludeMatch(trait, this)]
                    : [new NoMatch(trait, this)],
            _ => [new NoMatch(trait, this)],
        };
}

public sealed record ProductCategorySearch(params HashSet<GameProductCategory> Categories) : SearchQuery
{
    public bool ExcludeOnMismatch { get; init; } = true;

    public override IEnumerable<SearchMatch> Match(SearchableTrait trait, int depth = 0)
        => trait switch
        {
            SearchableProductCategory data => Categories.Contains(data.Category)
                ? [new SoftMatch(trait, this)]
                : ExcludeOnMismatch
                    ? [new ExcludeMatch(trait, this)]
                    : [new NoMatch(trait, this)],
            _ => [new NoMatch(trait, this)],
        };
}
