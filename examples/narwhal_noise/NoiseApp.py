from narwhal.nwtypes import attribute, cause, event
from narwhal.nwapp import NWApp

# app specific
from narwhal_noise.NoiseTree import *

# here we structure the output variables as desired. Pick a prefix like "N_"
# and put a polarity field in each one. The total polarity is a formula you, the
# client, must write below in the N_Summary class
# Each NAR corresponds with an intermediate sub-structure of the final data

# problem_/noise
problem = attribute(PROBLEM, SOUND)

# sound_/intensity_/source_/timeOfDay ::[me_/affect]
sound = attribute(attribute(attribute(SOUND, SOURCE), INTENSITY), TOD)

#[sound->me] :: me_/affect
affect = cause(attribute(SOUND, [TOD]), AFFECT)

# location _nearfar_/ source
proximity = attribute(LOC, SOURCE, PROX)


# (barrier_/state)-letInOut->sound
letin = event(attribute(BARRIER, [STATE]), SOUND, LETINOUT)


class NoiseApp:
    def __init__(self):
        nars_calibs_thresholds = [
            (problem, True, 0.6),
            (sound, True, 0.6),
            (affect, True, 0.6),
            (proximity, True, 0.6),
            (letin, True, 0.6),
        ]
        nars, calibs, thresholds = zip(*nars_calibs_thresholds)

        self.object = NWApp(EXPERIENCE, nars, calibs, thresholds)

    def run(self):
        text = ""
        while 1:
            text = input('Enter text: ')
            self.object.readText(text)
            h = self.object.report()
            print(h)
            print(self.object.printFinal())

    def test(self, text):
        self.object.readText(text)
        h = self.object.report(text)
        print(h)
        print(self.object.printFinal())

    def testFile(self, filename):
        fin = open(filename, "r")
        fout = open("output.txt", "w")

        s = "START"
        while len(s) > 0:
            s = fin.readline()
 #           if s=="\n" or len(s)<1 or s=='\n':
            if not s.strip():
                continue
            self.object.readText(s)
            fout.write(s)
            fout.write("A:")
            h = self.object.printFinal() + "\n"
            fout.write(h)
            print(s)
            print(h)

        fin.close()
        fout.close()
