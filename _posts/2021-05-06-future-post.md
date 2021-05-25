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

1. To *reuse* the hard work done for this viz, you can **create 2 parameters** that will work as selectors to divide your data. It is much better if you just create a list of integers. These integers can then be asked to be displayed as a string within Tableau.
2. Now create two (very similar) fields, one for each selector parameter created:
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
3. Select what will be the measure that you will be using to divide your data. To know study things like the flux of calls, you need to make use of SUM(\[Number of records\]). If you prefer to do it on another measure, things actually simplify.
4. Create a **Path Frame**: 
```Tableau
Path Frame
IF {FIXED  [Dimension_1]: SUM([Number of Records])} 
= 
{FIXED [Granularity_1],[Granularity_2]: 
    (MAX( {FIXED  [Dimension_1]: SUM([Number of Records] ) 
          } ) )
} 
THEN 0 ELSE 97 END
```
  For this calculation aims to ensure that the data can be divided by **\[Dimension_1\]** in 2. The easiest way of achieving it is by comapring the entries to its minimum (however it is not guaranteed that this will indeed be the case). **If for some reason you do not get a Sankey Diagram at the end, then you surely have to modify this field**. Try and change the **LOD** and keep adding fields like **\[Granularity_n\]**.

5. We now need to create bins out of this field. To do so make a right click on *Path Frame*, *Create*, *Bins...* . Now modify the bin size to 1. It should look something like this:
<img src='https://github.com/cuspime/cuspime.github.io/blob/master/S1.png?raw=true' width='50%' align='center' >
</img>

6. Create a Field named **Path Index** which is simply defined as INDEX():
```Tableau 
Path Index
INDEX()
```

7. Create a Field **T** which will work as the independent variable of the diagram.
```Tableau
T
IF [Path Index] < 50
THEN -6 + (([Path Index]-1)%49)/4
ELSE  6 - (([Path Index]-1)%49)/4
END
```

8. Create a field named **Sigmoid** which will be used as the dependent variable of the diagram. This will define the smoothness of the transition of the curves:
```Tableau
Sigmoid
1/(1+EXP(-[T]) )
```

9. Create a field **Sankey Arm Size**. If you have decided to divide your Sankey diagram taking into account something different to the number of records, you should change here the *SUM( \[Number of Records\] )* with whatever your field is.
```Tableau
Sankey Arm Size
SUM( [Number of Records] ) / TOTAL(SUM([Number of Records]))
```

10. Create a field named **Sankey Polygons**
```Tableau
Sankey Polygons
IF [Path Index] > 49
THEN [Max Position 1 Wrap]+([Max Position 2 Wrap]-[Max Position 1 Wrap])*[Sigmoid]
ELSE [Min Position 1 Wrap]+([Min Position 2 Wrap]-[Min Position 1 Wrap])*[Sigmoid]
END
```











***
<a name="footnote1">1</a>: The core information on how to do this viz was beautifully gathered by [Ian Baldwin](https://www.theinformationlab.co.uk/2018/03/09/build-sankey-diagram-tableau-without-data-prep-beforehand/).
