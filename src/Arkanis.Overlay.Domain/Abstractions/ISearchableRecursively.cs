namespace Arkanis.Overlay.Domain.Abstractions;

public interface ISearchableRecursively : ISearchable
{
    ISearchableRecursively? Parent { get; }
}
