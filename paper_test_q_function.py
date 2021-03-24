AC = 156
QP = 11
i_frame = False
# standard

if i_frame:
    QAC = abs(AC) / (2*QP)
else:
    QAC = (abs(AC) - (QP / 2)) / (2 * QP)
print("standard: ", QAC)

# proposed
FPGA_AC_int = int(abs(AC))
FPGA_AC_s = 1 if (AC <0 ) else 0
if i_frame:
    div = 2*QP
    AC1 = (FPGA_AC_int)
else:
    div = 4*QP
    AC1 = (FPGA_AC_int<<1)
AC2 = AC1 + QP
AC3 = int (AC2 / div)
AC4 = AC3 if (AC3 < 127) else 127
QAC = AC4 if (FPGA_AC_s==0) else (~AC4)+1
print("proposed: ", QAC)
