.. rst-class:: sphx-glr-example-title

.. _sphx_glr_examples_meltsweb.py:


Interfacing with the Melts Web Services
=========================================

The MELTS web services provide the ability to conduct melting and fractionation
computations using whole-rock major element compositions. Some information can be found
`here <http://melts.ofm-research.org/web-services.html>`__. The MELTS WS Compute web
service can be found
`here <http://thermofit.ofm-research.org:8080/multiMELTSWSBxApp/Compute>`__.  A minimal
interface to this web service is provided in :mod:`pyrolite.ext.alphamelts.web`.
The basic functionality of this is demonstrated below (obtaining valid phases and oxides
for a specific model of MELTS, and performing a single computation). Here we use a
dictionary to pass information to the service; this can be customised to your use case.


.. code-block:: default

    from pyrolite_meltsutil.web import *

    def default_datadict():
        d = {}
        d["title"] = ("TestREST",)
        d["initialize"] = {
            "SiO2": 48.68,
            "TiO2": 1.01,
            "Al2O3": 17.64,
            "Fe2O3": 0.89,
            "Cr2O3": 0.0425,
            "FeO": 7.59,
            "MnO": 0.0,
            "MgO": 9.10,
            "NiO": 0.0,
            "CoO": 0.0,
            "CaO": 12.45,
            "Na2O": 2.65,
            "K2O": 0.03,
            "P2O5": 0.08,
            "H2O": 0.20,
        }
        d["calculationMode"] = "findLiquidus"
        d["constraints"] = {"setTP": {"initialT": 1200, "initialP": 1000}}
        return d


    D = default_datadict()







To obtain a list of phases or oxides for a specific model of MELTS (defaulting to
rhyolite-MELTS version 1.0.2, can be changed with a `modelSelection` parameter; see
below), you can use the Phases and Oxides services:



.. code-block:: default

    melts_oxides(D)




.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    ['SiO2', 'TiO2', 'Al2O3', 'Fe2O3', 'Cr2O3', 'FeO', 'MnO', 'MgO', 'NiO', 'CoO', 'CaO', 'Na2O', 'K2O', 'P2O5', 'H2O', 'CO2', 'SO3', 'Cl2O-1', 'F2O-1']




.. code-block:: default

    melts_phases(D)




.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    ['olivine', 'fayalite', 'sphene', 'garnet', 'melilite', 'orthopyroxene', 'clinopyroxene', 'aegirine', 'aenigmatite', 'cummingtonite', 'amphibole', 'hornblende', 'biotite', 'muscovite', 'feldspar', 'quartz', 'tridymite', 'cristobalite', 'nepheline', 'kalsilite', 'leucite', 'corundum', 'sillimanite', 'rutile', 'perovskite', 'spinel', 'rhm-oxide', 'ortho-oxide', 'whitlockite', 'apatite', 'water', 'alloy-solid', 'alloy-liquid']



The compute service is also simple to access, and can be customised to provide
different versions of MELTS and different computation modes
(:code:`"findLiquidus", "equilibrate", "findWetLiquidus"`).



.. code-block:: default

    melts_compute(D)




