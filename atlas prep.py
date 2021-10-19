# from Samual Roberts, adapted to enable editor tracking by Wilfred Waters
# Use this script in prep for sharing on atlas (Adds global Ids & Enables editor tracking)
print("Importing Arcpy...")
import arcpy, os

# currently it uses a .SDE file stored on C:\ but you can also specify a UNC path
SDEpath = r"C:\dev\SDEs\GBR_00000000_FuseDemo Creator.sde"
arcpy.env.workspace = SDEpath

print("Preparing for sharing...")
print("WARNING: Will fail if ArcPro is open")

for fds in arcpy.ListDatasets("", "feature") + [""]:
    for fc in arcpy.ListFeatureClasses():
        FCpath = os.path.join(SDEpath, fc)
        fc_properties = arcpy.da.Describe(fc)

        try:
            if fc_properties["hasGlobalID"]:
                print(fc + " already has GUID")
            else:
                arcpy.management.AddGlobalIDs(FCpath)
                print("Added GUID for: " + fc)
        except Exception as ex:
            print("Failed to add global IDs for " + fc)
            pass

        try:
            if fc_properties["editorTrackingEnabled"]:
                print(fc + " already has editor tracking enabled")
            else:
                arcpy.EnableEditorTracking_management(fc, "ET_CREATOR", "ET_CREATED", "ET_EDITOR", "ET_EDITED", "ADD_FIELDS", "UTC")
                print("Enabled editor tracking on " + fc)
        except Exception as ex:
            print("Failed to enable editor tracking for " + fc)
            pass

print("Done!")