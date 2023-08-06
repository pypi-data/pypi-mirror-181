#!/usr/bin/env python3

import pysam
import skbio
import numpy as np
from collections import Counter
from skbio import Protein
from ingenannot.Commands.Command import Command
from ingenannot.Utils import Utils
from math import *

from ingenannot.Entities.CDS import CDS

class AddIsoforms(Command):

    def __init__(self, args):

        self.gff_gene = args.Gff_genes
        self.gff_transcripts = args.Gff_transcripts
        self.gff_output = args.Output
        self.bam_fof = args.Bam_fof
        self.BLOSUM50 = self.get_blosum50()


    def extract_states(self,tr, tr_tp):
        """
        compare new 2 transcripts and return
        differences as states
        """

        l_diff_bases,min_pos,max_pos = tr.get_diff_vs_another_transcript(tr_tp)
        codeToState = {0:'I',1:'AS',2:'IR',3:'E'}
        states = []
        start = min_pos
        end = min_pos
        prev_state = l_diff_bases[0]
        cur_state = l_diff_bases[0]
        
        for i,base in enumerate(l_diff_bases[1:]):
            if base != cur_state:
                prev_state = cur_state
                cur_state = base
                states.append((codeToState[prev_state], start, end))
                start = end + 1
            end += 1
        states.append((codeToState[cur_state],start, end))

        return states


    def get_AS_IR_events_in_annotated_regions(self, states):
        """
        export significative AS, IR events, when previous
        area with common exons found. No specific AS, IR
        in UTR exported.
        """

        check_exon_5_prime = False
        view_event = False
        current_event = None
        RReck_exon_3_prime = False
        events_to_check = []

        for s in states:
            if s[0] == 'E':
                check_exon_5_prime = True
            if (s[0] == 'AS' or s[0] == 'IR') and check_exon_5_prime:
                view_event = True
                current_event = s
            if s[0] == 'E' and check_exon_5_prime and view_event:
                events_to_check.append(current_event)
                current_event = None
                view_event = False

        return events_to_check

    def AS_event_validation (self,event_to_check,chr,strand,bam_file):

        sam_file = pysam.AlignmentFile(bam_file, "rb")
        start = event_to_check[1]-1
        stop = event_to_check[2]

        depth_start = 0
        depth_stop = 0
        junction_support_read = 0
        paired = True


        for reads in sam_file.fetch(chr,start-1,start) :
            if not reads.is_paired:
                paired = False

        if paired:

            for reads in sam_file.fetch(chr,start-1,start) :
                if strand == -1:
                    if (reads.is_reverse and reads.is_read2) or ((not reads.is_reverse) and reads.is_read1):
                        depth_start +=1
                else:
                    if (reads.is_reverse and reads.is_read1) or ((not reads.is_reverse) and reads.is_read2):
                        depth_start +=1

            for reads in sam_file.fetch(chr,stop,stop+1) :
                if strand == -1:
                    if (reads.is_reverse and reads.is_read2) or ((not reads.is_reverse) and reads.is_read1):
                        depth_stop +=1
                else:
                    if (reads.is_reverse and reads.is_read1) or ((not reads.is_reverse) and reads.is_read2):
                        depth_stop +=1

            for reads in sam_file.fetch(chr,start,start+1) :

                if strand == -1:
                    if (reads.is_reverse and reads.is_read2) or ((not reads.is_reverse) and reads.is_read1):
                        cigar = reads.cigartuples
                        nb_n=0
                        for n in cigar:
                            if (n[0]==3 and n[1] == stop-start): nb_n+=1
                        if nb_n != 0 :
                            i = 0
                            sum_bf_skip = 0
                            while not (cigar[i][0] == 3 and cigar[i][1] == stop-start):
                                if (cigar[i][0] == 0) or (cigar[i][0] == 1) or (cigar[i][0] == 2) or (cigar[i][0] == 3) :
                                    sum_bf_skip += cigar[i][1]
                                i +=1
                            if (sum_bf_skip+reads.reference_start == start) and (cigar[i][1]+start == stop) and (sum_bf_skip > 4):
                                junction_support_read +=1
                else:
                    if (reads.is_reverse and reads.is_read1) or ((not reads.is_reverse) and reads.is_read2):
                        cigar = reads.cigartuples
                        nb_n=0
                        for n in cigar:
                            if (n[0]==3 and n[1] == stop-start): nb_n+=1
                        if nb_n != 0 :
                            i = 0
                            sum_bf_skip = 0
                            while not (cigar[i][0] == 3 and cigar[i][1] == stop-start):
                                if (cigar[i][0] == 0) or (cigar[i][0] == 1) or (cigar[i][0] == 2) or (cigar[i][0] == 3) :
                                    sum_bf_skip += cigar[i][1]
                                i +=1
                            if (sum_bf_skip+reads.reference_start == start) and (cigar[i][1]+start == stop) and (sum_bf_skip > 4):
                                junction_support_read +=1



        else :

            for reads in sam_file.fetch(chr,start-1,start) :
                if strand == -1:
                    if not reads.is_reverse :
                        depth_start +=1
                else:
                    if reads.is_reverse :
                        depth_start +=1

            for reads in sam_file.fetch(chr,stop,stop+1) :
                if strand == -1:
                    if not reads.is_reverse:
                        depth_stop +=1
                else:
                    if reads.is_reverse :
                        depth_stop +=1

            for reads in sam_file.fetch(chr,start,start+1) :

                if strand == -1:
                    if not reads.is_reverse :
                        cigar = reads.cigartuples
                        nb_n=0
                        for n in cigar:
                            if (n[0]==3 and n[1] == stop-start): nb_n+=1
                        if nb_n != 0 :
                            i = 0
                            sum_bf_skip = 0
                            while not (cigar[i][0] == 3 and cigar[i][1] == stop-start):
                                if (cigar[i][0] == 0) or (cigar[i][0] == 1) or (cigar[i][0] == 2) or (cigar[i][0] == 3) :
                                    sum_bf_skip += cigar[i][1]
                                i +=1
                            if (sum_bf_skip+reads.reference_start == start) and (cigar[i][1]+start == stop) and (sum_bf_skip > 4):
                                junction_support_read +=1
                else:
                    if reads.is_reverse :
                        cigar = reads.cigartuples
                        nb_n=0
                        for n in cigar:
                            if (n[0]==3 and n[1] == stop-start): nb_n+=1
                        if nb_n != 0 :
                            i = 0
                            sum_bf_skip = 0
                            while not (cigar[i][0] == 3 and cigar[i][1] == stop-start):
                                if (cigar[i][0] == 0) or (cigar[i][0] == 1) or (cigar[i][0] == 2) or (cigar[i][0] == 3) :
                                    sum_bf_skip += cigar[i][1]
                                i +=1
                            if (sum_bf_skip+reads.reference_start == start) and (cigar[i][1]+start == stop) and (sum_bf_skip > 4):
                                junction_support_read +=1

        out={}
        out['strat pos'] = start
        out['stop pos'] = stop
        out['depth start']= depth_start
        out['depth stop']=depth_stop
        out['AS support']= junction_support_read
        out['ratio']=max(junction_support_read/max(1,depth_start),junction_support_read/max(1,depth_stop))
        
        return(out)



    def IR_event_validation(self,event_to_check,chr,strand,bam_file):
        
        sam_file = pysam.AlignmentFile(bam_file, "rb")
        
        start = event_to_check[1]-1
        stop = event_to_check[2]

        pileup = sam_file.pileup(chr,start,stop,truncate = True,min_base_quality=0)
        IR_support_reads = []
        depth_start = 0
        depth_stop = 0
        paired = True

        for reads in sam_file.fetch(chr,start-1,start) :
            if not reads.is_paired:
                paired = False

        if paired:

            for reads in sam_file.fetch(chr,start-1,start) :
                if strand == -1:
                    if (reads.is_reverse and reads.is_read2) or ((not reads.is_reverse) and reads.is_read1):
                        depth_start +=1
                else:
                    if (reads.is_reverse and reads.is_read1) or ((not reads.is_reverse) and reads.is_read2):
                        depth_start +=1

            for reads in sam_file.fetch(chr,stop,stop+1) :
                if strand == -1:
                    if (reads.is_reverse and reads.is_read2) or ((not reads.is_reverse) and reads.is_read1):
                        depth_stop +=1
                else:
                    if (reads.is_reverse and reads.is_read1) or ((not reads.is_reverse) and reads.is_read2):
                        depth_stop +=1


            for pileupcolumn in pileup:
                support_reads = 0
                for pileupread in pileupcolumn.pileups:
                        if strand == -1:
                            if (pileupread.alignment.is_reverse and pileupread.alignment.is_read2) or ((not pileupread.alignment.is_reverse) and pileupread
        .alignment.is_read1):
                                if not pileupread.is_refskip: support_reads +=1


                        else:
                            if (pileupread.alignment.is_reverse and pileupread.alignment.is_read1) or ((not pileupread.alignment.is_reverse) and pileupread
        .alignment.is_read2):
                                if not pileupread.is_refskip: support_reads +=1

                IR_support_reads.append(support_reads)

        else:

            for reads in sam_file.fetch(chr,start-1,start) :
                if strand == -1:
                    if not reads.is_reverse :
                        depth_start +=1
                else:
                    if reads.is_reverse :
                        depth_start +=1

            for reads in sam_file.fetch(chr,stop,stop+1) :
                if strand == -1:
                    if not reads.is_reverse:
                        depth_stop +=1
                else:
                    if reads.is_reverse :
                        depth_stop +=1
            for pileupcolumn in pileup:
                support_reads = 0
                for pileupread in pileupcolumn.pileups:
                        if strand == -1:
                            if not pileupread.alignment.is_reverse :
                                if not pileupread.is_refskip: support_reads +=1


                        else:
                            if pileupread.alignment.is_reverse:
                                if not pileupread.is_refskip: support_reads +=1

                IR_support_reads.append(support_reads)


        IR_support_reads.sort()

        out={}
        out['strat pos'] = start
        out['stop pos'] = stop
        out['depth start']= depth_start
        out['depth stop']=depth_stop
        out['mean depth']=(depth_start+depth_stop)/2
        out['median support']= 0
        out['min support']= 0
        out['mean IR support']= 0
        out['ratio']= 0

        if  IR_support_reads:
            out['median support']=IR_support_reads[floor(len(IR_support_reads)/2)]
            out['min support']=IR_support_reads[0]
            out['mean IR support']= sum(IR_support_reads)/len(IR_support_reads)
            out['ratio']= out['mean IR support']/max(1,out['mean depth'])
        return(out)


    def inferring_cds(self, tr, tr_tp):
        """
        try to find CDS sequence with
        strong postulate on the original
        annotation
        """
        genome = "/work/egip/annotation_comparison/data/Mygr_323_reformat_with_mito.clean.fsa"


        fh = pysam.FastaFile(genome)
        min_cds = tr.get_min_cds_start() - 1
        max_cds = tr.get_max_cds_end()
        cds_seq = ''
        for cds in sorted(tr.lCDS, key=lambda x : x.start):
           cds_seq +=  fh.fetch(cds.seqid, cds.start-1, cds.end)
        if tr.strand == -1:
            cds_seq = Utils.reverse_complement(cds_seq)
        prot = ""
