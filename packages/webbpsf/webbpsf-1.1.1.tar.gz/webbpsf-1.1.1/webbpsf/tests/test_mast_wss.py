import webbpsf

def test_load_mast_opd():
    """Test the machinery for loading an OPD from MAST.

    NOTE THIS TEST WILL DOWNLOAD A FILE FROM MAST.
    """

    nrc = webbpsf.NIRCam()
    nrc.load_wss_opd_by_date('2022-07-30')

    assert nrc.pupilopd[0].data.shape==(1024, 1024), "OPD data does not have expected dimensions"
    assert nrc.pupilopd[0].header['CORR_ID'] == 'O2022073001', "Missing expected correction ID in header"
