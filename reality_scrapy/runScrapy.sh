#!/bin/bash

source $HOME/scrapy/bin/activate
cd $HOME/reality/reality_scrapy
scrapy crawl topreality && scrapy crawl nehnutelnosti && scrapy crawl byty && scrapy crawl bazos
