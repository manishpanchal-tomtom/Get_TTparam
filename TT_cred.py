########################################################################################
# ---------------This script helps to get TomTom related details, like MN-R server,  ###
# MN-R schema, Country code and epsg code for any given input polygon -------------- ###
# -----------------------------------------------------------------------------------###
# -----------------------------------------------------------------------------------###
# By Manish Panchal ####################################################################
########################################################################################

# Import libraries / dependencies
import geopandas as gpd
from sqlalchemy import create_engine
import os
from pyproj import CRS
from InputReader import InputReader

# File path
path = 'C:\\Manish\\Python\\PyCharmProject\\Get_cred\\Colombo_AOI.shp'

solite = InputReader(path)


def get_param(solite_file):
    # Process AOI input file
    solite_file['centre'] = solite_file.geometry.representative_point()
    pt = solite_file.centre[0].wkt

    # Connect global spatial file from db
    conn = create_engine('postgresql://grip_ro@weu-gdt-centerline-db:grip_ro@weu-gdt-centerline-db.postgres.database.azure.com:5432/gripdb')

    # Intersect query within input point & global data
    sql = "select * FROM grip.grip_global as gbl " \
          "where ST_Intersects(gbl.geom, ST_GeomFromText('" + pt + "',4326))"

    # Create dataframe from intersection
    gbl = gpd.read_postgis(sql, conn)
    utm = gbl['utm_zone'].iloc[0]

    z = (utm[:-1])
    if "S" in utm:
        s = True
    else:
        s = False

    # PYProj dict
    crs = CRS.from_dict({'proj': 'utm', 'zone': z, 'south': s})

    # Get all required details
    country = gbl['name'].iloc[0]
    ccode = gbl['isocode'].iloc[0]
    server = gbl['mnr_server'].iloc[0]
    schema = gbl['mnr_schema'].iloc[0]
    ep = crs.to_authority()[1]

    return country, ccode, server, schema, ep
