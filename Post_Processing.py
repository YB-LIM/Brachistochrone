"""
Author: Youngbin LIM
Contact: lyb0684@naver.com
Linkedin: https://www.linkedin.com/in/lyb0684/

This python script is used for post processing 

1. Open odb file and save report file for time vs x-displacement (U1.rpt)
2. Save animation in the path name Video_name = Video\Run_i (if i=1, avi is file saved in Video\Run_1)
3. Read U1.rpt to measure drop time, and save as Drop_Time.txt file
"""

from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=74.3541641235352, 
    height=118.391204833984)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from viewerModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
o1 = session.openOdb(name='Ball_Drop.odb', readOnly=False)
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
# Define file parameter
Run_num = 103
Video_name = 'Video\Run_'+str(int(Run_num))

# Write report file for U1

odb = session.odbs['Ball_Drop.odb']
xy_result = session.XYDataFromHistory(name='U1_History', odb=odb, 
    outputVariableName='Spatial displacement: U1 PI: BALL-1 Node 5930 in NSET BALL_CENTER_RP_1', 
    steps=('Drop', ), __linkedVpName__='Viewport: 1')
c1 = session.Curve(xyData=xy_result)
xyp = session.XYPlot('XYPlot-1')
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
chart.setValues(curvesToPlot=(c1, ), )
session.charts[chartName].autoColor(lines=True, symbols=True)
session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
x0 = session.xyDataObjects['U1_History']
session.xyReportOptions.setValues(numDigits=9)
session.writeXYReport(fileName='U1.rpt', appendMode=OFF, xyData=(x0, ))

# Decoration-Off
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triad=OFF, 
    legend=OFF, title=OFF, state=OFF, annotations=OFF, compass=OFF)
# For animation
odb = session.odbs['Ball_Drop.odb']
session.viewports['Viewport: 1'].setValues(displayedObject=odb)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    DEFORMED, ))
session.viewports['Viewport: 1'].enableMultipleColors()
session.viewports['Viewport: 1'].setColor(initialColor='#BDBDBD')
cmap = session.viewports['Viewport: 1'].colorMappings['Part instance']
session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
session.viewports['Viewport: 1'].disableMultipleColors()
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(pointElements=OFF)
# Set views
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=0 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=324.19, 
    farPlane=525.401, width=279.091, height=136.314, cameraPosition=(-80.2638, 
    78.0113, 384.862), cameraUpVector=(0.0523979, 0.791681, -0.608684), 
    cameraTarget=(86.6386, -42.446, 6.84688))
session.viewports['Viewport: 1'].view.setValues(nearPlane=329.061, 
    farPlane=521.372, width=283.284, height=138.362, cameraPosition=(-3.17078, 
    158.31, 376.615), cameraUpVector=(0.125009, 0.675358, -0.726818), 
    cameraTarget=(85.6178, -43.5093, 6.95609))
session.viewports['Viewport: 1'].view.setValues(nearPlane=328.975, 
    farPlane=521.458, width=266.218, height=130.026, viewOffsetX=4.67171, 
    viewOffsetY=-1.27782)
session.viewports['Viewport: 1'].view.setValues(nearPlane=345.329, 
    farPlane=508.088, width=279.452, height=136.49, cameraPosition=(54.0564, 
    141.51, 395.254), cameraUpVector=(0.0925354, 0.70865, -0.699466), 
    cameraTarget=(84.8288, -42.7765, 7.49921), viewOffsetX=4.90394, 
    viewOffsetY=-1.34134)
session.viewports['Viewport: 1'].view.setValues(nearPlane=338.555, 
    farPlane=514.862, width=291.458, height=142.354, viewOffsetX=9.8551, 
    viewOffsetY=-5.08274)
session.viewports['Viewport: 1'].view.setValues(nearPlane=346.669, 
    farPlane=508.431, width=298.443, height=145.766, cameraPosition=(69.2001, 
    129.162, 402.502), cameraUpVector=(0.0522136, 0.730952, -0.680428), 
    cameraTarget=(84.457, -42.7102, 8.1799), viewOffsetX=10.0913, 
    viewOffsetY=-5.20455)
session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)
session.viewports['Viewport: 1'].view.setProjection(projection=PERSPECTIVE)
session.viewports['Viewport: 1'].view.setValues(nearPlane=343.696, 
    farPlane=511.406, width=297.871, height=145.487, viewOffsetX=7.545, 
    viewOffsetY=-2.1763)
session.viewports['Viewport: 1'].view.setValues(nearPlane=345.905, 
    farPlane=511.542, width=299.786, height=146.422, cameraPosition=(108.256, 
    135.667, 400.542), cameraUpVector=(-0.015335, 0.708218, -0.705827), 
    cameraTarget=(96.3625, -47.974, 14.6227), viewOffsetX=7.59349, 
    viewOffsetY=-2.19029)
# Set views
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=0 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=348.708, 
    farPlane=558.49, width=267.038, height=130.427, viewOffsetX=-13.4346, 
    viewOffsetY=9.86168)
session.graphicsOptions.setValues(backgroundStyle=SOLID, 
    backgroundColor='#FFFFFF')
# Save animation
session.viewports['Viewport: 1'].animationController.setValues(
    animationType=TIME_HISTORY)
session.viewports['Viewport: 1'].animationController.play(duration=UNLIMITED)
session.imageAnimationOptions.setValues(vpDecorations=ON, vpBackground=OFF, 
    compass=OFF)
#: AVI Codec set to:None - 24 bits/pixel
session.aviOptions.setValues(compressionMethod=CODEC, 
    codecOptions='[12]:aaaaaaaabiaaaaaaaaaaaaaa')
session.imageAnimationOptions.setValues(vpDecorations=ON, vpBackground=OFF, 
    compass=OFF)
session.writeImageAnimation(fileName=Video_name, format=AVI, canvasObjects=(
    session.viewports['Viewport: 1'], ))
session.viewports['Viewport: 1'].animationController.stop()

import numpy as np
from decimal import *

# Get decending time
file=open("U1.rpt","r").readlines()
List_Len = len(file) -3

Time_vs_U1 = np.zeros((List_Len,2))
for i in range(len(file)-3):
    Lines = file[i+3].split()
    if Lines != []:
        Time_vs_U1[i,:] = [float(Lines[0]), float(Lines[1])]
    elif  Lines == []:
        break

Drop_Time = Time_vs_U1[Time_vs_U1[:,1].argmax(),0]
file=open("Drop_Time.txt","w")
file.write(str(Decimal(Drop_Time))[0:10])
file.close()
