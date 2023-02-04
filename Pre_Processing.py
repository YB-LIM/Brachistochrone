"""
Author: Youngbin LIM
Contact: lyb0684@naver.com
Linkedin: https://www.linkedin.com/in/lyb0684/

This python script generate Abaqus input file for ball drop simulation
The curve is devided into 6-segment with uniform x-distance
5 Y-coordinate values are to be optimized 

Start   : (0.0,0.0)
point_1 : (50*pi/6, y_1)
point_2 : (2*50*pi/6, y_2)
point_3 : (3*50*pi/6, y_3)
point_4 : (4*50*pi/6, y_4)
point_5 : (5*50*pi/6, y_5)
End     : (50*pi, -100.0)

Parameter description:
s1 (0.0~1.0): determines a y-coordinate of first point
s2 (0.0~1.0): determines a y-coordinate of second point
s3 (0.0~1.0): determines a y-coordinate of third point
s4 (0.0~1.0): determines a y-coordinate of forth point
s5 (0.0~1.0): determines a y-coordinate of fifth point

if si = 0.0, y_coordinate of i_th point is equal to the previous point (y_i=y_i-1)
if si = 1.0, y_coordinate of i_th point is equal to the linear extrapolation of i-2 and i-1 
i.e., y_i = y_i-1 + (y_i-1 - y_i-2)*si

Conversion from y to s enables generation of monotonically decreasing curve
"""
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=74.3541641235352, 
    height=118.391204833984)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
import numpy as np
from scipy import interpolate
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
Mdb()
session.viewports['Viewport: 1'].setValues(displayedObject=None)
##############################
#### Parameter definition ####
##############################
s1 = 0.2
s2 = 0.326
s3 = 0.579
s4 = 0.8
s5 = 0.674
# X coordinates
X_coord = np.linspace(0, np.pi*50., endpoint=True, num=7)
# Y coordinates
s = [s1, s2, s3, s4, s5]
Y_coord = np.linspace(0, -1, endpoint=True, num=7)
Y_coord[1] = 0.1
for i in range(len(Y_coord)-2):
    Y_coord[i+2] = Y_coord[i+1] + (Y_coord[i+1] - Y_coord[i])*s[i]

# Scale Y values
Y_coord = Y_coord/max(Y_coord)*-100.
# PchipInterolator
X_interp = np.linspace(0.0, np.pi*50., num=50, endpoint=True);
Spline = interpolate.PchipInterpolator(X_coord, Y_coord);
Y_interp = Spline(X_interp)
# Combine X&Y coordinate
Coord_curve = np.stack((X_interp,Y_interp), axis=1)
# Add guide part of the track
Guide = np.array([[0, 20], [0, 15], [0, 10], [0, 5], [0, 2.5]]) 
Coord = np.concatenate((Guide, Coord_curve), axis=0)

##############################
####      Draw curve 1    ####
##############################
# Draw Curve to be optimized
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.Spline(points=Coord)
s.offset(distance=10.1, objectList=(g[2], ), side=RIGHT)
s.Line(point1=(np.pi*50.,-100.), point2=(np.pi*50.+5.,-100.))
s.Line(point1=(np.pi*50.+5.,-100.), point2=(np.pi*50.+5.,-110.1))
s.Line(point1=(np.pi*50.+5.,-110.1), point2=(np.pi*50.,-110.1))
p = mdb.models['Model-1'].Part(name='Track', dimensionality=THREE_D, 
    type=DISCRETE_RIGID_SURFACE)
p = mdb.models['Model-1'].parts['Track']
p.BaseShellExtrude(sketch=s, depth=20.0)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Track']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']

##############################
####      Draw curve 2    ####
##############################
# Draw Cycloid curve
theta = np.linspace(0., np.pi, endpoint=True, num=20)
X_coord_Cycl = 50*(theta - np.sin(theta))
Y_coord_Cycl = -50*(1 - np.cos(theta))
Coord_curve_2 = np.stack((X_coord_Cycl,Y_coord_Cycl), axis=1)
# Add guide part of the track
Guide = np.array([[0, 20], [0, 15], [0, 10], [0, 5], [0, 2.5]]) 
Coord = np.concatenate((Guide, Coord_curve_2), axis=0)
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.Spline(points=Coord)
s.offset(distance=10.1, objectList=(g[2], ), side=RIGHT)
s.Line(point1=(np.pi*50.,-100.), point2=(np.pi*50.+5.,-100.))
s.Line(point1=(np.pi*50.+5.,-100.), point2=(np.pi*50.+5.,-110.1))
s.Line(point1=(np.pi*50.+5.,-110.1), point2=(np.pi*50.,-110.1))
p = mdb.models['Model-1'].Part(name='Track_Cycloid', dimensionality=THREE_D, 
    type=DISCRETE_RIGID_SURFACE)
p = mdb.models['Model-1'].parts['Track_Cycloid']
p.BaseShellExtrude(sketch=s, depth=20.0)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Track']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']