#        print(tr.id)
#        print(cds_seq)
        for i in range(0,len(cds_seq),3):
            prot += Utils.translate(cds_seq[i:i+3].upper())
#        print(prot)


        cds_seq_tp = ''
#        for exon in sorted([ex for ex in tr_tp.lExons if ex.end > min_cds and ex.start < max_cds], key=lambda x : x.start):
        lexons = sorted(tr_tp.lExons , key=lambda x : x.start)
        for exon in lexons:
#            cds_seq_tp += fh.fetch(exon.seqid, max(exon.start-1,min_cds), min(exon.end, max_cds))
            cds_seq_tp += fh.fetch(exon.seqid, exon.start-1, exon.end)
#            if tr_tp.strand == 1:
#                cds_seq_tp += fh.fetch(exon.seqid, max(exon.start-1,min_cds), exon.end)
#            if tr_tp.strand == -1:
#                cds_seq_tp += fh.fetch(exon.seqid, min_cds, min(max_cds,exon.end))
        if tr_tp.strand == -1:
            cds_seq_tp = Utils.reverse_complement(cds_seq_tp)





        ## look initial CDS start in intron 
        if tr_tp.strand == 1:
            lcds = sorted(tr.lCDS, key=lambda x : x.start)
            cds_start = lcds[0].start
            out = True
            lexons = sorted(tr_tp.lExons , key=lambda x : x.start)
            for exon in lexons:
                if cds_start >= exon.start and cds_start <= exon.end:
                    out = False
                    break
            if out == True:
                if cds_start < lexons[0].start:
                    print ("AAAAA REMOVE: {} - {}".format(tr.id, tr_tp.id))
                else:
