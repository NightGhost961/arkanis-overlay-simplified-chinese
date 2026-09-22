namespace Arkanis.Overlay.Domain.Abstractions.Services;

public interface IIconPicker
{
    string PickIconFor<T>(T value);
}
