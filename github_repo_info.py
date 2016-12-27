#!/usr/bin/env python
# coding=utf-8
"""
http://www.kryogenix.org/code/browser/sorttable/

https://developer.github.com/v3/
"""

import json
import os
import requests

import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")


def get_repo_info(full_name):
    """ Parameter: full name of github repos
        Return repo record info or nil.
    """
    repo_key = [
        "full_name",
        "language",
        "html_url",
        "homepage",
        "description",
        "created_at",
        "updated_at",
        "stargazers_count",
        "forks_count",
        "open_issues",
        "size"
    ]

    base_url = "https://api.github.com/repos/"
    url = base_url + full_name

    resp = requests.get(url)

    rec = {}

    if resp.status_code == 200:
        repo_infos = json.loads(resp.content)

        for key in repo_key:
            rec[key] = repo_infos[key]

    return rec

# pylint: disable=W0223
class RepoInfoHandler(tornado.web.RequestHandler):
    """ Provide server side function
    """
    def get(self):
        repos_str = self.get_argument("repos", default="", strip=True)

        if repos_str == "":
            self.write("Please input repos")
            return

        repos = repos_str.split(",")
        recs = []

        for repo in repos:
            rec = get_repo_info(repo)

            if len(rec) != 0:
                recs.append(rec)

        self.render("repos.html", recs=recs)

def run_main():
    """ run_main function
        :return: nil
    """
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", RepoInfoHandler),
        ],
        cookie_secret="repo_test_aaa",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=options.debug,
        )

    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    run_main()
