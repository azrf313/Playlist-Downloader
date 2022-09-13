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
        streams = vid_obj.streams.filter(progressive=True)
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
    streams = get_streams(vid_obj)
    res_dict = get_resolution_dict(streams)

    try:
        print(f"Downloading \"{res_dict[resolution].title}\" ")
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
            return False

    except Exception as err:
        return False


def get_user_link():
    link = ""
    while (link == ""):
        link = input("Url > ")
    return link


def get_user_quality(available_qs):
    q = ""
    
    while (q == ""):
        q = input("Video quality > ")
        if (q not in available_qs):
            print(f"Invalid Quality, Available : {available_qs}\n")
            q = "" # start over

    return q

def find_q(link): # find the available downlaod qaulity for a given link and return a list
    y = YouTube(link)
    s = y.streams.filter(progressive=True)
    qs = []

    for i in s:
        qs.append(i.resolution)
    
    return qs

def main():
    pytube.request.default_range_size = 10000

    link = get_user_link()
    is_playlist = is_link_playlist(link)

    if (is_playlist):
        links = parse_playlist_link(link)
        available_q = find_q(links[0]) # q for quality
        print(f"\nChoose one from: {available_q}")
        user_q = get_user_quality(available_q)

        for link in links:
            vid = YouTube(link, on_progress_callback=on_progress)
            download(vid, user_q)

    else:
        available_q = find_q(link)
        print(f"\nChoose one from: {available_q}")
        user_q = get_user_quality(available_q)
        vid = YouTube(link, on_progress_callback=on_progress)
        download(vid, user_q)

    # link = "https://www.youtube.com/watch?v=ig3Qa6IINYo"
    # link = "https://www.youtube.com/watch?v=zgCnMvvw6Oo&list=PLpPXw4zFa0uKKhaSz87IowJnOTzh9tiBk"


if __name__ == "__main__":
    main()
