from flask import Flask, render_template, request, redirect, url_for
import subprocess
import matplotlib.pyplot as plt
import pandas as pd
import io, base64
import os
import sys

app = Flask(__name__)

# ---------- Utilities ----------
def fig_to_uri(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return 'data:image/png;base64,' + string.decode('utf-8')

def load_csv(year):
    if year == "all":
        dfs = []
        for y in ["2020", "2021", "2022", "2023", "2024"]:
            path = f"{y}_playlist_data.csv"
            if os.path.exists(path):
                dfs.append(pd.read_csv(path))
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        return None
    else:
        filepath = f"{year}_playlist_data.csv"
        if os.path.exists(filepath):
            return pd.read_csv(filepath)
        return None

# ---------- Charts ----------
def generate_bar_chart(data):
    top_artists = (data[['Artist', 'Artist Popularity']]
                   .dropna()
                   .groupby('Artist')
                   .max()
                   .sort_values(by='Artist Popularity', ascending=False)
                   .head(10))

    fig, ax = plt.subplots()
    bars = ax.bar(top_artists.index, top_artists['Artist Popularity'], color='orange', width=0.6)
    ax.set_title("Top 10 Artists by Popularity")
    ax.set_ylabel("Popularity")
    ax.set_ylim(0, max(top_artists['Artist Popularity']) + 5)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig_to_uri(fig)

def generate_histogram(data):
    durations_ms = data["Duration (ms)"].dropna()
    durations_sec = durations_ms / 1000
    fig, ax = plt.subplots()
    ax.hist(durations_sec, bins=20, color='skyblue', edgecolor='black')
    ax.set_title("Distribution of Track Durations (seconds)")
    ax.set_xlabel("Duration (s)")
    ax.set_ylabel("Number of Tracks")
    plt.tight_layout()
    return fig_to_uri(fig)

def generate_pie_chart(data):
    exploded = data['Genres'].dropna().str.split(', ')
    genres = exploded.explode()
    genre_counts = genres[genres.str.lower() != 'unknown'].value_counts().head(5)

    fig, ax = plt.subplots()
    genre_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=140)
    ax.set_ylabel("")
    ax.set_title("Top 5 Genres")
    plt.tight_layout()
    return fig_to_uri(fig)

def generate_explicit_chart(data):
    counts = data['Explicit'].value_counts()
    labels = ['Non-Explicit', 'Explicit']
    fig, ax = plt.subplots()
    counts.plot(kind='pie', ax=ax, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_ylabel("")
    ax.set_title("Explicit vs Non-Explicit Tracks")
    plt.tight_layout()
    return fig_to_uri(fig)

def generate_top_tracks_chart(data):
    top_tracks = (data[['Song', 'Artist', 'Popularity']]
                  .dropna()
                  .assign(Label=lambda df: df['Song'] + " – " + df['Artist'])
                  .groupby('Label')
                  .max()
                  .sort_values(by='Popularity', ascending=False)
                  .head(10))

    fig, ax = plt.subplots()
    top_tracks.plot(kind='bar', y='Popularity', ax=ax, color='mediumseagreen', legend=False)
    ax.set_title("Top 10 Tracks by Popularity")
    ax.set_ylabel("Popularity")
    ax.set_xlabel("Track")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig_to_uri(fig)


def generate_followed_artists_chart(data):
    top_followed = (data[['Artist', 'Artist Followers']]
                    .dropna()
                    .groupby('Artist')
                    .max()
                    .sort_values(by='Artist Followers', ascending=False)
                    .head(10))
    fig, ax = plt.subplots()
    top_followed.plot(kind='bar', y='Artist Followers', ax=ax, color='slateblue', legend=False)
    ax.set_title("Top 10 Most Followed Artists")
    ax.set_ylabel("Followers")
    ax.set_xlabel("Artist")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig_to_uri(fig)


# ---------- Routes ----------
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/generate", methods=["POST"])
def generate():
    subprocess.run([sys.executable, "data/data.py"])
    return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard_redirect():
    year = request.args.get("year")
    return redirect(url_for("dashboard", year=year))

@app.route("/dashboard/<year>")
def dashboard(year):
    data = load_csv(year)
    if data is None:
        return f"CSV file for {year} not found. Please generate data first.", 404

    return render_template("dashboard.html",
                           year=year,
                           histogram=generate_histogram(data),
                           bar=generate_bar_chart(data),
                           pie=generate_pie_chart(data),
                           explicit=generate_explicit_chart(data),
                           top_tracks=generate_top_tracks_chart(data),
                           followed=generate_followed_artists_chart(data))


# ---------- Main ----------
if __name__ == "__main__":
    app.run(debug=True)
