FROM flant/addon-operator:latest
ADD modules /modules
RUN apk --update --no-cache add python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade setuptools pip kubernetes requests
#ADD global-hooks /global-hooks
RUN chmod +x -R /global-hooks