FROM python:3
RUN mkdir /x_be
WORKDIR /x_be
COPY *.py /x_be/
COPY *.db /x_be/
COPY requirements.txt /x_be
RUN apt-get update && apt-get upgrade -y
RUN pip3 install -r /x_be/requirements.txt
EXPOSE 4555
CMD ["python3", "/x_be/app.py"]