#                    print ("IIIIIIIIIIIIIII: {} - {}".format(tr.id, tr_tp.id))
#                    print(prot)
#                    print(cds_seq)
#                    print(cds_seq_tp)
                    orfs, positions = self.getlongestORF(cds_seq_tp, floor(len(prot)*0.5))
                    sk_prot = Protein(prot)

                    # on garde si prot > 70% longueur, si fin pareil, si algmt de plus de 
                    for i,orf in enumerate(orfs):
                        sk_orf = Protein(orf)
                        algmt, score, coordinates = skbio.alignment.local_pairwise_align_ssw(sk_prot, sk_orf, gap_open_penalty=11, gap_extend_penalty=1, substitution_matrix=self.BLOSUM50)

                        #print(algmt.conservation())
                        #print(Counter(algmt.conservation()))
                        c = Counter(algmt.conservation())
                        print("ratio len: {}".format(len(orf)/len(prot)))
                        print("% aligned: {}".format(c[1.0]/len(orf)))
                        len_ratio = len(orf)/len(prot)
                        percent_aligned = c[1.0]/len(orf)
                        if len_ratio > 0.5 and len_ratio < 1.5 and percent_aligned > 0.3:
                            print("ON GARDE {}\n{}".format(tr_tp.id, orf))

                            cds_seq_tp_start = self.infer_cds_start(tr_tp,positions[i][0])
                            cds_seq_tp_end = self.infer_cds_end(tr_tp, positions[i][1])
