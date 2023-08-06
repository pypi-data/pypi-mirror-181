import os
import re
from pathlib import Path

import numpy as np
import pandas as pd


def read_csv(filepath: str | Path) -> tuple[int, np.ndarray, np.ndarray]:
    match_result = re.fullmatch(
        pattern=r"(?P<id>\d+).*", string=os.path.basename(filepath)
    )
    assert match_result
    id = int(match_result.group("id"))
    df = pd.read_csv(filepath)
    x = df["flowTime"].to_numpy()
    y = df["frequency"].to_numpy()
    return id, x, y


def prepare_y(x: np.ndarray, y: np.ndarray, func: str = "cdf") -> np.ndarray:
    if func == "cdf":
        return y.cumsum()
    elif func == "pdf":
        return y / (x[1] - x[0])
    else:
        raise NotImplementedError()
