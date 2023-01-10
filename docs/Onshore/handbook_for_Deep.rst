GeoSon_Deep
==================

.. toctree:
    :maxdepth: 2
    
    Installations
    
    Lateral Capacity

    Axial Capacity

    
    

Installations
------------------

Driven Pile
............

- H pile
- Timber pile
- Precase Prestressed Concrete Pile


Drilled Shaft
.............

- Auger Cast Pile
    - Continuous Flight Auger Cast (CFA)
    - Displacement Auger Cast (DACP)
- Drilled Shafts
  - Cast-In Drilled-Hole (CIDH)
- Micropiles
- Helical Piles


Lateral Capacity
------------------
- Failure mechanisms: short/long
- p-y analysis
- Cyclic loading
- Group effect

Axial Capacity
------------------

Topics
.......

- API method
- FHWA method
- t-z modelling
- Downdrag force
- Frost Heave
- Cyclic loading
- Group effect

Driven Pile
............

- CLAY
    - alpha (Tomlinson,1980)
    - beta* (Ersig_Kirby,1979)
    - lambda (1972)
- SAND
    - (Meyerhof,1976)
    - (Nordlund,1963)
- Mixed
    - API is for offshore
    - beta** <-- Nt (Fellenius,1991)(Fellenius,2014)
    - Brown <-- SPT
    - CPT (Schmertmann,1975)(Elsami_Fellenius,1997)

Drilled Shaft
.............

- CLAY
    - alpha
        - Su(UU)/Su(CIUC) = 0.911 + 0.499*log(Su(UU)/s'v) (Chen_Kulhawy,1993)
        - alpha = 0.30 + 0.17/(Su(CIUC)/Pa)

- SAND
    - beta: SPT value is required
        - N1_60 = N60*(Pa/s'v)^0.5 (Liao_Whitman,1986)
        - phi = 27.5+9.2*log(N1_60) (Chen_Kulhawy,2002)
        - phi = (arctan(N/(12.2+20.3*(s'v/Pa))))^0.34 (Kulhawy_Mayne,1990)
        - K0 = 1-sin(phi)
        - s'p = 2116*0.47*N60^0.8
        - OCR = s'p/s'v


References
-----------
