---
title: 'How to make a Sankey Diagram on Tableau'
date: 2021-04-04
permalink: /Tableau-Sankey-Diagram
tags:
  - Tableau
  - Sankey
  - Chart
  - Diagram
  - Data analysis
  - Flux
---

Right, so here we are. After several attempts and a myriad of hours trying to come up with a good solution to create a Sankey Diagram in Tableau to show the flux of information generated back at my workplace, I found a way that puts together several sources (some of which I cannot find again) which help in creating a Sankey Diagram. Here I will explain clearly many of the steps necessary to come up with this beautiful piece of viz. Hopefully this will help you and save you many hours of wasted hours looking at outdated sources with people doubling their data (that's just nonsense imo).

So, first of all we need some data. As you may know by now, some people will tell you to duplicate your data so that you can match your data from the left side to the same data on the right of the diagram. This might become inconvenient if you have hundreds of thousands of rows or if you do not want to filter half of your data for the remainder of the sheets. 
The Superstore that comes along Tableau is the usual go-to so we will stick to it. 

Most of the instructions follow the recipe written by [Ian Baldwin](https://www.theinformationlab.co.uk/2018/03/09/build-sankey-diagram-tableau-without-data-prep-beforehand/)
