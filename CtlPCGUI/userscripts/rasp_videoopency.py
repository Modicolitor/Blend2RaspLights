import sys
import vlc

import cv2


def play_video(videopath, fillervideopath):

    import cv2  # opencv

    cap = cv2.VideoCapture("testmovie.mp4")
    ret, frame = cap.read()
    while(1):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or ret == False:
            cap.release()
            cv2.destroyAllWindows()
            break
        cv2.imshow('frame', frame)

    #player = vlc.MediaPlayer(videopath)
    # player.play()


if __name__ == "__main__":
    play_video(str(sys.argv[1]), str(sys.argv[2]))
