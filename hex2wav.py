'''
Created by Marcel Gerardino <skeptiker@sentineldr.com>

It may be that I'm bored but while disassembling some binaries I realized hex is perfect to turn into ABC musical
notation. Hex lacks g but has 9 which ironically is the only digit not used in music, and hell, it looks a lot like g.

Requires PySynth https://mdoege.github.io/PySynth/

If there is a problem, you fix it.
'''

import sys
import re
import pysynth
import os

def mtab(hexvals):
    tab = re.findall(r'[a-f9][0-8][1-9]', hexvals)
    if len(tab) > 0:
        tabt = []
        for i in tab:
            note = re.search('^.{2}', i)
            note = re.sub('9', 'g', note.group(0)).rstrip('0')
            duration = re.search('.$', i)
            tuplen = (note, int(duration.group(0)))
            tabt.append(tuplen)
        return tabt
    else:
        print "Nothing found to play. Perhaps try different offset"
        return

def wavc(tab):
    pysynth.make_wav(tab, fn="hex2wav.wav")
    return

def main():
    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            with open(file, 'rb') as f:
                if len(sys.argv) > 2:
                    bcount = sys.argv[2]
                else:
                    bcount = 100
                if len(sys.argv) > 3:
                    f.seek(int(sys.argv[3]))
                hexv = (f.read(int(bcount)).strip('\n')).encode('hex')
                f.close()
                tab = mtab(hexv)
                if tab is not None:
                    wavc(tab)
                    print hexv
                    if sys.platform == "linux" or sys.platform == "linux2":
                        os.system("aplay hex2wav.wav")
                    elif sys.platform == "darwin":
                        os.system("afplay hex2wav.wav")
                    elif sys.platform == "win32":
                        os.system("start hex2wav.wav")
        except IOError as err:
            print "I/O error({0}): {1}".format(err.errno, err.strerror)
        except:
            print '''usage: python hex2wav.py file -b --bytes bytes -o --offset offset
    file: the file to use to produce sound
    bytes: number of bytes/notes to read (default 100)
    offset: byte offset from where to read bytes/notes'''
    else:
        print "Need at least a file as argument"

if __name__ == "__main__":
    main()
