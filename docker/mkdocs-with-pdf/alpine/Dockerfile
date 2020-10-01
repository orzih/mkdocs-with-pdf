FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

#
# Runtimes for WeasyPrint
#
RUN apk update \
    && apk --update --upgrade --no-cache add cairo-dev pango-dev gdk-pixbuf-dev \
    && apk --update --upgrade --no-cache add libsass

RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
        musl-dev g++ jpeg-dev zlib-dev libffi-dev libsass-dev \
    && SYSTEM_SASS=1 pip install --no-cache-dir \
        mkdocs mkdocs-material \
        mdx-gh-links mkdocs-redirects mkdocs-minify-plugin \
        mkdocs-with-pdf \
    && apk del .build-deps

# Headless Chrome
RUN apk --update --upgrade --no-cache add udev chromium \
    && chromium-browser --version

# Additional font
COPY fonts /usr/share/fonts/Additional
RUN apk --update --upgrade --no-cache add fontconfig ttf-freefont font-noto terminus-font \
    && fc-cache -f \
    && fc-list | sort

# Set working directory and User
RUN addgroup -g 1000 -S mkdocs && \
    adduser -u 1000 -S mkdocs -G mkdocs
USER mkdocs
WORKDIR /docs

# Expose MkDocs development server port
EXPOSE 8000

# Start development server by default
ENTRYPOINT ["mkdocs"]
CMD ["serve"]