.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    OrderedDict([('status', 'Success: Find liquidus'), ('sessionID', '596494845.959248.846930886'), ('title', 'TestREST'), ('time', 'Tue Nov 26 13:00:45 2019'), ('release', 'MELTS Web Services, MELTS v.1.0.x'), ('buildDate', 'Sep 27 2016'), ('buildTime', '08:37:35'), ('temperature', 1229.4921875), ('pressure', 1000), ('log_fO2', 0), ('deltaHM', 2.3904448726254035), ('deltaNNO', 7.230776039289125), ('deltaFMQ', 7.90281702750676), ('deltaCOH', 10.111657465859615), ('deltaIW', 11.387343272423262), ('liquid', OrderedDict([('mass', 100.36249999999914), ('density', 2.678695226570551), ('viscosity', 2.074298416297876), ('gibbsFreeEnergy', -1649909.033880872), ('enthalpy', -1239348.1080483224), ('entropy', 273.22600766028984), ('volume', 37.46693502287309), ('dvdt', 0.0027303073383925327), ('dvdp', -0.00022741935320387744), ('d2vdt2', 5.663692390045417e-08), ('d2vdtdp', -1.14190293669883e-08), ('d2vdp2', 9.204498389545907e-09), ('heatCapacity', 153.16796061100376), ('SiO2', 48.50417237514078), ('TiO2', 1.00635197409391), ('Al2O3', 17.576285963382844), ('Fe2O3', 0.8867854029144667), ('Cr2O3', 0.04234649395939756), ('FeO', 7.56258562710062), ('MgO', 9.067131647776886), ('CaO', 12.405031759870697), ('Na2O', 2.6404284468800805), ('K2O', 0.02989164279486886), ('P2O5', 0.07971104745298291), ('H2O', 0.199277618632459)])), ('system', OrderedDict([('mass', 100.36249999999914), ('density', 2.678695226570551), ('viscosity', 2.074298416297876), ('gibbsFreeEnergy', -1649909.033880872), ('enthalpy', -1239348.1080483224), ('entropy', 273.22600766028984), ('volume', 37.46693502287309), ('dvdt', 0.0027303073383925327), ('dvdp', -0.00022741935320387744), ('d2vdt2', 5.663692390045417e-08), ('d2vdtdp', -1.14190293669883e-08), ('d2vdp2', 9.204498389545907e-09), ('heatCapacity', 153.16796061100376)])), ('potentialSolid', [OrderedDict([('name', 'olivine'), ('formula', "(Ca-0.0Mg-0.0Fe''0.20Mn0.27Co0.27Ni0.27)2SiO4"), ('affinity', 725.0794789734882), ('density', 4.367508919977463), ('gibbsFreeEnergy', 7081700.983626623), ('enthalpy', 4781379.714013856), ('entropy', -1530.8509828543376), ('volume', -175.80341400663093), ('dvdt', -0.00672059825576166), ('dvdp', 0.00011944382718172318), ('d2vdt2', 2559.9999982251943), ('d2vdtdp', 0), ('d2vdp2', -0.0010681152314939884), ('heatCapacity', -712.1878634399751), ('SiO2', 29.072788440078867), ('FeO', 13.647042376409999), ('MnO', 18.47754025478575), ('MgO', -0.07344087459470887), ('NiO', 19.460058388253472), ('CoO', 19.518196788940127), ('CaO', -0.10218537387348572), ('component', [OrderedDict([('name', 'tephroite'), ('formula', 'Mn2SiO4'), ('moleFraction', -1)]), OrderedDict([('name', 'fayalite'), ('formula', 'Fe2SiO4'), ('moleFraction', -0.7292301861862682)]), OrderedDict([('name', 'co-olivine'), ('formula', 'Co2SiO4'), ('moleFraction', -1)]), OrderedDict([('name', 'ni-olivine'), ('formula', 'Ni2SiO4'), ('moleFraction', -1)]), OrderedDict([('name', 'monticellite'), ('formula', 'CaMgSiO4'), ('moleFraction', 0.013990926821801938)]), OrderedDict([('name', 'forsterite'), ('formula', 'Mg2SiO4'), ('moleFraction', 0)])])]), OrderedDict([('name', 'fayalite'), ('formula', 'Fe2SiO4'), ('affinity', 35816.08519423078), ('density', 4.236305222142011), ('gibbsFreeEnergy', -1901663.2427676737), ('enthalpy', -1258445.4221051754), ('entropy', 428.05787433177477), ('volume', 48.10255383273913), ('dvdt', 0.0017267618504064346), ('dvdp', -4.582805467578152e-05), ('d2vdt2', 3.94698010392075e-07), ('d2vdtdp', -1.0475238375467179e-08), ('d2vdp2', 2.7801158387866883e-10), ('heatCapacity', 199.1981820589044), ('SiO2', 29.485305267373498), ('FeO', 70.51469473262651), ('component', OrderedDict([('name', 'fayalite'), ('formula', 'Fe2SiO4'), ('moleFraction', 1)]))]), OrderedDict([('name', 'sphene'), ('formula', 'CaTiSiO5'), ('affinity', 40034.48154957197), ('density', 3.4213046650926686), ('gibbsFreeEnergy', -2997228.350602335), ('enthalpy', -2363829.327156818), ('entropy', 421.52351951420036), ('volume', 57.30635508740625), ('dvdt', 0.00140238), ('dvdp', -3.28335e-05), ('d2vdt2', 0), ('d2vdtdp', 0), ('d2vdp2', 0), ('heatCapacity', 205.69071245063552), ('SiO2', 30.645482945489366), ('TiO2', 40.75169907554995), ('CaO', 28.602817978960676), ('component', OrderedDict([('name', 'sphene'), ('formula', 'CaTiSiO5'), ('moleFraction', 1)]))]), OrderedDict([('name', 'garnet'), ('formula', "(Ca0.55Fe''0.45Mg0.00)3Al2Si3O12"), ('affinity', 21167.102354018574), ('density', 3.756369449487527), ('gibbsFreeEnergy', -2883570.086291271), ('enthalpy', -2225859.363532077), ('entropy', 437.7028198931714), ('volume', 51.49220892101746), ('dvdt', 0.0018568667113258944), ('dvdp', -3.0234022190670385e-05), ('d2vdt2', 7.675856636432794e-07), ('d2vdtdp', 0), ('d2vdp2', 1.0604880620443246e-10), ('heatCapacity', 212.32090606497235), ('SiO2', 38.209226747661205), ('Al2O3', 21.6133092283218), ('FeO', 20.574040238054003), ('CaO', 19.603423785963), ('component', [OrderedDict([('name', 'almandine'), ('formula', 'Fe3Al2Si3O12'), ('moleFraction', 0.18463037030206317)]), OrderedDict([('name', 'grossular'), ('formula', 'Ca3Al2Si3O12'), ('moleFraction', 0.22538091509037092)]), OrderedDict([('name', 'pyrope'), ('formula', 'Mg3Al2Si3O12'), ('moleFraction', 0)])])]), OrderedDict([('name', 'melilite'), ('formula', 'Na0.00Ca2.00Al0.41Mg0.35Fe0.44Si1.79O7'), ('affinity', 22634.094509413568), ('density', 2.986071218052302), ('gibbsFreeEnergy', -1983829.8228457058), ('enthalpy', -1510907.3385027049), ('entropy', 314.7272772434397), ('volume', 43.228400124099466), ('dvdt', 0.0015724573604369515), ('dvdp', -3.418608120920956e-05), ('d2vdt2', 4.504297686961943e-07), ('d2vdtdp', 0), ('d2vdp2', 2.990159043446068e-11), ('heatCapacity', 142.16012019565147), ('SiO2', 37.588755043603875), ('Al2O3', 7.30727074827661), ('FeO', 11.021516021992545), ('MgO', 4.980120921362733), ('CaO', 39.10233726476424), ('component', [OrderedDict([('name', 'akermanite'), ('formula', 'Ca2MgSi2O7'), ('moleFraction', 0.1594985545843497)]), OrderedDict([('name', 'gehlenite'), ('formula', 'Ca2Al2SiO7'), ('moleFraction', 0.09251012000896448)]), OrderedDict([('name', 'iron-akermanite'), ('formula', 'Ca2FeSi2O7'), ('moleFraction', 0.198018446291261)]), OrderedDict([('name', 'soda-melilite'), ('formula', 'Na2Si3O7'), ('moleFraction', 0)])])]), OrderedDict([('name', 'orthopyroxene'), ('formula', "opx Na0.00Ca0.95Fe''-0.0Mg0.32Fe'''0.74Ti0.03Al0.79Si1.20O6"), ('affinity', 2963.816848319897), ('density', 3.458289820784237), ('gibbsFreeEnergy', -4231789.715050029), ('enthalpy', -3227344.6580480216), ('entropy', 668.4525866221938), ('volume', 83.72177296333842), ('dvdt', 0.0030148997305712967), ('dvdp', -6.943906878829836e-05), ('d2vdt2', 9.493121234183983e-07), ('d2vdtdp', 1.1156217980101426e-25), ('d2vdp2', 3.299284374527222e-10), ('heatCapacity', 324.49339375685565), ('SiO2', 30.438878892335296), ('TiO2', 0.9921304048101884), ('Al2O3', 17.057187619436334), ('Fe2O3', 24.82718084382543), ('FeO', -1.290309130858682), ('MgO', 5.4639118259946935), ('CaO', 22.51101954445675), ('component', [OrderedDict([('name', 'diopside'), ('formula', 'CaMgSi2O6'), ('moleFraction', 0.24377467798302502)]), OrderedDict([('name', 'clinoenstatite'), ('formula', 'Mg2Si2O6'), ('moleFraction', 0.056391578940377836)]), OrderedDict([('name', 'hedenbergite'), ('formula', 'CaFeSi2O6'), ('moleFraction', -0.05199823013709002)]), OrderedDict([('name', 'alumino-buffonite'), ('formula', 'CaTi0.5Mg0.5AlSiO6'), ('moleFraction', 0.07018078847388216)]), OrderedDict([('name', 'buffonite'), ('formula', 'CaTi0.5Mg0.5FeSiO6'), ('moleFraction', 0.0017240808412823483)]), OrderedDict([('name', 'essenite'), ('formula', 'CaFeAlSiO6'), ('moleFraction', 0.8985474204644843)]), OrderedDict([('name', 'jadeite'), ('formula', 'NaAlSi2O6'), ('moleFraction', 0)])])]), OrderedDict([('name', 'clinopyroxene'), ('formula', "cpx Na0.00Ca0.79Fe''-0.1Mg0.81Fe'''0.45Ti0.13Al0.68Si1.30O6"), ('affinity', 1979.8797384295772), ('density', 3.3384404739443485), ('gibbsFreeEnergy', -1856827.2043336057), ('enthalpy', -1432930.007914002), ('entropy', 282.1012213991254), ('volume', 34.60672859933411), ('dvdt', 0.0012403340828379657), ('dvdp', -2.7495692889570552e-05), ('d2vdt2', 4.0129326238146657e-07), ('d2vdtdp', 9.457549198946089e-26), ('d2vdp2', 1.222697384621135e-10), ('heatCapacity', 136.47069220449552), ('SiO2', 34.79298833472624), ('TiO2', 4.7886386540446715), ('Al2O3', 15.354922453233375), ('Fe2O3', 16.171616090496613), ('FeO', -5.564255180049923), ('MgO', 14.61942182652983), ('CaO', 19.83666782101921), ('component', [OrderedDict([('name', 'diopside'), ('formula', 'CaMgSi2O6'), ('moleFraction', 0.1379162158689312)]), OrderedDict([('name', 'clinoenstatite'), ('formula', 'Mg2Si2O6'), ('moleFraction', 0.10595313863504739)]), OrderedDict([('name', 'hedenbergite'), ('formula', 'CaFeSi2O6'), ('moleFraction', -0.08947592790410104)]), OrderedDict([('name', 'alumino-buffonite'), ('formula', 'CaTi0.5Mg0.5AlSiO6'), ('moleFraction', 0.1262331335785882)]), OrderedDict([('name', 'buffonite'), ('formula', 'CaTi0.5Mg0.5FeSiO6'), ('moleFraction', 0.012252904186240348)]), OrderedDict([('name', 'essenite'), ('formula', 'CaFeAlSiO6'), ('moleFraction', 0.22174065234225426)]), OrderedDict([('name', 'jadeite'), ('formula', 'NaAlSi2O6'), ('moleFraction', 0)])])]), OrderedDict([('name', 'aegirine'), ('formula', 'NaFeSi2O6'), ('affinity', 137826.333702471), ('density', 0.36096093566885945), ('gibbsFreeEnergy', -3035099.219976642), ('enthalpy', -2225754.650026077), ('entropy', 538.6142999865464), ('volume', 639.97), ('dvdt', 0), ('dvdp', 0), ('d2vdt2', 0), ('d2vdtdp', 0), ('d2vdp2', 0), ('heatCapacity', 263.12688098198424), ('SiO2', 52.020099896901264), ('Fe2O3', 34.564787293662405), ('Na2O', 13.415112809436321), ('component', OrderedDict([('name', 'aegirine'), ('formula', 'NaFeSi2O6'), ('moleFraction', 1)]))]), OrderedDict([('name', 'aenigmatite'), ('formula', 'Na2Fe5TiSi6O20'), ('affinity', 136212.14334900957), ('density', 3.7699873985980936), ('gibbsFreeEnergy', -10492582.880197857), ('enthalpy', -7442315.918095419), ('entropy', 2029.9356609821245), ('volume', 228.54600000000002), ('dvdt', 0), ('dvdp', 0), ('d2vdt2', 0), ('d2vdtdp', 0), ('d2vdp2', 0), ('heatCapacity', 924.1539441517609), ('SiO2', 41.840679893032586), ('TiO2', 9.273138225896679), ('FeO', 41.69284133384664), ('Na2O', 7.193340547224097), ('component', OrderedDict([('name', 'aenigmatite'), ('formula', 'Na2Fe5TiSi6O20'), ('moleFraction', 1)]))]), OrderedDict([('name', 'cummingtonite'), ('formula', "(Fe''0.00Mg1.00)7Si8O22(OH)2"), ('affinity', 135202.6319835514), ('density', 2.8464260437026576), ('gibbsFreeEnergy', 10704883.727696454), ('enthalpy', 8405774.357622461), ('entropy', -1530.0444704664537), ('volume', -211.36241481056885), ('dvdt', -0.00877551521779244), ('dvdp', 0.00023115205435870903), ('d2vdt2', -2.551917242145984e-06), ('d2vdtdp', 0), ('d2vdp2', 0), ('heatCapacity', -801.4274609180233), ('SiO2', 61.56017440118108), ('MgO', 36.13261128935672), ('H2O', 2.3072143094622013), ('component', [OrderedDict([('name', 'cummingtonite'), ('formula', 'Mg7Si8O22(OH)2'), ('moleFraction', -0.7705068696677079)]), OrderedDict([('name', 'grunerite'), ('formula', 'Fe7Si8O22(OH)2'), ('moleFraction', 0)])])]), OrderedDict([('name', 'amphibole'), ('formula', 'cAph Ca-0.0Fe-232Mg239.Si8O22(OH)2'), ('affinity', 123811.93782141982), ('density', 41.31226126292197), ('gibbsFreeEnergy', 'nan'), ('enthalpy', 'nan'), ('entropy', 'nan'), ('volume', 4.031735761472852), ('dvdt', -0.003233877459821707), ('dvdp', -0.00012751047755486225), ('d2vdt2', -2.8816565942849933e-06), ('d2vdtdp', 0), ('d2vdp2', 4.084863571922726e-09), ('heatCapacity', 22.73319588966092), ('SiO2', -7.339174364704158), ('FeO', 254.93593694149305), ('MgO', -147.32169759722058), ('H2O', -0.2750649795683264), ('component', [OrderedDict([('name', 'cummingtonite'), ('formula', 'Mg7Si8O22(OH)2'), ('moleFraction', -0.869735590568263)]), OrderedDict([('name', 'grunerite'), ('formula', 'Fe7Si8O22(OH)2'), ('moleFraction', 0.8443043678712879)]), OrderedDict([('name', 'tremolite'), ('formula', 'Ca2Mg5Si8O22(OH)2'), ('moleFraction', 0)])])]), OrderedDict([('name', 'hornblende'), ('formula', 'NaCa2Mg3.89Fe2+0.11Al1.00Fe3+0.00Al2Si6O22(OH)2'), ('affinity', 81365.9091126849), ('density', 2.9424702761703276), ('gibbsFreeEnergy', 'nan'), ('enthalpy', 'nan'), ('entropy', 'nan'), ('volume', 29.33792254249651), ('dvdt', 0.0013529369575475815), ('dvdp', -3.8987582370427095e-05), ('d2vdt2', 5.536225870396054e-07), ('d2vdtdp', 0), ('d2vdp2', 1.959730953939338e-10), ('heatCapacity', 111.43466464339964), ('SiO2', 42.953363299640195), ('Al2O3', 18.22264677435004), ('FeO', 0.9409430556450107), ('MgO', 18.68082300173162), ('CaO', 13.36344015450431), ('Na2O', 3.692317747379661), ('H2O', 2.1464659667491572), ('component', [OrderedDict([('name', 'pargasite'), ('formula', 'NaCa2Mg4AlAl2Si6O22(OH)2'), ('moleFraction', 0.10002878553432219)]), OrderedDict([('name', 'ferropargasite'), ('formula', 'NaCa2Fe4AlAl2Si6O22(OH)2'), ('moleFraction', 0.002826440062821175)]), OrderedDict([('name', 'magnesiohastingsite'), ('formula', 'NaCa2Mg4FeAl2Si6O22(OH)2'), ('moleFraction', 0)])])]), OrderedDict([('name', 'biotite'), ('formula', "K(Fe''1.00Mg0.00)3AlSi3O10(OH)2"), ('affinity', 139479.0049375812), ('density', 3.1950806263146565), ('gibbsFreeEnergy', -11437.861809763102), ('enthalpy', -8078.317821347667), ('entropy', 2.235757798072228), ('volume', 0.288719474977139), ('dvdt', 9.564964191635333e-06), ('dvdp', -4.71198766944606e-07), ('d2vdt2', 0), ('d2vdtdp', 0), ('d2vdp2', 0), ('heatCapacity', 1.0786069091174584), ('SiO2', 35.213234633935784), ('Al2O3', 9.959302946627814), ('FeO', 42.106575940858065), ('K2O', 9.201534143180243), ('H2O', 3.519352335398098), ('component', [OrderedDict([('name', 'annite'), ('formula', 'KFe3Si3AlO10(OH)2'), ('moleFraction', 0.001802111097499836)]), OrderedDict([('name', 'phlogopite'), ('formula', 'KMg3Si3AlO10(OH)2'), ('moleFraction', 0)])])]), OrderedDict([('name', 'muscovite'), ('formula', 'KAl2Si3AlO10(OH)2'), ('affinity', 195774.9017905055), ('density', 2.7222383070858047), ('gibbsFreeEnergy', -6929949.878560412), ('enthalpy', -5379610.566299979), ('entropy', 1031.7421706625905), ('volume', 146.31772646914163), ('dvdt', 0.00472294849), ('dvdp', -0.0002406649267733), ('d2vdt2', 0), ('d2vdtdp', 0), ('d2vdp2', 1.2100733e-09), ('heatCapacity', 544.1770652128347), ('SiO2', 45.25422952656276), ('Al2O3', 38.39754451613924), ('K2O', 11.825336196484518), ('H2O', 4.522889760813472), ('component', OrderedDict([('name', 'muscovite'), ('formula', 'KAl2Si3AlO10(OH)2'), ('moleFraction', 1)]))]), OrderedDict([('name', 'feldspar'), ('formula', 'K-0.0Na0.18Ca0.82Al1.82Si2.18O8'), ('affinity', 374.4186806294715), ('density', 2.6759526293795135), ('gibbsFreeEnergy', -4802903.034134931), ('enthalpy', -3783922.014687973), ('entropy', 678.1261886053351), ('volume', 102.8631625456105), ('dvdt', 0.002359193967591223), ('dvdp', -0.00013981053760530444), ('d2vdt2', 8.108200107552146e-07), ('d2vdtdp', 0), ('d2vdp2', 7.018442151296747e-10), ('heatCapacity', 340.0796910302072), ('SiO2', 47.6257234128158), ('Al2O3', 33.66379689316185), ('CaO', 16.660165653534566), ('Na2O', 2.0503140404877653), ('component', [OrderedDict([('name', 'albite'), ('formula', 'NaAlSi3O8'), ('moleFraction', 0.1821145020877655)]), OrderedDict([('name', 'anorthite'), ('formula', 'CaAl2Si2O8'), ('moleFraction', 0.8177381336025658)]), OrderedDict([('name', 'sanidine'), ('formula', 'KAlSi3O8'), ('moleFraction', 0)])])]), OrderedDict([('name', 'quartz'), ('formula', 'SiO2'), ('affinity', 9226.48147238663), ('density', 2.538340058847875), ('gibbsFreeEnergy', -1046498.0378346498), ('enthalpy', -828391.1225105742), ('entropy', 145.1489364124322), ('volume', 23.670705503214418), ('dvdt', 0), ('dvdp', -2.930704121238e-05), ('d2vdt2', 0), ('d2vdtdp', 0), ('d2vdp2', 3.359238e-11), ('heatCapacity', 72.38504883804082), ('SiO2', 100), ('component', OrderedDict([('name', 'quartz'), ('formula', 'SiO2'), ('moleFraction', 1)]))]), OrderedDict([('name', 'tridymite'), ('formula', 'SiO2'), ('affinity', 10195.56569616741), ('density', 2.1841635864416724), ('gibbsFreeEnergy', -1045528.953610869), ('enthalpy', -824373.902663587), ('entropy', 147.17745367925926), ('volume', 27.50906588360731), ('dvdt', 0.00013216973), ('dvdp', -2.0049550553900003e-05), ('d2vdt2', 0), ('d2vdtdp', 0), ('d2vdp2', 2.044539e-10), ('heatCapacity', 73.01369062974815), ('SiO2', 100), ('component', OrderedDict([('name', 'tridymite'), ('formula', 'SiO2'), ('moleFraction', 1)]))]), OrderedDict([('name', 'cristobalite'), ('formula', 'SiO2'), ('affinity', 10199.705884496914), ('density', 2.1948591866104015), ('gibbsFreeEnergy', -1045524.8134225395), ('enthalpy', -824264.5597460669), ('entropy', 147.24746550913173), ('volume', 27.3750135619362), ('dvdt', 8.705969999999999e-05), ('dvdp', -2.9728091211e-05), ('d2vdt2', 0), ('d2vdtdp', 0), ('d2vdp2', 3.0221100000000004e-10), ('heatCapacity', 72.83888938610167), ('SiO2', 100), ('component', OrderedDict([('name', 'cristobalite'), ('formula', 'SiO2'), ('moleFraction', 1)]))]), OrderedDict([('name', 'leucite'), ('formula', 'K0.32Na0.68AlSi2O5.32(OH)1.37'), ('affinity', 24390.397303126207), ('density', 2.2958991694140156), ('gibbsFreeEnergy', -330052.3388745485), ('enthalpy', -225955.13388292637), ('entropy', 69.276109680384), ('volume', 8.029193373488294), ('dvdt', 9.915884568531664e-05), ('dvdp', -1.231311331800022e-05), ('d2vdt2', 0), ('d2vdtdp', 0), ('d2vdp2', 2.0183845335736563e-11), ('heatCapacity', 28.685195610761163), ('SiO2', 54.73312724308386), ('Al2O3', 23.220124525490426), ('Na2O', 9.66278322423486), ('K2O', 6.766670734612595), ('H2O', 5.617294272578268), ('component', [OrderedDict([('name', 'leucite'), ('formula', 'KAlSi2O6'), ('moleFraction', 0.026482756703934504)]), OrderedDict([('name', 'analcime'), ('formula', 'NaAlSi2O5(OH)2'), ('moleFraction', 0.057479478119790296)]), OrderedDict([('name', 'na-leucite'), ('formula', 'NaAlSi2O6'), ('moleFraction', 0)])])]), OrderedDict([('name', 'corundum'), ('formula', 'Al2O3'), ('affinity', 16785.26335491473), ('density', 3.861755783177419), ('gibbsFreeEnergy', -1879607.8393672432), ('enthalpy', -1530254.248243733), ('entropy', 232.49286758329498), ('volume', 26.40282962588254), ('dvdt', 0.0008366601082343749), ('dvdp', -9.829134185e-06), ('d2vdt2', 2.4137287999999996e-07), ('d2vdtdp', 0), ('d2vdp2', 1.9185e-11), ('heatCapacity', 132.02380663614892), ('Al2O3', 100), ('component', OrderedDict([('name', 'corundum'), ('formula', 'Al2O3'), ('moleFraction', 1)]))]), OrderedDict([('name', 'sillimanite'), ('formula', 'Al2SiO5'), ('affinity', 26054.399467931828), ('density', 3.2025677634783913), ('gibbsFreeEnergy', -2926063.2225613487), ('enthalpy', -2359692.241560144), ('entropy', 376.91673088421425), ('volume', 50.59864207962867), ('dvdt', 0.00066926673), ('dvdp', -3.752199e-05), ('d2vdt2', 0), ('d2vdtdp', 0), ('d2vdp2', 0), ('heatCapacity', 206.80089208347067), ('SiO2', 37.07864170068703), ('Al2O3', 62.92135829931297), ('component', OrderedDict([('name', 'sillimanite'), ('formula', 'Al2SiO5'), ('moleFraction', 1)]))]), OrderedDict([('name', 'rutile'), ('formula', 'TiO2'), ('affinity', 36904.21492840187), ('density', 4.110762301120149), ('gibbsFreeEnergy', -1101140.8157395024), ('enthalpy', -856010.5453970958), ('entropy', 163.1328285479849), ('volume', 19.436492345526336), ('dvdt', 0.0005538350357210936), ('dvdp', -8.52232022176e-06), ('d2vdt2', 5.7999475999999995e-08), ('d2vdtdp', 0), ('d2vdp2', 2.198176e-11), ('heatCapacity', 76.45851361724478), ('TiO2', 100), ('component', OrderedDict([('name', 'rutile'), ('formula', 'TiO2'), ('moleFraction', 1)]))]), OrderedDict([('name', 'perovskite'), ('formula', 'CaTiO3'), ('affinity', 38077.51393720857), ('density', 4.043841075358354), ('gibbsFreeEnergy', -1943460.7989078376), ('enthalpy', -1505042.738791994), ('entropy', 291.76477524915987), ('volume', 33.626), ('dvdt', 0), ('dvdp', 0), ('d2vdt2', 0), ('d2vdtdp', 0), ('d2vdp2', 0), ('heatCapacity', 134.33544693137972), ('TiO2', 58.7585362947884), ('CaO', 41.24146370521161), ('component', OrderedDict([('name', 'perovskite'), ('formula', 'CaTiO3'), ('moleFraction', 1)]))]), OrderedDict([('name', 'spinel'), ('formula', "Fe''0.91Mg0.09Fe'''0.03Al0.59Cr1.38Ti0.00O4"), ('affinity', 7.774692862205147), ('density', 4.7869232388102905), ('gibbsFreeEnergy', -2298777.8097413545), ('enthalpy', -1586736.3973672965), ('entropy', 473.8595909906583), ('volume', 48.95621193645829), ('dvdt', 0.00017371948770896045), ('dvdp', -2.2895808590911655e-06), ('d2vdt2', 5.7436238335645225e-08), ('d2vdtdp', 0), ('d2vdp2', 2.2518024952187906e-12), ('heatCapacity', 223.14943047493702), ('Al2O3', 14.643930134430615), ('Fe2O3', 0.9841888329691911), ('Cr2O3', 50.88427177161222), ('FeO', 31.79177994179081), ('MgO', 1.6958293191971472), ('component', [OrderedDict([('name', 'chromite'), ('formula', 'FeCr2O4'), ('moleFraction', 0.7845709915112387)]), OrderedDict([('name', 'hercynite'), ('formula', 'FeAl2O4'), ('moleFraction', 0.23797484059432275)]), OrderedDict([('name', 'magnetite'), ('formula', 'Fe3O4'), ('moleFraction', 0.01444305279038849)]), OrderedDict([('name', 'spinel'), ('formula', 'MgAl2O4'), ('moleFraction', 0.09860386735133653)]), OrderedDict([('name', 'ulvospinel'), ('formula', 'Fe2TiO4'), ('moleFraction', 0)])])]), OrderedDict([('name', 'rhm-oxide'), ('formula', "Mn0.42Fe''0.00Mg0.25Fe'''0.66Al0.00Ti0.67O3"), ('affinity', 18839.108334035813), ('density', 4.760281333085705), ('gibbsFreeEnergy', -1426984.0279071585), ('enthalpy', -985384.9823760493), ('entropy', 293.88170331209295), ('volume', 28.40129485254534), ('dvdt', 0.0008244247765034733), ('dvdp', -1.4724537912553223e-05), ('d2vdt2', -1.5614151863330226e-07), ('d2vdtdp', 1.8355163282262343e-10), ('d2vdp2', 5.139124415356904e-11), ('heatCapacity', 117.38786002508726), ('TiO2', 36.72230247402611), ('Fe2O3', 35.90515252775798), ('MnO', 20.49001347988543), ('MgO', 6.882531518330483), ('component', [OrderedDict([('name', 'geikielite'), ('formula', 'MgTiO3'), ('moleFraction', 0.23086947187204324)]), OrderedDict([('name', 'hematite'), ('formula', 'Fe2O3'), ('moleFraction', 0.3039791756179228)]), OrderedDict([('name', 'ilmenite'), ('formula', 'FeTiO3'), ('moleFraction', 0)]), OrderedDict([('name', 'pyrophanite'), ('formula', 'MnTiO3'), ('moleFraction', 0.39051501636936387)]), OrderedDict([('name', 'corundum'), ('formula', 'Al2O3'), ('moleFraction', 0)])])]), OrderedDict([('name', 'ortho-oxide'), ('formula', "Fe''0.30Mg0.00Fe'''1.40Ti1.30O5"), ('affinity', 73578.08797422006), ('density', 4.299275371389998), ('gibbsFreeEnergy', -1882908.077437167), ('enthalpy', -1294621.2975047668), ('entropy', 391.5015729134785), ('volume', 44.15125372735433), ('dvdt', 0), ('dvdp', 0), ('d2vdt2', 0), ('d2vdtdp', 0), ('d2vdp2', 0), ('heatCapacity', 176.78175455459976), ('TiO2', 43.82294300563444), ('Fe2O3', 47.060199594781466), ('FeO', 9.116857399584077), ('component', [OrderedDict([('name', 'pseudobrookite'), ('formula', 'Fe2TiO5'), ('moleFraction', 0.5593818411687983)]), OrderedDict([('name', 'ferropseudobrookite'), ('formula', 'FeTi2O5'), ('moleFraction', 0.24086763766180747)]), OrderedDict([('name', 'karrooite'), ('formula', 'MgTi2O5'), ('moleFraction', 0)])])]), OrderedDict([('name', 'whitlockite'), ('formula', 'Ca3(PO4)2'), ('affinity', 37177.87667606771), ('density', 3.1774505224339276), ('gibbsFreeEnergy', -4802701.459922556), ('enthalpy', -3668647.498828648), ('entropy', 754.7065898506906), ('volume', 97.62), ('dvdt', 0), ('dvdp', 0), ('d2vdt2', 0), ('d2vdtdp', 0), ('d2vdp2', 0), ('heatCapacity', 330.45334161320164), ('CaO', 54.238417923474394), ('P2O5', 45.761582076525606), ('component', OrderedDict([('name', 'whitlockite'), ('formula', 'Ca3(PO4)2'), ('moleFraction', 1)]))]), OrderedDict([('name', 'apatite'), ('formula', 'Ca5(PO4)3OH'), ('affinity', 85418.37861484883), ('density', 3.0624684042066757), ('gibbsFreeEnergy', -7866757.235996729), ('enthalpy', -6040527.572807831), ('entropy', 1215.3456613828089), ('volume', 164.025), ('dvdt', 0), ('dvdp', 0), ('d2vdt2', 0), ('d2vdtdp', 0), ('d2vdp2', 0), ('heatCapacity', 591.7608281516289), ('CaO', 55.82024002243365), ('P2O5', 42.38656534985609), ('H2O', 1.7931946277102557), ('component', OrderedDict([('name', 'apatite'), ('formula', 'Ca5(PO4)3OH'), ('moleFraction', 1)]))]), OrderedDict([('name', 'water'), ('formula', 'H2O'), ('affinity', 57402.596061687334), ('density', 0.14155085351962876), ('gibbsFreeEnergy', -483817.34118686465), ('enthalpy', -196609.12979285698), ('entropy', 191.14232462457576), ('volume', 127.2701615854393), ('dvdt', 0.10230835048018053), ('dvdp', -0.12322563573600752), ('d2vdt2', -3.6738014919212675e-05), ('d2vdtdp', -8.934739460098331e-05), ('d2vdp2', 0.00025101722869057394), ('heatCapacity', 53.59982112657247), ('H2O', 100), ('component', OrderedDict([('name', 'water'), ('formula', 'H2O'), ('moleFraction', 1)]))]), OrderedDict([('name', 'alloy-solid'), ('formula', 'solid Fe1.00Ni0.00'), ('affinity', 71357.97893785918), ('density', 0), ('gibbsFreeEnergy', -1.0115500503463773e-10), ('enthalpy', -1.5052403767867872e-12), ('entropy', 6.631636292845061e-14), ('volume', 0), ('dvdt', 0), ('dvdp', 0), ('d2vdt2', 0), ('d2vdtdp', 0), ('d2vdp2', 0), ('heatCapacity', 0), ('component', [OrderedDict([('name', 'Fe-metal'), ('formula', 'Fe'), ('moleFraction', 0)]), OrderedDict([('name', 'Ni-metal'), ('formula', 'Ni'), ('moleFraction', 0)])])]), OrderedDict([('name', 'alloy-liquid'), ('formula', 'liquid Fe1.00Ni0.00'), ('affinity', 73642.83150153467), ('density', 0), ('gibbsFreeEnergy', -1.0174502284556578e-10), ('enthalpy', -2.284172850863797e-12), ('entropy', 6.619064127314206e-14), ('volume', 0), ('dvdt', 0), ('dvdp', 0), ('d2vdt2', 0), ('d2vdtdp', 0), ('d2vdp2', 0), ('heatCapacity', 0), ('component', [OrderedDict([('name', 'Fe-liquid'), ('formula', 'Fe'), ('moleFraction', 0)]), OrderedDict([('name', 'Ni-liquid'), ('formula', 'Ni'), ('moleFraction', 0)])])])])])



