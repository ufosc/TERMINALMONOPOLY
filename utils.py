# Loading animation function
import itertools
import sys
import time
loading = True
def loading_animation():
    for frame in itertools.cycle(['|', '/', '-', '\\']):
        if not loading:
            break
        sys.stdout.write(f'\rLoading {frame}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rLoading complete!     \n')