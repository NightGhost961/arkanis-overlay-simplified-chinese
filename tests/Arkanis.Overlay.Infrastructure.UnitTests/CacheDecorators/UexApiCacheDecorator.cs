namespace Arkanis.Overlay.Infrastructure.UnitTests.CacheDecorators;

using Microsoft.Extensions.Logging;

public abstract class UexApiCacheDecorator(ILogger logger) : ServiceCacheDecorator(logger)
{
    protected override string CacheSubPath
        => "uex";
}
