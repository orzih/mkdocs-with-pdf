# _Templates_ for Docker

This sample uses [`docker-compose`](https://docs.docker.com/compose/), but it's not required.

## Build docker images

```sh
docker-compose build
```

## How to use

* _Create_ a new mkdocs project.

    ```sh
    docker-compose run tiny new .
    ```

* on _Debug(Edit)_ the mkdocs project.

    ```sh
    docker-compose up tiny
    ```

    or

    ```sh
    docker-compose up alpine
    ```

    or

    ```sh
    docker-compose up debian
    ```

    and access to `http://localhost:8000` from any browser.

* Building the site.

    ```sh
    docker-compose run tiny build
    ```

    or

    ```sh
    docker-compose run alpine build
    ```

    or

    ```sh
    docker-compose run debian build
    ```

    see `docs-src` directory.

## TODO

* `tiny`
* `alpine`
  * [ ] MathJax font.
* `debian`
  * [ ] Slim image.