##############################
####     Define ball      ####
##############################

s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
s.FixedConstraint(entity=g[2])
session.viewports['Viewport: 1'].view.setValues(nearPlane=176.784, 
    farPlane=200.34, width=72.5622, height=35.4409, cameraPosition=(5.1377, 
    0.177156, 188.562), cameraTarget=(5.1377, 0.177156, 0))
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, 5.0))
s.CoincidentConstraint(entity1=v[1], entity2=g[2], addUndoState=False)
s.CoincidentConstraint(entity1=v[0], entity2=g[2], addUndoState=False)
s.autoTrimCurve(curve1=g[3], point1=(-4.98195838928223, -0.0175748467445374))
s.Line(point1=(0.0, 5.0), point2=(0.0, -5.0))
s.VerticalConstraint(entity=g[5], addUndoState=False)
s.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
p = mdb.models['Model-1'].Part(name='Ball', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Ball']
p.BaseSolidRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Ball']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
p = mdb.models['Model-1'].parts['Ball']
p.ReferencePoint(point=(0.0, 0.0, 0.0))
mdb.models['Model-1'].parts['Ball'].features.changeKey(fromName='RP', 
    toName='Ball_Center')
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
mdb.models['Model-1'].Material(name='Steel')
mdb.models['Model-1'].materials['Steel'].Density(table=((7.85e-09, ), ))
mdb.models['Model-1'].materials['Steel'].Elastic(table=((200000.0, 0.3), ))
mdb.models['Model-1'].HomogeneousSolidSection(name='Ball', material='Steel', 
    thickness=None)
p = mdb.models['Model-1'].parts['Ball']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region = p.Set(cells=cells, name='Set-1')
p = mdb.models['Model-1'].parts['Ball']
p.SectionAssignment(region=region, sectionName='Ball', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
    
##############################
####   Create assembly    ####
##############################

a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['Ball']
a.Instance(name='Ball-1', part=p, dependent=ON)
p = mdb.models['Model-1'].parts['Track']
a.Instance(name='Track-1', part=p, dependent=ON)
# Move the ball to starting position
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Ball-1', ), vector=(-5.0, 5.0, 10.0))

#For cycloid
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Track_Cycloid']
a.Instance(name='Track_Cycloid-1', part=p, dependent=ON)
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Track_Cycloid-1', ), vector=(0.0, 0.0, -50.0))
p = mdb.models['Model-1'].parts['Ball']
a.Instance(name='Ball-2', part=p, dependent=ON)
# Move the ball to starting position
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Ball-2', ), vector=(-5.0, 5.0, -40.0))

# Generate mesh on ball
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=ON)
p = mdb.models['Model-1'].parts['Ball']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
    engineeringFeatures=OFF, mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
p = mdb.models['Model-1'].parts['Ball']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
elemType1 = mesh.ElemType(elemCode=C3D20R)
elemType2 = mesh.ElemType(elemCode=C3D15)
elemType3 = mesh.ElemType(elemCode=C3D10)
p = mdb.models['Model-1'].parts['Ball']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))
p = mdb.models['Model-1'].parts['Ball']
p.seedPart(size=1.1, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['Ball']
p.generateMesh()
# Generate mesh on track
p = mdb.models['Model-1'].parts['Track']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Track']
e = p.edges
pickedEdges = e.getSequenceFromMask(mask=('[#1ffff ]', ), )
p.seedEdgeBySize(edges=pickedEdges, size=5.0, deviationFactor=0.1, 
    constraint=FINER)
p = mdb.models['Model-1'].parts['Track']
p.generateMesh()
# Generate mesh on track_Cycloid
p = mdb.models['Model-1'].parts['Track_Cycloid']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Track_Cycloid']
e = p.edges
pickedEdges = e.getSequenceFromMask(mask=('[#1ffff ]', ), )
p.seedEdgeBySize(edges=pickedEdges, size=5.0, deviationFactor=0.1, 
    constraint=FINER)
p = mdb.models['Model-1'].parts['Track_Cycloid']
p.generateMesh()

# Define contact
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF, 
    interactions=ON, constraints=ON, connectors=ON, engineeringFeatures=ON)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=OFF)
mdb.models['Model-1'].ContactProperty('IntProp-1')
mdb.models['Model-1'].interactionProperties['IntProp-1'].TangentialBehavior(
    formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
    pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
    0.0, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
    fraction=0.005, elasticSlipStiffness=None)
mdb.models['Model-1'].interactionProperties['IntProp-1'].NormalBehavior(
    pressureOverclosure=HARD, allowSeparation=ON, 
    constraintEnforcementMethod=DEFAULT)
#: The interaction property "IntProp-1" has been created.
mdb.models['Model-1'].ContactExp(name='Gencont', createStepName='Initial')
mdb.models['Model-1'].interactions['Gencont'].includedPairs.setValuesInStep(
    stepName='Initial', useAllstar=ON)
