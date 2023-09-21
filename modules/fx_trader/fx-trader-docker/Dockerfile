FROM amazon/aws-lambda-python

RUN pip install aws-lambda-powertools
COPY results.py ${LAMBDA_TASK_ROOT}/
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target ${LAMBDA_TASK_ROOT}/
CMD [ "results.handler" ]