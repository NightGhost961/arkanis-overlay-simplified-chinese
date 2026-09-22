namespace Arkanis.Overlay.Domain.Abstractions.Game;

using Enums;
using Models;
using Models.Trade;

public interface IGameSellable : IGameEntity
{
    Bounds<PriceTag> LatestSalePrices { get; }
    GameTerminalType TerminalType { get; }

    void UpdateSalePrices(Bounds<PriceTag> newPrices);
}
