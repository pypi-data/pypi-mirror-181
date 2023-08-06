#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

def _findRawContent(item):
	if item.has_attr('content'):
		title = item['content'].strip()
		if title:
			return title
	if item.find('div', class_='title'):
		return item.find('div', class_='title').text.strip()
	return item.text.strip()

def _seemsValidText(soup, limit=500):
	if not soup:
		return False
	return soup.text and len(soup.text) > limit
