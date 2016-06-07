import os
import numpy as np
import datetime
import pytz

def mjd_to_datetime(mjd):
    mjd_epoch = datetime.datetime(1858, 11, 17, tzinfo=pytz.utc)
    d = mjd_epoch + datetime.timedelta(mjd)
    return d

def makeNewPage(outfilename,trigger_id,event_paramfile):

	event_params = np.load(event_paramfile)

	d = mjd_to_datetime(float(str(event_params['MJD'])))

	html = 	'<!DOCTYPE HTML>\
		<html>\
	        <head>\
	                <title>DES GW Trigger '+str(trigger_id)+'</title>\
	                <meta charset="utf-8" />\
	                <meta name="viewport" content="width=device-width, initial-scale=1" />\
	                <link rel="stylesheet" href="../../assets/css/main.css" />\
	        </head>\
	        <body id="top">\
	                <!-- Header -->\
	                        <header id="header">\
	                                <div class="content">\
	                                        <h1><a href="https://gracedb.ligo.org/events/'+str(trigger_id)+'">DES GW Trigger '+str(trigger_id)+'</a></h1>\
	                                        <p>Probability of Detection: '+str(round(float(str(event_params['integrated_prob'])),6))+'<br />\
	                                        <p>'+str(d.strftime('%H:%M:%S \t %b %d, %Y'))+'</p>\
	                                        <p>MJD: '+str(event_params['MJD'])+'<br />\
	                                        <p># Hexes: '+str(event_params['nHexes'])+'<br />\
	                                        <p><ul class="actions">\
												<li><a href="'+str(trigger_id)+'_'+str(event_params['nHexes'])+'Hexes.json" download class="button special icon fa-download">.json</a></li>\
											</ul><br />\
									</div>\
	                                <div class="5u"><div class="image fit"><a href="images/'+str(trigger_id)+'_sourceProbxLIGO.png"><img src="images/'+str(trigger_id)+'_sourceProbxLIGO.png" alt=""  /></a></div></div>\
	                        </header>\
	                <section>\
	                <section id="one" class="wrapper style2 special">\
	                <h4></h4>\
						<div class="table-wrapper">\
							<table class="alt">\
								<tbody>\
									<tr>\
										<td>FAR</td>\
										<td>False Alarm Rate </td>\
										<td>'+str(event_params['FAR'])+'</td>\
									</tr>\
									<tr>\
										<td>ETA</td>\
										<td>Estimated ratio of reduced mass to total mass</td>\
										<td>'+str(event_params['ETA'])+'</td>\
									</tr>\
									<tr>\
										<td>Chirp Mass</td>\
										<td>Estimated CBC chirp mass</td>\
										<td>'+str(event_params['ChirpMass'])+'</td>\
									</tr>\
									<tr>\
										<td>M1</td>\
										<td>Estimated Merger Mass Obj #1</td>\
										<td>'+str(event_params['M1'])+'</td>\
									</tr>\
									<tr>\
										<td>M2</td>\
										<td>Estimated Merger Mass Obj #2</td>\
										<td>'+str(event_params['M2'])+'</td>\
									</tr>\
									<tr>\
										<td>Max Dist</td>\
										<td>Estimated maximum distance for CBC event</td>\
										<td>'+str(event_params['MaxDistance'])+'</td>\
									</tr>\
								</tbody>\
							</table>\
						</div>\
					</section>\
					</section>\
	                <!-- Two -->\
	                        <section id="two" class="wrapper">\
	                                <div class="inner alt">\
	                                        <section class="special">\
	                                                <div class="12u"><div class="image fit"><a href="images/'+str(trigger_id)+'_LIGO.png"><img src="images/'+str(trigger_id)+'_LIGO.png" alt="" /></a></div></div>\
	                                                <div class="content">\
	                                                        <h3>LIGO Probability Map</h3>\
	                                                </div>\
	                                        </section>\
	                                        <section class="special">\
	                                                <div class="12u"><div class="image fit"><a href="images/'+str(trigger_id)+'_sourceProbMap.png"><img src="images/'+str(trigger_id)+'_sourceProbMap.png" alt="" /></a></div></div>\
	                                                <div class="content">\
	                                                        <h3>Source Probability Map</h3>\
	                                                </div>\
	                                        </section>\
	                                        <section class="special">\
	                                                <div class="12u"><div class="image fit"><a href="images/'+str(trigger_id)+'_limitingMagMap.png"><img src="images/'+str(trigger_id)+'_limitingMagMap.png" alt="" /></a></div></div>\
	                                                <div class="content">\
	                                                        <h3>Limiting Magnitude Map</h3>\
	                                                </div>\
	                                        </section>\
	                                        <section class="special">\
	                                                <div class="12u"><div class="image fit"><a href="images/'+str(trigger_id)+'_sourceProbxLIGO.png"><img src="images/'+str(trigger_id)+'_sourceProbxLIGO.png" alt="" /></a></div></div>\
	                                                <div class="content">\
	                                                        <h3>DES Source Prob x LIGO Detection Prob</h3>\
	                                                </div>\
	                                        </section>\
	                                </div>\
	                        </section>\
	                <!-- Three -->\
	                        <section id="three" class="wrapper style2 special">\
	                                 <!-- <header class="major">\
	                                        <h2>Magna leo sapien gravida</h2>\
	                                        <p>Gravida at leo elementum elit fusce accumsan dui libero, quis vehicula<br />\
	                                        lectus ultricies eu. In convallis amet leo sapien iaculis efficitur.</p>\
	                                </header> -->\
	                                <ul class="actions">\
	                                        <li><a href="../../" class="button special icon fa-download">View All Triggers</a></li>\
	                                        <li><a href="mailto:dbrout@physics.upenn.edu?subject=DESGW Trigger '+str(trigger_id)+' Issue Report&body=Please address issue related to trigger '+str(trigger_id)+'." class="button">Report Issue</a></li>\
	                                </ul>\
	                        </section>\
	                <!-- Scripts -->\
	                        <script src="assets/js/jquery.min.js"></script>\
	                        <script src="assets/js/jquery.scrolly.min.js"></script>\
	                        <script src="assets/js/skel.min.js"></script>\
	                        <script src="assets/js/util.js"></script>\
	                        <script src="assets/js/main.js"></script>\
	        </body>\
	</html>\
	'

	a = open(outfilename,'w')
	a.write(html)
	a.close()



