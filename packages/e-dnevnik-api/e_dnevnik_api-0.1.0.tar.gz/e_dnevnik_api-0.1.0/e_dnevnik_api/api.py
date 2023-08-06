import requests
from bs4 import BeautifulSoup
from .errors import AuthenticationError
from .helpers import authentication_required

class EDnevnik:
    def __init__(self, session: requests.Session = None, is_authenticated = False, root_url: str = "https://ocjene.skole.hr") -> None:
        if not session:
            session = requests.Session()
        self.session = session
        self.is_authenticated = is_authenticated
        self.root_url = root_url

    def login(self, username: str, password: str) -> None:
        r = self.session.get(url=f"{self.root_url}/login")
        soup = BeautifulSoup(r.text, "lxml")
        token = soup.find("input", { "name": "csrf_token" }).get("value")
        r = self.session.post(url=f"{self.root_url}/login", data={ "username": username, "password": password, "csrf_token": token })
        if "Neispravno korisničko ime ili lozinka" in r.text:
            raise AuthenticationError("incorrect username or password")
        self.is_authenticated = True

    @authentication_required
    def logout(self) -> None:
        r = self.session.get(url=f"{self.root_url}/logout")
        self.is_authenticated = False

    @authentication_required
    def get_all_courses(self) -> list:
        r = self.session.get(url=f"{self.root_url}/course")
        soup = BeautifulSoup(r.text, "lxml")
        courses = []
        for course in soup.find("ul", { "class": "list" }).findChildren("li"):
            name = course.find_all("span")[0].text
            teacher = course.find_all("span")[1].text.strip()
            url = f"{self.root_url}{course.find('a').get('href')}"
            id = int(url.split("/").pop())
            courses.append({ "id": id, "name": name, "teacher": teacher, "url": url })
        return courses

    @authentication_required
    def get_course_grades(self, id: int) -> list:
        """Get all grades from a course."""
        r = self.session.get(f"{self.root_url}/grade/{id}")
        soup = BeautifulSoup(r.text, "lxml")
        grades = []
        for row in soup.find("div", { "class": "table-container" }).findChildren("div", { "class": "flex-table" }):
            if not "first" in row["class"]:
                grades_row = []
                for col in row.findChildren("div", { "class": "flex-row" }):
                    grades_row.append(col.text.strip())
                grades.append(grades_row)
        return grades
