import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient import discovery
import mammoth
from base2 import get_courses_html
import datetime


# Function to build HTML from file
def build_html(file_path):
    if file_path.endswith('.html'):
        with open(file_path, 'r') as file:
            html = file.read()
    elif file_path.endswith('.docx'):
        with open(file_path, 'rb') as file:
            result = mammoth.convert_to_html(file)
            html = result.value
    else:
        raise ValueError('Invalid file extension. Only .html and .docx files are supported.')
    return html

# Build HTML content from files
html1 = build_html('first.html')
html4 = "Updated Time (IST): " + datetime.datetime.now().strftime("%d/%m/%Y, %H:%M") + "\n"
html2 = get_courses_html()
html3 = build_html('file2.docx')
all_html = html1 + html4 + html2 + html3



# Function to authorize credentials
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

# Function to update a blog post
def update_post(post_id, blog_id, title, content):
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = 'https://blogger.googleapis.com/$discovery/rest?version=v3'
    service = discovery.build('blogger', 'v3', http=http, discoveryServiceUrl=discovery_url)

    post = service.posts().get(blogId=blog_id, postId=post_id).execute()
    post['title'] = title
    post['content'] = content

    updated_post = service.posts().update(blogId=blog_id, postId=post_id, body=post).execute()
    print('Post updated successfully!')

# Get the current date
from datetime import date
today = date.today().strftime("%d-JUNE-%y")
title = f"UDEMY COURSES WITH FREE CERTIFICATE | {today} | IHTREEKTECHCOURSES"

# Specify the post ID, blog ID, title, and content to update
post_id = '8097252119400957177'
blog_id = '5651255862571344247'
test_post_id = '3359690114760599976'
test_blog_id = '3481597162520342949'
content = all_html
# Call the update_post function to update the blog post
update_post(post_id, blog_id, title, content)
# update_post(test_post_id, test_blog_id, title, content)

# Delete temporary files
# file_list = ['post.docx', 'modified.docx']
# for file in file_list:
#     os.remove(file)
#     print(f"{file} deleted successfully!")
