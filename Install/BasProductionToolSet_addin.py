import arcpy
import pythonaddins

mxd = arcpy.mapping.MapDocument("CURRENT")  # for testing only
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]  # for testing only
mxdlyrs = arcpy.mapping.ListLayers(mxd, "*")  # for testing only





# This class will read the selected layer, store its value, and then zoom to the layer
class Zoom(object):
    # Values are store here
    def __init__(self):
        self.CurrentNumber = int()  # Current feature number
        self.CurrentLayer = str()  # Current Layer
        self.TotalNumber = int()  # Current total number of features
        self.XYValue = str()  # Value of XY column
        self.CommentValue = str()  # Value of comment column
        self.counter = int()  # Used to count the current feature number
        self.OID = int()  # add in more variables here


    # This zooms to first feature no matter if it is empty or not
    # This takes one variable, The number you want to go too
    def zoomtolayernumber(self, CurrentNumber):
        self.CurrentLayer = WorkingLayer.fc
        self.CurrentNumber = CurrentNumber
        arcpy.SelectLayerByAttribute_management(WorkingLayer.fc, "CLEAR_SELECTION")
        # Too See more layers add in layers here for the cursor
        cur = arcpy.da.SearchCursor(WorkingLayer.fc, ['OID@', 'SHAPE@', UserType.XYColumn, UserType.CommentColumn])
        myOIDs = [x[0] for x in arcpy.da.SearchCursor(WorkingLayer.fc, 'OID@')]
        TotalNum = len(myOIDs)
        # print(myOIDs[CurrentNumber])
        self.TotalNumber = TotalNum
        for row in cur:
            # print row[0]
            if row[0] == myOIDs[CurrentNumber]:
                df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]  # needs to be here for it to not error
                df.extent = row[1].extent  # Set dataframe extent to the extent of the feature
                df.scale = df.scale * 1.07  # add some space
                arcpy.RefreshActiveView()
                self.XYValue = row[2]
                self.CommentValue = row[3]
                self.OID = row[0]
                # add in more columns you want here
                Zoom.update(self)

                # test print #print WorkingLayer.object.CurrentNumber, WorkingLayer.object.CurrentLayer, WorkingLayer.object.TotalNumber, WorkingLayer.object.XYValue, WorkingLayer.object.CommentValue
                whereClause = "OBJECTID = " + str(self.OID)
                arcpy.SelectLayerByAttribute_management(WorkingLayer.fc, "NEW_SELECTION", whereClause)
                break

    # This will zoom to the first empty feature. It takes no inputs from the user
    def zoomtolayerattribute(self):
        self.CurrentLayer = WorkingLayer.fc
        arcpy.SelectLayerByAttribute_management(WorkingLayer.fc, "CLEAR_SELECTION")
        # Too See more layers add in layers here for the cursor
        cur = arcpy.da.SearchCursor(WorkingLayer.fc, ['OID@', 'SHAPE@', UserType.XYColumn, UserType.CommentColumn])
        count = int(arcpy.GetCount_management(WorkingLayer.fc).getOutput(0))
        self.TotalNumber = count
        counter = int()
        # Need to still get Current Number from this
        for row in cur:
            counter += 1  # increases the counter by one
            self.CurrentNumber = counter - 1  # Needs the minus 1 to be the actual spot
            # print row[2]
            if row[2] == "":
                df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]  # needs to be here for it to not error
                df.extent = row[1].extent  # Set dataframe extent to the extent of the feature
                df.scale = df.scale * 1.07  # add some space
                arcpy.RefreshActiveView()
                self.XYValue = row[2]
                self.CommentValue = row[3]
                Zoom.update(self)
                # print WorkingLayer.object.CurrentNumber, WorkingLayer.object.CurrentLayer, WorkingLayer.object.TotalNumber, WorkingLayer.object.XYValue, WorkingLayer.object.CommentValue
                self.OID = row[0]
                whereClause = "OBJECTID = " + str(self.OID)
                arcpy.SelectLayerByAttribute_management(WorkingLayer.fc, "NEW_SELECTION", whereClause)
                break

    # updates all the features boxes
    def update(self):
        CurrentFeatureNumber.refresh(self)
        CommentColumn.refresh(self)
        XYColumn.refresh(self)
        TotalFeatureCount.refresh(self)
        print"Everything is updated"

    # edits all the attributes with the values the user puts in
    def EditAttributes(self):
        arcpy.SelectLayerByAttribute_management(WorkingLayer.fc, "CLEAR_SELECTION")
        myOIDs = [x[0] for x in arcpy.da.SearchCursor(self.CurrentLayer, 'OID@')]
        edit = arcpy.da.Editor(WorkingLayer.layerworkspace)
        # Edit session is started without an undo/redo stack for versioned data
        #  (for second argument, use False for unversioned data)
        edit.startEditing(False, True)
        # Create update cursor
        with arcpy.da.UpdateCursor(self.CurrentLayer,
                                   ['OID@', 'SHAPE@', UserType.XYColumn, UserType.CommentColumn]) as cursor:
            # Start an edit operation
            edit.startOperation()
            for row in cursor:
                # Your Code
                if row[0] == myOIDs[self.CurrentNumber]:  # test the FEATURE field
                    row[2] = XYColumn.xyfield
                    row[3] = CommentColumn.comment  # set the FERRY field
                    print "YES"
                else:
                    print "NO"
                cursor.updateRow(row)  # commit the changes
        # Stop the edit operation.
        edit.stopOperation()
        # Stop the edit session and save the changes
        edit.stopEditing(True)

    # Select features that touch the current boundary
    def SelectNear(self):
        #if arcpy.Exists("selectedchanges"):
        #    arcpy.Delete_management("selectedchanges")
        arcpy.RefreshActiveView()
        self.CurrentLayer = WorkingLayer.fc
        #self.MultipleNumbers = arcpy.mapping.Layer(self.CurrentLayer)
        arcpy.SelectLayerByLocation_management(self.CurrentLayer, "BOUNDARY_TOUCHES", self.CurrentLayer, "",
                                               "ADD_TO_SELECTION", "NOT_INVERT")
        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]  # needs to be here for it to not error
        df.zoomToSelectedFeatures()  # Set dataframe extent to the extent of the feature
        df.scale = df.scale * 1.07  # add some space
        # Write the selected features to a new featureclass
            #arcpy.mapping.RemoveLayer(df, "selectedchanges")
        #arcpy.CopyFeatures_management(self.CurrentLayer, "selectedchanges")
        #arcpy.mapping.AddLayer(df, selectedchanges, "BOTTOM")

    # edit the features that are selected
    def EditSelectedAttributes(self):
        myOIDs = [x[0] for x in arcpy.da.SearchCursor("bas20_20400900000_changes_incplace", 'OID@')]
        print myOIDs
        arcpy.SelectLayerByAttribute_management(WorkingLayer.fc, "CLEAR_SELECTION")
        edit = arcpy.da.Editor(WorkingLayer.layerworkspace)
        # Edit session is started without an undo/redo stack for versioned data
        #  (for second argument, use False for unversioned data)
        edit.startEditing(False, True)
        # Create update cursor
        with arcpy.da.UpdateCursor(self.CurrentLayer,
                                   ['OID@', 'SHAPE@', UserType.XYColumn, UserType.CommentColumn]) as cursor:
            # Start an edit operation
            edit.startOperation()
            for x, y in [(x[0], y) for x in cursor for y in myOIDs]:
                #print (x, y)
                if x == y:
                    fid = x
                    with arcpy.da.UpdateCursor(self.CurrentLayer,
                                               ['OID@', 'SHAPE@', UserType.XYColumn, UserType.CommentColumn]) as cursor:
                        for row in cursor:
                            # Your Code
                            print row[0]
                            if row[0] == fid:  # test the FEATURE field
                                row[2] = XYColumn.xyfield
                                row[3] = CommentColumn.comment  # set the FERRY field
                                print "YES"
                            else:
                                print "NO"
                            cursor.updateRow(row)  # commit the changes

        # Stop the edit operation.
        edit.stopOperation()
        # Stop the edit session and save the changes
        edit.stopEditing(True)

