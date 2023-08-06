#/usr/bin/env python3

import logging
import re

from  ingenannot.Utils import Utils


class StringtieFilter(object):

    def __init__(self, args):

        self.gff_transcripts = args.Gff_transcripts
        self.gff_output = args.Output
        self.TPM = args.TPM
        self.len = args.len
        self.cov = args.cov



    def filter_and_export(self):

        tr_to_remove = ''
        tr_removed = []

        fh = open(self.gff_output, 'w')

        with open(self.gff_transcripts,'r') as f:
            for line in f:
                values = line.rstrip().split("\t")
                if len(values) == 9 and values[2] == 'transcript':
                    v = values[8].split(";")
                    d = {}
                    for val in v[:-1]:
                        val = val.replace(" ","")
                        k = val.split('"')[0]
                        i = val.split('"')[1]
                        d[k] = i
                    if  float(d['TPM']) < self.TPM:
                        tr_to_remove = d['transcript_id']
                        tr_removed.append(d['transcript_id'])
                    elif  float(d['cov']) < self.cov:
                        tr_to_remove = d['transcript_id']
                        tr_removed.append(d['transcript_id'])
                    elif int(values[4]) - int(values[3]) <= self.len:
                        tr_to_remove = d['transcript_id']
                        tr_removed.append(d['transcript_id'])
                    else:
                        fh.write(line)

                elif len(values) == 9 and values[2] == 'exon':
                    v = values[8].split(";")
                    d = {}
                    for val in v[:-1]:
                        val = val.replace(" ","")
                        #print("ici",val)
                        k = val.split('"')[0]
                        i = val.split('"')[1]
                        d[k] = i
                    if d['transcript_id'] != tr_to_remove:
                        fh.write(line)
                else:
                    fh.write(line)


    def run(self):
        """"launch command"""

        self.filter_and_export()

        return 0


