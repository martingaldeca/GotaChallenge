# Gota, an API for recipes.

Challenge for Drop.

The requisites of the challenge was the following:

We want to create a (REST) API that can manage recipes that supports these operations:

    Create a new recipe.
    Retrieve a recipe.
    Modify a recipe.

Also, we want a diagram and brief explanation on how this will run and be deployed on a Cloud Platform (e.g. AWS).

Optionally, you can:

    Add some kind of authentication (e.g. token).
    Create a lightweight client to query the API.

Deliverable

You should share with us a private Git repository that contains:

    A separated branch (not main) with the code of your solution and a Pull Request against the main branch so we can discuss your solution.
    Instructions on how to run your solution (README).
    A document (in the format that you prefer) with the diagram and explanation on how to deploy and run your solution in the cloud.
    You should give access to this repo to the following users (so they can review your solution on the Pull Request): davidag , jacalvo , kabute, rmunoz
    Optional: Provide a containerized solution (e.g. Dockerfile).

Considerations

    Programming Languages: Python or Go are recommended.
    You can choose what Schema definitions and data structures to use.
    You can choose any storage/persistence that you consider.
    Standard specifications (e.g. OpenAPI) are optional but encouraged.

Recipe Format

The recipe format is open the whatever you consider but, please think about things such as:

    A recipe has a list of ingredients and ingredients have quantities (e.g. 50 gr of Olive Oil).
    A recipe has steps to follow.

## Local Environment 🚀

### Prerequisites 📋

You will need in your computer `Docker`, `docker-compose` and, of course, `git` to run it, but, is
highly recommended having also `Make`

The project will run inside Docker containers, and you can see what python packages are used in the pyproject.toml
file (poetry-based).

### Install 🔧

Installing the project is quite simple if you have Make.

Go to your project path and clone the repository:

After cloning it, go to the main path:

```shell script
$ cd GotaChallenge
```

Then just use `make` command:

```shell script
$ make
```

Now all the magic will start if you have `docker` and `docker-compose` installed, all the volumes and containers
will be created.

After the deployment, you can check if all was ok by going to `http://localhost/gotadmin/`. Then, if you see the Django-admin login
page ... IT WORKS!

![](https://media.tenor.com/images/202be43371949d5b86f8e58319debd88/tenor.gif)

By default, it will create a user with the name `admin` and password `root1234`.

If it does not work you can check for problems in logs using the following command:

```shell script
$ make alllogs
```

## Passing tests 🖥️

You can pass the test in your local environment just using the following command:

```shell script
$ make test
```

Or you can enter the docker container and be more specific

```shell script
$ make sh
$ pytest core/models/tests/test_device.py::DeviceTest::test_active_actions
```

If there are more than 5 test that does not pass, you should use the next command if you want to run them all:

```shell script
$ make localtest
```
