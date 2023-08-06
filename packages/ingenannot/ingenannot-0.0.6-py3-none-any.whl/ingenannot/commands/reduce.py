#/usr/bin/env python3

import logging
import numpy as np
import seaborn as sns
import matplotlib
import pandas as pd
import re


#matplotlib.use('Agg')
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg
#from matplotlib import gridspec


from ingenannot.commands.command import Command
from  ingenannot.utils import Utils

class Reduce(Command):

    def __init__(self, args):

        self.gff_genes = args.Gff_genes
        self.aedtr = args.aedtr
        self.aedpr = args.aedpr
        self.no_tr_penalty = args.no_tr_penalty
        self.no_lg_penalty = args.no_lg_penalty
        self.aed_operator = args.aed_operator
        self.use_ev_lg = args.use_ev_lg
        self.prefix = args.prefix

    def get_aed(self, genes):
        l_aed_tr = []
        l_aed_tr_no_penalty = []
        l_aed_pr = []
        l_aed_pr_no_penalty = []
        l_aed_lg = []
        l_tr_penalty = []
        l_lg_penalty = []
    #l_filtered_features = []
        l_filtered_features ={}
        l_removed_features ={}
        ID = 0
        for g in genes:
            for tr in g.lTranscripts:
                if "aed_ev_tr" in tr.dAttributes:
                    l_aed_tr.append(float(tr.dAttributes["aed_ev_tr"][0]))
                else:
                    print("problem aed_ev_tr")
                if "aed_ev_pr" in tr.dAttributes:
                    l_aed_pr.append(float(tr.dAttributes["aed_ev_pr"][0]))
                else:
                    print("problem aed_ev_pr")
                if "aed_ev_lg" in tr.dAttributes:
                    l_aed_lg.append(float(tr.dAttributes["aed_ev_lg"][0]))
                else:
                    print("problem aed_ev_lg")
                if "ev_tr_penalty" in tr.dAttributes:
                    l_tr_penalty.append(tr.dAttributes["ev_tr_penalty"][0])
                else:
                    print("problem ev_tr_penalty")
                if "ev_lg_penalty" in tr.dAttributes:
                    l_lg_penalty.append(tr.dAttributes["ev_lg_penalty"][0])
                else:
                    print("problem ev_lg_penalty")

                if self.use_ev_lg:
                    l_aed_tr[-1] = min(float(tr.dAttributes["aed_ev_tr"][0]),float(tr.dAttributes["aed_ev_lg"][0]))



                to_remove = False

                if self._no_penalty_filter(tr):
                    if self.aed_operator == "AND":
                        if l_aed_tr[-1] <= self.aedtr and \
                           l_aed_pr[-1] <= self.aedpr :
                                to_remove = False
                        else:
                            to_remove = True
                    else:
                        if l_aed_tr[-1] <= self.aedtr or \
                           l_aed_pr[-1] <= self.aedpr :
                                to_remove = False
                        else:
                            to_remove = True
                    if self.use_ev_lg:
                        l_aed_tr_no_penalty.append(min(float(tr.dAttributes["aed_ev_tr"][0]),float(tr.dAttributes["aed_ev_lg"][0])))
                    else:
                        l_aed_tr_no_penalty.append(float(tr.dAttributes["aed_ev_tr"][0]))
                    l_aed_pr_no_penalty.append(float(tr.dAttributes["aed_ev_pr"][0]))
                else:
                    to_remove = True


                if to_remove:
                    l_removed_features[tr.id] = ( float(tr.dAttributes["aed_ev_tr"][0]), float(tr.dAttributes["aed_ev_pr"][0]), float(tr.dAttributes["aed_ev_lg"][0]))
                else:
                    l_filtered_features[tr.id] = ( float(tr.dAttributes["aed_ev_tr"][0]), float(tr.dAttributes["aed_ev_pr"][0]), float(tr.dAttributes["aed_ev_lg"][0]))




        print(len(l_filtered_features))

        return l_aed_tr, l_aed_tr_no_penalty, l_aed_pr, l_aed_pr_no_penalty,l_filtered_features, l_removed_features


    def _no_penalty_filter(self, tr):
        """
            test penalty
        """

        if self.no_tr_penalty and tr.dAttributes["ev_tr_penalty"][0] == 'yes':
            return False
        elif self.no_lg_penalty and tr.dAttributes["ev_lg_penalty"][0] == 'yes':
            return False
        else:
            return True


    def plotDensity(self, laed, out="", legend="", title="", xax="", yax="",hist=False):
    
        fig = plt.Figure(figsize=(20,20))
        ax = fig.add_subplot(111)
        axis_font = {'size':'28'}
        fig.suptitle(title, fontsize=32)
        for i,l in enumerate(laed):
            sn = sns.distplot(l, hist=hist, kde=True,
               #      bins=int(180/5), color = 'darkblue',
                   #  hist_kws={'edgecolor':'black'},
                     kde_kws={'linewidth': 2},
                     label=legend[i], ax=ax)
            data_x, data_y = sn.lines[0].get_data()
            maxy = 0
            maxx = 0
            for j,h in enumerate(data_y):
                if h > maxy and j < len(data_y)-25: #bidouille for 2 small runs
                    maxy = h
                    maxx = data_x[j]
        #    print("limit maxx {}: {}".format(legend[i], maxx))
        ax.set_xlabel(xax, **axis_font)
        ax.set_ylabel(yax, **axis_font)
        canvas = FigureCanvasAgg(fig)
        canvas.print_figure(out, dpi=80)

    def scatter_hist(self, laed, out="", legend="", title=""):
        """scatter plot of AEDs with histograms"""

        plt.style.use('bmh')
        #plt.style.use('seaborn')
        #plt.style.use('ggplot')

        fig = plt.Figure(figsize=(20,20))
        # add gridspec
        gs = fig.add_gridspec(2,2,width_ratios=(7, 2), height_ratios=(2, 7),
                                      left=0.1, right=0.9, bottom=0.1, top=0.9,
                                                            wspace=0.05, hspace=0.05)
        ax = fig.add_subplot(gs[1, 0])
        ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
        ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)
        ax_legend = fig.add_subplot(gs[0, 1])

        ax.scatter(laed[0],laed[1], color="#20C2EF")
        # By using ``transform=vax.get_xaxis_transform()`` the y coordinates are scaled
        # such that 0 maps to the bottom of the axes and 1 to the top.
        ax.vlines(self.aedtr, 0, 1, transform=ax.get_xaxis_transform(), colors='r', linestyle="dashed")
        ax.text(self.aedtr,0.9,self.aedtr,size=20,ha="center", va="center", color='r',bbox=dict(boxstyle="round",fc='#EEEEEE'))
        ax.hlines(self.aedpr, 0, 1, transform=ax.get_yaxis_transform(), colors='r', linestyle="dashed")
        ax.text(0.9,self.aedpr,self.aedpr,size=20,ha="center", va="center", color='r', bbox=dict(boxstyle="round",fc='#EEEEEE'))

        lb,rb,lt,rt = 0,0,0,0
        lb_no_penalty,rb_no_penalty,lt_no_penalty,rt_no_penalty = 0,0,0,0

        for i,val in enumerate(laed[0]):
            if laed[0][i] <= self.aedtr and laed[1][i] <= self.aedpr:
                lb += 1
            if laed[0][i] > self.aedtr and laed[1][i] <= self.aedpr:
                rb += 1
            if laed[0][i] <= self.aedtr and laed[1][i] > self.aedpr:
                lt += 1
            if laed[0][i] > self.aedtr and laed[1][i] > self.aedpr:
                rt += 1
        ax.text(self.aedtr/2,self.aedpr/2,lb,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))
        ax.text(1-((1-self.aedtr)/2),self.aedpr/2,rb,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))
        ax.text(self.aedtr/2,1-((1-self.aedpr)/2),lt,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))
        ax.text(1-((1-self.aedtr)/2),1-((1-self.aedpr)/2),rt,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))

        if self.no_lg_penalty or self.no_tr_penalty:
            for i,val in enumerate(laed[2]):
                if laed[2][i] <= self.aedtr and laed[3][i] <= self.aedpr:
                    lb_no_penalty += 1
                if laed[2][i] > self.aedtr and laed[3][i] <= self.aedpr:
                    rb_no_penalty += 1
                if laed[2][i] <= self.aedtr and laed[3][i] > self.aedpr:
                    lt_no_penalty += 1
                if laed[2][i] > self.aedtr and laed[3][i] > self.aedpr:
                    rt_no_penalty += 1

            ax.text(self.aedtr/2,self.aedpr/2-0.05,lb_no_penalty,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(.5, 1., 1.)))
            ax.text(1-((1-self.aedtr)/2),self.aedpr/2-0.05,rb_no_penalty,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(.5, 1., 1.)))
            ax.text(self.aedtr/2,1-((1-self.aedpr)/2)-0.05,lt_no_penalty,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(.5, 1., 1.)))
            ax.text(1-((1-self.aedtr)/2),1-((1-self.aedpr)/2)-0.05,rt_no_penalty,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0.0,0,0), fc=(.5, 1., 1.)))

        ax.set_xlabel("AED with transcript evidence", fontsize=20)
        ax.set_ylabel("AED with protein evidence", fontsize=20)
        ax.tick_params(labelsize=15)

        #ax.margins(0.02)
        #ax.set_xlim((0,1))
        #ax.set_ylim((0,1))

        bins = np.arange(0.0,1.01,0.01)
        ax_histx.hist(laed[0], bins=bins, color = '#36953a', edgeColor = 'black', label="AED transcripts")
        ax_histx.vlines(self.aedtr, 0, 1, transform=ax_histx.get_xaxis_transform(), colors='r', linestyle="dashed")
        ax_histx.tick_params(labelsize=12)
        ax_histx.set_ylabel("Nb. Transcripts", fontsize=20)
        #ax_histx.legend(fontsize=20)
        ax_histy.hist(laed[1], bins=bins, color = '#fc4b67', edgeColor = 'black', orientation='horizontal', label="AED proteins")
        ax_histy.hlines(self.aedpr, 0, 1, transform=ax_histy.get_yaxis_transform(), colors='r', linestyle="dashed")
        ax_histy.tick_params(labelsize=12)
        ax_histy.set_xlabel("Nb. Transcripts", fontsize=20)
        #ax_histy.legend(fontsize=20)

        h,l=ax_histx.get_legend_handles_labels() # get labels and handles from histx  
        hy,ly=ax_histy.get_legend_handles_labels() # get labels and handles from histy
        h.extend(hy)
        l.extend(ly)
        ax_legend.legend(h,l, fontsize=20)
        # Hide grid lines
        ax_legend.grid(False)
        # Hide axes ticks
        #ax_legend.set_xticks([])
        #ax_legend.set_yticks([])
        # change background color
        ax_legend.set_facecolor('w')
        ax_legend.axis('off')

        canvas = FigureCanvasAgg(fig)
        canvas.print_figure(out, dpi=80)



    def export(self, output, references, genes, filtered):
    
        with open(output, 'w') as f:
            self.natural_sort(references)
            ID=0
            for ref in references:
                for gene in sorted([ g for g in genes if g.seqid == ref],key=lambda x: x.start):
                    #for tr in filtered:
                        #if gene.lTranscripts[0].id == tr[0]:
                    if gene.lTranscripts[0].id in filtered:
                        ID += 1
                        atts = {'ID':['{}_{:05}'.format(self.prefix,ID)],'source':['{}'.format(gene.gene_id)]}
                        f.write(gene.to_gff3(atts=atts))
                        tr = gene.lTranscripts[0]
                        atts = {'ID':['{}_{:05}.1'.format(self.prefix,ID)],'Parent':['{}_{:05}'.format(self.prefix,ID)], 'aed_ev_tr':['{:.4f}'.format(filtered[tr.id][0])], 'aed_ev_pr' : ['{:.4f}'.format(filtered[tr.id][1])], 'aed_ev_lg' : ['{:.4f}'.format(filtered[tr.id][2])],'source':['{}'.format(tr.id)]}
                        f.write(tr.to_gff3(atts=atts))
                        for i,exon in enumerate(tr.lExons):
                            atts = {'ID':['exon:{}_{:05}.{}'.format(self.prefix,ID,i+1)],'Parent':['{}_{:05}.1'.format(self.prefix,ID)],'source':['{}'.format(exon.exon_id)]}
                            f.write(exon.to_gff3(atts=atts))
                        for i,cds in enumerate(tr.lCDS):
                            atts = { 'ID':['cds:{}_{:05}'.format(self.prefix,ID)],'Parent':['{}_{:05}.1'.format(self.prefix,ID)],'source':['{}'.format(cds.cds_id)]}
                            f.write(cds.to_gff3(atts=atts))
                        continue
    
        f.close()
    
    def atoi(self,text):
        return int(text) if text.isdigit() else text
    
    def natural_keys(self,text):
        '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        '''
        return [ self.atoi(c) for c in re.split('(\d+)', text) ]
    
    def natural_sort(self,ls):
    
        ls.sort(key=self.natural_keys)
    
    

    def run(self):
        """"launch command"""

        genes = Utils.extract_genes(self.gff_genes, coding_only=False)

        l_aed_tr, l_aed_tr_no_penalty, l_aed_pr, l_aed_pr_no_penalty, l_filtered_features, l_removed_features = self.get_aed(genes)
        self.plotDensity([l_aed_tr, l_aed_pr], "density_aed.png",legend=['aed_tr','aed_pr'], title="all runs - density of aed", xax="x", hist=True)
        self.scatter_hist([l_aed_tr, l_aed_pr, l_aed_tr_no_penalty, l_aed_pr_no_penalty], "scatter_hist_aed.png",legend=['aed_tr','aed_pr'], title="all runs - density of aed")
 
        references = list(set([x.seqid for x in genes]))


        self.export("filtered_aed.gff", references, genes, l_filtered_features)
        self.export("removed_aed.gff", references, genes, l_removed_features)
