#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
import ROOT as R
r = R
import sys
import os
import glob
import math
# import math as m
# import datetime
import numpy as np
from array import array
# import re
from xml.dom import minidom

# import myfit
# import luminosity

# R.gSystem.Load('libRooFit')


def get_gr_from_file_comma(filename, ix=[0, 1, 2, 3, 4, 5], k=1.):
    fin = open(filename)
    x, xel, xeh = [], [], []
    y, yel, yeh = [], [], []
    for line in fin:
        if len(line) < 5:
            continue
        if line[0] == '#':
            if 'SIG [PB]' in line:
                k *= 1.e-3
            continue
        lin = line.split(',')
        for i, a in enumerate([x, xel, xeh, y, yeh, yel]):
            if not ix[i] == -1:
                if i == 3 and '<' in lin[ ix[i] ]:
                    print lin[ ix[i] ]
                    a.append(float( lin[ ix[i] ][2:-1] ))
                    yeh.append( 0. )
                    yel.append( a[-1] )
                    break
                if i == 3 and '-' in lin[ ix[i] ]:
                    print lin[ ix[i] ]
                    a.append( 0. )
                    yeh.append( 0. )
                    yel.append( 0. )
                    break
                else:
                    a.append(float( lin[ ix[i] ] ))
            else:
                a.append(0.)
            # a.append(float(lin[i]))
        xel[-1] = x[-1] - xel[-1]
        xeh[-1] = xeh[-1] - x[-1]
        yel[-1] = abs(yel[-1])
    gr = R.TGraphAsymmErrors(len(x), np.array(x), k*np.array(y), np.array(xel), np.array(xeh),
            k*np.array(yel), k*np.array(yeh))
    gr.SetTitle('')
    fin.close()
    return gr


def get_gr(fname, ix=[0, 1, 2, 3, 4, 5],
        ms=20, mc=r.kBlack, msi=0.75,
        lw=1, lc=-666, ls=1,
        k=1.):
    gr = get_gr_from_file_comma(fname, ix, k)
    gr.SetName(fname.split('.')[-2])
    gr.SetMarkerStyle(ms)
    gr.SetMarkerSize(msi)
    gr.SetMarkerColor(mc)
    if lc == -666:
        gr.SetLineColor(mc)
    else:
        gr.SetLineColor(lc)
    gr.SetLineWidth(lw)
    gr.SetLineStyle(ls)
    return gr


