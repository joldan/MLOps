FROM python:3.11.2

WORKDIR /app

# Load Scrapy Spider Code
COPY ../../scrapy /app

#COPY requirements.txt /app

#Install scrapy
RUN pip install -r requirements.txt

# Run command
CMD scrapy parse --spider=gallito_crawler-img https://www.gallito.com.uy/venta-apartamento-de-revista-en-punta-carretas-3dormitorios-inmuebles-20817942
