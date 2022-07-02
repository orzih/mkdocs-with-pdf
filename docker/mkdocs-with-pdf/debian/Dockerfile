FROM python:3.8-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt-get upgrade -y \
    && pip3 install --no-cache-dir beautifulsoup4==4.9.3\
        mkdocs mkdocs-material \
        mdx-gh-links mkdocs-redirects mkdocs-minify-plugin mkdocs-extra-sass-plugin livereload \
        weasyprint mkdocs-with-pdf

# Headless Chrome
RUN apt-get install --no-install-recommends -y curl gnupg \
    && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install --no-install-recommends -y google-chrome-stable

RUN echo '#!/bin/sh\n\
exec google-chrome $*\n\
' > /usr/local/bin/chromium-browser \
    && chmod a+x /usr/local/bin/chromium-browser \
    && chromium-browser --version

# Additional font
COPY fonts /usr/share/fonts/Additional
RUN apt-get install --no-install-recommends -y fontconfig fonts-symbola fonts-noto fonts-freefont-ttf \
    && fc-cache -f \
    && fc-list | sort

RUN apt-get purge --auto-remove -y curl gnupg \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/* \
    && dpkg -l

# Set working directory and User
RUN useradd -m --uid 1000 mkdocs
USER mkdocs
WORKDIR /docs

# Expose MkDocs development server port
EXPOSE 8000

# Start development server by default
ENTRYPOINT ["mkdocs"]
CMD ["serve"]
