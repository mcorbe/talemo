# Asset Management Templates

This directory contains HTML templates for the asset management views in the Talemo platform. These templates provide the user interface for managing audio, image, and other media assets used in stories.

## Overview

The asset management templates allow users to upload, browse, and manage various types of media assets that are used in the creation and presentation of stories. This includes audio files for narration, images for illustrations, and other media types.

## File Structure

- `index.html`: Main landing page for the asset management section

## Template Details

### index.html

The `index.html` template serves as the main landing page for the asset management section. It provides:

- A list view of existing assets
- Upload functionality for new assets
- Filtering and sorting options
- Asset type selection (audio, image, document)

This template extends the base template and uses Bootstrap for layout and styling.

## Integration with Backend

The asset templates interact with the backend through several API endpoints:

- `/api/v1/assets/`: For listing and creating assets
- `/api/v1/assets/<id>/`: For retrieving, updating, and deleting specific assets
- `/api/v1/assets/upload/`: For handling file uploads

These endpoints are called asynchronously using HTMX, and the results are displayed in the UI without requiring a full page reload.

## Asset Types

The templates support various asset types:

1. **Audio Assets**:
   - Story narrations
   - Sound effects
   - Background music

2. **Image Assets**:
   - Story illustrations
   - Character portraits
   - Background images

3. **Document Assets**:
   - Story scripts
   - Metadata files
   - Reference materials

## Storage Integration

Assets are stored using MinIO (S3-compatible storage):

- File uploads are processed through the Django backend
- Files are stored in MinIO buckets
- URLs are generated for accessing the assets
- Permissions are managed through the Django application

## Usage Example

The asset management interface allows users to:

1. Browse existing assets with filtering options
2. Preview assets (audio playback, image viewing)
3. Upload new assets with metadata
4. Edit asset metadata
5. Delete assets when no longer needed

Example HTMX interaction for asset upload:

```html
<form hx-post="/api/v1/assets/upload/"
      hx-encoding="multipart/form-data"
      hx-target="#upload-result"
      hx-indicator="#upload-indicator">
  
  <select name="assetType" class="form-select">
    <option value="audio">Audio</option>
    <option value="image">Image</option>
    <option value="document">Document</option>
  </select>
  
  <input type="file" name="assetFile" class="form-control">
  
  <button type="submit" class="btn btn-primary">Upload</button>
  
  <div id="upload-indicator" class="htmx-indicator">
    Uploading...
  </div>
</form>

<div id="upload-result">
  <!-- Upload result will appear here -->
</div>
```

## Styling

The asset templates use Bootstrap 5 for styling, with custom components for:

- Asset cards
- Upload forms
- Preview modals
- Filter controls

## JavaScript Functionality

The templates include JavaScript functionality for:

- File type validation
- Preview generation
- Audio playback controls
- Image zooming and panning

## Related Components

- `talemo/assets/views.py`: Backend views that handle asset requests
- `talemo/assets/models.py`: Asset data models
- `talemo/assets/storage.py`: Storage backends for MinIO integration

## Best Practices

When modifying these templates:

- Ensure proper file type validation
- Implement progress indicators for uploads
- Optimize preview generation for performance
- Support responsive design for mobile and desktop
- Implement proper error handling for failed uploads

## Related Documentation

- [Django File Uploads](https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/)
- [MinIO Documentation](https://docs.min.io/)
- [HTMX File Upload](https://htmx.org/examples/file-upload/)