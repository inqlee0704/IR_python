
Prefix1=CBDPI_CBD
Path1=/data1/inqlee0704/IR/IR_python/INEX
for s in $(ls -d ${Prefix1}*/); do cp -p ${Path1}/* ${s}/; done

