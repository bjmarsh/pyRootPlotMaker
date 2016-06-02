import ROOT

def getMT2Color(sample):
    
    if 'top' in sample: return 855
    if 'wjets' in sample: return 417
    if 'zinv' in sample: return 418
    if 'qcd' in sample: return 401
    if 'gjet' in sample: return 18
    if 'dyjets' in sample: return 430
    if 'fragphoton' in sample: return 38
    if 'fakephoton' in sample: return 46

    return ROOT.kBlack

def SetYBounds(stack, mc_max, mc_min, data_max):
    tmax = max(MC_MAX,data_Max)
    if isLog:
        tmin = mc_min
        if tmin>0:
            tmin = min(0.1, 0.5*tmin)
        else:
            tmin = 0.1
        stack.SetMinimum(tmin)
        stack.SetMaximum(tmax**(1.0/0.69))
    else:
        stack.SetMaximum(tmax*1.33)





