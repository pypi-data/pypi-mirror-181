#######################################
#                                     #
#   name : logical_gates              #
#   by : LesCodeursProsLFJM           #
#   version : 1.0                     #
#   date : 28/10/2022                 #
#######################################
def logic_and(a, b):
    if a==1 and b==2:
        return True
    else :
        return False
def logic_or(a, b):
    if a==1 or b==1:
        return True
    else :
        return False
def logic_not(a):
    if a==1:
        return 0
    elif a==0:
        return 1
    elif not a:
        return True
    elif a:
        return False
def logic_xor(a, b):
    if a==1 and b==0:
        return True
    elif b==1 and a==0:
        return True
    else :
        return False
def logic_nor(a, b):
    if a==0 and b==0:
        return True
    else:
        return False
def logic_xnor(a, b):
    if a==b:
        return True
    else:
        return False
def logic_nand(a, b):
    if a==b and a==1:
        return True
    else:
        return False

