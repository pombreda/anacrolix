@ECHO OFF
echo Compiling java source files...
javac *.java
echo Compiling Runer.jar file...
jar cfm Runer.jar MANIFEST.MF *.class resources\*.jpg resources\v110.rune
echo Cleaning up...
del *.class
echo Compilation complete! Testing new JAR...
Runer.jar