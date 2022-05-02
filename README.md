# ROS2022
PlatypOUs programozása

A telepítési útmutatók megtalálható a PlatypOUs [GitHub](https://github.com/ABC-iRobotics/PlatypOUs-Mobile-Robot-Platform) oldalán.

##Feladat leírása

1.1. PlatypOUs pályakövetés

    Basic: Szimulátor élesztése, SLAM tesztelése. ROS node/node-ok implementálása szenzorok adatainak beolvasására és a a robot mozgatására.
    Advanced: ROS rendszer implementálása pályakövetésre szimulált környezetben bármely szenzor felhasználásával(pl. fal mellett haladás adott távolságra LIDAR segítségével).
    Epic: Implementáció és tesztelés a valós hardware-en és/vagy nyűgözz le!

##Program működése
A Robot a Lidar Scanner-ét használja a navigáláshoz, ami viszont belerak random 0 és 1000+ értékeket.
Ezeket ki kell szűrni, ami megtalálható a [LaserScan](http://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/LaserScan.html) dokumentációjának a ranges részében.

A robotnak a látó terét felosztottam 6 részre.
- Elülső rész
- Jobb elülső rész
- Bal elülő rész
- Hátsó rész
- Bal hátsó rész
- Jobb hátsó rész

Kell a robotnak egy alap sebesség és egy szögelfordulás is.

A Main-ben fel lehet paraméterezni ezeket az adatokat a következőek alapján:
> front_degree, front_side_degree, side_degree, x_speed, z_angular

Alapból a következő paraméterek azok, amik beváltak nekem: 
- front_degree: 75, 
- front_side_degree: 15
- side_degree: 40
- x_speed: 0.6
- z_angular: 0.45

Ezek közül a side_degree-t nem használom fel, mert side logikát nem használok.
A faltól való egyenletes nagyságú távolság tartáshoz vagy pedig a kerék megakadásának
megakadályozásához lehetne hasznos.

### Főbb logikája

A tartományokra bontott scan-ek értékeiből kiválasztom a minimumut és az alapján irányítom.
Ha a robotnak az elülső tartomány 1.1 m-en belülre kerülne akkor annyival előtte található egy fal, hogy beavatkozás szükséges már miatta.
Megvizsgáljuk, hogy jobb vagy baloldalt van e elégséges hely a forduláshoz és ha van akkor a fordulással kikerüljük az ekadályt.
Ezzel: "min(Distance.Front_Left) > (min(Distance.Front_Right) + 0.8" azt díjazom a program számára, hogy ha jobb elől annyival több a hely akkor tartsa azt az irányt.
Ezzel a módszerrel azt érem el, hogy ne kacsázzon annyira a robot a 2 fordulási irány közül és azt, hogy ha van egy ajtó akkor ezzel nagyobb valószínűséggel inkább átmegy rajta mintsem kikerüli, mert az ajtón "átnézve" sokkal nagyobb szabad helyet lát a robot számára.

Ezen kívül van még az is, hogy ha nem tud se előre menne is fordulni akkor hátrafelé kell tolatnia.
A hátrafelé tolatásnál vizsgálom, hogy van e hely hátul és van e hely abban az irányban hátul, amerre tolatni szeretne a robot.
Ha van elég hely abban az irányban, amerre tolatni szeretne a robot akkor lassított sebességgel meg is teszi.

