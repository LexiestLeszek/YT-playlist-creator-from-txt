import os
import google_auth_oauthlib.flow
import googleapiclient.discovery

# Load the OAuth client credentials from the JSON file
credentials_path = ""
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Remove this line if running on a production server

# Perform OAuth2 authorization
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
credentials = flow.run_local_server()

# Create an authenticated YouTube Data API client
youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

# Function to create a YouTube playlist
def create_playlist(playlist_name):
    # Create the playlist
    request = youtube.playlists().insert(
        part="snippet",
        body={
            "snippet": {
                "title": playlist_name,
                "description": "Playlist created by Python script"
            }
        }
    )
    response = request.execute()
    playlist_id = response["id"]
    print("Created playlist:", playlist_name)
    return playlist_id

# Read song names from the text file
with open('songs.txt', 'r') as file:
    song_names = file.read().splitlines()

# Create a YouTube playlist based on the song names
playlist_name = "My playlist"
playlist_id = create_playlist(playlist_name)

# Add songs to the playlist
for song_name in song_names:
    # Search for the song on YouTube
    search_request = youtube.search().list(
        part="id",
        q=song_name,
        type="video",
        maxResults=1
    )
    search_response = search_request.execute()

    # Check if any search results were found
    if len(search_response["items"]) > 0:
        video_id = search_response["items"][0]["id"]["videoId"]

        # Add the video to the playlist
        playlist_item_request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        playlist_item_request.execute()
    else:
        print("No search results found for:", song_name)

print("Playlist created successfully!")
