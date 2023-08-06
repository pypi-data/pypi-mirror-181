#print("module currently in beta will be released soon");
def login(unmlst,upslst):
    unm = input("username?\n")
    ups = input("\npassword?\n")
    l = len(unmlst) -1
    while l>=0:
        if unmlst[l] == unm:
            pi = l
            l = -1
        elif unm == "root" and ups == "rootp@1234567456234198abc":
            acess = 2
            r = 1
        else:
            l = l-1
    if r !=1 :
        if ups == upslst[pi]:
            print("\nsucessfully logged")
            acess = 1
        else:
            print("\nnot logged in(wrong password) ")

