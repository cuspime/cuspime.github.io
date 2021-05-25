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
It doesn't matter if you divide your flux by hierarchies or just completely unrelated labels, for the time being, we will do the basics and then give pointers into how to modify this<sup>[1](#footnote1)</sup>.

To *recycle* the hard work done for this viz, you can **create 2 parameters** that will work as selectors to divide your data. This is usually done as a list of integers which can be displayed as a string within Tableau. You can then create two very similar fields, one for each selector
```Tableau
Dimension 1
CASE [Select Dimension 1]
  WHEN 1 THEN [Region]
  WHEN 2 THEN [Category]
  //...
END

Dimension 2
CASE [Select Dimension 2]
  WHEN 1 THEN [Region]
  WHEN 2 THEN [Category]
  //...
END
```




***
<a name="footnote1">1</a>: The core information on how to do this viz was beautifully gathered by [Ian Baldwin](https://www.theinformationlab.co.uk/2018/03/09/build-sankey-diagram-tableau-without-data-prep-beforehand/).
