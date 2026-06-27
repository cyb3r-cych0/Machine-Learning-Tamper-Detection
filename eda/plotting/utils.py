from pathlib import Path
import matplotlib.pyplot as plt


def save_figure(fig, output_dir, filename):

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    fig.savefig(
        output_dir / f"{filename}.png",
        dpi=600,
        bbox_inches="tight"
    )

    fig.savefig(
        output_dir / f"{filename}.pdf",
        bbox_inches="tight"
    )

    plt.close(fig)