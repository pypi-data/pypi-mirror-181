#/usr/bin/env python3

import logging
import re

from  ingenannot.Utils import Utils


class StringtieJaclip(object):

    def __init__(self, args):

        self.gff_transcripts = args.Gff_transcripts
        self.fasta_clip = args.Fasta_clip
        self.gff_output = args.Output

    def transcripts_to_clip(self):

        tr_to_clip = {}
        with open(self.fasta_clip, 'r') as f:
            for line in f:
                m = re.search(r"^>(.*)(\.)(\d+)-(\d+);(.*)(\s)gene=(.*)", line)
                if m:
                    if m.group(5) in tr_to_clip:
                        tr_to_clip[m.group(5)].append((int(m.group(3)),int(m.group(4))))
                    else:
                        tr_to_clip[m.group(5)] = [(int(m.group(3)),int(m.group(4)))]

        return tr_to_clip


    def clip_and_export(self, genes, tr_to_clip):

        fh = open(self.gff_output, 'w')

        for g in genes:
            for tr in g.lTranscripts:
                strand = "+"
                if tr.strand == -1:
                    strand = "-"
                if tr.id in tr_to_clip:
                    if tr.strand == -1:
                        mytr = [0]*(tr.end-tr.start+1)
                        for e in tr.lExons:
                            for i in range(e.start-tr.start,e.end-tr.start+1):
                                mytr[i] = 1
                        for cut in tr_to_clip[tr.id]:
                            start = None
                            end = None
                            idx_start = None
                            idx_end = None
                            count = sum(mytr)
                            for idx,val in enumerate(mytr):
                                if count == cut[0]:
                                    end = tr.start + idx
                                    idx_end = idx
                                if count == cut[1]:
                                    start = tr.start + idx
                                    idx_start = idx
                                count -= val
                            fh.write("{}\tJaClip\ttranscript\t{}\t{}\t.\t{}\t.\ttranscript_id \"{}\";\n".format(tr.seqid, start, end,strand,"{}_{}-{}".format(tr.id,cut[0],cut[1])))
                            e_start = None
                            e_end = None
                            for idx, val in enumerate(mytr[idx_start:idx_end]):
                                if (val == 1) and not(e_start):
                                    e_start = idx+idx_start+tr.start
                                if (val == 0) and e_start:
                                    e_end = idx+idx_start+tr.start -1
                                if e_start and e_end:
                                    fh.write("{}\tJaClip\texon\t{}\t{}\t.\t{}\t.\ttranscript_id \"{}\";\n".format(e.seqid, e_start, e_end,strand,"{}_{}-{}".format(tr.id,cut[0],cut[1])))
                                    e_start = None
                                    e_end = None
                            if e_start and not(e_end):
                                    e_end = idx_end+tr.start
                                    fh.write("{}\tJaClip\texon\t{}\t{}\t.\t{}\t.\ttranscript_id \"{}\";\n".format(e.seqid, e_start, e_end,strand,"{}_{}-{}".format(tr.id,cut[0],cut[1])))
                    else:
                        mytr = [0]*(tr.end-tr.start+1)
                        for e in tr.lExons:
                            for i in range(e.start-tr.start,e.end-tr.start+1):
                                mytr[i] = 1
                        for cut in tr_to_clip[tr.id]:
                            start = None
                            end = None
                            idx_start = None
                            idx_end = None
                            count = 0
                            for idx,val in enumerate(mytr):
                                count += val
                                if count == cut[0]:
                                    start = tr.start + idx
                                    idx_start = idx
                                if count == cut[1]:
                                    end = tr.start + idx
                                    idx_end = idx
                            fh.write("{}\tJaClip\ttranscript\t{}\t{}\t.\t{}\t.\ttranscript_id \"{}\";\n".format(tr.seqid, start, end,strand,"{}_{}-{}".format(tr.id,cut[0],cut[1])))
                            e_start = None
                            e_end = None
                            for idx, val in enumerate(mytr[idx_start:idx_end]):
                                if (val == 1) and not(e_start):
                                    e_start = idx+idx_start+tr.start
                                if (val == 0) and e_start:
                                    e_end = idx+idx_start+tr.start-1
                                if e_start and e_end:
                                    fh.write("{}\tJaClip\texon\t{}\t{}\t.\t{}\t.\ttranscript_id \"{}\";\n".format(e.seqid, e_start, e_end,strand,"{}_{}-{}".format(tr.id,cut[0],cut[1])))
                                    e_start = None
                                    e_end = None
                            if e_start and not(e_end):
                                    e_end = idx_end+tr.start
                                    fh.write("{}\tJaClip\texon\t{}\t{}\t.\t{}\t.\ttranscript_id \"{}\";\n".format(e.seqid, e_start, e_end,strand,"{}_{}-{}".format(tr.id,cut[0],cut[1])))
                else:
                    fh.write("{}\tJaClip\ttranscript\t{}\t{}\t.\t{}\t.\ttranscript_id \"{}\";\n".format(tr.seqid, tr.start, tr.end,strand,tr.id))
                    for e in tr.lExons:
                        fh.write("{}\tJaClip\texon\t{}\t{}\t.\t{}\t.\ttranscript_id \"{}\";\n".format(e.seqid, e.start, e.end,strand,tr.id))


    def run(self):
        """"launch command"""

        genes = Utils.extract_genes(self.gff_transcripts)
        tr_to_clip = self.transcripts_to_clip()

        self.clip_and_export(genes, tr_to_clip)

        return 0
