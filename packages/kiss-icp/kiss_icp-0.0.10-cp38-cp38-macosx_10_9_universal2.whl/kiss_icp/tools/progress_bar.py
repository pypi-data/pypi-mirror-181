import warnings

import tqdm.auto

warnings.simplefilter("ignore")
# Use the old tqdm inside python notebooks
if tqdm.auto.notebook_tqdm != tqdm.auto.std_tqdm:
    from tqdm.auto import trange
else:
    from tqdm.rich import trange


def get_progress_bar(first_scan, last_scan):
    return trange(
        first_scan,
        last_scan,
        unit="frames",
        dynamic_ncols=True,
        bar_format="{l_bar}{bar}[{elapsed}<{remaining}, {postfix}]",
    )
