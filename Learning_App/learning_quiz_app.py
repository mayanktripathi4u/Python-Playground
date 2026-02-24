from __future__ import annotations

import json
import random
import re
import textwrap
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
import streamlit as st
import pandas as pd 

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
page_title="🎒 Grade 5 Tutor (Math & ELA)", page_icon="🎒", layout="wide"
)

