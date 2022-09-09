""" 
* A script to download youtube videos using pytube 
* This script is heavily depended on the library pytube

"""

from pytube import YouTube, Playlist

def get_streams(link):  # get all the streams (mp4 with audio and video) from the link
    try:
        vid = YouTube(link)
        streams = vid.streams.filter(file_extension="mp4", progressive=True)
        return streams
    except Exception as err:
        print(f"Failed to parse link : {link}")
        print(err)
        return 0

def get_resolution_dict(streams): # return a dict of resolutions available in given streams
    resolutions = dict()
    for s in streams:
        resolutions[s.resolution] = s
    return resolutions

def download(resolution, res_dict): # download the stream from the dict using given resolution
    try:
        print(f"Downloading [{res_dict[resolution].title}]")
        res_dict[resolution].download()
        return 1
    except Exception as err:
        print("Failed to download video : {res_dict[resolution].title}")
        print(err)
        return 0

def parse_playlist_link(link):
    # return a list of all the youtube urls in a playlist
    try:
        p = Playlist(link)
        return p.video_urls
    except Exception as err:
        print("Unable to disassemble url")
        print(err)
        return 0

def main():
    link = input("url: ")

    # if the link is a link to playlist download all vids
    if "playlist" in link:
        links = parse_playlist_link(link)

        print(len(links), "Total links to download")
        for l in links:
            streams = get_streams(l)
            d = get_resolution_dict(streams)
            download("360p", d)

    # download the single video
    else:
        streams = get_streams(link)
        d = get_resolution_dict(streams)
        download("360p", d)


if __name__ == "__main__":
    main()
