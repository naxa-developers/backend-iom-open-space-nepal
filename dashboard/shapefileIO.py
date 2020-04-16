from osgeo import ogr, osr
import os
import tempfile
import zipfile
import traceback
import shutil
import os.path
from dashboard import utils
from django.contrib.gis.geos import GEOSGeometry
from core.models import OpenSpace, CommunitySpace


def importData(shapefile,  oid=None, cid=None, from_openspace=True, data=[], characterEncoding=None):
    fd, fname = tempfile.mkstemp(suffix=".zip")
    os.close(fd)

    f = open(fname, "wb")
    for chunk in shapefile.chunks():
        f.write(chunk)
    f.close()

    if not zipfile.is_zipfile(fname):
        os.remove(fname)
        return "Not a valid zip archive."

    zip = zipfile.ZipFile(fname)

    required_suffixes = [".shp", ".shx", ".dbf", ".prj"]
    hasSuffix = {}
    for suffix in required_suffixes:
        hasSuffix[suffix] = False

    for info in zip.infolist():
        extension = os.path.splitext(info.filename)[1].lower()
        if extension in required_suffixes:
            hasSuffix[extension] = True
        else:
            print("Extraneous file: " + info.filename)

    for suffix in required_suffixes:
        if not hasSuffix[suffix]:
            zip.close()
            os.remove(fname)
            return "Archive missing required " + suffix + " file."

    zip = zipfile.ZipFile(fname)
    shapefileName = None
    dirname = tempfile.mkdtemp()
    for info in zip.infolist():
        if info.filename.endswith(".shp"):
            shapefileName = info.filename

        dstFile = os.path.join(dirname, info.filename)
        f = open(dstFile, "wb")
        f.write(zip.read(info.filename))
        f.close()
    zip.close()

    try:
        datasource = ogr.Open(os.path.join(dirname, shapefileName))
        layer = datasource.GetLayer(0)
        shapefileOK = True
    except:
        traceback.print_exc()
        shapefileOK = False

    if not shapefileOK:
        os.remove(fname)
        shutil.rmtree(dirname)
        return "Not a valid shapefile."

    # Import the data from the opened shapefile.

    geometryType = layer.GetLayerDefn().GetGeomType()
    geometryName = utils.ogrTypeToGeometryName(geometryType)
    srcSpatialRef = layer.GetSpatialRef()
    dstSpatialRef = osr.SpatialReference()
    dstSpatialRef.ImportFromEPSG(4326)

    coordTransform = osr.CoordinateTransformation(srcSpatialRef,
                                                  dstSpatialRef)

    for i in range(layer.GetFeatureCount()):
        srcFeature = layer.GetFeature(i)
        srcGeometry = srcFeature.GetGeometryRef()
        srcGeometry.Transform(coordTransform)
        geometry = GEOSGeometry(srcGeometry.ExportToWkt())
        geometry = utils.wrapGEOSGeometry(geometry)
        geometryField = utils.calcGeometryField(geometryName)
        # print('check keys', srcFeature.keys())
        if from_openspace:
            try:
                feature_oid = srcFeature.GetField('OID_')
            except:
                raise ValueError('OID does not exist in shape file.')
        else:
            try:
                feature_cid = srcFeature.GetField('CID')
            except:
                raise ValueError('CID does not exist in shape file.')

        if oid and oid == feature_oid:
            open_space = OpenSpace.objects.get(oid=feature_oid)
            open_space.polygons = geometry
            open_space.save()
            return
        elif cid and cid == feature_cid:
            open_space = CommunitySpace.objects.get(cid=feature_cid)
            open_space.polygons = geometry
            open_space.save()
            return
        if from_openspace:
            print('geommmmmmmm', geometry)
            if feature_oid in data:
                print('feature_oid', feature_oid)
                obj = OpenSpace.objects.get(oid=feature_oid)
                obj.polygons = geometry

                obj.save()
        else:
            if feature_cid in data:
                obj = CommunitySpace.objects.get(cid=feature_cid)
                obj.polygons = geometry
                obj.save()



