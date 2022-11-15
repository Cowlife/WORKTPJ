import time

from pygame_widgets.progressbar import ProgressBar


def progressing(screen):  # 0.1
    startTime = time.time()
    progressBar = ProgressBar(screen, 100, 100, 500, 40, lambda: (time.time() - startTime) / 10, curved=False) #10 seconds
    return progressBar
