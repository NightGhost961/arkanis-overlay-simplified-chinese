namespace Arkanis.Overlay.Infrastructure.Services;

using Abstractions;

public class NoSystemAutoStartStateProvider : ISystemAutoStartStateProvider
{
    public bool IsAutoStartEnabled()
        => false;
}
