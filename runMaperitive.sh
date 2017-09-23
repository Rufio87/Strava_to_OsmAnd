#!/bin/bash

mscriptFilename="MaperitiveScript.mscript"
mrulesFilename="TransparentBackground.mrules"

cp $mscriptFilename ./Maperitive/Scripts/
cp $mrulesFilename ./Maperitive/Rules/

cd Maperitive/Rules/
mv Default.mrules Default.mrules.backup
mv $mrulesFilename Default.mrules
cd ..


#./Maperitive.sh -exitafter "Scripts/"$mscriptFilename
./Maperitive.sh "Scripts/"$mscriptFilename

cd Rules
rm Default.mrules
mv Default.mrules.backup Default.mrules