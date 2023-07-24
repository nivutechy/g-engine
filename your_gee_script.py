import ee

# Initialize the Earth Engine API
ee.Initialize()

def export_satellite_image(bbox, output_filename):
    # Convert the bounding box coordinates to a geometry object
    bbox_geometry = ee.Geometry.Rectangle(bbox)

    # Load Landsat 8 imagery collection
    landsat = ee.ImageCollection('LANDSAT/LC08/C01/T1')

    # Filter the imagery collection by the bounding box and date range (if needed)
    # Example date range filter:
    # landsat = landsat.filterDate('YYYY-MM-DD', 'YYYY-MM-DD')

    # Filter the imagery collection based on the bounding box
    landsat = landsat.filterBounds(bbox_geometry)

    # Select the latest image from the filtered collection (or any other specific image selection criteria)
    image = ee.Image(landsat.sort('system:time_start', False).first())

    # Select the bands you want to export
    bands = ['B4', 'B3', 'B2']  # Example: Red, Green, and Blue bands

    # Clip the image to the bounding box
    clipped_image = image.clip(bbox_geometry)

    # Export the image as a GeoTIFF file
    task = ee.batch.Export.image.toDrive(
        image=clipped_image,
        description='Satellite_Image_Export',
        folder='Satellite_Images',  # The folder where the exported image will be saved in Google Drive
        fileNamePrefix=output_filename,
        region=bbox_geometry,
        scale=30,  # The spatial resolution of the exported image (30 meters for Landsat)
    )

    task.start()

if __name__ == '__main__':
    # Define the bounding box as [minX, minY, maxX, maxY]
    bounding_box = [-122.5258, 37.6493, -122.3442, 37.8199]  # Example bounding box for San Francisco, USA

    # Call the function to export the satellite image
    export_satellite_image(bounding_box, 'exported_image')
