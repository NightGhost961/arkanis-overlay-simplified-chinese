namespace Arkanis.Overlay.Domain.Models;

public sealed record StarCitizenVersion(string Version)
{
    public static StarCitizenVersion Create(string version)
        => new(version);
}
