trigger_path  = '/data/des41.a/data/djbrout/maininjector/test-triggers'
exposure_length = 180. #sec

exposureList = [60,60]
filterList = ["i","z"]
tilingList = [0,1,2]

hex_centers = "all-sky-hexCenters.txt" 

nHexes = 10 # Top x # of hexes go into .json


####Only used for testing####
test_mjd = 55456.
trigger_id = 'M178857'
#############################

#############################
import os
os.environ['DESGW_DIR'] = "/data/des41.a/data/djbrout/osgsetup/eeups/fnaleups/Linux64/gw/v1.1"
os.environ['DESGW_DATA_DIR'] = os.path.join(os.environ['DESGW_DIR'],"data/")
#############################
