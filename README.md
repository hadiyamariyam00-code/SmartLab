CineTrack 

A responsive personal movie tracking web app built with React.js and styled with Tailwind CSS. CineTrack allows users to discover movies, manage a personal watchlist, and log what you've watched with your own ratings and notes. Includes personal stats on your viewing habits.

Live Demo

[Link here]()

Features

- Search for movies via a REST API
- Add movies to your watchlist
- Mark movies as watched
- Rate movies and add personal notes
- View stats on your watching habits
- Data persists locally (no account/login needed)

Tech Stack

- React — frontend
- Vite — build tool
- Tailwind CSS — styling
- REST API — fetching movie data
- LocalStorage — storing watchlist, ratings, and notes


Getting Started

 Prerequisites

- Node.js (v16 or higher recommended)
- npm

Installation

```bash
# Clone the repo
git clone https://github.com/your-username/cinetrack.git

# Move into the project folder
cd cinetrack

# Install dependencies
npm install
```

API

Uses an API key from the [OMDb API](https://www.omdbapi.com/) (public).

Running the App

```bash
npm run dev
```

Usage

1. Search for a movie using the search bar
2. Add it to your watchlist
3. Once you've watched it, mark it as watched
4. Rate it and add any personal notes
5. Check your stats to see your watching trends over time

Future Enhancements

- Add filtering/sorting on watchlist
- Share current stats
- Dark mode
- Movie recommendations based on ratings

