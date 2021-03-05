import vlc


def play_video(videopath, fillervideopath):

    player = vlc.MediaPlayer(videopath)
    player.play()


if __name__ == "__main__":
    play_video(str(sys.argv[1]), str(sys.argv[2]))
