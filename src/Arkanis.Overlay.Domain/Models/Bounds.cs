namespace Arkanis.Overlay.Domain.Models;

public static class Bounds
{
    public static Bounds<T> All<T>(T value) where T : IComparable<T>
        => new(value, value, value);
}

public record Bounds<T>(T Min, T Max, T Avg) where T : IComparable<T>;
