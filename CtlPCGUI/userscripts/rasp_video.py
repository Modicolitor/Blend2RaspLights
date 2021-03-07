import sys
import vlc as vl
from time import sleep


def play_video(videopath, fillervid):

    vlc = vl.Instance()

    player = vlc.media_player_new()
    #video = "Sidefight.mp4"
    media = vlc.media_new(videopath)

    player.set_media(media)
    print(videopath)
    player.set_fullscreen(True)
    player.play()

    # player.set_fullscreen(True)
    sleep(5)  # Or however long you expect it to take to open vlc
    # while player.is_playing():
    #    sleep(1)
    #duration = player.get_length()
    print(fillervid)
    media2 = vlc.media_new(fillervid)
    player.set_media(media2)
    player.play()
    sleep(5)
    while player.is_playing():
        sleep(1)

    # sleep(2)
    print("sfg")


if __name__ == "__main__":
    play_video(str(sys.argv[1]), str(sys.argv[2]))
