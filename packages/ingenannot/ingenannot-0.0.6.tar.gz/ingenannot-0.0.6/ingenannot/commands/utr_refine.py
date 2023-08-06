#/usr/bin/env python3

import logging
import copy

from ingenannot.commands.command import Command
from ingenannot.utils import Utils
from ingenannot.entities.exon import Exon

class UTRRefine(Command):

    def __init__(self, args):

        self.gff_gene = args.Gff_genes
        self.gff_transcripts = args.Gff_transcripts
        self.gff_output = args.Output
        self.utr_mode = args.utr_mode
        self.erase = args.erase
        self.onlynew = args.onlynew

    def get_best_evidence(self, tr, tr_tps):

        t = None
        if self.utr_mode == "shortest":
            len_utrs = 1000000
            for tr_tp in tr_tps:
                l = tr_tp.getExonTotalLength() - tr.getCDSTotalLength()
                if l < len_utrs:
                    len_utrs = l
                    t = tr_tp
                    print(t, len_utrs)
        elif self.utr_mode == "rank": #rank tag in gff3
            rank = 10000
            for tr_tp in tr_tps:
                if 'rank' not in tr_tp.dAttributes:
                    raise Exception("Cannot clasified with rank, missing tag rank in gff3")
                if int(tr_tp.dAttributes['rank'][0]) < rank:
                    rank = int(tr_tp.dAttributes['rank'][0])
                    t = tr_tp
        else: # (default = longest)
            len_utrs = 0
            for tr_tp in tr_tps:
                l = tr_tp.getExonTotalLength() - tr.getCDSTotalLength()
                if l > len_utrs:
                    len_utrs = l
                    t = tr_tp
        return t


    def update_transcript_coords(self, tr, tr_tp):

        tr.lExons = copy.deepcopy(tr_tp.lExons)
        for e in tr.lExons:
            e.lTranscript_ids = []
        tr.start = min([x.start for x in tr.lExons])
        tr.end = max([x.end for x in tr.lExons])

#        if self.erase: # replace exons
#            print(tr.lExons)
#            print(tr_tp.lExons)
#            tr.lExons = copy.deepcopy(tr_tp.lExons)
#            for e in tr.lExons:
#                e.lTranscript_ids = []
#            tr.start = min([x.start for x in tr.lExons])
#            tr.end = max([x.end for x in tr.lExons])
#            print(tr.lExons)
#            print(tr_tp.lExons)
#
#        else: # update exons
#            print(tr.lExons)
#            print(tr_tp.lExons)

    def update_gene_coords(self, g):

        g.start = min([x.start for x in g.lTranscripts])
        g.end = max([x.end for x in g.lTranscripts])

    def update_cds_transcript(self, tr):

        for cds in tr.lCDS:
            cds.cds_id = "cds_{}".format(tr.id)


    def update_exon_transcripts(self, g):

        lExons = {}
        for tr in g.lTranscripts:
#            print("TRRRRRR", g.gene_id, tr.id)
            tr_exons = []
            for e in tr.lExons:
                if (e.start, e.end) in lExons:
                    tr_exons.append(lExons[(e.start, e.end)])
                    lExons[(e.start, e.end)].add_transcript(tr.id)
                else:
                    e.add_transcript(tr.id)
                    tr_exons.append(e)
                    lExons[(e.start, e.end)] = e
            tr.lExons = tr_exons

        for i,e in enumerate(sorted(lExons.values(), key=lambda x: x.start)):
#            print("ICI")
#            print(e.exon_id)
            e.exon_id = "{}_exon{:03}".format(g.gene_id, i+1)
#            print(e.exon_id)

    def export(self, genes, updated_transcripts):
        """export to Gff3"""

        logging.info("exporting genes in {}".format(self.gff_output))

        with open(self.gff_output, 'w') as f:
                for gene in genes :
                    atts = {'ID':[gene.gene_id],'source':[gene.source]}
                    f.write(gene.to_gff3(atts))

                    for tr in gene.lTranscripts:
                        #atts = {'ID':[tr.id], 'source':[gene.source],'Parent':[gene.gene_id]}
