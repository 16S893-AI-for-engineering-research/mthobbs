from PIL import Image

from plots.plot_figure6 import plot_figure_6


def test_figure_6_plot_is_generated(tmp_path):
    output = tmp_path / "figure6.png"

    reported_delta = plot_figure_6(output)

    assert output.exists()
    assert output.stat().st_size > 20_000
    assert Image.open(output).size == (2100, 1500)
    assert abs(reported_delta - 0.64e-3) < 0.01e-3
