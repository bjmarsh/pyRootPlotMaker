import ROOT

def GetMT2Color(sample):
    
    if 'top' in sample: return 855
    if 'wjets' in sample: return 417
    if 'zinv' in sample: return 418
    if 'qcd' in sample: return 401
    if 'gjets' in sample: return 18
    if 'dyjets' in sample: return 430
    if 'fragphoton' in sample: return 38
    if 'fakephoton' in sample: return 46

    return ROOT.kBlack

def SetYBounds(stack, isLog, mc_max, mc_min, data_max):
    tmax = max(mc_max,data_max)
    if isLog:
        tmin = mc_min
        if tmin>0:
            tmin = max(0.1, 0.5*tmin)
        else:
            tmin = 0.1
        stack.SetMinimum(tmin)
        stack.SetMaximum(tmax**(1.0/0.69))
    else:
        stack.SetMaximum(tmax*1.33)

def PutOverflowInLastBin(h, xmax=None):

    nb = h.GetNbinsX()
    if xmax!=None:
        lastbin=1
        while h.GetXaxis().GetBinUpEdge(lastbin) <= xmax:
            lastbin += 1
        lastbin -= 1
    else:
        lastbin = nb

    bc1 = h.GetBinContent(lastbin)
    bc2 = h.Integral(lastbin+1,nb+1)
    be1 = h.GetBinError(lastbin)
    be2 = ROOT.TMath.Sqrt(sum([h.GetBinError(i)**2 for i in range(lastbin+1,nb+2)]))
    
    h.SetBinContent(lastbin,bc1+bc2)
    h.SetBinError(lastbin,ROOT.TMath.Sqrt(be1**2+be2**2))




