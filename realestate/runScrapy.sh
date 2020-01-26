#!/bin/bash

source $HOME/scrapy/bin/activate
cd $HOME/reality/realestate
scrapy crawl topreality && scrapy crawl nehnutelnosti && scrapy crawl byty
