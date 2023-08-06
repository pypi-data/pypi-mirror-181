import subprocess
import shutil
from yoakecli.styling import *

class Player():
    __type1 = [
        ('vlc', 'vlc "{0}"  --meta-title "{1}"'),
        ('mpv', 'mpv "{0}"  --force-media-title="{1}"'),
        ('ffplay', 'ffplay "{0}"'),
    ]
    __type2 = {
        'am': [
            ('mxplayer', 'am start --user 0 -a android.intent.action.VIEW -d "{0}" -n com.mxtech.videoplayer.ad/.ActivityScreen -e "title" "{1}"'),
            ('vlc', 'am start --user 0 -a android.intent.action.VIEW -d "{0}" -n org.videolan.vlc/org.videolan.vlc.gui.video.VideoPlayerActivity -e "title" "{1}"'),
            ('mpv', 'am start --user 0 -a android.intent.action.VIEW -d "{0}" -n is.xyz.mpv/.MPVActivity'),
        ]
    }

    def play(ep, anime):
        command = None
        run = False
        
        if not command:
            for i in range(len(Player.__type1)):
                if shutil.which(Player.__type1[i][0]):
                    command = Player.__type1[i][1]
                    Player.__type1.insert(0, Player.__type1.pop(i))
                    break

        if command:
            process = subprocess.Popen(command.format(
                ep['path'], '{} - Tập {}'.format(anime['name'], ep['eps'])))
            process.wait()
            run = True
        else:
            for _, commands in Player.__type2.items():
                for i in range(len(commands)):
                    cmd = commands[i][1]
                    process = subprocess.Popen(cmd.format(ep['path'], '{} - Tập {}'.format(
                        anime['name'], ep['eps'])), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                    process.wait()
                    if not process.stderr.readlines():
                        run = True
                        commands.insert(0, commands.pop(i))
                        break
        return run
