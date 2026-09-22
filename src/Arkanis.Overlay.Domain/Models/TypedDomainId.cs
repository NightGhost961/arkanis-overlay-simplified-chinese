namespace Arkanis.Overlay.Domain.Models;

using Abstractions.Game;

public abstract record TypedDomainId<T>(T Identity) : IDomainId where T : notnull
{
    /// <remarks>
    ///     This method must be overriden in subclasses to ensure the instance type matches.
    /// </remarks>
    public virtual bool Equals(IDomainId? other)
        => other is TypedDomainId<T> otherTyped && Identity.Equals(otherTyped.Identity);

    public override int GetHashCode()
        // The <c>GetType().GetHashCode()</c> ensures that any two distinct subclassed strongly-typed IDs
        // with the same underlying identity type are still considered fundamentally different.
        => HashCode.Combine(GetType().GetHashCode(), Identity.GetHashCode());
}
