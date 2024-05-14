FROM spapanik/django-api:2.1.0

ENV WEBSERVER="/home/${DJANGO_USER}/zelda"
ENV PYTHONBREAKPOINT=ipdb.set_trace
ENV DJANGO_SETTINGS_MODULE=zelda.settings

USER ${DJANGO_USER}

COPY --chown=${DJANGO_USER}:${DJANGO_USER} . ${WEBSERVER}

WORKDIR ${WEBSERVER}

RUN yam install_py

CMD yam -bf migrations && \
    yam -bf runserver
