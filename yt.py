#/usr/bin/python3

""" 
* A script to download youtube videos using pytube 
* This script is heavily dependend on the library pytube

"""

import sys 
import pytube
from pytube import YouTube, Playlist
from pytube.cli import on_progress
import pytube.request

def error(msg, err):
    print(msg)
    print(err)
    sys.exit(1)

def get_streams(vid_obj):  
    # get all the streams (mp4 with audio and video) from the link
    try:
        streams = vid_obj.streams.filter(file_extension="mp4", progressive=True)
        return streams
    except Exception as err:
        error(f"Failed to extract streams: {link}", err)

def get_resolution_dict(streams): 
    # return a dict of resolutions available in given streams
    resolutions = dict()
    for s in streams:
        resolutions[s.resolution] = s
    return resolutions

def download(vid_obj, resolution): 
    try:
        streams = get_streams(vid_obj)
        res_dict = get_resolution_dict(streams)

        if not (resolution in res_dict.keys()):
            error(f"Given video is not available in {resolution}")

        print(f"Downloading \"{res_dict[resolution].title}\"")
        res_dict[resolution].download()
        return True

    except Exception as err:
        print(f"Failed to download video : {res_dict[resolution].title}")
        print(err)
        return False

def parse_playlist_link(link):
    # return a list of all the youtube urls in a playlist
    try:
        p = Playlist(link)
        return p.video_urls
    except Exception as err:
        error("Unable to disassemble url", err)

def is_link_playlist(link):
    # return True or False
    try:
        p = Playlist(link)
        urls = p.video_urls
        if len(urls) > 0:
            return True
        else:
            print("Not a playlist\n")
            return False

    except Exception as err:
        print("Not a playlist\n")
        return False

def main():
    quality = "360p"
    pytube.request.default_range_size = 10000

    # take the user input for link
    link = ""
    while link == "":
        link = input("url: ")

    # if the link is a link to playlist download all vids
    if is_link_playlist(link):
        links = parse_playlist_link(link)
        print(f"{len(links)} to download")
        for l in links:
            vid = YouTube(link, on_progress_callback=on_progress)
            download(vid, quality)

    else:
        vid = YouTube(link, on_progress_callback=on_progress)
        download(vid, quality)


if __name__ == "__main__":
    main()
