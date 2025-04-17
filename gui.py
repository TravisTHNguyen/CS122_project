from flask import Flask, render_template
import random
import matplotlib.pyplot as plt
import os
import csv

#just some very basic framework stuff to get us started on 
app = Flask(__name__)

def generate_line_chart():
    import io, base64
    years = list(range(2020, 2026))
    values = [random.randint(50, 100) for _ in years]

    fig, ax = plt.subplots()
    ax.plot(years, values, marker='o', color='blue')
    ax.set_title("Artist Popularity Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Popularity Score")

    return fig_to_uri(fig)

def generate_bar_chart():
    import io, base64
    genres = ['Pop', 'Hip-Hop', 'Rock', 'EDM', 'Latin']
    counts = [random.randint(10, 50) for _ in genres]

    fig, ax = plt.subplots()
    ax.bar(genres, counts, color='green')
    ax.set_title("Number of Artists per Genre")
    ax.set_ylabel("Count")

    return fig_to_uri(fig)

def generate_pie_chart():
    import io, base64
    genres = ['Pop', 'Hip-Hop', 'Rock', 'EDM', 'Latin']
    sizes = [random.randint(10, 30) for _ in genres]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=genres, autopct='%1.1f%%', startangle=140)
    ax.set_title("Genre Distribution")

    return fig_to_uri(fig)

def fig_to_uri(fig):
    import io, base64
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + string.decode('utf-8')
    return uri


#some csv parse functions will go here, will wait till final files are given
import csv

def read_csv_as_dicts(filepath):
    """Returns list of dictionaries from a CSV file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

from collections import defaultdict

def parse_artists_per_genre_per_year(rows):
    """Returns a nested dict of genre -> year -> count of artists."""
    data = defaultdict(lambda: defaultdict(int))
    for row in rows:
        year = row.get("year")
        genre = row.get("genre")
        if year and genre:
            data[genre][year] += 1
    return data

def track_new_vs_returning_artists(rows):
    """Returns a dict of year -> {'new': set(), 'returning': set()}"""
    seen = set()
    yearly_stats = defaultdict(lambda: {'new': set(), 'returning': set()})
    for row in rows:
        year = row.get("year")
        artist = row.get("artist_name")
        if not year or not artist:
            continue
        if artist in seen:
            yearly_stats[year]['returning'].add(artist)
        else:
            yearly_stats[year]['new'].add(artist)
            seen.add(artist)
    return yearly_stats

def genre_distribution_for_year(rows, target_year):
    """Returns genre count dict for a specific year."""
    genre_counts = defaultdict(int)
    for row in rows:
        if row.get("year") == str(target_year):
            genre = row.get("genre")
            if genre:
                genre_counts[genre] += 1
    return genre_counts


@app.route("/")
def dashboard():
    line = generate_line_chart()
    bar = generate_bar_chart()
    return render_template("dashboard.html", line=line, bar=bar)


@app.route("/line")
def line():
    chart = generate_line_chart()
    return render_template("line.html", chart=chart)

@app.route("/bar")
def bar():
    chart = generate_bar_chart()
    return render_template("bar.html", chart=chart)

@app.route("/pie")
def pie():
    chart = generate_pie_chart()
    return render_template("pie.html", chart=chart)

if __name__ == "__main__":
    app.run(debug=True)
