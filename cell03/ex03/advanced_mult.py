import sys
if len(sys.argv) > 1:
    print("none")
else:

    for i in range(11):
        row = [i * j for j in range(11)] 
        row_str = " ".join(map(str, row))
        print(f"Table de {i}: {row_str}")