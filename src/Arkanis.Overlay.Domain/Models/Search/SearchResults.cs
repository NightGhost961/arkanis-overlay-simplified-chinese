namespace Arkanis.Overlay.Domain.Models.Search;

using Abstractions.Game;

public abstract record SearchResults(TimeSpan SearchTime);

public record GameEntitySearchResults(List<SearchMatchResult<IGameEntity>> GameEntities, TimeSpan SearchTime) : SearchResults(SearchTime)
{
    public static readonly GameEntitySearchResults Empty = new([], TimeSpan.Zero);
}
