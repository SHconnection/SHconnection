FROM python:3.7
MAINTAINER muxistudio <muxistudio@qq.com>
ENV DEPLOY_PATH /mana_api
RUN mkdir -p $DEPLOY_PATH
WORKDIR $DEPLOY_PATH
Add . .
RUN pip install pipenv
RUN pipenv install --system --deploy
