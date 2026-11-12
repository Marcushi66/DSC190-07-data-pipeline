import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt

    return mo, pd, plt


@app.cell
def _(mo):
    mo.md("""
    # Event Duration Analysis

    This notebook uses the output of the DVC pipeline
    to visualize the distribution of event durations.
    """)
    return


@app.cell
def _(pd):
    events = pd.read_csv("data/features/events.csv")
    return (events,)


@app.cell
def _(events, mo):
    mo.md(f"""
    **Number of cleaned events:** {len(events):,}
    """)
    return


@app.cell
def _(events, plt):
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.hist(
        events["duration_minutes"],
        bins=25,
        edgecolor="black",
    )

    ax.set_title("Distribution of Event Durations")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Number of Events")

    fig.tight_layout()
    fig
    return


if __name__ == "__main__":
    app.run()
