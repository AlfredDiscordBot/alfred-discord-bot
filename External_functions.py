import requests
def quad(eq):
    if "x^2" not in eq:
        return "x^2 not found, try again"
    print(eq)
    eq=eq.replace("2+","2 + ")
    eq=eq.replace("2-","2 - ")
    eq=eq.replace("x+","x + ")
    eq=eq.replace("x-","x - ")

    #try to get correct equation
    parts = [x.strip() for x in eq.split(" ")]
    a, b, c = 0, 0, 0
    for i in parts:
        if i==' ':
            parts.remove(' ')

    for index, part in enumerate(parts):
        if part in ["+", "-"]:
            continue

        symbol = -1 if index - 1 >= 0 and parts[index - 1] == "-" else 1

        if part.endswith("x^2"):
            coeff = part[:-3]
            a = float(coeff) if coeff != '' else 1
            a *= symbol
        elif part.endswith("x"):
            coeff = part[:-1]
            b = float(coeff) if coeff != '' else 1
            b *= symbol
        elif part.isdigit():
            c = symbol * float(part)

    determinant = b**2 - (4 * a * c)

    if determinant < 0:
        return "Not Real"
    if determinant == 0:
        root = -b / (2 * a)
        return "Equation has one root:"+str(root)

    if determinant > 0:
        determinant = determinant ** 0.5
        root1 = (-b + determinant) / (2 * a)
        root2 = (-b - determinant) / (2 * a)
        return "This equation has two roots: "+str(root1)+","+str(root2)
def pinterest(website, end_number=250):
    raw=requests.get(website)
    html_content=raw.content.decode()
    stop=0
    number=0
    for i in range(0,end_number):
        a=html_content.find("GrowthUnauthPinImage__Image",stop)
        b=html_content.find('src="',a)+len('src="')
        c=html_content.find('" ',b)
        stop=c
        if i==0:
            continue
        link=html_content[b:c]
        if link.find("</div>")!=-1 or link.find("<html")!=-1:
            continue
    return link
