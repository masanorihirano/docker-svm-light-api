From alpine:latest

RUN apk --update add make gcc libc-dev python py-pip python-dev && \
    rm -rf /var/cache/apk/*

WORKDIR /root
RUN mkdir svm_light && \
    mkdir bin && \
    cd svm_light && \
    wget http://download.joachims.org/svm_light/current/svm_light.tar.gz && \
    gunzip -c svm_light.tar.gz | tar xvf - && \
    make && \
    mv svm_learn ../bin/ && \
    mv svm_classify ../bin/ && \
    cd ../ && \
    rm -rf svm_light
COPY requirement.txt .
RUN pip install -r requirement.txt
COPY server.py .
CMD ["python", "server.py"]