from cjdg_open_api.base import baseApi


class reviewTask(baseApi):
    def __init__(self, token, app_secret=None):
        super().__init__(token, app_secret)

    def list(self):
        api_name = f"enter/superguide/inspection/task/list"
        data = {"pageNum": 1, "pageSize": 10, "queryParameter": {"name": ""}}
        s = self.request(api_name, data)
        return s

    def list_name(self, name):
        api_name = f"enter/superguide/inspection/task/list"
        data = {"pageNum": 1, "pageSize": 10, "queryParameter": {"name": name}}
        s = self.request(api_name, data)
        return s


def main():
    a = reviewTask(token="896b715ddf064d55cf04de66d8bdd83b_csz_web")
    a.list()


if __name__ == "__main__":
    main()
