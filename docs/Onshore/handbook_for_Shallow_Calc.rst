Terzaghi
----------
- Eqiation

  - strip: qu = c'Nc + qNq + 0.5GBNg
  - square: qu = c'Nc*1.3 + qNq + 0.5GBNg*0.8
  - circle: qu = c'Nc*1.3 + qNq + 0.5GBNg*0.6
  
- Correction

  - q & g terms must be adjusted by ground water table
  - which consider the soil under the footing up to Df + B.

- Notice

  - Terzaghi introduced **original NcNqNg**, but **no longer used**.

Meyerhof
-----------
- Main Features
  - suggested to add correction factors to Terzaghi approach.
  - Updated NcNqNg table is important and widely used.
  
- Equation
  - Nq = (tan(45+phi/2))^2*exp(pi*tan(phi))
  - Nc = (Nq-1)cot(phi)
  - Ng = 2(Nq+1)tan(phi)

FHWA
--------------------------

Main Features
..............

- Equation is same, but a little different order.
  
  - q_ult = c Nc + 0.5 G B Ng + q Nq
  
- FHWA uses correction factor of GWT.

  - Thus, surcharge term q uses total unit weight ???? (Not Sure)



Correction Factors
...................

  - Footing shape
  
    - Strip: sc,sg,sq = (C) 1, 1, 1 / (NC) 1, 0.6 ,1 
    - Square: sc,sg,sq = (C) 1.2, 1, 1 / (NC) 1+(Nq/Nc), 0.6 ,1+tan(phi) 
    
  - Ground water table
  - Embedment depth
  - Sloping
  
.. image:: ./images/GEC06-Table_5-2_Shape_factor.png
   :width: 600
   
.. image:: ./images/GEC06-Table_5-3_Groundwater_factor.png
   :width: 400
   
.. image:: ./images/GEC06-Table_5-4_Depth_Factor.png
   :width: 400