#                        print(tr.id)
                        atts = tr.dAttributes
                        if tr.id in updated_transcripts:
                            atts['ID'] = [tr.id]
                            atts['utr_refine_evidence'] = [updated_transcripts[tr.id]]
                            #atts = {'ID':[tr.id],'Parent':[gene.gene_id],'utr_refine_evidence':[updated_transcripts[tr.id]]}
                        f.write(tr.to_gff3(atts=atts))
 #                       print(tr.to_gff3(atts=atts))
                    #dedup exons
                    lExons = []
                    for tr in gene.lTranscripts:
                        for i,exon in enumerate(tr.lExons):
                            atts = {'ID':[exon.exon_id], 'source':[gene.source],'Parent':[",".join(exon.lTranscript_ids)]}
                            #tr.add_cds(CDS('cds:{}_{}-{}'.format(exon.seqid,exon.start,exon.end),exon.seqid,exon.start,exon.end,exon.strand,'.',tr.id))
                            if exon.exon_id not in lExons:
                                f.write(exon.to_gff3(atts=atts))
                                lExons.append(exon.exon_id)
                    for tr in gene.lTranscripts:
                        for i,cds in enumerate(tr.lCDS):
                            atts = {'ID':[cds.cds_id], 'source':[gene.source],'Parent':[tr.id]}
                            f.write(cds.to_gff3(atts=atts))

                    for tr in gene.lTranscripts:
                        strand = '+'
                        if tr.strand == -1:
                           strand = '-'
                        five_prime_utrs = tr.infer_five_prime_utrs()
                        for i,utr in enumerate(five_prime_utrs):
                            atts = {'ID':['five_prime_UTR_{}_{:03}'.format(tr.id,i+1)], 'source':[gene.source],'Parent':[tr.id]}
                            str_atts = ''
                            for att in atts:
                                str_atts += '{}={};'.format(att,",".join(atts[att]))
                            f.write("{}\t{}\tfive_prime_UTR\t{}\t{}\t.\t{}\t.\t{}\n".format(tr.seqid,'ingenannot',utr[0],utr[1],strand,str_atts))
                        three_prime_utrs = tr.infer_three_prime_utrs()
                        for i,utr in enumerate(three_prime_utrs):
                            atts = {'ID':['three_prime_UTR_{}_{:03}'.format(tr.id,i+1)], 'source':[gene.source],'Parent':[tr.id]}
                            str_atts = ''
                            for att in atts:
                                str_atts += '{}={};'.format(att,",".join(atts[att]))
                            f.write("{}\t{}\tthree_prime_UTR\t{}\t{}\t.\t{}\t.\t{}\n".format(tr.seqid,'ingenannot',utr[0],utr[1],strand,str_atts))


        f.close()

        logging.info("{} genes exported".format(len(genes)))



    def run(self):
        """"launch command"""

        tr_to_genes = {}
        selected_tr_tp = set()
        tr_tp_to_remove = set()
        genes = Utils.extract_genes(self.gff_gene)
        tr_templates = Utils.extract_genes(self.gff_transcripts)


        if self.erase:
            for g in genes:
