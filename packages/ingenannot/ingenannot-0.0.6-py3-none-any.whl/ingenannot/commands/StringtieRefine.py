#/usr/bin/env python3

import logging
import re
import sys
import pyBigWig
import os
import shutil
import subprocess
import time

class StringtieRefine(object):

    def __init__(self, args):

        self.gff_transcripts = args.Gff_transcripts
        self.out = args.Output
        print(args)
        if "bigWigs" in args:
            self.bigwigs = args.bigWigs
        else:
            logging.info("No BW files, no transform")
            sys.exit(1)


    def convertBWtoWig(self, bw, wig):

        args = [bw, wig]
        cmd = ['bigWigToWig']
        cmd.extend(args)
        subprocess.call(cmd)

    def runJaccardClip(self, wig, out):

        stdout = open(out, 'w')
        args = ['/work/egip/transcript_assembly/jaccard/jaccard_wig_clipper.pl', '--jaccard_wig', wig, '--trough_win', '400']
        cmd = ['perl']
        cmd.extend(args)
        print(cmd)
        subprocess.call(cmd, stdout=stdout)
        stdout.close()


    def run(self):
        """launch command"""

        print(self.gff_transcripts)
        print(self.out)
        print(self.bigwigs)

        if len(self.bigwigs) == 1:
            logging.info("one bw file, data not oriented")
        elif len(self.bigwigs) == 2:
            logging.info("two bw files, data oriented, {} as forward cov file and {} as reverse cov file".format(self.bigwigs[0],self.bigwigs[1]))
        else:
            logging.info("Problem more than 2 bw files, exit")
            sys.exit(1)

        jaccard_clip = True
        if jaccard_clip:
            for i,bw in enumerate(self.bigwigs):
                #self.convertBWtoWig(bw, '{}.wig'.format(bw))
                self.runJaccardClip(bw, '{}.clip.wig'.format(i,bw))
                #self.runWigToBigWig()


        return 0
