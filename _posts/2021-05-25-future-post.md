---
title: 'How to make a Sankey Diagram on Tableau'
date: 2021-05-25
permalink: /Tableau-Sankey-Diagram
tags:
  - Tableau
  - Sankey
  - Chart
  - Diagram
  - Data analysis
  - Flux
---
How to create a Sankey diagram and not waste your time miserably.

Right, so here we are. After several attempts and a myriad of hours trying to come up with a good solution to create a Sankey Diagram in Tableau to show the flux of information generated back at my workplace, I found a way that puts together several sources (some of which I cannot find again) which help in creating a Sankey Diagram. Here I will explain clearly many of the steps necessary to come up with this beautiful piece of viz. Hopefully this will help you and save you many hours of wasted hours looking at outdated sources with people doubling their data (that's just nonsense imo).

So, first of all we need some data. As you may know by now, some people will tell you to duplicate your data so that you can match your data from the left side to the same data on the right of the diagram. This might become inconvenient if you have hundreds of thousands of rows or if you do not want to filter half of your data for the remainder of the sheets. 
It doesn't matter if you divide your flux by hierarchies or just completely unrelated labels, for the time being, we will do the basics and then give pointers into how to modify this<sup>[1](#footnote1)</sup>.


1. Select what will be the measure that you will be using to divide your data. For example, to study things like the flux of calls, you need to make use of SUM(\[Number of records\]). If you prefer to do it on another measure (like the sales amount) things actually simplify.

2. Create a **Path Frame**: 
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

3. We now need to create bins out of this field. To do so make a right click on *Path Frame*, *Create*, *Bins...* . Now modify the bin size to 1. It should look something like this:
<img src='https://github.com/cuspime/cuspime.github.io/blob/master/S1.png?raw=true' width='50%' align='center' >
</img>

4. Create a Field named **Path Index** which is simply defined as INDEX():
```Tableau 
Path Index
INDEX()
```

5. Create a Field **T** which will work as the independent variable of the diagram.
```Tableau
T
IF [Path Index] < 50
THEN -6 + (([Path Index]-1)%49)/4
ELSE  6 - (([Path Index]-1)%49)/4
END
```

6. Create a field named **Sigmoid** which will be used as the dependent variable of the diagram. This will define the smoothness of the transition of the curves:
```Tableau
Sigmoid
1/(1+EXP(-[T]) )
```

7. Create a field **Sankey Arm Size**. If you have decided to divide your Sankey diagram taking into account something different to the number of records, you should change here the *SUM( \[Number of Records\] )* with whatever your field is.
```Tableau
Sankey Arm Size
SUM( [Number of Records] ) / TOTAL(SUM([Number of Records]))
```

8. Create a field named **Sankey Polygons**
```Tableau
Sankey Polygons
IF [Path Index] > 49
THEN [Max Position 1 Wrap]+([Max Position 2 Wrap]-[Max Position 1 Wrap])*[Sigmoid]
ELSE [Min Position 1 Wrap]+([Min Position 2 Wrap]-[Min Position 1 Wrap])*[Sigmoid]
END
```

9. We now need to create 10 fields. If you prefer, you can create those with 1 in its name and duplicate them while changing in their definitions from 1 to 2 where referenced. Stay with me, It'll all be worth it.

```Tableau
Max for Min Position 1:
RUNNING_SUM([Sankey Arm Size])

Max Position 1:
RUNNING_SUM([Sankey Arm Size])

Max Position 1 Wrap :
WINDOW_SUM([Max Position 1])

Min Position 1:
RUNNING_SUM([Max for Min Position 1])-[Sankey Arm Size]

Min Position 1 Wrap:
WINDOW_SUM([Min Position 1])

Max for Min Position 2:
RUNNING_SUM([Sankey Arm Size])

Max Position 2:
RUNNING_SUM([Sankey Arm Size])

Max Position 2 Wrap:
WINDOW_SUM([Max Position 2])

Min Position 2:
RUNNING_SUM([Max for Min Position 2])-[Sankey Arm Size]

Min Position 2 Wrap:
WINDOW_SUM([Min Position 2])
```

10. Now, in a new sheet drag **T** to the Columns and **Sankey Polygons** to the Rows
11. Change the Marks Card to **Polygons**
12. Drag **Path Index** to the Path Mark (or put it in the marks card and change its type to Path)
13. Now put the subdivisions you want on the left of the Sankey diagram on top of the Marks card, immediately below the subdivisions you want on the right of the diagram, the **Path Index** and the **Path Frame (bin)** in **that specific order**. I know this might be somewhat confusing so hopefully this image might help:
<img src='https://github.com/cuspime/cuspime.github.io/blob/master/images/Screenshot%202021-05-25%20at%2015.52.28.png?raw=true' width='70%' align='center' >
</img>

**NB**: As you can see, in this tutorial we have decided to go from a division of the data by *Tipo fuori orario* to a division by *Tipo Gestito*.

14. Next, right click on **T** and Compute it using *Path Frame (bin)*
15. Now here comes the fun part. To make this all happen you need to tell all the Sankey Polygons' dependencies to be calculated in a very, very specific way. To be able to do it, you need to right click on it and **Edit Table Calculation**.
16. Make sure all your calculations match the following order (remember that your left and right subdivisions have to match the placement of *Tipo fuori orario* and *Tipo Gestito* respectively):
<img src='https://github.com/cuspime/cuspime.github.io/blob/master/images/Screenshot%202021-05-25%20at%2016.22.16.png?raw=true' width='90%' align='center' >
</img>

Even though it is hard to go one by one, you'll get there. Just make sure all the fields are in the correct order.


When you complete all these steps you'll end up with something like this
<img src='https://github.com/cuspime/cuspime.github.io/blob/master/images/Screenshot%202021-05-25%20at%2016.25.21.png?raw=true' width='90%' align='center' >
</img>

If you don't, here there are some potential sources of error (I'll write them down in ascending time consumption when looking for mistakes):
* In the sheet you did not put your the fields in order in the Marks card.
* You have not Computed **T** with **Path Frame (bin)**
* Either of the fields that you are using to divide the data is not being used for detail or colour
* You have messed up the order of the fields within the calculations or you have selected fields that shouldn't be considered inside some subcalculations. Make sure you have the equivalent of the last image shown.
* You have to add granularity to the LOD calculation for the Path Frame to ensure your data creates at least one entry value with Path Frame 0 and at least one more with value 97. This is the most troublesome of the calculations and, when combined with other filters on the dashboard can lead to problems of this calculation.

17. After you get this diagram, make sure to create another 2 sheets with a column that divided in the same order as your Sankey diagram on the left or right.

So go have fun with Sankey Diagrams!






 
 
 
 

 

***
<a name="footnote1">1</a>: The core information on how to do this viz was beautifully gathered by [Ian Baldwin](https://www.theinformationlab.co.uk/2018/03/09/build-sankey-diagram-tableau-without-data-prep-beforehand/).
