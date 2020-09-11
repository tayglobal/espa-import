FROM python:3

COPY requirement.txt .

RUN python -m pip install --upgrade pip
RUN pip install -r requirement.txt

WORKDIR /espa-import

COPY epimport epimport

ENV PYTHONPATH "${PYTHONPATH}:/espa-import"