#                            print(cds_seq_tp_start , tr_tp.get_min_exon_start(), positions[i][0], positions[i][2])
#                            print(cds_seq_tp_end, tr_tp.get_max_exon_end() , positions[i][1])
#                            print(tr_tp)

                            self.infer_cds_coordinates(tr_tp, cds_seq_tp_start, cds_seq_tp_end)
                            return True


        else:
            lcds = sorted(tr.lCDS, key=lambda x : x.start)
            cds_start = lcds[-1].end
            out = True
            lexons = sorted(tr_tp.lExons , key=lambda x : x.start)
            for exon in lexons:
                if cds_start >= exon.start and cds_start <= exon.end:
                    out = False
                    break
            if out == True:
                if cds_start > lexons[-1].end:
                    print ("AAAAA REMOVE: {} - {}".format(tr.id, tr_tp.id))
                else:
#                    print ("IIIIIIIIIIIIIII: {} - {}".format(tr.id, tr_tp.id))
#                    print(prot)
#                    print(cds_seq)
#                    print(cds_seq_tp)
#                    print(len(prot), floor(len(prot)*0.5))
                    orfs, coordinates = self.getlongestORF(cds_seq_tp,floor(len(prot)*0.5))
                    sk_prot = Protein(prot)

                    # on garde si prot > 70% longueur, si fin pareil, si algmt de plus de 
                    for orf in orfs:
                        sk_orf = Protein(orf)
                        algmt, score, coordinates = skbio.alignment.local_pairwise_align_ssw(sk_prot, sk_orf, gap_open_penalty=11, gap_extend_penalty=1, substitution_matrix=self.BLOSUM50)

                        #print(algmt.conservation())
                        #print(Counter(algmt.conservation()))
                        c = Counter(algmt.conservation())
                        print("ratio len: {}".format(len(orf)/len(prot)))
                        print("% aligned: {}".format(c[1.0]/len(orf)))
                        len_ratio = len(orf)/len(prot)
                        percent_aligned = c[1.0]/len(orf)
                        if len_ratio > 0.5 and len_ratio < 1.5 and percent_aligned > 0.3:
                            print("ON GARDE {}\n{}".format(tr_tp.id, orf))


        prot_tp = ""
        for i in range(0,len(cds_seq_tp),3):
            codon = cds_seq_tp[i:i+3]
            if len(codon) == 3:
                prot_tp += Utils.translate(cds_seq_tp[i:i+3].upper())
#        print(prot_tp)






        if tr.id == "mRNA:chr_1g0019761":

            if prot == prot_tp[0:len(prot)]:
                print("SAME PROTEIN")
                print(tr.id, tr_tp.id)
                return "SAMEPROTEIN"
            else:
                for i, aa in enumerate(prot_tp):
                    if aa == "*": 
                        if i+1 <= floor(len(prot)*0.9):
                            print("NM DECAY")
                            return "NMDECAY"
                            break
                        else:
                            print("AUTRE")
    #                        print(tr.id, tr_tp.id)
    #                        print(prot)
    #                        print(prot_tp)
                            return "AUTRE"
                            break
    


    def infer_cds_start(self, tr, start):

        cds_start = tr.get_min_exon_start()
        delta = start
        for ex in sorted(tr.lExons , key=lambda x : x.start):
            for i in range(ex.start, ex.end+1):
                if delta >= 0:
                    cds_start = i
                    delta = delta - 1
        return cds_start

    def infer_cds_end(self, tr, start):

        cds_start = tr.get_min_exon_start()
        delta = start
        for ex in sorted(tr.lExons , key=lambda x : x.start):
            for i in range(ex.start, ex.end+1):
                if delta >= 0:
                    cds_start =  i
                    delta = delta - 1
        return cds_start + 2




    def infer_cds_coordinates(self,tr,start, end):

        print(start)
        print(end)
        from datetime import datetime
        # current date and time
        now = datetime.now()

        for ex in tr.lExons:
            if ex.end > start and ex.start < end:
                idx =  datetime.timestamp(now)
                cds = CDS(idx,tr.seqid,max(ex.start,start),min(ex.end,end),tr.strand,-1,tr.id)
                tr.add_cds(cds)

    def run(self):


        ### Change ORDER 
        ### test support if AUTRE, NM DECAY, mais pas SAME Protein


        ### TODO:
        ### status validate or not
        ### validaton with several bams
        ### test translation
        ### add iso

        threshold_AS = 0.1
        threshold_IR = 0.1
        bam_files =[]
        with open(self.bam_fof, 'r') as f:
            for line in f:
               bam_files.append(line.rstrip("\n"))
        bam_file = 0
