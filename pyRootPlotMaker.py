import ROOT
import utils

## plot a stacked histogram of backgrounds
## if calling this from another function, must give it a THStack defined in the other
## function's scope so it doesn't disappear
def plotBackgrounds(h_bkg_vec, bkg_names, canvas=None, stack=None, saveAs=None, xRangeUser=None, doPause=False, 
                    isLog=True, xAxisTitle="H_{T}", xAxisUnit="GeV", dataMax=0, userMax=None, userMin=None,
                    doLegend=False, doMT2Colors=False):

    if canvas==None:
        canvas = ROOT.TCanvas()
    if stack==None:
        stack = ROOT.THStack()

    if(isLog):
        canvas.SetLogy(1)

    canvas.cd()

    colors = [ROOT.kAzure+7, ROOT.kSpring-5, ROOT.kOrange-2, ROOT.kRed-7,
              ROOT.kCyan-7, ROOT.kMagenta-7, ROOT.kGray]

    nh = len(h_bkg_vec)
    
    for i in range(nh):
        if doMT2Colors:
            h_bkg_vec[i].SetFillColor(utils.getMT2Color(bkg_names[i]))
        else:
            h_bkg_vec[i].SetFillColor(colors[nh-1-i])
        h_bkg_vec[i].SetLineColor(ROOT.kBlack)
    
    for i in range(nh):
        stack.Add(h_bkg_vec[i])

    stack.Draw("HIST")

    if xRangeUser!=None:
        stack.GetXaxis().SetRangeUser(*xRangeUser)
    if xAxisUnit==None:
        stack.GetXaxis().SetTitle(xAxisTitle)
        stack.GetYaxis().SetTitle("Events")
    else:
        stack.GetXaxis().SetTitle(xAxisTitle + " [{0}]".format(xAxisUnit))
        stack.GetYaxis().SetTitle("Events / {0} GeV".format(h_bkg_vec[0].GetXaxis().GetBinWidth(1)))
    stack.GetYaxis().SetTitleOffset(1.2)

    utils.SetYBounds(stack, stack.GetMaximum(), stack.GetMinimum(), dataMax)
    if userMax!=None:
        stack.SetMaximum(userMax)
    if userMin!=None:
        stack.SetMinimum(userMin)

    ## legend
    if doLegend:
        leg = ROOT.TLegend(0.65,0.71,0.88,0.88)
        for i in range(len(h_bkg_vec)):
            leg.AddEntry(h_bkg_vec[-i-1],bkg_names[-i-1],"f")
        leg.Draw()

    if saveAs != None:
        canvas.saveAs(saveAs)
        
    if doPause:
        raw_input()

## make a ratio plot. For use within the plotDataMC and plotComparison functions
def plotRatio(h1, h2, canvas=None, ratioHist=None, xRangeUser=None, ratioTitle = "Data/MC", markerSize=0.7):

    if canvas==None:
        canvas = ROOT.TCanvas()
    if ratioHist==None:
        ratioHist = ROOT.TH1F()

    canvas.cd()

    h2.Copy(ratioHist)
    ratioHist.Divide(h1)
    ratioHist.SetTitle("")
    #yaxis
    ratioHist.GetYaxis().SetRangeUser(0,2)
    ratioHist.GetYaxis().SetTitle(ratioTitle)
    ratioHist.GetYaxis().SetTitleSize(0.18)
    ratioHist.GetYaxis().SetTitleOffset(0.17)
    ratioHist.GetYaxis().SetLabelSize(0.13)
    ratioHist.GetYaxis().CenterTitle()
    ratioHist.GetYaxis().SetNdivisions(505)
    #xaxis
    ratioHist.GetXaxis().SetLabelSize(0.0)
    ratioHist.GetXaxis().SetTitle("")
    ratioHist.GetXaxis().SetTickSize(0.06)
    #markers
    ratioHist.SetMarkerStyle(20)
    ratioHist.SetMarkerSize(markerSize)
    
    ratioHist.Draw()

    # # boxes = []
    # # colors = []
    # # for i in range(1,ratioHist.GetNbinsX()+1):
    # #     boxes.append(ROOT.TBox())
    # #     try:
    # #         sigma = (ratioHist.GetBinContent(i)-1)/ratioHist.GetBinError(i)
    # #     except:
    # #         sigma = 0
    # #     s = min(abs(sigma)**2 * 0.03, 0.4)
    # #     if sigma>0:
    # #         colors.append(ROOT.TColor(12345+i, 1.0-s, 1.0-s, 1.0))
    # #     else:
    # #         colors.append(ROOT.TColor(12345+i, 1.0, 1.0-s, 1.0-s))
    # #     boxes[-1].SetFillColor(12345+i)
    # #     boxes[-1].DrawBox(ratioHist.GetXaxis().GetBinLowEdge(i),0.0,ratioHist.GetXaxis().GetBinUpEdge(i),1.98)

    #line
    line = ROOT.TLine()
    line.SetLineColor(ROOT.kGray+2)
    line.SetLineWidth(2)
    line.SetLineStyle(7)
    xmin = ratioHist.GetXaxis().GetBinLowEdge(1)
    xmax = ratioHist.GetXaxis().GetBinUpEdge(ratioHist.GetNbinsX())
    if xRangeUser!=None:
        xmin = xRangeUser[0]
        xmax = xRangeUser[1]
    line.DrawLine(xmin,1,xmax,1)
    ratioHist.Draw("SAME")
    ratioHist.Draw("SAMEAXIS")


