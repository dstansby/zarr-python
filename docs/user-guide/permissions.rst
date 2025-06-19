Write permissions
-----------------

Zarr Python handles write permissions at both a store and an array/group level.
Whether it is possible to write to a store, array, or group, can be inspected using the ``.read_only`` property - if this is `True`, then trying to write data will raise an error.
If you want to write to or modify an array or group, both the array/group *and* the underlying store must be writeable.

Various functions in the API accept a ``mode`` argument.
The accepted values are:

- ``'r'``: read only (must exist)
- ``'r+'``: read/write (must exist)
- ``'a'``: read/write (create if doesn't exist)
- ``'w'``: read/write (overwrite if exists)
- ``'w-'``: read/write (create if doesn't exist).

If not given, this will always default to ``'a'``.

The resulting array will be read only if ``mode='r'``, and read/write otherwise::

    >>> import zarr
    >>>
    >>> arr = zarr.ones(store="data/perms.zarr", shape=(1,))
    >>> arr.read_only
    False
    >>> arr = zarr.open_array(store="data/perms.zarr", mode='r')
    >>> arr.read_only
    True

If the store given to the same function call does not already have ``read_only`` set (e.g., if it is just a filesystem path), the ``mode`` argument will also be used to set ``read_only`` on the resulting store::

    >>> arr = zarr.open_array(store="data/perms.zarr", mode='r')
    >>> arr.read_only
    True
    >>> arr.store.read_only
    True

But if the store already has ``read_only`` set, the mode will not be propagated to the store::

    >>> import zarr.storage
    >>>
    >>> store = zarr.storage.LocalStore("data/perms.zarr")
    >>> store.read_only
    False
    >>> arr = zarr.open_array(store="data/perms.zarr", mode='r')
    >>> arr.read_only
    True
    >>> store.read_only
    False
