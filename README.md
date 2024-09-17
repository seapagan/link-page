# Link Page <!-- omit in toc -->

A Python FastAPI app to create a link page for social media profiles, Homepage,
GitHub, etc.

The use-case that prompted this is to have a configurable target for a static
link in a QR code on a business card. The page is deliberately simple and static
to ensure that it loads quickly and is easy to maintain.

In addition:

- It's an example of using FastAPI with Jinja2 templates. This allows having
a simple web site, but still able to access config files, databases and API's.
- It shows how to hook into the 'uvicorn' logger so we can add our own logs to
that and take advantage of the same formatting and colors as the rest of the
uvicorn logging.
- Shows how to use a `TOML` configuration file for your FastAPI applications.
Shameless plug - it uses my
[simple-toml-settings](https://github.com/seapagan/simple-toml-settings)
library.

I may build this into a complete 'linktree' type clone later with database use
and user login etc. Just for fun :grin:

<!-- vim-markdown-toc GFM -->

- [Working Example](#working-example)
- [Configuration](#configuration)
- [Development setup](#development-setup)
- [License](#license)
- [Credits](#credits)

<!-- vim-markdown-toc -->

## Working Example

A working example of this app can be found at
[https://me.seapagan.net](https://me.seapagan.net).

## Configuration

This app uses a `TOML` configuration file. This is stored in the `config.toml`
file in the root of the project. There are a few settings that can be changed
in this file:

```toml
[linkpage]
name="Grant Ramsay" # put your name here
role="Python and Full-Stack Developer" # put your role here
github_user="seapagan" # put your GitHub username here
schema_version = "none"

[linkpage.homepage]
url="https://www.gnramsay.com" # put your homepage URL here
title="My Homepage" # put the title of your homepage here

[linkpage.social]
twitter="gnramsay_dev" # put your Twitter username here
linkedin="gnramsay" # put your LinkedIn username here
youtube="seapagan" # put your YouTube username here
medium="seapagan" # put your Medium username here
devto="" # put your Dev.to username here
twitch="" # put your Twitch username here
```

If any of the social media profiles are not used, then leave the value as an
empty string or remove the line from the configuration file.

> [!NOTE]
> If you are serving your app using a gunicorn service etc, you will need to
> restart the service to pick up the changes to the configuration file.

## Development setup

I have recently changed the development setup to use
[uv](https://docs.astral.sh/uv/) for python version control and virtual
environments instead of `poetry`

Install the dependencies using `uv`:

```console
uv sync
```

Then, activate the virtual environment:

```console
source .venv/bin/activate
```

You can use the poe task runner to easily run uvicorn:

```console
poe serve
```

> [!IMPORTANT]
> This is the recommended way to run the app in development but **NOT
> in production**. For production, you should use a proper ASGI server like
> `gunicorn` to run the 'uvicorn' server, usually behind a reverse proxy like
> `nginx`.

These is also a browser-sync task that will start a browser-sync server to
reload the browser when changes are made to the templates or static files,
which should be run in a separate terminal:

```console
poe show
```

The latter will automatically open your default browser to the correct URL, and
reload when required.

## License

This project is licensed under the MIT License.

```pre
The MIT License (MIT)
Copyright (c) 2024 Grant Ramsay

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
```

## Credits

The original Python boilerplate for this program was created using my
[Pymaker](https://github.com/seapagan/py-maker) application.
