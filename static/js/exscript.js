document.getElementById('submit').addEventListener('click', async function () {
    const genre = document.getElementById('textBox').value;

    // Fetch song titles related to the genre from the backend (app.py)
    const response = await fetch(`/songs?genre=${genre}`);
    const songs = await response.json();

    // Clear the previous list
    const songsListDiv = document.getElementById('songsList');
    songsListDiv.innerHTML = '';

    // Display songs
    if (songs.length === 0) {
        songsListDiv.innerHTML = 'No songs found for this genre.';
    } else {
        for (let song of songs) {
            const songDiv = document.createElement('div');
            songDiv.innerHTML = `<span id="details-${song.title}"></span></p>`;
            songsListDiv.appendChild(songDiv);

            getSongDetails(song.title);
        }
    }
});
async function getSongDetails(songTitle) {
    const response = await fetch(`https://shazam.p.rapidapi.com/search?term=${songTitle}&locale=en-US&offset=0&limit=1`, {
        method: 'GET',
        headers: {
            "x-rapidapi-key": "9c65998478mshccdb8aa604f07a8p18c52ejsn9d3144756c73",
            "x-rapidapi-host": "shazam.p.rapidapi.com",
        }
    });
    const data = await response.json();
    console.log(data);
    const songDetailsDiv = document.getElementById(`details-${songTitle}`);
    setSongDataDisplay(data, songDetailsDiv);
}

function setSongDataDisplay(results, songDetailsDiv) {
    // Clear previous results
    songDetailsDiv.innerHTML = '';

    // Check if results have tracks
    if (results.tracks && results.tracks.hits.length > 0) {
        const tracks = results.tracks.hits;

        // Create a list element to add results
        const list = document.createElement('ul');

        // Loop through each track in the results
        tracks.forEach(track => {
            const item = document.createElement('li');
            // Get track details
            const songTitle = track.track.title;
            const artistName = track.track.subtitle;
            const songLink = track.track.url; // assuming there's a URL to the song or artist page
            // Create content for list item
            item.innerHTML = `
                <div class="music-card container">
                    <div class="col">
                        <div>
                            <img src="${track.track.images.coverart}" alt="" class="song-img" id="song-img">
                            <h4 id="title">Title: ${songTitle}</h4>
                            <a href="${track.track.images.background}" class="artist-img" id="artist-img" target="_blank">
                                <img src="${track.track.images.background}" class="artist-img" id="artist-img" style="width: 100px; height: 100px;">
                                <p id="artist-text">${artistName}</p>
                            </a>
                            <p id="genre">Artist: ${artistName}</p>
                            <a href="${songLink}" class="song-link" id="song-link" target="_blank">Listen on Shazam</a>
                        </div>
                    </div>
                </div>`;

            // Append the item to the list
            list.appendChild(item);
        });
        // Append the list to the song details container
        songDetailsDiv.appendChild(list);
    }
}