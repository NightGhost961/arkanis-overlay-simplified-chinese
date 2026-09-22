namespace Arkanis.Overlay.Infrastructure.UnitTests.Repositories.Sync.Cached;

using CacheDecorators;
using External.UEX.Abstractions;
using Live;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

public class CachedUexSyncRepositoryTestFixture : LiveUexSyncRepositoryTestFixture
{
    protected override void AddServices(IServiceCollection services, IConfiguration? configuration)
    {
        base.AddServices(services, configuration);
        services.Decorate<IUexGameApi, UexGameApiCacheDecorator>();
        services.Decorate<IUexItemsApi, UexItemsApiCacheDecorator>();
        services.Decorate<IUexStaticApi, UexStaticApiCacheDecorator>();
        services.Decorate<IUexVehiclesApi, UexVehiclesApiCacheDecorator>();
    }
}
