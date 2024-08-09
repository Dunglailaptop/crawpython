from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from concurrent.futures import ThreadPoolExecutor, as_completed
from unidecode import unidecode 
from tkinter import ttk, filedialog, Tk
from datetime import datetime
from tkinter import *
from tkcalendar import DateEntry
import pandas as pd
import math
import time
import csv
import json
import unicodedata
import re
import requests
import io
import os
from PIL import Image
import numpy as np

def login(chromedriver_path, url, username, password):
    try:      
       
    except Exception as e:
        print(f"Lỗi trong quá trình thực thi chính: {e}")

    return driver