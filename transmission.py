#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys, os
import ROOT
from array import array
import CMS_lumi, tdrstyle


# In[2]:


ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(1)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetLabelSize(0.05,'X')
ROOT.gStyle.SetLabelSize(0.05,'Y')
ROOT.gStyle.SetTitleSize(0.06,'X')
ROOT.gStyle.SetTitleSize(0.06,'Y')
ROOT.gStyle.SetTitleOffset(0.8,'X')
ROOT.gStyle.SetTitleOffset(0.8,'Y')
ROOT.gStyle.SetLegendFont(42)
ROOT.gStyle.SetLegendTextSize(0.038)
ROOT.gStyle.SetPadTopMargin(0.07)
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kWarning


# In[65]:


inputdir = '/eos/user/f/fcetorel/LabCrystalsAndFilters_June23/Transmission/'
outdir = '/eos/user/f/fcetorel/www/SCEPCal_RD/LabMeasurments_June23/Transmission/'
filters = ['IF_2-11-3-3-1-10', 'IF_2-5-416-53-2-10', 'IF_2-5-453-26-3-8', 'IF_2-5-461-20-2-36', 'IF_2-5-462-29-1-21', 'HoyaU330_Black', 'HoyaO56_Orange']
crystals = ['BSO', 'BGO', 'PWO']


# In[96]:


crystals = True

fil = 'PWO' #change to select the filter from list above
#fil = 'IF_2-5-462-29-1-21'


# In[97]:


'''
kWhite  = 0,   kBlack  = 1,   kGray    = 920,  kRed    = 632,  kGreen  = 416,
kBlue   = 600, kYellow = 400, kMagenta = 616,  kCyan   = 432,  kOrange = 800,
kSpring = 820, kTeal   = 840, kAzure   =  860, kViolet = 880,  kPink   = 900
'''
basecols = [632+1, 416+2, 601, 800 , 616+2 , 860 + 3 , 900 +1]


# In[98]:


datadict = {}
histodict = {}
cols = {}

extralabels = ['0deg','20deg','40deg']
if 'Hoya' in fil: extralabels = ['0deg','20deg','40deg', '60deg']

dimension = {
#'BGO': ['1x1x1','0.8x0.8x5', '1.2x1.2x5', '1x1x5', '1x1x13', '1x1x16'],
'BGO': ['0.8x0.8x5', '1x1x5', '1.2x1.2x5'],
#'BGO': ['1x1x1', '1x1x5', '1x1x13'],
'BSO': ['1x1x1', '1x1x5', '1x1x13'],
'PWO': ['1x1x1', '1x1x5', '1x1x13'],   
}

if crystals:
    extralabels = dimension[fil]
    
for i,exlab in enumerate(extralabels):
    cols['%s_%s'%(fil, exlab)] = basecols[i] 
    
    with open('%s/%s_%s.Sample.Raw.asc'%(inputdir, fil, exlab)) as f: 
        lines_after_90 = f.readlines()[90:]
        #print (lines_after_90)
    x = []
    y = []
    for i,l in enumerate(lines_after_90):
        mydata = l.replace('\n', '').split('\t')
        #print (mydata)
        x.append(float(mydata[0]))   
        y.append(float(mydata[1]))
        #datadict[float(mydata[0])] = float(mydata[1])
    datadict['%s_%s'%(fil, exlab)] = [x, y] 


# In[99]:


for key, datas in datadict.items():
    histo = ROOT.TGraph(len(x), array("f", datas[0]), array("f", datas[1]) )
    histo.SetName(key)
    histodict [key] = histo


# In[100]:


#Now plotting
c = ROOT.TCanvas("", "", 1200, 800)
c.cd()

hdummy = ROOT.TH2F('hdummy','',100,200,800,100,0,100.)
hdummy.GetXaxis().SetTitle('Wavelenght (nm)')
hdummy.GetYaxis().SetTitle('Transmission (%)')

hdummy.Draw()

if 'Orange' in fil: 
    leg = ROOT.TLegend(0.15,0.8,0.6,0.92)
    #leg.SetNColumns(2)
    hdummy.GetYaxis().SetRangeUser(0,110)
    
elif 'Black' in fil: 
    leg = ROOT.TLegend(0.5,0.8,0.8,0.92)
    #leg.SetNColumns(2)
    hdummy.GetYaxis().SetRangeUser(0,110)
elif crystals: 
    leg = ROOT.TLegend(0.5,0.2,0.8,0.4)
    #leg.SetNColumns(2)
    hdummy.GetYaxis().SetRangeUser(0,110)
    

else: leg = ROOT.TLegend(0.55,0.6,0.90,0.75)
leg.SetBorderSize(0)
leg.SetFillStyle(0)


for key,histo in histodict.items():

    histo.SetMarkerColor(cols[key])
    histo.SetLineColor(cols[key])

    histo.SetMarkerStyle(22)
    histo.Draw("PL same")
    leg.AddEntry(histo, key, 'l')
    
leg.Draw("same")
c.SaveAs("%s/%s.png"%(outdir, fil))

c.Delete()
hdummy.Delete()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