#        print('bam_files', bam_files)
        tr_to_genes = {}
        genes_to_update = {}
        tr_tp_to_remove = set()

        genes = Utils.extract_genes(self.gff_gene)
        references = set([g.seqid for g in genes])
        strands = [1,-1]
        tr_templates = Utils.extract_genes(self.gff_transcripts)

        with open(self.gff_output, 'w') as f:
            for ref in ["chr_1"]:
    #        for ref in references:
                print("ref",ref)
                for strand in strands:
                    print("strand",strand)
                    g_tp_ref_str = [gene for gene in tr_templates if (gene.seqid == ref) & (gene.strand == strand)]
                    g_ref_str = [gene for gene in genes if (gene.seqid == ref) & (gene.strand == strand)]
                    for g_tp in g_tp_ref_str:
                        for g in g_ref_str:
                            if g.is_feature_spanning(g_tp):
                             #   l_tr_tp = deepcopy.copy(gt_tp.lTranscripts)
                                for tr_tp in g_tp.lTranscripts:
                                    for tr in g.lTranscripts:
                                            tr_to_genes[tr.id] = []

                                            print("ICICICICIC: {} - {}".format(tr.id, tr_tp.id))
                                            states =  self.extract_states(tr, tr_tp)
                                            events_to_check = self.get_AS_IR_events_in_annotated_regions(states)
                                            if events_to_check:
#                                                print('#### {} {} -- {}'.format(tr_tp.seqid,tr_tp.id,events_to_check))
                                                CDS = self.inferring_cds(tr, tr_tp)
                                                if CDS == True:
                                                    print("OK TRUE")
                                                    g.add_transcript_with_update(tr_tp)
                                                    break
#                                                if CDS == "AUTRE" or CDS == "INMDECAY":
#                                                    validate = False
#                                                    chr = tr.seqid
#                                                    strand = tr.strand 
#                                                    for e in events_to_check:
#                                                        if e[0] == 'AS':
#                                                            #print(self.AS_event_validation(e,chr,strand))
#                                                            #f.write(str(self.AS_event_validation(e,chr,strand)) + "\n")a
#                                                             for bam_file in bam_files:
#                                                                if validate == False:      
#                                                                    res = self.AS_event_validation(e,chr,strand,bam_file)
#                                                                    if res['ratio'] > threshold_AS:
#                                                                        validate = True
#        
#                                                        if e[0] == 'IR':
#                                                            #print(self.IR_event_validation(e,chr,strand))
#                                                            #f.write(str(self.IR_event_validation(e,chr,strand)) + "\n")
#                                                            for bam_file in bam_files:
#                                                                if validate == False:    
#                                                                    res = self.IR_event_validation(e,chr,strand,bam_file)
#                                                                    if res['ratio'] > threshold_IR:
#                                                                        validate = True
#            
#                                                    if validate:
#                                                        print("isoform to add")
#                                                    else:
#                                                        print("not validated by the bam: {}".format(tr_tp))
        f.close()


        self.export(genes)
        return 0


    def getlongestORF(self, cds_seq, minlen):

        all_prots = []
        all_coordinates = []
        for frame in range(0,3):
            prot = ''
            for i in range(frame,len(cds_seq),3):
                codon = cds_seq[i:i+3]
                if len(codon) == 3:
                    prot += Utils.translate(cds_seq[i:i+3].upper())
            prots, coordinates = self._get_longest_orfs(prot, minlen, frame)
            all_prots.extend(prots)
            all_coordinates.extend(coordinates)

            #print("frame {}: {}".format(frame,prot))
            #print("frame {}: {}".format(frame,prots))
#        print(all_prots)
        return all_prots, all_coordinates


