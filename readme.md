# Simple URL Shortener

This simple URL shortener was created as a project for [boot.dev](https://boot.dev).
It allows you to create URL short links and track visits across them.
There's basic auth via an API key and API docs created by FastAPI.
It's likely not production ready, so use at your own discretion.

## Running the project locally

You need to have [UV](https://docs.astral.sh/uv/) installed and running.
Once you've done that you can run the tests with the following command:

`sh bin/dev.sh`

This will spin up a FastAPI server and create a `tmp.db` file.
You can then visit `127.0.0.1:8000/docs` for an API playground, or hit the endpoint directly.
For the authorized endpoints, use the API key, `devmode`.

## Testing the project

You need to have [UV](https://docs.astral.sh/uv/) installed and running.
Once you've done that you can run the tests with the following command:

`sh bin/test.sh`

There's only E2E tests at the moment, and they're not comprehensive.

## Deploying the project

Coming Soon