#                if len(g.lTranscripts) > 1:
#                    print(g.gene_id) 
#                    raise ("Excpetion multi transcript not yt implemented")
                for t in g.lTranscripts:
                    exons = []
                    for idx,cds in enumerate(t.lCDS):
                        exons.append(Exon("exon:{}.{}".format(g.gene_id,idx),g.seqid,cds.start,cds.end,cds.strand,[]))
                    t.lExons = exons

                    t.start = min([x.start for x in t.lExons])
                    t.end = max([x.end for x in t.lExons])
                self.update_gene_coords(g)
                self.update_exon_transcripts(g)


        for g in genes:
            for g_tp in [gene for gene in tr_templates if (gene.seqid == g.seqid) & (gene.strand == g.strand)]:
                if g.is_feature_spanning(g_tp):
                    for tr in g.lTranscripts:
                        tr_to_genes[tr.id] = []
                        for tr_tp in g_tp.lTranscripts:
                            # check no specific CDS bases
                            if tr.get_nb_specific_bases_vs_another_transcript(tr_tp,True,False) == 0:
                                # check bases in introns
                                if tr_tp.get_nb_specific_bases_vs_another_transcript_specific_positions(tr,tr.get_min_cds_start(), tr.get_max_cds_end(), False, False) == 0:
                                    # check new specific bases (not same coord = same UTRs)
                                    if tr_tp.get_nb_specific_bases_vs_another_transcript(tr,False,False) > 0:
        #                                print("OK: ", tr.id, tr_tp.id)
                                        tr_to_genes[tr.id].append(tr_tp)
                                        if tr_tp.id in selected_tr_tp:
                                            tr_tp_to_remove.add(tr_tp.id)
                                        selected_tr_tp.add(tr_tp.id)
         #                               print(tr_tp.id)
                                    else:
                                        logging.debug("NOK 3: no changes same UTRs {} - {}".format(tr.id, tr_tp.id))
                                else:
                                    logging.debug("NOK 2: not same CDS coordinates, false intron in annotation {} - {}".format(tr.id, tr_tp.id))
                            else:
                                logging.debug("NOK 1: not same CDS coordinates, missing intron in annotation {} - {}".format(tr.id, tr_tp.id))

          #2: control overlap on adjacent genes
          # if a transcript span several gene possible bug
          # or readthrought = to remove
        logging.info("removing {} transcripts before UTR definition, overlapping multiple CDS".format(len(tr_tp_to_remove)))
        for tr_id in tr_to_genes:
            l = []
            for tr_tp in tr_to_genes[tr_id]:
                if tr_tp.id not in tr_tp_to_remove:
                    l.append(tr_tp)
            tr_to_genes[tr_id] = l
#        print("### TO REMOVE ###")
#        print(tr_tp_to_remove)

        # change utr
        updated_transcripts = {}
        for g in genes:
            replaced_transcripts = []
            created_transcripts = []
            utr_change_flag = False
            for tr in g.lTranscripts:
                if self.onlynew:
                    if tr.has_UTRs():
                        continue
                if tr.id in tr_to_genes :
                    if len(tr_to_genes[tr.id]) > 0:
                    #write function to add utr with mode
                        if self.utr_mode == 'all':
                            #self.update_transcript_coords(tr, start, end)
                            if len(tr_to_genes[tr.id]) == 1:
                                t = tr_to_genes[tr.id][0]
                                self.update_transcript_coords(tr, t)
                                logging.info("{} UTRs changed with {}".format(tr.id, t.id))
                                updated_transcripts[tr.id] = t.id
                            else:
                                for i,tr_tp in enumerate(tr_to_genes[tr.id]):
                                    tr_iso = copy.deepcopy(tr) # exon deepcopied too will be removed in update_exons (to refactor)
                                    # need implementation tr copy method
                                    tr_iso.id = "{}_utr_isoform{:03}".format(tr.id,i+1)
                               #     print("REEE",tr_tp)
                                    self.update_transcript_coords(tr_iso, tr_tp)
                                    logging.info("{} UTRs changed with {}".format(tr_iso.id, tr_tp.id))
                                    updated_transcripts[tr_iso.id] = tr_tp.id
                                    created_transcripts.append(tr_iso)
                                replaced_transcripts.append(tr)
                        else:
                            t = self.get_best_evidence(tr, tr_to_genes[tr.id])
                            self.update_transcript_coords(tr, t)
                            logging.info("{} UTRs changed with {}".format(tr.id, t.id))
                            updated_transcripts[tr.id] = t.id
                        utr_change_flag = True
            if utr_change_flag:
                if self.utr_mode == 'all':
                    for xtr in replaced_transcripts:
                        g.remove_transcript(xtr.id)
                    for xtr in created_transcripts:
                        g.add_transcript(xtr)
                        self.update_cds_transcript(xtr)
                self.update_gene_coords(g)
                self.update_exon_transcripts(g)
        #        self.add_utrs(g)
        #        print(g)
        #        print(g.lTranscripts[0].lExons)

        self.export(genes, updated_transcripts)

        return 0
