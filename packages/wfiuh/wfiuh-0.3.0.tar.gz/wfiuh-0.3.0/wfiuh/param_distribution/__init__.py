import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_param_distribution(
    data: pd.DataFrame, x: str, fname: str, kind: str = "kde"
) -> None:
    plt.figure(dpi=600)
    sns.displot(data=data, x=x, kind=kind)
    plt.savefig(fname=fname)
    plt.close()


def plot_params_distribution(data: pd.DataFrame, fname: str, kind: str = "kde") -> None:
    params = filter(lambda column: len(column) == 1, data.columns)
    dfs: list[pd.DataFrame] = list()
    for param in params:
        df = pd.DataFrame()
        df["value"] = data[param]
        df["param"] = param
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    plt.figure(dpi=600)
    sns.displot(
        data=df,
        x="value",
        col="param",
        kind=kind,
        facet_kws={"sharex": False, "sharey": False},
    )
    plt.savefig(fname=fname)
    plt.close()
