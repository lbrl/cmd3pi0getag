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


def get_gr_from_file(filename):
    fin = open(filename)
    x, xel, xeh = [], [], []
    y, yel, yeh = [], [], []
    for line in fin:
        if len(line) < 5:
            continue
        if line[0] == '#':
            continue
        lin = line.split()
        for i, a in enumerate([x, xel, xeh, y, yeh, yel]):
            a.append(float(lin[i]))
        xel[-1] = x[-1] - xel[-1]
        xeh[-1] = xeh[-1] - x[-1]
        yel[-1] = abs(yel[-1])
    gr = R.TGraphAsymmErrors(len(x), np.array(x), np.array(y), np.array(xel), np.array(xeh),
            np.array(yel), np.array(yeh))
    fin.close()
    return gr


def get_snd2016_v1():
    gr = get_gr_from_file('cs_pi0gamma_snd_2016.dat')
    gr.SetName('cs_pi0gamma_snd_2016')
    gr.SetMarkerStyle(7)
    gr.SetMarkerColor(R.kOrange+7)
    gr.SetLineColor(R.kOrange+7)
    fbw = R.TF1('fbw_snd_2016', '[2]*TMath::BreitWigner(x, [0], [1])', 782-30, 782+30)
    fbw.SetLineColor(R.kOrange+7)
    fbw.SetLineWidth(1)
    fbw.SetParameters(782, 12, 1000)
    fbw.SetNpx(1000)
    fbw.SetTitle('SND 2016 (VEPP-2M)')
    gr.Fit( fbw, 'r', 'goff')
    return gr, fbw

def get_gr_from_file_comma(filename, ix=[0, 1, 2, 3, 4, 5]):
    fin = open(filename)
    x, xel, xeh = [], [], []
    y, yel, yeh = [], [], []
    for line in fin:
        if len(line) < 5:
            continue
        if line[0] == '#':
            continue
        lin = line.split(',')
        for i, a in enumerate([x, xel, xeh, y, yeh, yel]):
            if not ix[i] == -1:
                if not (i == 3 and '<' in lin[ ix[i] ]):
                    a.append(float( lin[ ix[i] ] ))
                else:
                    print lin[ ix[i] ]
                    a.append(float( lin[ ix[i] ][2:-1] ))
                    yeh.append( 0. )
                    yel.append( a[-1] )
                    break
            else:
                a.append(0.)
            # a.append(float(lin[i]))
        xel[-1] = x[-1] - xel[-1]
        xeh[-1] = xeh[-1] - x[-1]
        yel[-1] = abs(yel[-1])
    gr = R.TGraphAsymmErrors(len(x), np.array(x), np.array(y), np.array(xel), np.array(xeh),
            np.array(yel), np.array(yeh))
    gr.SetTitle('')
    fin.close()
    return gr

def get_snd2016():
    gr = get_gr_from_file_comma('cs_pi0gamma_snd_2016.dat')
    gr.SetName('cs_pi0gamma_snd_2016')
    gr.SetMarkerStyle(7)
    gr.SetMarkerColor(R.kRed)
    gr.SetLineColor(R.kRed)
    return gr

def get_snd2003():
    gr = get_gr_from_file_comma('cs_pi0gamma_snd_2003.dat')
    gr.SetName('cs_pi0gamma_snd_2003')
    gr.SetMarkerStyle(7)
    gr.SetMarkerColor(R.kViolet)
    gr.SetLineColor(R.kViolet)
    return gr

def get_snd2000():
    gr = get_gr_from_file_comma('cs_pi0gamma_snd_2000.dat')
    gr.SetName('cs_pi0gamma_snd_2000')
    gr.SetMarkerStyle(7)
    gr.SetMarkerColor(R.kMagenta)
    gr.SetLineColor(R.kMagenta)
    return gr

def get_cmd2005():
    gr = get_gr_from_file_comma('cs_pi0gamma_cmd_2005.dat', [0, 0, 0, 1, 2, 3])
    gr.SetName('cs_pi0gamma_cmd_2005')
    gr.SetMarkerStyle(7)
    gr.SetMarkerColor(R.kBlue)
    gr.SetLineColor(R.kBlue)
    return gr

