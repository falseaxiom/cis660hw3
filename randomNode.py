# randomNode.py
#   Produces random locations to be used with the Maya instancer node.

import sys
import random

import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

# Useful functions for declaring attributes as inputs or outputs.
def MAKE_INPUT(attr):
    attr.setKeyable(True)
    attr.setStorable(True)
    attr.setReadable(True)
    attr.setWritable(True)
def MAKE_OUTPUT(attr):
    attr.setKeyable(False)
    attr.setStorable(False)
    attr.setReadable(True)
    attr.setWritable(False)

# Define the name of the node
kPluginNodeTypeName = "randomNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
randomNodeId = OpenMaya.MTypeId(0x8704)

# Node definition
class randomNode(OpenMayaMPx.MPxNode):
    # Declare class variables:
    # TODO:: declare the input and output class variables
    #         i.e. inNumPoints = OpenMaya.MObject()

    inNumPoints = OpenMaya.MObject()

    inMinBounds = OpenMaya.MObject()
    minX = OpenMaya.MObject()
    minY = OpenMaya.MObject()
    minZ = OpenMaya.MObject()

    inMaxBounds = OpenMaya.MObject()
    maxX = OpenMaya.MObject()
    maxY = OpenMaya.MObject()
    maxZ = OpenMaya.MObject()

    outPoints = OpenMaya.MObject()
    
    # constructor
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    # compute
    def compute(self,plug,data):
        # TODO:: create the main functionality of the node. Your node should 
        #         take in three floats for max position (X,Y,Z), three floats 
        #         for min position (X,Y,Z), and the number of random points to
        #         be generated. Your node should output an MFnArrayAttrsData 
        #         object containing the random points. Consult the homework
        #         sheet for how to deal with creating the MFnArrayAttrsData.
        
        if plug == randomNode.outPoints:
            # create handles
            inNumPointsData = data.inputValue(randomNode.inNumPoints)
            inNumPointsValue = inNumPointsData.asLong()

            inMinBoundsData = data.inputValue(randomNode.inMinBounds)
            inMinBoundsValue = inMinBoundsData.asFloat3()

            inMaxBoundsData = data.inputValue(randomNode.inMaxBounds)
            inMaxBoundsValue = inMaxBoundsData.asFloat3()

            outPointsData = data.outputValue(randomNode.outPoints)
            outPointsAAD = OpenMaya.MFnArrayAttrsData()
            outPointsObject = outPointsAAD.create()

            # create position and id arrays
            positionArray = outPointsAAD.vectorArray("position")
            idArray = outPointsAAD.doubleArray("id")

            # fill in arrays
            for i in range(inNumPointsValue):
                x = random.uniform(inMinBoundsData[0], inMaxBoundsData[0])
                y = random.uniform(inMinBoundsData[1], inMaxBoundsData[1])
                z = random.uniform(inMinBoundsData[2], inMaxBoundsData[2])

                positionArray.append(OpenMaya.MVector(x,y,z))
                idArray.append(i)

        # set the output data handle
        outPointsData.setMObject(outPointsObject)

        data.setClean(plug)
    
# initializer
def nodeInitializer():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    # TODO:: initialize the input and output attributes. Be sure to use the 
    #         MAKE_INPUT and MAKE_OUTPUT functions.
    
    randomNode.inNumPoints = nAttr.create("inNumPoints", "inp", OpenMaya.MFnNumericData.kInt, 0.0)
    MAKE_INPUT(nAttr)

    randomNode.minX = nAttr.create("minX", "mnx", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.minY = nAttr.create("minY", "mny", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.minZ = nAttr.create("minZ", "mnz", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.inMinBounds = nAttr.create("inMinBounds", "imnb", randomNode.minX, randomNode.minY, randomNode.minZ)
    MAKE_INPUT(nAttr)

    randomNode.maxX = nAttr.create("maxX", "mxx", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.maxY = nAttr.create("maxY", "mxy", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.maxZ = nAttr.create("maxZ", "mxz", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.inMaxBounds = nAttr.create("inMaxBounds", "imxb", randomNode.maxX, randomNode.maxY, randomNode.maxZ)
    MAKE_INPUT(nAttr)

    randomNode.outPoints = tAttr.create("outPoints", "op", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)

    try:
        # TODO:: add the attributes to the node and set up the
        #         attributeAffects (addAttribute, and attributeAffects)
        
        randomNode.addAttribute(randomNode.inNumPoints)
        randomNode.addAttribute(randomNode.inMinBounds)
        randomNode.addAttribute(randomNode.inMaxBounds)
        randomNode.addAttribute(randomNode.outPoints)

        randomNode.attributeAffects(randomNode.inNumPoints, randomNode.outPoints)
        randomNode.attributeAffects(randomNode.inMinBounds, randomNode.outPoints)
        randomNode.attributeAffects(randomNode.inMaxBounds, randomNode.outPoints)

        print "Initialization!\n"

    except:
        sys.stderr.write( ("Failed to create attributes of %s node\n", kPluginNodeTypeName) )

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr( randomNode() )

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeTypeName, randomNodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( randomNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