#

    def _get_longest_orfs(self, prot, minlen, frame):

        start = False
        cur_prot = ''
        prots = []
        coordinates = []
        pos_start = None
        pos_end = None
        for i, aa in enumerate(prot):
            if start and aa != '*':
                cur_prot += aa
            if start and aa == '*':
                if len(cur_prot) >= minlen:
                    pos_end = i*3 + frame
                    prots.append(cur_prot)
                    coordinates.append((pos_start,pos_end, frame))
                    cur_prot = ''
                    start = False
                    pos_start = None
                    pos_end = None
            if aa == 'M' and start == False:
                start = True
                cur_prot += aa
                pos_start = i*3 + frame
        return prots, coordinates



    def get_blosum50(self):

        blosum50 = \
    {
        '*': {'*': 1, 'A': -5, 'C': -5, 'B': -5, 'E': -5, 'D': -5, 'G': -5,
              'F': -5, 'I': -5, 'H': -5, 'K': -5, 'M': -5, 'L': -5,
              'N': -5, 'Q': -5, 'P': -5, 'S': -5, 'R': -5, 'T': -5,
              'W': -5, 'V': -5, 'Y': -5, 'X': -5, 'Z': -5},
        'A': {'*': -5, 'A': 5, 'C': -1, 'B': -2, 'E': -1, 'D': -2, 'G': 0,
              'F': -3, 'I': -1, 'H': -2, 'K': -1, 'M': -1, 'L': -2,
              'N': -1, 'Q': -1, 'P': -1, 'S': 1, 'R': -2, 'T': 0, 'W': -3,
              'V': 0, 'Y': -2, 'X': -1, 'Z': -1},
        'C': {'*': -5, 'A': -1, 'C': 13, 'B': -3, 'E': -3, 'D': -4,
              'G': -3, 'F': -2, 'I': -2, 'H': -3, 'K': -3, 'M': -2,
              'L': -2, 'N': -2, 'Q': -3, 'P': -4, 'S': -1, 'R': -4,
              'T': -1, 'W': -5, 'V': -1, 'Y': -3, 'X': -1, 'Z': -3},
        'B': {'*': -5, 'A': -2, 'C': -3, 'B': 6, 'E': 1, 'D': 6, 'G': -1,
              'F': -4, 'I': -4, 'H': 0, 'K': 0, 'M': -3, 'L': -4, 'N': 5,
              'Q': 0, 'P': -2, 'S': 0, 'R': -1, 'T': 0, 'W': -5, 'V': -3,
              'Y': -3, 'X': -1, 'Z': 1},
        'E': {'*': -5, 'A': -1, 'C': -3, 'B': 1, 'E': 6, 'D': 2, 'G': -3,
              'F': -3, 'I': -4, 'H': 0, 'K': 1, 'M': -2, 'L': -3, 'N': 0,
              'Q': 2, 'P': -1, 'S': -1, 'R': 0, 'T': -1, 'W': -3, 'V': -3,
              'Y': -2, 'X': -1, 'Z': 5},
        'D': {'*': -5, 'A': -2, 'C': -4, 'B': 6, 'E': 2, 'D': 8, 'G': -1,
              'F': -5, 'I': -4, 'H': -1, 'K': -1, 'M': -4, 'L': -4, 'N': 2,
              'Q': 0, 'P': -1, 'S': 0, 'R': -2, 'T': -1, 'W': -5, 'V': -4,
              'Y': -3, 'X': -1, 'Z': 1},
        'G': {'*': -5, 'A': 0, 'C': -3, 'B': -1, 'E': -3, 'D': -1, 'G': 8,
              'F': -4, 'I': -4, 'H': -2, 'K': -2, 'M': -3, 'L': -4, 'N': 0,
              'Q': -2, 'P': -2, 'S': 0, 'R': -3, 'T': -2, 'W': -3, 'V': -4,
              'Y': -3, 'X': -1, 'Z': -2},
        'F': {'*': -5, 'A': -3, 'C': -2, 'B': -4, 'E': -3, 'D': -5,
              'G': -4, 'F': 8, 'I': 0, 'H': -1, 'K': -4, 'M': 0, 'L': 1,
              'N': -4, 'Q': -4, 'P': -4, 'S': -3, 'R': -3, 'T': -2, 'W': 1,
              'V': -1, 'Y': 4, 'X': -1, 'Z': -4},
        'I': {'*': -5, 'A': -1, 'C': -2, 'B': -4, 'E': -4, 'D': -4,
              'G': -4, 'F': 0, 'I': 5, 'H': -4, 'K': -3, 'M': 2, 'L': 2,
              'N': -3, 'Q': -3, 'P': -3, 'S': -3, 'R': -4, 'T': -1,
              'W': -3, 'V': 4, 'Y': -1, 'X': -1, 'Z': -3},
        'H': {'*': -5, 'A': -2, 'C': -3, 'B': 0, 'E': 0, 'D': -1, 'G': -2,
              'F': -1, 'I': -4, 'H': 10, 'K': 0, 'M': -1, 'L': -3, 'N': 1,
              'Q': 1, 'P': -2, 'S': -1, 'R': 0, 'T': -2, 'W': -3, 'V': -4,
              'Y': 2, 'X': -1, 'Z': 0},
        'K': {'*': -5, 'A': -1, 'C': -3, 'B': 0, 'E': 1, 'D': -1, 'G': -2,
              'F': -4, 'I': -3, 'H': 0, 'K': 6, 'M': -2, 'L': -3, 'N': 0,
              'Q': 2, 'P': -1, 'S': 0, 'R': 3, 'T': -1, 'W': -3, 'V': -3,
              'Y': -2, 'X': -1, 'Z': 1},
        'M': {'*': -5, 'A': -1, 'C': -2, 'B': -3, 'E': -2, 'D': -4,
              'G': -3, 'F': 0, 'I': 2, 'H': -1, 'K': -2, 'M': 7, 'L': 3,
              'N': -2, 'Q': 0, 'P': -3, 'S': -2, 'R': -2, 'T': -1, 'W': -1,
              'V': 1, 'Y': 0, 'X': -1, 'Z': -1},
        'L': {'*': -5, 'A': -2, 'C': -2, 'B': -4, 'E': -3, 'D': -4,
              'G': -4, 'F': 1, 'I': 2, 'H': -3, 'K': -3, 'M': 3, 'L': 5,
              'N': -4, 'Q': -2, 'P': -4, 'S': -3, 'R': -3, 'T': -1,
              'W': -2, 'V': 1, 'Y': -1, 'X': -1, 'Z': -3},
        'N': {'*': -5, 'A': -1, 'C': -2, 'B': 5, 'E': 0, 'D': 2, 'G': 0,
              'F': -4, 'I': -3, 'H': 1, 'K': 0, 'M': -2, 'L': -4, 'N': 7,
              'Q': 0, 'P': -2, 'S': 1, 'R': -1, 'T': 0, 'W': -4, 'V': -3,
              'Y': -2, 'X': -1, 'Z': 0},
        'Q': {'*': -5, 'A': -1, 'C': -3, 'B': 0, 'E': 2, 'D': 0, 'G': -2,
              'F': -4, 'I': -3, 'H': 1, 'K': 2, 'M': 0, 'L': -2, 'N': 0,
              'Q': 7, 'P': -1, 'S': 0, 'R': 1, 'T': -1, 'W': -1, 'V': -3,
              'Y': -1, 'X': -1, 'Z': 4},
        'P': {'*': -5, 'A': -1, 'C': -4, 'B': -2, 'E': -1, 'D': -1,
              'G': -2, 'F': -4, 'I': -3, 'H': -2, 'K': -1, 'M': -3,
              'L': -4, 'N': -2, 'Q': -1, 'P': 10, 'S': -1, 'R': -3,
              'T': -1, 'W': -4, 'V': -3, 'Y': -3, 'X': -1, 'Z': -1},
        'S': {'*': -5, 'A': 1, 'C': -1, 'B': 0, 'E': -1, 'D': 0, 'G': 0,
              'F': -3, 'I': -3, 'H': -1, 'K': 0, 'M': -2, 'L': -3, 'N': 1,
              'Q': 0, 'P': -1, 'S': 5, 'R': -1, 'T': 2, 'W': -4, 'V': -2,
              'Y': -2, 'X': -1, 'Z': 0},
        'R': {'*': -5, 'A': -2, 'C': -4, 'B': -1, 'E': 0, 'D': -2, 'G': -3,
              'F': -3, 'I': -4, 'H': 0, 'K': 3, 'M': -2, 'L': -3, 'N': -1,
              'Q': 1, 'P': -3, 'S': -1, 'R': 7, 'T': -1, 'W': -3, 'V': -3,
              'Y': -1, 'X': -1, 'Z': 0},
        'T': {'*': -5, 'A': 0, 'C': -1, 'B': 0, 'E': -1, 'D': -1, 'G': -2,
              'F': -2, 'I': -1, 'H': -2, 'K': -1, 'M': -1, 'L': -1, 'N': 0,
              'Q': -1, 'P': -1, 'S': 2, 'R': -1, 'T': 5, 'W': -3, 'V': 0,
              'Y': -2, 'X': -1, 'Z': -1},
        'W': {'*': -5, 'A': -3, 'C': -5, 'B': -5, 'E': -3, 'D': -5,
              'G': -3, 'F': 1, 'I': -3, 'H': -3, 'K': -3, 'M': -1, 'L': -2,
              'N': -4, 'Q': -1, 'P': -4, 'S': -4, 'R': -3, 'T': -3,
              'W': 15, 'V': -3, 'Y': 2, 'X': -1, 'Z': -2},
        'V': {'*': -5, 'A': 0, 'C': -1, 'B': -3, 'E': -3, 'D': -4, 'G': -4,
              'F': -1, 'I': 4, 'H': -4, 'K': -3, 'M': 1, 'L': 1, 'N': -3,
              'Q': -3, 'P': -3, 'S': -2, 'R': -3, 'T': 0, 'W': -3, 'V': 5,
              'Y': -1, 'X': -1, 'Z': -3},
        'Y': {'*': -5, 'A': -2, 'C': -3, 'B': -3, 'E': -2, 'D': -3,
              'G': -3, 'F': 4, 'I': -1, 'H': 2, 'K': -2, 'M': 0, 'L': -1,
              'N': -2, 'Q': -1, 'P': -3, 'S': -2, 'R': -1, 'T': -2, 'W': 2,
              'V': -1, 'Y': 8, 'X': -1, 'Z': -2},
        'X': {'*': -5, 'A': -1, 'C': -1, 'B': -1, 'E': -1, 'D': -1,
              'G': -1, 'F': -1, 'I': -1, 'H': -1, 'K': -1, 'M': -1,
              'L': -1, 'N': -1, 'Q': -1, 'P': -1, 'S': -1, 'R': -1,
              'T': -1, 'W': -1, 'V': -1, 'Y': -1, 'X': -1, 'Z': -1},
        'Z': {'*': -5, 'A': -1, 'C': -3, 'B': 1, 'E': 5, 'D': 1, 'G': -2,
              'F': -4, 'I': -3, 'H': 0, 'K': 1, 'M': -1, 'L': -3, 'N': 0,
              'Q': 4, 'P': -1, 'S': 0, 'R': 0, 'T': -1, 'W': -2, 'V': -3,
              'Y': -2, 'X': -1, 'Z': 5}}

        return blosum50




    def export(self,genes):

        references = list(set([x.seqid for x in genes]))
        Utils.natural_sort(references)

        self.output = "TEST.GFF"
        self.prefix = "bizarre"

        with open(self.output, 'w') as f:
            ID = 0
            for ref in references:
                seq_genes = [g for g in genes if g.seqid == ref]
             #   for tr in sorted([ t for t in export_tr if t.seqid == ref], key=lambda x: x.start):
                for gene in seq_genes:

                        atts = {'ID':['gene:{}'.format(gene.gene_id)],'source':[gene.source]}
                        #atts = {'ID':['{}_{:05}'.format(self.prefix,ID)],'gene_source':[gene.gene_id],'source':['{}'.format(gene.source)]}
                        f.write(gene.to_gff3(atts=atts))
            #            if gene.gene_id == tr.gene_id and gene.source == tr.source:
                        for tr in gene.lTranscripts:
                            if len(gene.lTranscripts) > 1:
                                print("multi: {}".format(gene.gene_id))
                            ID += 1
        
                            if not tr.best_tr_evidence[0]:
                                ev_tr = "None"
                            else:
                                #ev_tr = tr.best_tr_evidence[0].id
                                ev_tr = tr.best_tr_evidence[0]
                            if not tr.best_bx_evidence[0]:
                                ev_bx = "None"
                            else:
                                #ev_bx = tr.best_bx_evidence[0].id
                                ev_bx = tr.best_bx_evidence[0]
    
                            atts = {'ID':['mRNA:{}'.format(tr.id)], 'source':[gene.source],'Parent':['gene:{}'.format(gene.gene_id)], 'ev_tr': [ev_tr], 'aed_ev_tr':['{:.4f}'.format(tr.best_tr_evidence[1])], 'ev_tr_penalty': [tr.tr_penalty], 'ev_pr' : [ev_bx], 'aed_ev_pr' : ['{:.4f}'.format(tr.best_bx_evidence[1])]}
                            #atts = {'ID':['{}_{:05}.1'.format(self.prefix,ID)], 'transcript_source':[tr.id],'source':[gene.source],'Parent':['{}_{:05}'.format(self.prefix,ID)],'ev_tr': [ev_tr], 'aed_ev_tr':['{:.4f}'.format(tr.best_tr_evidence[1])], 'ev_tr_penalty': [tr.tr_penalty], 'ev_pr' : [ev_bx], 'aed_ev_pr' : ['{:.4f}'.format(tr.best_bx_evidence[1])]}
    
                            #if self.longread_gff_file:
                            if not tr.best_lg_evidence[0]:
                                ev_lg = "None"
                            else:
                                #ev_lg = tr.best_lg_evidence[0].id
                                ev_lg = tr.best_lg_evidence[0]
                            atts_lg = {'ev_lg': [ev_lg], 'aed_ev_lg':['{:.4f}'.format(tr.best_lg_evidence[1])],'ev_lg_penalty':[tr.lg_penalty]}
                            atts.update(atts_lg)
    
                            f.write(tr.to_gff3(atts=atts))

                        for tr in gene.lTranscripts:
                            printed_exons = [] 
                            for i,exon in enumerate(tr.lExons):
                                atts = {'ID':['exon:{}.{}'.format(gene.gene_id,i+1)], 'source':[gene.source],'Parent':['mRNA:{}'.format(tr.id)]}
                                #atts = {'ID':['exon:{}_{:05}.{}'.format(self.prefix,ID,i+1)],'Parent':['{}_{:05}.1'.format(self.prefix,ID)]}
                                if exon not in printed_exons:
                                    f.write(exon.to_gff3(atts=atts))
                                    printed_exons.append(exon)
                            for i,cds in enumerate(tr.lCDS):
                                atts = {'ID':['cds:{}'.format(tr.id)], 'source':[gene.source],'Parent':['mRNA:{}'.format(tr.id)]}
                                #atts = { 'ID':['cds:{}_{:05}.1'.format(self.prefix,ID)],'Parent':['{}_{:05}.1'.format(self.prefix,ID)]}
                                f.write(cds.to_gff3(atts=atts))
                            break
        f.close()


