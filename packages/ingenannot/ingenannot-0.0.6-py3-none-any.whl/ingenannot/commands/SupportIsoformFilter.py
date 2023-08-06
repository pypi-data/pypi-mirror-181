#!/usr/bin/env python3

import pysam
import skbio
import numpy as np
#from collections import Counter
#from skbio import Protein
from ingenannot.Commands.Command import Command
from ingenannot.Utils import Utils
from math import *

from ingenannot.Entities.CDS import CDS



class SupportIsoformFilter(Command):

    def __init__(self, args):

        self.gff_gene = args.Gff_genes
        self.gff_transcripts = args.Gff_transcripts
        self.gff_output = args.Output
        self.bam_fof = args.Bam_fof

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



    def run(self):



        ### TODO:
        ### status validate or not
        ### validaton with several bams
        ### test translation
        ### add iso

        threshold_AS = 0.01
        threshold_IR = 0.01
        bam_files =[]
        with open(self.bam_fof, 'r') as f:
            for line in f:
               bam_files.append(line.rstrip("\n"))
        bam_file = 0
#        print('bam_files', bam_files)
        #tr_to_genes = {}
        #genes_to_update = {}
        #tr_tp_to_remove = set()
        tr_validated = []
        tr_not_validated = []

        genes = Utils.extract_genes(self.gff_gene)
        references = set([g.seqid for g in genes])
        strands = [1,-1]
        tr_templates = Utils.extract_genes(self.gff_transcripts)

        with open(self.gff_output, 'w') as f:
    #        for ref in ["chr_1"]:
            for ref in references:
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
                                        #tr_to_genes[tr.id] = []
                                        states =  self.extract_states(tr, tr_tp)
                                        events_to_check = self.get_AS_IR_events_in_annotated_regions(states)
                                        if events_to_check:
                                            validate = False
                                            chr = tr.seqid
                                            strand = tr.strand
                                            for e in events_to_check:
                                                if e[0] == 'AS':
                                                    validate = False
                                                            #print(self.AS_event_validation(e,chr,strand))
                                                            #f.write(str(self.AS_event_validation(e,chr,strand)) + "\n")a
                                                    for bam_file in bam_files:
                                                        if validate == True:
                                                            break
                                                        if validate == False:
                                                            res = self.AS_event_validation(e,chr,strand,bam_file)
                                                            if res['ratio'] > threshold_AS:
                                                                validate = True
                                                if e[0] == 'IR':
                                                    validate = False
                                                            #print(self.IR_event_validation(e,chr,strand))
                                                         #f.write(str(self.IR_event_validation(e,chr,strand)) + "\n")
                                                    for bam_file in bam_files:
                                                        if validate == True:
                                                            break
                                                        if validate == False:
                                                            res = self.IR_event_validation(e,chr,strand,bam_file)
                                                            if res['ratio'] > threshold_IR:
                                                                validate = True
                                            if validate:
                                                print("isoform to add")
                                                tr_validated.append(tr_tp)
                                            else:
                                                print("not validated by the bam: {}".format(tr_tp))
                                                tr_not_validated.append(tr_tp)
                                        else:
                                                tr_validated.append(tr_tp)

        f.close()

        self.export(tr_templates, tr_validated, self.gff_output)
        self.export(tr_templates, tr_not_validated, 'no-export.{}'.format(self.gff_output))
        return 0

    def export(self, genes, tr_validated, fh):

        multi_exon = True
        source = "support_isoform_filter"
        if multi_exon:
            with open(fh, 'w') as f:
                for g in genes:
                    g.source = source
                    str_g = g.to_gff3()
                    validated_tr = False
                    for tr in g.lTranscripts:
                        if tr in tr_validated:
                            tr.source = source
                            str_g += tr.to_gff3()
                            for i,ex in enumerate(tr.lExons):
                                ex.source = source
                                atts = {"ID":['{}-exon.{}'.format(tr.id,i+1)],"Parent":['{}'.format(tr.id)]}
                                str_g += ex.to_gff3(atts=atts)
                            validated_tr = True

                    if validated_tr:
                        f.write(str_g)
        else:
            with open(fh, 'w') as f:
                for g in genes:
                    g.source = source
                    str_g = g.to_gff3()
                    validated_tr = False
                    l_exons = []
                    for tr in g.lTranscripts:
                        if tr in tr_validated:
                            tr.source = source
                            str_g += tr.to_gff3()
                            for ex in tr.lExons:
                                if ex not in l_exons:
                                    l_exons.append(ex)
                            validated_tr = True
                    for i,ex in enumerate(sorted(l_exons, key=lambda x: x.start)):
                        ex.source = source
                   #             atts = {"ID":['{}-exon.{}'.format(tr.id,i+1)],"Parent":['{}'.format(tr.id)]}
                        str_g += ex.to_gff3()

                    if validated_tr:
                        f.write(str_g)




