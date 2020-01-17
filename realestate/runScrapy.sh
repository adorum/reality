#!/bin/bash

source $HOME/.pyenv/versions/scrapy/bin/activate
cd $HOME/projects/reality/realestate
scrapy crawl topreality && scrapy crawl topreality
