import requests
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient import discovery
import httplib2
import mammoth



def get_courses_html():
    search_term = None
    url = "https://jobs.e-next.in/public/assets/data/udemy.json"
    response = requests.get(url)
    data = response.json()

    locale_data = [
        {
            "name": course["title"],
            "url": f"https://www.udemy.com/course/{course['url']}/?couponCode={course['code']}",
            "code": course["code"],
            "locale": course["locale"],
            "image": course["image"]
        }
        for course in data
        if course["locale"] == "English"
    ]

    def extract_link(url):
        if url.startswith(("http://click.linksynergy.com/fs-bin/click?", "https://click.linksynergy.com/fs-bin/click?")):
            text_to_remove = "http://click.linksynergy.com/fs-bin/click?id=bnwWbXPyqPU&subid=&offerid=323058.1&type=10&tmpid=14537&RD_PARM1="
            remaining_link = url.replace(text_to_remove, "")
            return remaining_link
        return url

    url = "https://www.real.discount/api-web/all-courses/?store=Udemy&page=1&per_page=400&orderby=date&free=1&search=&language=English&cat="
    response = requests.get(url)
    data = response.json()

    courses = data['results']
    course_list = [
        {
            'name': course['name'],
            'image': course['image'],
            'url': extract_link(course['url'])
        }
        for course in courses
    ]

    combined_data = course_list + locale_data

    unique_data = []
    urls_seen = set()
    for item in combined_data:
        url = item['url']
        if url not in urls_seen and url.startswith("https://www.udemy.com"):
            unique_data.append(item)
            urls_seen.add(url)

    if search_term:
        unique_data = [
            item
            for item in unique_data
            if search_term.lower() in item['name'].lower()
        ]
    url_count = len(unique_data)
    html_text = f"<h4>Total Count of Courses: {url_count}</h4> <br>"

    # search_box_html = '''
    # <div class="search-box">
    #     <input type="text" id="search-input" placeholder="Search courses..." />
    #     <button onclick="searchCourses()">Search</button>
    # </div>
    # '''

    html =''
    for i, item in enumerate(unique_data):
        image = item['image']
        url = item['url']
        title = item['name']

        if i % 3 == 0:
            html += '<div class="row">'

        html += f'''
            <div class="card">
                <a href="{url}" target="_blank">
                    <div class="image-div"><img class="image_hover" src="{image}" alt="Udemy-free-courses-with-certificate-ihtreektech-ihtreektechcourses-daily free courses-udemy-coureses-{title}-{title}"></div>
                </a>
                <p class="title">{title}</p>
            </div>
        '''

        if (i + 1) % 3 == 0 or (i + 1) == len(unique_data):
            html += '</div>'

    css = '''
    <style>
    .image_hover:hover {
        transform: scale(1.1);
        transition: transform 0.5s;
    }
    .image-div {
        width: 100%;
        height: 100%;
        overflow: hidden;
    }
    .row {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: stretch;
        gap: 20px;
        margin-bottom: 20px;
    }
    .card {
        flex: 1 0 calc(33.33% - 10px);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        background-color: #fff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.5s ease;
    }
    .card:hover {
        transform: translateY(-10px);
    }
    .card a {
        display: block;
        text-decoration: none;
        color: #333;
    }
    .card img {
        width: 100%;
        height: 100%;
        border-radius: 5px;
    }
    .title {
        margin-top: 10px;
        font-size: 16px;
        font-weight: bold;
    }
    .search-box {
        margin-bottom: 20px;
    }
    .search-box {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    }

    .search-box input[type="text"] {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-right: 8px;
    font-size: 14px;
    }

    .search-box button {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    background-color: #4CAF50;
    color: #fff;
    font-size: 14px;
    cursor: pointer;
    }

    .search-box button:hover {
    background-color: #45a049;
    }
    </style>
    '''
    search_box_html = '''
    <div class="search-box">
        <input type="text" id="search-input" placeholder="Search courses">
        <button onclick="searchCourses()">Search</button>
    </div>
    <script>
    function searchCourses() {
        var input = document.getElementById('search-input');
        var searchTerm = input.value.toLowerCase();
        var cards = document.getElementsByClassName('card');
        
        for (var i = 0; i < cards.length; i++) {
            var title = cards[i].getElementsByClassName('title')[0].textContent.toLowerCase();
            
            if (title.includes(searchTerm)) {
                cards[i].style.display = 'block';
            } else {
                cards[i].style.display = 'none';
            }
        }
    }
    </script>
    '''

    names_data = unique_data[:40]
    # print(names_data)
    names = [item['name'] for item in names_data]
    names_lines = '\n'.join(names)
    # print(names_lines)
    
    return html_text + css + search_box_html + html


output_html = get_courses_html()



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

    api_response = {}  # Replace with the actual API response received
    post_url = api_response.get("url")
    # post_url_1 = api_response.get()

    # Print the URL of the blog post
    print("URL of the blog post:", post_url)
    # print("URL of the blog post:", post_url_1)


