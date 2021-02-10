import requests


def get_page(url):
    headers = {'user-agent': 'jobs_parser/0.0.0'}
    return requests.get(url, headers=headers)


if __name__ == '__main__':
    page = get_page(
        "https://rabota.by/"
    )
    print(page.status_code)