mdb.models['Model-1'].interactions['Gencont'].contactPropertyAssignments.appendInStep(
    stepName='Initial', assignments=((GLOBAL, SELF, 'IntProp-1'), ))
#: The interaction "Gencont" has been created.
# B.C for ball center
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, interactions=OFF, constraints=OFF, 
    engineeringFeatures=OFF)
a = mdb.models['Model-1'].rootAssembly
r1 = a.instances['Ball-1'].referencePoints
refPoints1=(r1[2], )
region = a.Set(referencePoints=refPoints1, name='Ball_Center_RP_1')
mdb.models['Model-1'].DisplacementBC(name='XY_plane_Motion', 
    createStepName='Initial', region=region, u1=UNSET, u2=UNSET, u3=SET, 
    ur1=SET, ur2=SET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, 
    fieldName='', localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, interactions=OFF, constraints=OFF, 
    engineeringFeatures=OFF)
a = mdb.models['Model-1'].rootAssembly
r1 = a.instances['Ball-2'].referencePoints
refPoints1=(r1[2], )
region = a.Set(referencePoints=refPoints1, name='Ball_Center_RP_2')
mdb.models['Model-1'].DisplacementBC(name='XY_plane_Motion_2', 
    createStepName='Initial', region=region, u1=UNSET, u2=UNSET, u3=SET, 
    ur1=SET, ur2=SET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, 
    fieldName='', localCsys=None)

# B.C for track
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p = mdb.models['Model-1'].parts['Track']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Track']
v, e, d, n = p.vertices, p.edges, p.datums, p.nodes
p.ReferencePoint(point=p.InterestingPoint(edge=e[3], rule=MIDDLE))
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
r1 = a.instances['Track-1'].referencePoints
refPoints1=(r1[3], )
region = a.Set(referencePoints=refPoints1, name='Track_RP')
mdb.models['Model-1'].EncastreBC(name='Track_Fix', createStepName='Initial', 
    region=region, localCsys=None)

# B.C for track_Cycloid
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p = mdb.models['Model-1'].parts['Track_Cycloid']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Track_Cycloid']
v, e, d, n = p.vertices, p.edges, p.datums, p.nodes
p.ReferencePoint(point=p.InterestingPoint(edge=e[3], rule=MIDDLE))
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
r1 = a.instances['Track_Cycloid-1'].referencePoints
refPoints1=(r1[3], )
region = a.Set(referencePoints=refPoints1, name='Track_Cycloid_RP')
mdb.models['Model-1'].EncastreBC(name='Track_Cycloid_Fix', createStepName='Initial', 
    region=region, localCsys=None)

# Create step
mdb.models['Model-1'].ExplicitDynamicsStep(name='Drop', previous='Initial', 
    timePeriod=0.3, timeIncrementationMethod=FIXED_USER_DEFINED_INC, 
    userDefinedInc=5e-05, improvedDtMethod=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Drop')

#Define gravity load
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
mdb.models['Model-1'].Gravity(name='Gravity', createStepName='Drop', 
    comp2=-9800.0, distributionType=UNIFORM, field='')

#Rigidbody constraint for ball and RP
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF, adaptiveMeshConstraints=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
    constraints=ON, connectors=ON, engineeringFeatures=ON, 
    adaptiveMeshConstraints=OFF)
a = mdb.models['Model-1'].rootAssembly
region2=a.instances['Ball-1'].sets['Set-1']
a = mdb.models['Model-1'].rootAssembly
region1=a.sets['Ball_Center_RP_1']
mdb.models['Model-1'].RigidBody(name='Rigidbody_1', refPointRegion=region1, 
    bodyRegion=region2)

#Rigidbody constraint for ball and RP
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF, adaptiveMeshConstraints=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
    constraints=ON, connectors=ON, engineeringFeatures=ON, 
    adaptiveMeshConstraints=OFF)
a = mdb.models['Model-1'].rootAssembly
region4=a.instances['Ball-2'].sets['Set-1']
a = mdb.models['Model-1'].rootAssembly
region3=a.sets['Ball_Center_RP_2']
mdb.models['Model-1'].RigidBody(name='Rigidbody_2', refPointRegion=region3, 
    bodyRegion=region4)

#Modify output request
session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=OFF, 
    constraints=OFF, connectors=OFF, engineeringFeatures=OFF, 
    adaptiveMeshConstraints=ON)
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'U', 'UT'), numIntervals=50, timeMarks=OFF)
regionDef=mdb.models['Model-1'].rootAssembly.sets['Ball_Center_RP_1']
mdb.models['Model-1'].HistoryOutputRequest(name='H-Output-2', 
    createStepName='Drop', variables=('U1', ), frequency=1, region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)

#Write input file
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=OFF)
mdb.Job(name='Ball_Drop', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, numThreadsPerMpiProcess=1, 
    multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)
mdb.jobs['Ball_Drop'].writeInput(consistencyChecking=OFF)
#: The job input file has been written to "Ball_Drop.inp".
