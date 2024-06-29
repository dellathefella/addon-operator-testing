FROM flant/addon-operator:latest
ADD modules /modules
RUN apk --no-cache add python3 
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip kubernetes
# ADD global-hooks /global-hooks
# RUN chmod +x -R /global-hooks