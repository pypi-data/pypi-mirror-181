# InstagramProfilePhotosDownloader
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/massimopavoni/InstagramProfilePhotosDownloader?include_prereleases)](https://github.com/massimopavoni/InstagramProfilePhotosDownloader/releases)
[![PyPI Package](https://img.shields.io/pypi/v/InstagramProfilePhotosDownloader)](https://pypi.org/project/InstagramProfilePhotosDownloader/)
[![GitHub License](https://img.shields.io/github/license/massimopavoni/InstagramProfilePhotosDownloader)](https://github.com/massimopavoni/InstagramProfilePhotosDownloader/blob/main/LICENSE)
[![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/massimopavoni/InstagramProfilePhotosDownloader)](https://www.python.org/downloads/release/python-3100/)
[![Code style: pep8](https://img.shields.io/badge/code%20style-pep8-blue)](https://pypi.org/project/autopep8/)

[![Discord](https://img.shields.io/discord/926217143194886234?label=Join%20Not%20Declared%20Developers)](https://discord.gg/ZA76nJ3RsU)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/T6T8BD7A1)

A simple scraping tool to download an Instagram profile's photos.

### Dependencies
- [Selenium](https://www.selenium.dev/) ([LICENSE](https://github.com/SeleniumHQ/selenium/blob/trunk/LICENSE))
- [Requests](https://requests.readthedocs.io/en/latest/) ([LICENSE](https://github.com/psf/requests/blob/main/LICENSE))

### Usage
The package provides the simple console script with two entry points upon installation: `InstagramProfilePhotosDownloader` and `ippd`.

Two commands are available:
- `ippd urls_file scrape` is used to scrape some posts images links and save the URLs in a text file, uses _Selenium_
- `ippd urls_file download` is used to download the images with simple _Requests_ HTTP GET

This tool is intended to be used by people who know how scraping and HTTP works, meaning the `-h` help option (and the small size of the code) is more than enough to understand where to get the required arguments.