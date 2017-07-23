## Synopsis

This is the API for creating a photo gallery. This app also periodically gathers images from various aggregation sites. For demo of this app with a working UI, go to https://bell-sample.herokuapp.com/gallery/index/.

## How to Use

### Gallery Index

The json list of galleries can be accessed at https://bellapi-heroku.herokuapp.com/api/v0/index. 
The galleries have the following fields.

Field             | Description
------------------|-------------
name              | The name of the gallery
slug              | The gallery id. Used for the url of the gallery. 
description       | The gallery description
preview_image_url | A link to a single thumb image from a gallery for previewing the gallery.

### Gallery

If you want to get more information on a specific gallery,
just append the galleries *slug* at https://bellapi-heroku.herokuapp.com/api/v0/galleries/

**Example**: https://bellapi-heroku.herokuapp.com/api/v0/galleries/123

The json has the following fields.

Field       | Description
------------|-------------
description | The gallery description (Same as the gallery items at gallery index) 
images      | A list of image items from this gallery

Each image item also has its own fields.

Field     | Description
----------|-------------
name      | The name of image (Duh).
image_url | The url to the full size image
thumb_url | The url to the thumbnail of the image. **Warning**: Currently links to the full-size image due to a bug.

