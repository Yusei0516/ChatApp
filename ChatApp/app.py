from flask import Flask, request, redirect, render_remplate, session, flash, abort, url_for
from datetime import timedelta
import hashlib, uuid, re, os
