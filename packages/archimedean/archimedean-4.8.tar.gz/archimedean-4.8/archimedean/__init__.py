import click
import os
import requests
from bs4 import BeautifulSoup as bs
import json
import smtplib
import datetime
from PyPDF2 import PdfFileMerger
from PIL import Image