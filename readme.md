# Reddit radio

![workflow](https://github.com/martini97/reddit_radio/actions/workflows/ci.yaml/badge.svg)
[![codecov](https://codecov.io/gh/martini97/reddit_radio/branch/main/graph/badge.svg)](https://codecov.io/gh/martini97/reddit_radio)
[![CodeQL](https://github.com/martini97/reddit_radio/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/martini97/reddit_radio/actions?query=workflow%3ACodeQL)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

## Install

```bash
pip install reddit-radio
```

## Config

Before running you need to setup the config file, there is a sample in
`config.sample.ini` for your client\_id and client\_secret you need to go to this
url: https://www.reddit.com/prefs/apps and create a new app. Then move the file to
`~/.config/reddit_radio.ini`.

## Usage

```sh
python -m reddit_radio load-data play
```

## Dependencies

+ [MPV](https://mpv.io/)
