import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient import discovery

# Authorize credentials
def authorize_credentials():
    CLIENT_SECRET = 'client_secret.json'
    SCOPE = 'https://www.googleapis.com/auth/blogger'
    STORAGE = Storage('credentials.storage')
    credentials = STORAGE.get()

    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)

    return credentials

# Get the postId of a specific post
def get_post_id(blog_id, post_url):
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = 'https://blogger.googleapis.com/$discovery/rest?version=v3'
    service = discovery.build('blogger', 'v3', http=http, discoveryServiceUrl=discovery_url)

    posts = service.posts().list(blogId=blog_id).execute()
    for post in posts.get('items', []):
        if post['url'] == post_url:
            return post['id']

    return None

# Specify the blog ID and post URL to get the postId
blog_id = '3481597162520342949'
post_url = 'https://l-ihtreek.blogspot.com/2020/10/udemy-free-courses-with-certificate-21.html'

# Call the get_post_id function
postId = get_post_id(blog_id, post_url)
if postId:
    print('Post ID:', postId)
else:
    print('Post not found.')

