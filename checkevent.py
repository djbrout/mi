import urlparse
import matplotlib.pyplot as plt
import numpy as np; import os
import hp2np
import tempfile
import shutil
import sys
import glob
import gcn
import gcn.handlers
import gcn.notice_types
import requests
import healpy as hp
import subprocess


def get_skymap(root,outfolder,trigger_id):
    """
    Look up URL of sky map in VOEvent XML document,
    download sky map, and parse FITS file.
    """
    # Read out URL of sky map.
    # This will be something like
    # https://gracedb.ligo.org/apibasic/events/M131141/files/bayestar.fits.gz
    skymap_url = root.find(
        "./What/Param[@name='SKYMAP_URL_FITS_BASIC']").attrib['value']

    skymap_filename = os.path.join(outfolder,trigger_id+'_'+skymap_url.split('/')[-1])

    # Send HTTP request for sky map. Save in specific location
    try:
        subprocess.check_call([
            'curl', '-o',skymap_filename, '--netrc',
            skymap_url])
    except CalledProcessError:
        #SEND EMAIL OR TEXT
        raise CalledProcessError

    # Read HEALPix data from the temporary file
    skymap, header = hp.read_map(skymap_filename, h=True, verbose=False)
    header = dict(header)

    # Done!
    return skymap, header

# Function to call every time a GCN is received.
# Run only for notices of type LVC_INITIAL or LVC_UPDATE.
@gcn.handlers.include_notice_types(
    gcn.notice_types.LVC_INITIAL,
    gcn.notice_types.LVC_UPDATE)
def process_gcn(payload, root):
    # Print the alert
    import listener_config as config

    # Respond only to 'test' events.
    # VERY IMPORTANT! Replce with the following line of code
    # to respond to only real 'observation' events. DO SO IN CONFIG FILE
    if root.attrib['role'] != config.mode.lower(): return #This can be changed in the config file

    # Respond only to 'CBC' events. Change 'CBC' to "Burst' to respond to only
    # unmodeled burst events.
    if root.find("./What/Param[@name='Group']").attrib['value'] != 'CBC': return

    print('Got LIGO VOEvent!!!!!!!')
    print(payload)
    #print(root.attrib.items())


    # Read out integer notice type (note: not doing anythin with this right now)
    notice_type = int(root.find("./What/Param[@name='Packet_Type']").attrib['value'])

    #Creating unique folder to save trigger data
    skymap_url = root.find(
        "./What/Param[@name='SKYMAP_URL_FITS_BASIC']").attrib['value']
    
    trigger_id = str(root.find("./What/Param[@name='GraceID']").attrib['value'])
    
    outfolder = os.path.join(config.trigger_outpath,trigger_id)
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)

    # Numpy file to save all parameters for future use in webpage.
    event_paramfile = os.path.join(outfolder,trigger_id+'_params.npz')
    # Dictionary containing all pertinant parameters
    event_params = {}

    trigger_mjd_rounded = float(root.find("./What/Param[@name='Trigger_TJD']").attrib['value'])+40000.
    trigger_sod = float(root.find("./What/Param[@name='Trigger_SOD']").attrib['value'])
    seconds_in_day = 86400.
    trigger_mjd = round(trigger_mjd_rounded + trigger_sod/seconds_in_day,4)    

    event_params['MJD'] = str(trigger_mjd)
    event_params['ETA'] = str(root.find("./What/Param[@name='Eta']").attrib['value'])
    event_params['FAR'] = str(root.find("./What/Param[@name='FAR']").attrib['value'])+' '+str(root.find("./What/Param[@name='FAR']").attrib['unit'])
    event_params['ChirpMass'] = str(root.find("./What/Param[@name='ChirpMass']").attrib['value'])+' '+str(root.find("./What/Param[@name='ChirpMass']").attrib['unit'])
    event_params['MaxDistance'] = str(root.find("./What/Param[@name='MaxDistance']").attrib['value'])+' '+str(root.find("./What/Param[@name='MaxDistance']").attrib['unit'])
    

    #set to defualt
    event_params['integrated_prob'] = '-9.999'
    event_params['M1'] = '-999'
    event_params['M2'] = '-999'
    event_params['nHexes'] = '-999'

    np.savez(event_paramfile,
             MJD=event_params['MJD'],
             ETA=event_params['ETA'],
             FAR=event_params['FAR'],
             ChirpMass=event_params['ChirpMass'],
             MaxDistance=event_params['MaxDistance'],
             integrated_prob=event_params['integrated_prob'],
             M1 = event_params['M1'],
             M2 = event_params['M2'],
             nHexes = event_params['nHexes']
             )

    #save payload to file
    open(os.path.join(outfolder,trigger_id+'_payload.xml'), 'w').write(payload)
    #save url to file
    open(os.path.join(outfolder,trigger_id+'_skymapURL.txt'), 'w').write(skymap_url)
    #save mjd to file
    open(os.path.join(outfolder,trigger_id+'_eventMJD.txt'), 'w').write(str(trigger_mjd))
    

    # Read sky map
    skymap, header = get_skymap(root,outfolder,trigger_id) 
    
    #Fire off analysis code    
    if skymap_url.split('/')[-1] == 'bayestar.fits.gz':
        args = ['python', 'recycler.py', '--triggerpath='+config.trigger_outpath, '--triggerid='+trigger_id, '--mjd='+str(trigger_mjd)]    
        print 'ARGSSSSSSSSSSSSSSSSSSSSS'
        print args
        subprocess.Popen(args)

    #Need to send an email here saying analysis code was fired
    
    print 'Finished downloading, fired off job, listening again...'
    


import logging
# Set up logger
logging.basicConfig(level=logging.INFO)

# Listen for GCNs until the program is interrupted
# (killed or interrupted with control-C).
print 'Listening...'
gcn.listen(host='68.169.57.253', port=8096, handler=process_gcn)

#IF YOU END UP HERE THEN SEND AN EMAIL AND REBOOT
