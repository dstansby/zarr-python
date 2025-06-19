from pathlib import Path

import pytest

import zarr.storage


@pytest.fixture
def store_with_array(tmp_path: Path) -> zarr.storage.LocalStore:
    store = zarr.storage.LocalStore(tmp_path, read_only=False)
    zarr.create_array(store=store, shape=(1,), dtype=int)
    return store


@pytest.mark.parametrize("array_open_mode", ["r", "a"])
@pytest.mark.parametrize("store_read_only", [True, False])
def test_open_array_perms(
    store_with_array: zarr.storage.LocalStore, store_read_only: bool, array_open_mode: str
) -> None:
    store = zarr.storage.LocalStore(store_with_array.root, read_only=store_read_only)
    if store_read_only and array_open_mode == "a":
        # Error trying to open array with write from store with read
        with pytest.raises(ValueError, match="Store is read-only"):
            zarr.open_array(store, mode=array_open_mode)
    else:
        # Otherwise read/read, write/read, and write/write should work
        arr = zarr.open_array(store, mode=array_open_mode)
        assert arr.read_only == (array_open_mode == "r")


@pytest.mark.parametrize("array_open_mode", ["r", "a"])
def test_write_to_array(store_with_array: zarr.storage.LocalStore, array_open_mode: str) -> None:
    arr = zarr.open_array(store_with_array, mode=array_open_mode)

    if array_open_mode == "r":
        with pytest.raises(RuntimeError, match="Array is read-only"):
            arr[0] = 1
    else:
        arr[0] = 1
