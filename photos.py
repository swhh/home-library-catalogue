import requests

SCOPES = 'https://www.googleapis.com/auth/photoslibrary'


def get_media_items(album_id, service):
    results = service.mediaItems().search(
        body={"albumId": album_id, "pageSize": 100}
    ).execute()
    
    items = results.get('mediaItems', [])
    next_page_token = results.get('nextPageToken')
    
    while next_page_token:
        results = service.mediaItems().search(
            body={"albumId": album_id, "pageSize": 100, "pageToken": next_page_token}
        ).execute()
        items.extend(results.get('mediaItems', []))
        next_page_token = results.get('nextPageToken')
    
    return items


def get_media_items_bytes(album_id, service):
    media_items = get_media_items(album_id, service)
    # Add '=d' to the baseUrl to get full resolution download URL
    image_urls = [item['baseUrl'] + '=d' for item in media_items if 'baseUrl' in item]
    
    # Get the actual bytes for each image
    image_bytes_list = []
    for url in image_urls:
        response = requests.get(url)
        image_bytes_list.append(response.content)
    
    return image_bytes_list