## plot data and stacked background hist. Arguments should be self-explanatory
def plotDataMC(h_bkg_vec, bkg_names, h_data, title="Data/MC", subTitle="", doRatio=True, scaleMCtoData=False, saveAs=None, 
               isLog=True, dataTitle="Data", xRangeUser=None, doPause=False, lumi=1.0, lumiUnit="fb",
               energy=13, xAxisTitle="H_{T}", xAxisUnit="GeV", userMax=None, userMin=None, doSort=False,
               doMT2Colors=False):

    ROOT.gStyle.SetOptStat(0)
     
    #### setup canvas and pads ####

    c = ROOT.TCanvas()
    
    if doRatio:
        c.SetCanvasSize(700,600)
        pads = []
        pads.append(ROOT.TPad("1","1",0.0,0.16,1.0,1.0))
        pads.append(ROOT.TPad("2","2",0.0,0.0,1.0,0.17))
        
        pads[0].SetTopMargin(0.08)
        pads[0].SetLeftMargin(0.12)
        pads[0].SetBottomMargin(0.10)
        pads[1].SetLeftMargin(0.12)
        
        pads[0].Draw()
        pads[1].Draw()
        pads[0].cd()
    else:
        c.SetCanvasSize(700,504)
        pads = [c]
        pads[0].SetLeftMargin(0.12)
        pads[0].SetTopMargin(0.08)

    if isLog:
        pads[0].SetLogy()

    pads[0].cd()

    ## MC
    integrals = [h.Integral(0,-1) for h in h_bkg_vec]
    if doSort:
        zipped = zip(h_bkg_vec,bkg_names)
        sorted_bkg = [x for (y,x) in sorted(zip(integrals,zipped))]
        h_bkg_vec = [x for (x,y) in sorted_bkg]
        bkg_names = [y for (x,y) in sorted_bkg]
    else:
        h_bkg_vec = h_bkg_vec[::-1]
        bkg_names = bkg_names[::-1]

    scaleFactor = 1.0
    if(scaleMCtoData):
        tot_MC_integral = sum(integrals)
        data_integral = h_data.Integral(0,-1)
        scaleFactor = data_integral/tot_MC_integral
    for i in range(len(h_bkg_vec)):
        h_bkg_vec[i].Scale(scaleFactor)

    stack = ROOT.THStack("hs","")
    plotBackgrounds(h_bkg_vec, bkg_names, canvas=pads[0], stack=stack, xRangeUser=xRangeUser, isLog=isLog, 
                    xAxisTitle=xAxisTitle, xAxisUnit=xAxisUnit, dataMax=h_data.GetMaximum(), 
                    userMax=userMax, userMin=userMin, doMT2Colors=doMT2Colors)

    ## data
    h_data.SetMarkerStyle(20)
    h_data.SetMarkerSize(0.7)
    h_data.SetMarkerColor(ROOT.kBlack)
    h_data.SetLineColor(ROOT.kBlack)
    if xRangeUser!=None:
        h_data.GetXaxis().SetRangeUser(*xRangeUser)

    h_data.Draw("SAME")

    ## legend
    leg = ROOT.TLegend(0.65,0.71,0.88,0.88)
    for i in range(len(h_bkg_vec)):
        leg.AddEntry(h_bkg_vec[-i-1],bkg_names[-i-1],"f")
    leg.AddEntry(h_data,dataTitle)
    leg.Draw()
    
    # title
    text = ROOT.TLatex()
    text.SetNDC(1)
    text.SetTextAlign(13)
    text.SetTextFont(42)
    text.SetTextSize(0.040)
    text.DrawLatex(0.19,0.88,title)
    # subtitle
    text.SetTextFont(42)
    text.SetTextSize(0.03)
    text.DrawLatex(0.19,0.825,subTitle)
    # lumi
    text.SetTextAlign(31)
    text.SetTextSize(0.035)
    text.SetTextFont(42)
    text.DrawLatex(0.89,0.93,"{0} {1}^{{-1}} ({2} TeV)".format(lumi, lumiUnit, energy))
    # CMS text
    text.SetTextAlign(11)
    text.SetTextFont(62)
    text.DrawLatex(0.12,0.93,"CMS")
    #Data/MC integral ratio
    text.SetTextFont(62)
    text.SetTextAlign(13)
    text.SetTextSize(0.03)
    text.DrawLatex(0.65,0.70,"MC scaled by {0:.2f}".format(scaleFactor))
    text.DrawLatex(0.65,0.665,"# Data events: {0:d}".format(int(h_data.GetEntries())))
    #text.DrawLatex(0.65,0.63,"Total # Fakes: {0:.1f}".format(h_bkg_vec[1].Integral(0,-1)))

    ######## ratio plot ############
    
    if doRatio:
        pads[1].cd()
    
        h1 = ROOT.TH1F()
        h_bkg_vec[0].Copy(h1)
        for i in range(len(h_bkg_vec)-1):
            h1.Add(h_bkg_vec[i+1])
        ratio = ROOT.TH1F()

        plotRatio(h1, h_data, canvas=pads[1], ratioHist=ratio, xRangeUser=xRangeUser)
    
    c.Update()
    c.SetWindowSize(c.GetWw()+4, c.GetWh()+50)

    if saveAs!=None:
        c.SaveAs(saveAs)

    if doPause:
        raw_input()

