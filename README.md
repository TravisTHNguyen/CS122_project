# Spotify Music Trends Analysis

## Authors
- [Samuel Hendric]  
- [Travis Nguyen]  

## Project Description
This project analyzes music trends using the Spotify API by retrieving the top 50 artists over different time periods (short-term, medium-term, and long-term). It examines changes such as artist popularity and genre distribution. The data is stored in a structured format and analyzed to identify key trends in the music industry. Our visualization component presents analysis through graphs and charts, displaying shifts in music preferences over time. The project also includes an interactive interface (GUI or web) to allow users to explore trends.


## Project Outline
1. **Data Collection**  [Samuel]
   - Using the spotif API top 50 artists from different timeframes (short-term, medium-term, long-term).  
   - Extract audio features of top tracks.  

2. **Data Organization**  [Samuel]
   - Store data in structured JSON or CSV format.
   - CSV of top 50 artists from 2020-2025 extracting from the global 50 playlist

3. **Data Analysis**    [Travis]
  - **Genre Popularity Trends**
    - Track genre representation in the top 50 over the years.
    - Identify emerging or declining genres.

  - **Artist Longevity**
    - Detect which artists appear in multiple years
    - Rank artists based on consistency and popularity over time.

  - **Popularity Metrics**
    - Study changes in popularity scoes and follower counts year-over-year

4. **Visualization**  [Travis]
   - Generate time-series plots of popularity trends.  
   - Display audio feature comparisons in charts.  
  - **Bar Charts**
    - Number of artists per genre per year
    - New vs returning artists over time

  - **Line Graphs**
    - Growth in artist popularity or followers

  - **Pie Charts**
    - Genre distribution for a given year
