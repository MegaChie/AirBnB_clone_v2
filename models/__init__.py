#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This module instantiates an object of class FileStorage"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()