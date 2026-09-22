namespace Arkanis.Overlay.Domain.Abstractions.Game;

using Enums;
using Models.Game;

public interface IGameEntity : IIdentifiable, ISearchable
{
    new UexApiGameEntityId Id { get; }

    GameEntityName Name { get; }

    GameEntityCategory EntityCategory { get; }

    IDomainId IIdentifiable.Id
        => Id;
}
