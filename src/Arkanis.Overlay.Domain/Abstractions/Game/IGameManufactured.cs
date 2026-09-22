namespace Arkanis.Overlay.Domain.Abstractions.Game;

using Models.Game;

public interface IGameManufactured
{
    GameCompany Manufacturer { get; }
}