Compute Parameters
-------------------

Parameters can be passed to the compute query to customise the calculation. A
selection of parameters and possible values can be found in the
`XML schema <http://melts.ofm-research.org/WebServices/MELTSinput.xsd>`__ and
`documentation <http://melts.ofm-research.org/WebServices/MELTSinput_Schema_Generated_Docs/MELTSinput.html>`__
on the melts website.

..
  :code:`initialize`

    * :code:`modelSelection`

      * *`MELTS_v1.0.x`* |, *`MELTS_v1.1.x`* | *`MELTS_v1.2.x`* | *`pMELTS_v5.6.1`*
      * all compositional variables

  :code:`fractionateOnly`:

    * *`fractionateSolids`*, *`fractionateFluids`*, *`fractionateLiquids`*  (choose 1-2)

  :code:`constraints` (choose one; thermoengine also has SV)

    * These modes are available:

      1. *`setTP`* temperature-pressure
      2. *`setTV`* temperature-volume
      3. *`setHP`* enthalpy-pressure
      4. *`setSP`* entropy-pressure

    * :code:`initial<var>` must be set
    * Optional: :code:`final<var>`, :code:`inc<var>`, :code:`d<var2>d<var1>`
    * :code:`fo2Path`: *`none`* | *`fmq`* | *`coh`* | *`nno`* | *`iw`* | *`hm`*

  :code:`fractionationMode`: *`fractionateNone`*, *`fractionateSolids`*, *`fractionateFluids`*, *`fractionateLiquids`* (choose 0-2)

  :code:`multLiquids`: :code:`True` | :code:`False`

  :code:`suppressPhase`: `str`

  :code:`assimilant`
    * :code:`temperature`
    * :code:`increments`: :code:`int`
    * :code:`mass`
    * :code:`units`: `vol` | `wt`s
    * :code:`phase` (any number)

      * `amorphous` | `solid` | `liquid` (with properties..)