def main2():
    cx, cy = 600, 600
    xmin, xmax = 550., 1400.
    ymin, ymax = 0., 60.
    logx, logy = 0, 0
    for i, a in enumerate(sys.argv):
        if a == 'logy':
            logy = 1
        elif a == 'logx':
            logx = 1
        elif a == 'xmin':
            xmin = float( sys.argv[i+1] )
        elif a == 'xmax':
            xmax = float( sys.argv[i+1] )
        elif a == 'ymin':
            ymin = float( sys.argv[i+1] )
        elif a == 'ymax':
            ymax = float( sys.argv[i+1] )
        elif a == 'cx':
            cx = int( sys.argv[i+1] )
        elif a == 'cy':
            cy = int( sys.argv[i+1] )
        elif a == 'cxy':
            cx = int( sys.argv[i+1] )
            cy = int( sys.argv[i+2] )
    if logy == 1:
        if ymin <= 0.:
            ymin = 1.e-3
        if ymax == 60.:
            ymax = 100.
    c1 = R.TCanvas('c1', 'c1', cx, cy)
    frame = c1.DrawFrame(xmin, ymin, xmax, ymax)
    c1.SetLogx(logx)
    c1.SetLogy(logy)
    c1.SetGrid()
    c1.SetTopMargin(.025)
    c1.SetRightMargin(.025)
    gcmd2005 = get_gr('cs_etagamma_cmd2_2005.dat', [0, 0, 0, 1, 4, 5], mc=r.kBlue, k=1/.3941)
    gcmd2005.Draw('p')
    g = gcmd2005
    gsnd2014 = get_gr('cs_etagamma_snd_2014.dat', mc=r.kRed)
    gsnd2014.Draw('p')
    gsnd2006_3pi0 = get_gr('cs_etagamma_snd_2006_3pi0.dat', mc=r.kOrange+7)
    gsnd2006_3pi0.Draw('p')
    gsnd2006_pippimpi0 = get_gr('cs_etagamma_snd_2006_pippimpi0.dat', mc=r.kOrange+4)
    gsnd2006_pippimpi0.Draw('p')
    gcmd2001 = get_gr('cs_etagamma_cmd2_2001.dat', [0, 0, 0, 1, 2, 3], mc=r.kCyan)
    gcmd2001.Draw('p')
    gcmd1999 = get_gr('cs_etagamma_cmd2_1999.dat', mc=r.kCyan+2)
    gcmd1999.Draw('p')
    gsnd2000 = get_gr('cs_etagamma_snd_2000.dat', mc=r.kMagenta)
    gsnd2000.Draw('p')
    gsnd1995 = get_gr('cs_etagamma_snd_1995.dat', mc=r.kRed-6)
    gsnd1995.Draw('p')
    ################
    xmin, xmax = 600., 1600.
    ymin, ymax = 0., g.GetMaximum()
    for i, a in enumerate(sys.argv):
        if a == 'logy':
            c1.SetLogy()
        elif a == 'xmin':
            xmin = float( sys.argv[i+1] )
        elif a == 'xmax':
            xmax = float( sys.argv[i+1] )
        elif a == 'ymin':
            ymin = float( sys.argv[i+1] )
        elif a == 'ymax':
            ymax = float( sys.argv[i+1] )
    # g.GetXaxis().SetRangeUser(xmin, xmax)
    # g.GetYaxis().SetRangeUser(ymin, ymax)
    ################
    frame.GetXaxis().SetTitle('#sqrt{s}, MeV')
    frame.GetYaxis().SetTitle('Cross section #sigma_{0}, nb')
    frame.GetXaxis().SetTitleOffset(1.05)
    frame.GetYaxis().SetTitleOffset(1.30)
    ################
    lat = R.TLatex()
    lat.SetTextSize(0.04)
    lat.SetTextFont(12)
    x0, y0, dy = .65, .9, -.05
    lat.SetTextColor( gsnd2014.GetMarkerColor() )
    lat.DrawLatexNDC(x0, y0, 'SND 2014 (3#pi^{0})')
    lat.SetTextColor( gsnd2006_3pi0.GetMarkerColor() )
    lat.DrawLatexNDC(x0, y0+dy*1, 'SND 2006 (3#pi^{0})')
    lat.SetTextColor( gsnd2006_pippimpi0.GetMarkerColor() )
    lat.DrawLatexNDC(x0, y0+dy*2, 'SND 2006 (#pi^{+}#pi^{#minus}#pi^{0})')
    lat.SetTextColor( gcmd2005.GetMarkerColor() )
    lat.DrawLatexNDC(x0, y0+dy*3, 'CMD-2 2005 (2#gamma)')
    lat.SetTextColor( gcmd2001.GetMarkerColor() )
    lat.DrawLatexNDC(x0, y0+dy*4, 'CMD-2 2001 (3#pi^{0})')
    lat.SetTextColor( gsnd2000.GetMarkerColor() )
    lat.DrawLatexNDC(x0, y0+dy*5, 'SND 2000 (2#gamma)')
    lat.SetTextColor( gcmd1999.GetMarkerColor() )
    lat.DrawLatexNDC(x0, y0+dy*6, 'CMD-2 1999 (#pi^{+}#pi^{#minus}#pi^{0})')
    lat.SetTextColor( gsnd1995.GetMarkerColor() )
    lat.DrawLatexNDC(x0, y0+dy*7, 'SND 1995')
    ################
    c1.Update()
    if not '-b' in sys.argv:
        raw_input()
    if 'save' in sys.argv:
        c1.SaveAs('~/my_cross_section.png')
        drd[0].SaveAs('~/my_cross_section_diff.png')


if __name__ == '__main__':
    if 'robot' in sys.argv:
        os.system('%s xmin 550 xmax 1400 logy' % sys.argv[0])
        os.system('%s xmin 777 xmax 787 ymax 5' % sys.argv[0])
        os.system('%s xmin 1010 xmax 1030 ymax 75' % sys.argv[0])
        os.system('%s xmin 1020 xmax 1400 ymax .25' % sys.argv[0])
    else:
        main2()
