# IBL Open edX Task

Task Details

-   Stand up an instance of Open edX
-   Develop an extension that exposes a REST API endpoint and saves a greeting from the user which should be logged and save in the database and should be visible from the Django Admin
-   If the greeting is “hello”, then the view of this API endpoint should call the original greeting endpoint again with “goodbye”

Technical features and coding techniques that are showcased in this repo include:

-   Open edX Django urls
-   Open edX Django logging
-   Open edX Django RestFramework custom api
-   Django app setup
-   Django models
-   Django Admin
-   Django manage.py custom commands

## Getting Started

### Install using IBL image

```bash
tutor config save --set DOCKER_IMAGE_OPENEDX=public.ecr.aws/ibleducation/ibl-edx-ce:latest
echo "greeting-plugin @ git+https://github.com/tech-expert19/greeting_plugin.git" >> "$(tutor config printroot)/env/build/openedx/requirements/private.txt"
tutor images build openedx
tutor local launch
tutor local run lms ./manage.py lms greetings_plugin_init
tutor local run lms ./manage.py lms makemigrations greeting_plugin
tutor local run lms ./manage.py lms migrate greeting_plugin
```