Compute Output
-------------------

An example of formatted JSON output from the compute service is shown below.

.. code-block:: json

    { "status":"Success: Equilibrate",
      "sessionID":"552291051.596800.1804289383",
      "title":"Enter a title for the run",
      "time":"Mon Jul 2 23:10:51 2018",
      "release":"MELTS Web Services, MELTS v.1.0.x",
      "buildDate":"Sep 27 2016",
      "buildTime":"08:37:35",
      "temperature":"1200",
      "pressure":"1000",
      "log_fO2":"-9.292508501350249972",
      "deltaHM":"-6.5843402903737722198",
      "deltaNNO":"-1.7295882284656141081",
      "deltaFMQ":"-1.0655143052398710068",
      "deltaCOH":"1.1140739919464248686",
      "deltaIW":"2.4523554636227675729",
      "liquid":{"mass":"79.224930087117130029",
                "density":"2.6888739764023834589",
                "viscosity":"2.1808546355527487215",
                "gibbsFreeEnergy":"-1281817.8163060888182",
                "enthalpy":"-967241.03052840172313",
                "entropy":"213.54022725295251917",
                "volume":"29.463980380782754054",
                "dvdt":"0.0022228926591244097498",
                "dvdp":"-0.00018477679830941845605",
                "d2vdt2":"6.0547123990430293847e-08",
                "d2vdtdp":"-1.9823487546973320295e-08",
                "d2vdp2":"8.2176933278351927828e-09",
                "heatCapacity":"117.54760903391918703",
                "SiO2":"49.070879713300428193",
                "TiO2":"1.2746984706149677713",
                "Al2O3":"15.547239314502563801",
                "Fe2O3":"1.1219160810065404998",
                "Cr2O3":"0.050467309333368480517",
                "FeO":"8.6472380250776375021",
                "MgO":"8.6112592267950649472",
                "CaO":"12.433184035995937577",
                "Na2O":"2.8525803875263218146",
                "K2O":"0.037113330969942535942",
                "P2O5":"0.10097831567919893225",
                "H2O":"0.25244578919801691219"},
      "solid":[{"name":"olivine",
                "formula":"(Ca0.01Mg0.85Fe''0.15Mn0.00Co0.00Ni0.00)2SiO4",
                "mass":"5.0611455532498279553",
                "density":"3.256264076719213918",
                "gibbsFreeEnergy":"-80793.633565014824853",
                "enthalpy":"-62670.686010467339656",
                "entropy":"12.302173950071260577",
                "volume":"1.5542798231367915829",
                "dvdt":"7.3368482662024503633e-05",
                "dvdp":"-1.159590122970580791e-06",
                "d2vdt2":"2.5826647116800414035e-08",
                "d2vdtdp":"2.9194839589241691073e-14",
                "d2vdp2":"3.4022602849075366441e-12",
                "heatCapacity":"6.3269887937074473783",
                "SiO2":"39.907476858520290364",
                "FeO":"14.58265239333134744",
                "MgO":"44.973873816349971833",
                "CaO":"0.53599693179839225099",
                "component":[{"name":"tephroite",
                              "formula":"Mn2SiO4",
                              "moleFraction":"0"},
                              {"name":"fayalite",
                               "formula":"Fe2SiO4",
                               "moleFraction":"0.15279468642281898716"},
                              {"name":"co-olivine",
                               "formula":"Co2SiO4",
                               "moleFraction":"0"},
                               {"name":"ni-olivine",
                                "formula":"Ni2SiO4",
                                "moleFraction":"0"},
                               {"name":"monticellite",
                                "formula":"CaMgSiO4",
                                "moleFraction":"0.014390161918421261189"},
                               {"name":"forsterite",
                                 "formula":"Mg2SiO4",
                                 "moleFraction":"0.83281515165875974471"}]
                                 },


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  4.176 seconds)


.. _sphx_glr_download_examples_meltsweb.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example


  .. container:: binder-badge

    .. image:: https://mybinder.org/badge_logo.svg
      :target: https://mybinder.org/v2/gh/morganjwilliams/pyrolite-meltsutil/develop?filepath=docs/source/examples/meltsweb.ipynb
      :width: 150 px


  .. container:: sphx-glr-download

     :download:`Download Python source code: meltsweb.py <meltsweb.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: meltsweb.ipynb <meltsweb.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
