import ROOT

def plotComparison(h1, h2, title="", ratioTitle="Data/MC", h1Title="MC", h2Title="Data", fout="comparison.pdf",
                   size=(700,600)):


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
    h2.Copy(ratio)
    ratio.Divide(h1)
    #yaxis
    ratio.GetYaxis().SetRangeUser(0,2)
    ratio.GetYaxis().SetTitle(ratioTitle)
    ratio.GetYaxis().SetTitleSize(0.18)
    ratio.GetYaxis().SetTitleOffset(0.17)
    ratio.GetYaxis().SetLabelSize(0.13)
    ratio.GetYaxis().CenterTitle()
    ratio.GetYaxis().SetNdivisions(505)
    #xaxis
    ratio.GetXaxis().SetLabelSize(0.0)
    ratio.GetXaxis().SetTitle("")
    #markers
    ratio.SetMarkerStyle(20)
    
    ratio.Draw()

    
    # boxes = []
    # colors = []
    # for i in range(1,ratio.GetNbinsX()+1):
    #     boxes.append(ROOT.TBox())
    #     try:
    #         sigma = (ratio.GetBinContent(i)-1)/ratio.GetBinError(i)
    #     except:
    #         sigma = 0
    #     s = min(abs(sigma)**2 * 0.03, 0.4)
    #     if sigma>0:
    #         colors.append(ROOT.TColor(12345+i, 1.0-s, 1.0-s, 1.0))
    #     else:
    #         colors.append(ROOT.TColor(12345+i, 1.0, 1.0-s, 1.0-s))
    #     boxes[-1].SetFillColor(12345+i)
    #     boxes[-1].DrawBox(ratio.GetXaxis().GetBinLowEdge(i),0.0,ratio.GetXaxis().GetBinUpEdge(i),1.98)

    # pads[1].Draw()

    #line
    line = ROOT.TLine()
    line.SetLineColor(ROOT.kGray+2)
    line.SetLineWidth(2)
    line.SetLineStyle(7)
    line.DrawLine(ratio.GetXaxis().GetBinLowEdge(1),1,ratio.GetXaxis().GetBinUpEdge(ratio.GetNbinsX()),1)
    ratio.Draw("SAME")
    ratio.Draw("SAMEAXIS")

    c.SaveAs(fout)

    raw_input()








