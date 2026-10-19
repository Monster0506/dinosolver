import pytest

from dinosolver.viewer import GAP, HEADER_H, WINDOW, layout


@pytest.mark.parametrize("workers", [1, 2, 4, 7, 8, 16, 20, 64])
def test_tiles_fit_in_window(workers: int):
    cols, w, h = layout(workers, WINDOW)
    rows = -(-workers // cols)

    assert w > 0
    assert GAP + cols * (w + GAP) <= WINDOW[0]
    assert HEADER_H + GAP + rows * (h + GAP) <= WINDOW[1]
