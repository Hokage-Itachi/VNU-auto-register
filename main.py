import requests
from bs4 import BeautifulSoup


class Subject:
    def __init__(self, id, class_id, name, total_slot, registered_slot):
        self.id = id
        self.class_id = class_id
        self.name = name
        self.total_slot = total_slot
        self.registered_slot = registered_slot

    def __repr__(self):
        return "[Subject: id={}, CLASS_ID={}, NAME={}, total_slot={}, REGISTERED_SLOT={}".format(self.id, self.class_id,
                                                                                                 self.name,
                                                                                                 self.total_slot,
                                                                                                 self.registered_slot)


resource = {
    "login": "http://dangkyhoc.vnu.edu.vn/dang-nhap",
    "getSubjects": "http://dangkyhoc.vnu.edu.vn/danh-sach-mon-hoc/1/1",
    "confirmSubjects": "http://dangkyhoc.vnu.edu.vn/xac-nhan-dang-ky/1",
    "selectSubject": "http://dangkyhoc.vnu.edu.vn/chon-mon-hoc/",
    "home": "http://dangkyhoc.vnu.edu.vn/dang-ky-mon-hoc-nganh-1",
    "registeredSubjects": "http://dangkyhoc.vnu.edu.vn/danh-sach-mon-hoc-da-dang-ky/1"
}

class_to_register = [
    "MAT3505 1"
]


def get_login():
    url = resource.get("login")
    response = requests.get(url)
    cookie = response.headers.get("Set-Cookie")
    print("Login Cookie:", cookie)
    login_page = BeautifulSoup(response.text, "lxml")
    verification_token = login_page.input.get("value")
    print("Login Verification Token:", verification_token)
    return cookie, verification_token


def select_subject(subject_id, cookie):
    url = resource.get("selectSubject") + str(subject_id) + '/1/1/'
    header = {
        "Cookie": cookie
    }

    response = requests.post(url, headers=header)
    print(response.text)


def login(cookie, verification_token):
    url = resource.get("login")
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookie
    }

    data = {
        "__RequestVerificationToken": verification_token,
        "LoginName": "18001087",
        "Password": "uchihaitachi"
    }

    session = requests.Session()
    session.post(url, data=data, headers=header)
    session_id = session.cookies.get_dict().get("ASP.NET_SessionId")
    print("Session ID:", session_id)
    # response = requests.post(url, data=data, headers=header)
    # print(response.text)

    # print(response.headers)
    return session_id


def confirm_subject(cookie):
    url = resource.get("confirmSubjects")
    header = {
        "Cookie": cookie
    }

    response = requests.post(url, headers=header)
    print(response.text)


def get_subjects(cookie):
    url = resource.get("getSubjects")
    header = {
        "Cookie": cookie
    }

    response = requests.post(url, headers=header)
    soup = BeautifulSoup(response.text, "lxml")
    # f = open("list_subject.html", "w", encoding="UTF-8")
    # f.write(soup.prettify())
    # f.close()
    subjects = {}
    trs = soup.findAll("tr")
    for tr in trs:
        tds = tr.findAll("td")

        input = tds[0].input
        if input is not None:
            name = tds[1].text.strip()
            total_slot = tds[5].text.strip()
            empty_slot = tds[6].text.strip()
            class_id = tds[4].text.strip()
            subject_id = input.get("data-rowindex")
            subj = Subject(subject_id, class_id, name, total_slot, empty_slot)
            subjects[class_id] = subj
    # print(trs)
    # print(response.text)
    return subjects


def get_registered_subject(cookie):
    url = resource.get("registeredSubjects")
    header = {
        "Cookie": cookie
    }

    response = requests.post(url, headers=header)
    print(response.text)


def run():
    login_cookie, verification_token = get_login()
    session_id = login(login_cookie, verification_token)
    usage_cookie = login_cookie.split(";")[0] + "; ASP.NET_SessionId=" + session_id
    print("Usage Cookie:", usage_cookie)
    subjects = get_subjects(usage_cookie)
    # count = 0
    # for i in subjects:
    #     count += 1
    #     print(subjects.get(i))

    # get_registered_subject(usage_cookie)
    # for i in subjects:
    #     print(i)
    for class_id in class_to_register:
        if subjects.get(class_id) is not None:
            select_subject(subjects.get(class_id).id, usage_cookie)
    # # select_subject(163, cookie=usage_cookie)
    confirm_subject(usage_cookie)


# while True:
#     # import time
#
#     run()
    # print("a")
    # time.sleep(1)

login("a", "a")
