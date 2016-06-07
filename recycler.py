import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import spatial
import mags
import hp2np
import annis_config as config
import sys, getopt
import sourceProb
import hexalate as hexa
import jsonMaker as jm
import triggerpages as tp

class event:

    def __init__(self,skymap_filename,outfolder,trigger_id,mjd):
        self.skymap = skymap_filename
        self.mjd = mjd
        self.outfolder = outfolder
        self.trigger_id = trigger_id

        #Setup website directories
        self.website_imagespath = os.path.join('./DES_GW_Website/Triggers/',trigger_id,'images')
        self.website_jsonpath = os.path.join('./DES_GW_Website/Triggers/',trigger_id)
        if not os.path.exists(self.website_imagespath):
            os.makedirs(self.website_imagespath)
        
        self.event_paramfile = os.path.join(outfolder,trigger_id+'_params.npz')
        self.event_params = np.load(self.event_paramfile)
        
        
    def getContours(self,exposure_length=None):
        if exposure_length is None:
            exposure_length = config.exposure_length

        plt.ion()
        figure = plt.figure(1)

        self.ra,self.dec,self.ligo = hp2np.hp2np(self.skymap)

        #computing limiting mag
        self.obs = mags.observed(self.ra,self.dec,self.ligo,round(self.mjd,0))
        self.omags = self.obs.limitMag("i")
        #self.obs.resetTime(self.mjd)
        self.obs.limitMag("i",exposure=exposure_length)

        # plot as ra,dec map (all coordinates are stored as radians)
        plt.clf()
        plt.hexbin( self.obs.ra*360./2/np.pi,
                    self.obs.dec*360./2/np.pi,
                    self.obs.maglim,
                    vmin=15)
        plt.colorbar()
        plt.xlabel('RA')
        plt.ylabel('DEC')
        plt.savefig(os.path.join(self.outfolder,self.trigger_id+'_limitingMagMap.png'))
        os.system('cp '+os.path.join(self.outfolder,self.trigger_id+'_limitingMagMap.png')+' '+self.website_imagespath)

        #Calculate source probability map
        self.sm=sourceProb.map(self.obs, lumModel="delta")
        self.sm.calculateProb()

        plt.clf()
        #plt.hexbin(self.obs.x,self.obs.y,self.sm.probMap)
        plt.hexbin( self.obs.ra*360./2/np.pi,
                    self.obs.dec*360./2/np.pi,
                    self.sm.probMap,
                    )
        plt.colorbar()
        plt.xlabel('RA')
        plt.ylabel('DEC')
        plt.savefig(os.path.join(self.outfolder,self.trigger_id+'_sourceProbMap.png'))
        os.system('cp '+os.path.join(self.outfolder,self.trigger_id+'_sourceProbMap.png')+' '+self.website_imagespath)

        #DES Source Prob Map x Ligo Sky Map
        plt.clf()
        #plt.hexbin(self.obs.x,self.obs.y,self.sm.probMap*self.ligo)
        plt.hexbin( self.obs.ra*360./2/np.pi,
                    self.obs.dec*360./2/np.pi,
                    self.sm.probMap*self.ligo,
                    )
        plt.colorbar()
        plt.xlabel('RA')
        plt.ylabel('DEC')
        plt.savefig(os.path.join(self.outfolder,self.trigger_id+'_sourceProbxLIGO.png'))
        os.system('cp '+os.path.join(self.outfolder,self.trigger_id+'_sourceProbxLIGO.png')+' '+self.website_imagespath)

        plt.clf()
        #plt.hexbin(self.obs.x,self.obs.y,self.ligo)
        plt.hexbin( self.obs.ra*360./2/np.pi,
                    self.obs.dec*360./2/np.pi,
                    self.ligo,
                    )
        plt.colorbar()
        plt.xlabel('RA')
        plt.ylabel('DEC')
        plt.savefig(os.path.join(self.outfolder,self.trigger_id+'_LIGO.png'))
        os.system('cp '+os.path.join(self.outfolder,self.trigger_id+'_LIGO.png')+' '+self.website_imagespath)

        return

    def makeJSON(self):
        exposureList = config.exposureList
        filterList = config.filterList
        tilingList = config.tilingList
        nHexes = config.nHexes
        all_hex_centers = os.path.join(os.environ["DESGW_DATA_DIR"],config.hex_centers)
        
        jsonFile = os.path.join(self.outfolder,self.trigger_id+'_'+str(nHexes)+'Hexes.json') 

        raHexen, decHexen, hexVals, hexRank = hexa.hexalateNHexes(self.obs,self.sm,nHexes,all_hex_centers) #Getting top 10 hexes
        print hexVals
        jm.writeJson(raHexen, decHexen, exposureList, filterList, tilingList, jsonFile) #Writing hexes to .json
        
        #adding integrated probability to paramfile
        integrated_prob = np.sum(hexVals)
        nHexes = str(len(hexVals))

        np.savez(self.event_paramfile,
             MJD=self.event_params['MJD'],
             ETA=self.event_params['ETA'],
             FAR=self.event_params['FAR'],
             ChirpMass=self.event_params['ChirpMass'],
             MaxDistance=self.event_params['MaxDistance'],
             integrated_prob=integrated_prob,
             M1 = self.event_params['M1'],
             M2 = self.event_params['M2'],
             nHexes = nHexes
             )

        #Copy json file to web server for public download
        print jsonFile
        os.system('scp '+jsonFile+' codemanager@desweb.fnal.gov:/des_web/www/html/desgw/Triggers/'+self.trigger_id+'/'+self.trigger_id+'_'+str(config.nHexes)+'Hexes.json')
        return

    def send_nonurgent_Email(self):
        import smtplib
        from email.mime.text import MIMEText

        text = 'New event trigger. See \nhttp://des-ops.fnal.gov:8080/desgw/Triggers/'+self.trigger_id+'/'+self.trigger_id+'_trigger.html'

        # Create a text/plain message
        msg = MIMEText(text)
        

        # me == the sender's email address
        # you == the recipient's email address
        me = 'noreply-desGW@fnal.gov'
        you = 'djbrout@gmail.com'

        msg['Subject'] = 'New GW Trigger '+self.trigger_id
        msg['From'] = me
        msg['To'] = you

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP('localhost')
        s.sendmail(me, [you], msg.as_string())
        s.quit()
        print 'Email sent...'
        return

    def updateTriggerIndex(self):
        l = open('./DES_GW_Website/trigger_list.txt','r')
        lines = l.readlines()
        l.close()
        a = open('./DES_GW_Website/trigger_list.txt','a')
        triggers = []
        for line in lines:
            triggers.append(line.split(' ')[0])
        if not self.trigger_id in np.unique(triggers):
            a.write(self.trigger_id+' '+self.outfolder+'\n')
        a.close()
        tp.make_index_page('./DES_GW_Website')
        return
    
    def updateWebpage(self):
        os.system('scp -r DES_GW_Website/* codemanager@desweb.fnal.gov:/des_web/www/html/desgw/')
        tp.makeNewPage(os.path.join(self.outfolder,self.trigger_id+'_trigger.html'),self.trigger_id,self.event_paramfile)
        os.system('scp -r '+os.path.join(self.outfolder,self.trigger_id+'_trigger.html')+' codemanager@desweb.fnal.gov:/des_web/www/html/desgw/Triggers/'+self.trigger_id+'/')
        return