## make a comparison plot between two histograms. Plots both histos on one axis, as well as a ratio plot
def plotComparison(h1, h2, title="", ratioTitle="Data/MC", h1Title="MC", h2Title="Data", saveAs=None,
                   size=(700,600), xRangeUser=None, markerSize=0.65, doPause=False):


    ROOT.gStyle.SetOptStat(0)

    c = ROOT.TCanvas()
    c.SetCanvasSize(size[0],size[1])

    pads = []
    pads.append(ROOT.TPad("1","1",0.0,0.16,1.0,1.0))
    pads.append(ROOT.TPad("2","2",0.0,0.0,1.0,0.17))

    pads[0].SetLogy()
    pads[0].SetTopMargin(0.07)
    pads[0].SetLeftMargin(0.12)
    pads[0].SetBottomMargin(0.10)
    pads[1].SetLeftMargin(0.12)
    
    pads[0].Draw()
    pads[1].Draw()
    pads[0].cd()
    
    h1.SetTitle(title)
    h1.SetLineColor(ROOT.kRed)
    h1.GetXaxis().SetTitleOffset(1.15)
    if xRangeUser!=None:
        h1.GetXaxis().SetRangeUser(xRangeUser)
    h1.GetYaxis().SetTitle("Entries / {0} GeV".format(h1.GetXaxis().GetBinWidth(1)))
    h1.Draw()
    h2.SetLineColor(ROOT.kBlack)
    h2.Draw("SAME")
    
    leg = ROOT.TLegend(0.75,0.75,0.85,0.85)
    leg.AddEntry(h1, h1Title)
    leg.AddEntry(h2, h2Title)
    leg.Draw()
    
    ######## ratio plot ############
    
    pads[1].cd()
    ratio = ROOT.TH1D()
    plotRatio(h1,h2,canvas=pads[1], ratioHist=ratio, ratioTitle=ratioTitle, xRangeUser=xRangeUser, 
              markerSize=markerSize)

    if saveAs!=None:
        c.SaveAs(saveAs)

    if doPause:
        raw_input()








