from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


# Example:

# raw_html = simple_get('http://www.fabpedigree.com/james/mathmen.htm')
# html = BeautifulSoup(raw_html, 'html.parser')
# for i, li in enumerate(html.select('li')):
#     print(i, li.text)

# Actual:
# raw_html = simple_get('http://stephaniehurlburt.com/blog/2016/11/14/list-of-engineers-willing-to-mentor-you')
# print(len(raw_html))  # 95023

# raw_html = simple_get('http://stephaniehurlburt.com/blog/2016/11/14/list-of-engineers-willing-to-mentor-you')
# html = BeautifulSoup(raw_html, 'html.parser')
# for i, p in enumerate(html.select('p')):
#     print(i, p.text)
# for i, p in enumerate(html.select('blockquote')):
#     print(i, p.text)


# An even better site to scrape the data is : https://ishansharma.github.io/twitter-mentors/

raw_html = simple_get('https://ishansharma.github.io/twitter-mentors/')
html = BeautifulSoup(raw_html, 'html.parser')
for i, t in enumerate(html.select('tr')):
    print(i, t.text)
# for i, p in enumerate(html.select('blockquote')):
#     print(i, p.text)