def getAkhmetshin2004():
    xval = array("f", [599.86, 629.86, 659.86, 719.86, 749.86, 759.86, 763.86, 769.86, 773.86, 777.86, 779.86, 780.86, 781.86, 782.86, 783.86, 785.86, 789.86, 793.86, 799.86, 809.86, 819.86, 839.86, 879.86, 919.86, 939.86, 949.86, 957.86, 969.86, 983.93, 1003.91, 1010.53, 1015.77, 1016.77, 1016.91, 1017.61, 1017.77, 1018.58, 1018.83, 1019.5, 1019.84, 1020.62, 1021.54, 1022.79, 1027.67, 1033.67, 1039.59, 1049.8, 1059.49, 1079.0, 1163.4, 1310.0])
    xerrminus = array("f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    xerrplus = array("f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    yval = array("f", [1.23, 1.78, 1.92, 2.0, 5.08, 8.31, 12.97, 17.64, 34.33, 76.65, 125.81, 184.98, 172.26, 183.37, 162.0, 118.44, 42.8, 19.93, 11.18, 5.22, 2.74, 1.58, 0.44, 0.41, 0.74, 0.5, 0.35, 0.26, 0.16, 0.44, 0.61, 1.95, 2.95, 3.59, 3.97, 4.29, 5.72, 5.46, 4.77, 4.54, 2.85, 1.52, 0.78, 0.08, 0.11, 0.11, 0.13, 0.2, 0.08, 0.08, 0.05])
    yerrminus = array("f", [0.86, 0.74, 0.89, 0.65, 0.97, 1.4, 1.52, 1.77, 1.82, 2.64, 4.92, 10.99, 2.47, 4.8, 4.72, 4.16, 3.8, 2.06, 1.52, 1.09, 0.62, 0.45, 0.21, 0.13, 0.22, 0.15, 0.13, 0.12, 0.11, 0.12, 0.1, 0.17, 0.16, 0.3, 0.18, 0.24, 0.32, 0.17, 0.24, 0.52, 0.15, 0.17, 0.13, 0.08, 0.0, 0.0, 0.0, 0.0, 0.0, 0.04, 0.02])
    yerrplus = array("f", [0.86, 0.74, 0.89, 0.65, 0.97, 1.4, 1.52, 1.77, 1.82, 2.64, 4.92, 10.99, 2.47, 4.8, 4.72, 4.16, 3.8, 2.06, 1.52, 1.09, 0.62, 0.45, 0.21, 0.13, 0.22, 0.15, 0.13, 0.12, 0.11, 0.12, 0.1, 0.17, 0.16, 0.3, 0.18, 0.24, 0.32, 0.17, 0.24, 0.52, 0.15, 0.17, 0.13, 0.08, 0.0, 0.0, 0.0, 0.0, 0.0, 0.04, 0.02])
    numpoints = 51
    p1342_d1x1y1 = R.TGraphAsymmErrors(numpoints, xval, yval, xerrminus, xerrplus, yerrminus, yerrplus)
    p1342_d1x1y1.SetName("pi0gAkhmetshin2004")
    p1342_d1x1y1.SetTitle("pi0gAkhmetshin2004")
    p1342_d1x1y1.SetMarkerStyle(24)
    p1342_d1x1y1.SetMarkerColor(R.kViolet)
    p1342_d1x1y1.SetLineColor(R.kViolet)
    return p1342_d1x1y1



def main2():
    cx, cy = 600, 600
    xmin, xmax = 600., 1600.
    ymin, ymax = 0., 200.
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
            ymin = 1.e-2
        if ymax == 200.:
            ymax = 500.
    c1 = R.TCanvas('c1', 'c1', cx, cy)
    frame = c1.DrawFrame(xmin, ymin, xmax, ymax)
    c1.SetLogx(logx)
    c1.SetLogy(logy)
    c1.SetGrid()
    c1.SetTopMargin(.025)
    c1.SetRightMargin(.025)
    # gcmd2004 = getAkhmetshin2004()
    gcmd2004 = get_cmd2005()
    gcmd2004.Draw('p')
    g = gcmd2004
    # gsnd2016, fbw_snd2016 = get_snd2016()
    gsnd2016 = get_snd2016()
    gsnd2016.Draw('p same')
    gsnd2003 = get_snd2003()
    gsnd2003.Draw('p same')
    gsnd2000 = get_snd2000()
    gsnd2000.Draw('p same')
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
    x0, y0, dy = .75, .9, -.05
    lat.SetTextColor( gsnd2016.GetMarkerColor() )
    lat.DrawLatexNDC(x0, y0, 'SND 2016')
    lat.SetTextColor( gcmd2004.GetMarkerColor() )
    lat.DrawLatexNDC(x0, y0+dy*1, 'CMD-2 2004')
    lat.SetTextColor( gsnd2003.GetMarkerColor() )
    lat.DrawLatexNDC(x0, y0+dy*2, 'SND 2003')
    lat.SetTextColor( gsnd2000.GetMarkerColor() )
    lat.DrawLatexNDC(x0, y0+dy*3, 'SND 2000')
    ################
    c1.Update()
    if not '-b' in sys.argv:
        raw_input()
    if 'save' in sys.argv:
        c1.SaveAs('~/my_cross_section.png')
        drd[0].SaveAs('~/my_cross_section_diff.png')


if __name__ == '__main__':
    if 'robot' in sys.argv:
        # os.system('%s xmin 777 xmax 787 ymin 70' % sys.argv[0])
        # os.system('%s xmin 550 xmax 1400 logy' % sys.argv[0])
        # os.system('%s xmin 1010 xmax 1030 ymax 7' % sys.argv[0])
        os.system('%s xmin 1020 xmax 1400 ymax .25' % sys.argv[0])
    else:
        main2()
