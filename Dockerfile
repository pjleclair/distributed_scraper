FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt .
COPY src/ ./src

# Install dependencies
RUN pip install -r requirements.txt
# Make sure Python can find our modules
ENV PYTHONPATH=/var/task/src:$PYTHONPATH
# Set the command that Lambda will run
# This points to the "handler" function 
CMD [ "src.lambda_handler.handler" ]
