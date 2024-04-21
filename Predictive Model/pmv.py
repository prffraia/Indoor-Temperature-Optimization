from pythermalcomfort import pmv_ppd
def pmv_ppd_diy(predicted_temp, predicted_hum, tr = 23, vr = 0.15, met = 1.1, clo = 1.0): 
    pmv_ppd_val = pmv_ppd(tdb = predicted_temp, rh = predicted_hum, tr=tr, vr = vr, met = met, clo = clo)
    return pmv_ppd_val