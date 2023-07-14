FROM spapanik/django-app:2.1.0

ENV WEBSERVER="/home/${DJANGO_USER}/zelda"
ENV PYTHONBREAKPOINT=ipdb.set_trace
ENV DJANGO_SETTINGS_MODULE=zelda.settings
ENV webserver_netloc="0.0.0.0:8000"

USER ${DJANGO_USER}

COPY --chown=${DJANGO_USER}:${DJANGO_USER} . ${WEBSERVER}

WORKDIR ${WEBSERVER}

RUN yam install_code

CMD yam -bf -r5 migrations && \
    yam -bf runserver
