from dataclasses import dataclass

@dataclass
class ExerciseFolder:
    main:int
    parent:int
    name : str = None
    short_name : str = None

class Folders:
    Z1_Kairat=ExerciseFolder(main=29,parent=28)
    Z100_Unlinked=ExerciseFolder(main=70,parent=28)

class Sources:
    #last one was Coachlab
#                                             <option value="33">Pozytywny Coaching</option>
                                        
#                                             <option value="18"> Rodrigo Cantó Matellán</option>
                                        
#                                             <option value="39">Andreti Leal</option>
                                        
#                                             <option value="25">Análisis de Ejercicios Fútbol</option>
                                        
#                                             <option value="34">Fútbol Revolucionario</option>
                                        
#                                             <option value="28">Roger Crussels</option>
                                        
#                                             <option value="27">Diogo Calhau</option>
                                        
#                                             <option value="9">Felipe Ragel Official Youtube</option>
                                        
#                                             <option value="12">Juanton Soup10</option>
                                        
#                                             <option value="23">Luis Fernando Serrano Maylle</option>
                                        
#                                             <option value="41">РФС</option>
                                        
#                                             <option value="16">FutbolSiete.eu</option>
                                        
#                                             <option value="24">Entrenamiento de Fútbol</option>
                                        
#                                             <option value="21">Slavco Vojneski</option>
                                        
#                                             <option value="42">John Gall</option>
                                        
#                                             <option value="38">FC Dallas Coaching Education</option>
                                        
#                                             <option value="29">Bebeto Stival TV</option>
                                        
#                                             <option value="43">нет</option>
                                        
#                                             <option value="2">NFTV</option>
    NF=1
    Kairat=6
    no=7
    CoachLab=8
    KonstantinosFoundas=10
    HikmetKaraman=11
    CoachGameLive=13
    CoachThomasVlaminck=14
    FootballTraining=15
    DarioGrabusic=17
    SoccerSoaches=19
    ProfeBazan=20
    BekasVagelis=22
    FootballCoachesLyceum=26
    mlc7=30
    FootballFocus=31
    GaryCurneen=32
    JuegosEF=35
    SoccerCoachTv=36
    SeanBuckley=37
    BebetoStivalTV=40
    Workout=44
    
    

__BASIC__SCHEME__="""

                                <svg id="block" class="d-block bg-success mx-auto" viewBox="0 0 600 400" height="100%" width="100%" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
                                    <defs>
                                        <marker id="arrow" markerWidth="15" markerHeight="12" refX="1" refY="6" orient="auto" markerUnits="userSpaceOnUse" fill="#000000"><polyline points="1 1, 16 5.5, 1 12"></polyline></marker>
                                        <marker id="ffffffarrow" markerWidth="15" markerHeight="12" refX="1" refY="6" orient="auto" markerUnits="userSpaceOnUse" fill="#ffffff"><polyline points="1 1, 16 5.5, 1 12"></polyline></marker>
                                        <marker id="ffff00arrow" markerWidth="15" markerHeight="12" refX="1" refY="6" orient="auto" markerUnits="userSpaceOnUse" fill="#ffff00"><polyline points="1 1, 16 5.5, 1 12"></polyline></marker>
                                        <marker id="ff0000arrow" markerWidth="15" markerHeight="12" refX="1" refY="6" orient="auto" markerUnits="userSpaceOnUse" fill="#ff0000"><polyline points="1 1, 16 5.5, 1 12"></polyline></marker>
                                        <marker id="000000arrow" markerWidth="15" markerHeight="12" refX="1" refY="6" orient="auto" markerUnits="userSpaceOnUse" fill="#000000"><polyline points="1 1, 16 5.5, 1 12"></polyline></marker>
                                        <filter id="f3" x="0" y="0" width="200%" height="200%"><feOffset result="offOut" in="SourceAlpha" dx="5" dy="5"></feOffset><feGaussianBlur result="blurOut" in="offOut" stdDeviation="3"></feGaussianBlur><feBlend in="SourceGraphic" in2="blurOut" mode="normal"></feBlend></filter>
                                    </defs>
                                    <image id="plane" x="0" y="0" data-width="600" data-height="400" width="100%" height="100%" href="/static/exercises/img/field.svg"></image>
                                    <g id="selects"></g>
                                    <g id="figures"></g>
                                    <g id="lines"></g>
                                    <g id="objects"></g>
                                    <g id="dots"></g>
                                    <line id="xLine" x1="-1" y1="0" x2="-1" y2="1600" stroke="red" stroke-dasharray="10" stroke-width="1"></line>
                                    <line id="yLine" x1="0" y1="-1" x2="2400" y2="-1" stroke="red" stroke-dasharray="10" stroke-width="1"></line>
                                    <line id="xLine2" x1="-2400" y1="0" x2="-2400" y2="1600" stroke="red" stroke-dasharray="10" stroke-width="1"></line>
                                    <line id="yLine2" x1="0" y1="-1600" x2="2400" y2="-1600" stroke="red" stroke-dasharray="10" stroke-width="1"></line>
                                </svg>
"""   