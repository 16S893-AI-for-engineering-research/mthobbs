from pathlib import Path

from plots.plot_paper_overlays import generate_figure6_overlay, generate_figure7_overlay


def test_published_figure_overlays_are_generated(tmp_path):
    paper = Path(__file__).parents[1] / "paper" / "kato-matsuda.pdf"
    figure6 = tmp_path / "figure6_overlay.png"
    figure7 = tmp_path / "figure7_overlay.png"

    generate_figure6_overlay(paper, figure6, render_dpi=150)
    generate_figure7_overlay(paper, figure7, render_dpi=150)

    assert figure6.stat().st_size > 20_000
    assert figure7.stat().st_size > 20_000
