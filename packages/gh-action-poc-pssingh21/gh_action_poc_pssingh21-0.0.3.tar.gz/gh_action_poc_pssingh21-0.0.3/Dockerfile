FROM python:3-alpine
RUN mkdir WORK_REPO
RUN cd WORK_REPO
WORKDIR /WORK_REPO
ADD src/gh_action_poc_pssingh21/hello_world.py .
ENTRYPOINT ["python","-u","src/gh_action_poc_pssingh21/hello_world.py"]