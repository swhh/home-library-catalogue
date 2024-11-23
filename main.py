from googleapiclient.errors import HttpError
from connect_service import generate_creds, create_service
from generative_ai import generate_texts
from photos import get_media_items_bytes
from sheets import update_sheet, remove_duplicates
from utils import generate_books, find_top_n_authors, remove_duplicate_books



SPREADSHEET_SCOPES = "https://www.googleapis.com/auth/spreadsheets"
PHOTO_SCOPES = 'https://www.googleapis.com/auth/photoslibrary'
PHOTO_JSON = "photos_token.json"
SPREADSHEET_JSON = "spreadsheet_token.json"
SPREADSHEET_ID = '17JKh35FI-euWNCr3d_yPKR-gy9uK9BUo6vNrZDE6ffE' # spreadsheet where book details stored
SHEET_VERSION = 'v4'
PHOTO_VERSION = 'v1'
RANGE = 'Sheet1!A:B' # data range in spreadsheet where book details are stored
ALBUM_ID = 'AKXWFB1yUkhQM_VjQKs7Rgc1QsExBwG2-m8sg23PfRi9qJ177T_4n1aIqV6geSQUb5p0lVURfz07' # Google Photos album ID where book images stored



def main():
  """Fetch photos from Google Photos API, 
  get the book details from Google Vertex API 
  and then add to spreadsheet with Google Sheets API; 
  finally remove duplicates"""
  try:
    sheet_creds = generate_creds(SPREADSHEET_JSON, SPREADSHEET_SCOPES)
    photo_creds = generate_creds(PHOTO_JSON, PHOTO_SCOPES)
    
    sheet_service = create_service('sheets', SHEET_VERSION, sheet_creds)
    photo_service = create_service('photoslibrary', PHOTO_VERSION, photo_creds)

  except HttpError as err:
    print(err)

  try:
    book_images = get_media_items_bytes(ALBUM_ID, photo_service)
    texts = generate_texts(book_images)
    books = generate_books(texts, separator='#')

    update_sheet(sheet_service, SPREADSHEET_ID, books, range=RANGE) # upload book details to spreadsheet
    
    books = remove_duplicate_books(books)
    top_authors = find_top_n_authors(filter(lambda x: len(x) > 1, books), 10)
    print('Top 10 most common authors')
    for i, (author, num) in enumerate(top_authors, start=1):
      print(i, f'Author: {author} with {num} books')
    
    remove_duplicates(SPREADSHEET_ID, sheet_id=0, service=sheet_service) # remove any duplicate rows from sheet
  except HttpError as err:
    print(err)

if __name__ == "__main__":
  main()