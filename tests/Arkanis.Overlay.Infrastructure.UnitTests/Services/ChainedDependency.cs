namespace Arkanis.Overlay.Infrastructure.UnitTests.Services;

using Domain.Abstractions;

internal sealed class ChainedDependency(IDependable dependable) : IDependable
{
    public bool IsReady
        => dependable.IsReady;

    public async Task WaitUntilReadyAsync(CancellationToken cancellationToken = default)
        => await dependable.WaitUntilReadyAsync(cancellationToken);

    public static ChainedDependency Create(IDependable dependable)
        => new(dependable);
}
