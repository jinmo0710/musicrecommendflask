from flask import Flask, request, jsonify, render_template
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import os

app = Flask(__name__, template_folder='templates')

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    content = request.json
    mood = content['mood']
    genre = content['genre']
    
    query = f"{mood} {genre}"
    
    # 한국 곡만 검색
    if genre.lower() == 'k-pop':
        results_kr = sp.search(q=query, limit=25, type='track', market='KR')
        recommended_songs_kr = [{'title': track['name'], 'artist': track['artists'][0]['name'], 'url': track['external_urls']['spotify']} for track in results_kr['tracks']['items']]
        random.shuffle(recommended_songs_kr)
        selected_songs = recommended_songs_kr[:10]
    else:
        results_kr = sp.search(q=query, limit=15, type='track', market='KR')
        recommended_songs_kr = [{'title': track['name'], 'artist': track['artists'][0]['name'], 'url': track['external_urls']['spotify']} for track in results_kr['tracks']['items']]
        
        results_us = sp.search(q=query, limit=10, type='track', market='US')
        recommended_songs_us = [{'title': track['name'], 'artist': track['artists'][0]['name'], 'url': track['external_urls']['spotify']} for track in results_us['tracks']['items']]
        
        # 중복 제거
        combined_songs = recommended_songs_kr + recommended_songs_us
        unique_songs = {song['url']: song for song in combined_songs}.values()
        unique_songs = list(unique_songs)
        
        random.shuffle(unique_songs)
        selected_songs = unique_songs[:10]
    
    return jsonify({'songs': selected_songs})


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # Render가 제공하는 PORT 사용
    app.run(host="0.0.0.0", port=port)