# Go Back one feature, runs zoomtolayernumber()
class BackOne(object):
    """Implementation for BasProductionToolSet_addin.BackOne (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        WorkingLayer.object.zoomtolayernumber(WorkingLayer.object.CurrentNumber - 1)


# Go Back to first feature, runs zoomtolayernumber()
class BackToBeginning(object):
    """Implementation for BasProductionToolSet_addin.BackToBeginning (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        WorkingLayer.object.zoomtolayernumber(0)


# Display the Comment Column
class CommentColumn(object):
    """Implementation for BasProductionToolSet_addin.CommentColumn (ComboBox)"""

    def __init__(self):
        self.items = []
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        self.comment = str()

    def onSelChange(self, selection):
        pass

    def onEditChange(self, text):
        self.comment = text

    def onFocus(self, focused):
        pass

    def onEnter(self):
        print self.comment

    def refresh(self):
        self.items = []
        self.items.append(WorkingLayer.object.CommentValue)


# Display the Current Feature Number,  runs zoomtolayernumber() on number if you hit enter
class CurrentFeatureNumber(object):
    """Implementation for BasProductionToolSet_addin.CurrentFeatureNumber (ComboBox)"""

    def __init__(self):
        self.items = []
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        self.num = int()

    def onSelChange(self, selection):
        pass

    def onEditChange(self, text):
        self.num = text

    def onFocus(self, focused):
        pass

    def onEnter(self):
        WorkingLayer.object.zoomtolayernumber(int(CurrentFeatureNumber.num))

    def refresh(self):
        self.items = []
        self.items.append(WorkingLayer.object.CurrentNumber)


# Go forward to next empty feature, runs zoomtolayerattribute()
class ForwardEmpty(object):
    """Implementation for BasProductionToolSet_addin.ForwardEmpty (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        WorkingLayer.object.zoomtolayerattribute()


# Go forward one feature, runs zoomtolayernumber()
class ForwardOne(object):
    """Implementation for BasProductionToolSet_addin.ForwardOne (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        WorkingLayer.object.zoomtolayernumber(WorkingLayer.object.CurrentNumber + 1)


# Go to last feature, runs zoomtolayer()
class ForwardToEnd(object):
    """Implementation for BasProductionToolSet_addin.ForwardToEnd (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        WorkingLayer.object.zoomtolayernumber(WorkingLayer.object.TotalNumber - 1)


class SelectNear(object):
    """Implementation for BasProductionToolSet_addin.SelectNear (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        WorkingLayer.object.SelectNear()


# Button that triggers the editattributes function.
class Submit(object):
    """Implementation for BasProductionToolSet_addin.Submit (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        WorkingLayer.object.EditAttributes()

# Button that triggers the editselectedattributes function.
class SubmitSelected(object):
    """Implementation for BasProductionToolSet_addin.SubmitSelected (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        WorkingLayer.object.EditSelectedAttributes()


# displays total features
class TotalFeatureCount(object):
    """Implementation for BasProductionToolSet_addin.TotalFeatureCount (ComboBox)"""

    def __init__(self):
        self.items = ["item1", "item2"]
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'

    def onSelChange(self, selection):
        pass

    def onEditChange(self, text):
        pass

    def onFocus(self, focused):
        pass

    def onEnter(self):
        pass

    def refresh(self):
        self.items = []
        self.items.append(WorkingLayer.object.TotalNumber)


# makes the user select what they are doing and then will get the layers for it.
class UserType(object):
    """Implementation for BasProductionToolSet_addin.UserType (ComboBox)"""

    def __init__(self):
        self.items = ["Processing", "Verifying", "Digitizing", "Initial QC"]
        self.editable = True
        self.enabled = False
        self.dropdownWidth = 'Processing'
        self.width = 'Processing'
        self.CommentColumn = str()
        self.XYColumn = str()
        WorkingLayer.__init__()

    def onSelChange(self, selection):
        self.usertype = selection
        if selection == "Processing":
            self.CommentColumn = "P_Comments"
            self.XYColumn = "PROCESS"
            self.CommentColumn = "P_Comments"
            self.XYColumn = "PROCESS"
        elif selection == "Verifying":
            self.CommentColumn = "V_Comments"
            self.XYColumn = "VERIFY"
        elif selection == "Digitizing":
            self.CommentColumn = "D_Comments"
            self.XYColumn = "DIGITIZE"
        elif selection == "Initial QC":
            self.CommentColumn = "Q_Comments"
            self.XYColumn = "QC"
        # gets the value of the column and puts it into the table, Probably put somewhere else like onrefresh
        # UserType.value = arcpy.da.SearchCursor(WorkingLayer.fc, (UserType.column)).next()[WorkingLayer.rows]
        # self.items.append(value)
        # print self.CommentColumn

        WorkingLayer.object.zoomtolayerattribute()

    def onEditChange(self, text):
        pass

    def onFocus(self, focused):
        pass

    def onEnter(self):
        pass

    def refresh(self):
        pass


# Gathers the layers that have "change" in the name.
class WorkingLayer(object):
    """Implementation for BasProductionToolSet_addin.WorkingLayer (ComboBox)"""

    def __init__(self):
        self.items = []
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWWWWW'
        self.width = 'WWWWWWwwwww'
        self.layers = []  # variable for layers in the mxd
        self.count = int()  # variable to count the number of items in a layer
        self.fc = []  # variable to get the layers in the mxd
        self.object = None
        self.layerworkspace = []

    def onSelChange(self, selection):
        # makes fc the layer that gets selected
        self.fc = fc = arcpy.mapping.ListLayers(self.mxd, selection)[0]  # no idea but it needs the fc in here to work
        # create a new instances of Zoom called object that records all the fun stuff.
        self.object = Zoom()
        # print(fc)
        # print(fc.workspacePath)
        # gathers workspace for editing
        self.layerworkspace = fc.workspacePath
        WorkingLayer.items = [process.name for process in arcpy.ListFields(selection)]
        UserType.enabled = True  # Turns on UserType ComboBox

    def onEditChange(self, text):
        pass

    def onFocus(self, focused):
        # when combox is focused this will get the layers
        if focused:
            self.mxd = arcpy.mapping.MapDocument('current')
            layers = arcpy.mapping.ListLayers(self.mxd)
            self.items = []
            for layer in layers:  # only change layers will show up
                if "changes" in layer.name:
                    self.items.append(layer.name)

    def onEnter(self):
        pass

    def refresh(self):
        pass


# Displays the column user types one letter
class XYColumn(object):
    """Implementation for BasProductionToolSet_addin.XYColumn (ComboBox)"""

    def __init__(self):
        self.items = []
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        self.xyfield = str()

    def onSelChange(self, selection):
        pass

    def onEditChange(self, text):
        self.xyfield = text[0]  # Only get the first character
        print self.xyfield

    def onFocus(self, focused):
        pass

    def onEnter(self):
        pass

    def refresh(self):
        self.items = WorkingLayer.object.XYValue