if __name__ == "__main__":

    try:
        args = sys.argv[1:]
        opt,arg = getopt.getopt(
            args,"tp:tid:mjd:exp",
            longopts=["triggerpath=","triggerid=","mjd=","exposure_length="])
        
    except getopt.GetoptError as err:
        print str(err)
        print "Error : incorrect option or missing argument."
        print __doc__
        sys.exit(1)

    #Set defaults to config
    trigger_path = config.trigger_path
    trigger_id = config.trigger_id
    mjd = config.test_mjd
    exposure_length = config.exposure_length

    #Override defaults with command line arguments
    for o,a in opt:
        print 'Option'
        print o
        print a
        print '-----'
        if o in ["-tp","--triggerpath"]:
            trigger_path = str(a)
        elif o in ["-tid","--triggerid"]:
            trigger_id = str(a)
        elif o in ["-mjd","--mjd"]:
            mjd = float(a)
        elif o in ["-exp","--exposure_length"]:
            exposure_length = float(a)
        else:
            print "Warning: option", o, "with argument", a, "is not recognized"


    ####### BIG MONEY NO WHAMMIES ###############################################
    e = event(os.path.join(trigger_path,
                           trigger_id,
                           trigger_id+'_bayestar.fits.gz'),
              os.path.join(trigger_path,
                           trigger_id),
              trigger_id, mjd)
    e.getContours(exposure_length=exposure_length)
    e.makeJSON()
    e.updateTriggerIndex()
    e.updateWebpage()                                                                                                                                                                         
    e.send_nonurgent_Email()
    #############################################################################

    print 'Done'
