def DivEntier(x: int, y: int) -> int:
    try:
        x/y
    except ZeroDivisionError:
        return("division by 0")
    if x < 0 or y < 0:
        return("forbidden negative figure")
    
    if x < y:
        return 0
    else:
        x = x - y

if __name__ == "__main__":
    print(DivEntier(1, 1))