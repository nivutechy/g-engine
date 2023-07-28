import ee

# Initialize Earth Engine
ee.Initialize()

# Function to get satellite imagery
def get_satellite_image(bbox=[longitude_west_default, latitude_south_default, longitude_east_default, latitude_north_default]):
    # Define the bounding box
    region = ee.Geometry.Rectangle(bbox)

    # Get a satellite image (e.g., Landsat 8 imagery)
    image = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
        .filterBounds(region) \
        .filterDate('2020-01-01', '2023-02-01') \
        .first()

    # Export the image to Google Drive
    task = ee.batch.Export.image.toDrive(image=image,
                                         description='satellite_image',
                                         folder='GEE_Export',
                                         fileNamePrefix='exported_image',
                                         region=region.getInfo(),
                                         scale=30)

    # Start the export task
    task.start()

    # Wait for the task to complete
    print("Exporting the image to Google Drive...")
    task_status = None
    while task_status != 'COMPLETED':
        task_status = ee.batch.Task.list()[0]['state']
        if task_status == 'FAILED':
            print("Export task failed. Please check the GEE tasks for more information.")
            return

    print("Image exported successfully!")

if __name__ == "__main__":
    # Set the default bounding box coordinates [west, south, east, north]
    longitude_west_default = -74.5
    latitude_south_default = 40.0
    longitude_east_default = -73.5
    latitude_north_default = 41.0

    # Call the function to get the satellite image and export it
    get_satellite_image()