def make_index_page(webpage_dir):
	tt = open(os.path.join(webpage_dir,'trigger_list.txt'),'r')
	lines = tt.readlines()
	tt.close()
	triggers = ''
	isFirst = True
	firstTrigger = ''
	for line in reversed(lines):
            print
            trig, outfolder = line.split(' ')
            if isFirst:
                firstTrigger = trig
                isFirst = False
            outfolder = outfolder.strip('\n')
            params = np.load(os.path.join(outfolder,trig+'_params.npz'))
            
            d = mjd_to_datetime(float(str(params['MJD'])))
            

            if float(str(params['integrated_prob'])) > .1:
                triggers += '<tr>\
						<td><a href="Triggers/'+trig+'/'+trig+'_trigger.html" ><span class="label">'+trig+'</span></a></td>\
						<td bgcolor="green"><a href="Triggers/'+trig+'/'+trig+'_trigger.html" ><span class="label">'+str(round(float(str(params['integrated_prob'])),6))+'</span></a></td>\
						<td><a href="Triggers/'+trig+'/'+trig+'_trigger.html" ><span class="label">'+str(params['FAR'])+'</span></a></td>\
						<td><a href="Triggers/'+trig+'/'+trig+'_trigger.html" ><span class="label">'+str(params['ChirpMass'])+'</span></a></td>\
						<td><a href="Triggers/'+trig+'/'+trig+'_trigger.html" ><span class="label">'+str(params['MaxDistance'])+'</span></a></td>\
						<td><a href="Triggers/'+trig+'/'+trig+'_trigger.html" ><span class="label">'+str(params['MJD'])+'</span></a></td>\
						<td><a href="Triggers/'+trig+'/'+trig+'_trigger.html" ><span class="label">'+str(d.strftime('%H:%M:%S \t %b %d, %Y'))+'</span></a></td>\
					</tr>'
            else:	
                triggers += '<tr>\
						<td><a href="Triggers/'+trig+'/'+trig+'_trigger.html" ><span class="label">'+trig+'</span></a></td>\
						<td><a href="Triggers/'+trig+'/'+trig+'_trigger.html" ><span class="label">'+str(round(float(str(params['integrated_prob'])),6))+'</span></a></td>\
						<td><a href="Triggers/'+trig+'/'+trig+'_trigger.html" ><span class="label">'+str(params['FAR'])+'</span></a></td>\
						<td><a href="Triggers/'+trig+'/'+trig+'_trigger.html" ><span class="label">'+str(params['ChirpMass'])+'</span></a></td>\
						<td><a href="Triggers/'+trig+'/'+trig+'_trigger.html" ><span class="label">'+str(params['MaxDistance'])+'</span></a></td>\
						<td><a href="Triggers/'+trig+'/'+trig+'_trigger.html" ><span class="label">'+str(params['MJD'])+'</span></a></td>\
						<td><a href="Triggers/'+trig+'/'+trig+'_trigger.html" ><span class="label">'+str(d.strftime('%H:%M:%S \t %b %d, %Y'))+'</span></a></td>\
					</tr>'

            html = '<!DOCTYPE HTML>\
	<html>\
	<head>\
		<title>DES GW Trigger Index</title>\
		<meta charset="utf-8" />\
		<meta name="viewport" content="width=device-width, initial-scale=1" />\
		<link rel="stylesheet" href="assets/css/main.css" />\
	</head>\
	<body id="top">\
		<!-- Header -->\
			<header id="header">\
				<div class="content">\
					<h1>DES GW Trigger Index</h1>\
					<ul class="actions">\
						<li><a href="Triggers/'+firstTrigger+'/'+firstTrigger+'_trigger.html" class="button icon fa-chevron-down scrolly">Most Recent</a></li>\
					</ul>\
				</div>\
			</header>\
		<!-- Two -->\
		<section>\
		<div class="table-wrapper">\
							<table>\
							</table>\
			</div>\
		</section>\
		<section>\
			<div class="table-wrapper">\
							<table>\
								<thead>\
									<tr>\
										<th>ID</th>\
										<th>Prob</th>\
										<th>FAR</th>\
										<th>ChirpMass</th>\
										<th>MaxDist</th>\
										<th>MJD</th>\
										<th>Date</th>\
									</tr>\
								</thead>\
								<tbody>\
								'+triggers+'\
								</tbody>\
							</table>\
			</div>\
		</section>\
		<!-- Three -->\
			<section id="three" class="wrapper style2 special">\
				<ul class="actions">\
					<li><a href="#" class="button special icon fa-download">View All Triggers</a></li>\
					<li><a href="mailto:dbrout@physics.upenn.edu?subject=DESGW Index Page Issue Report&body=Please address issue related to DESGW Index Page." class="button">Report Issue</a></li>\
				</ul>\
			</section>\
		<!-- Scripts -->\
			<script src="assets/js/jquery.min.js"></script>\
			<script src="assets/js/jquery.scrolly.min.js"></script>\
			<script src="assets/js/skel.min.js"></script>\
			<script src="assets/js/util.js"></script>\
			<script src="assets/js/main.js"></script>\
	</body>\
	</html>'


	a = open(os.path.join(webpage_dir,'index.html'),'w')
	a.write(html)
	a.close()








