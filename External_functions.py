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
def memes2():
    st=requests.get("https://cheezburger.com/14858757/40-dumb-memes-for-distractible-scrollers").content.decode()
    stop=0
    link=[]
    for i in range(0,40):
      a=st.find("<img class='resp-media' src='",stop)+len("<img class='resp-media' src='")
      b=st.find("' id",a)
      stop=b
      link=link+[st[a:b]]
    return link
def memes1():
    st=requests.get("http://www.quickmeme.com/").content.decode()
    stop=0
    link=[]
    for i in range(10):
      a=st.find('"post-image" src="',stop)+len('post-image" src="')+1
      b=st.find('" alt',a)
      stop=b
      link=link+[st[a:b]]
    return link
def memes3():
    st=requests.get("https://www.paulbarrs.com/business/funny-memes-website-design").content.decode()
    stop=0
    link=[]
    for i in range(20):
      a=st.find('srcset="',stop)+len('srcset="')
      b=st.find(".jpg",a)+len(".jpg")
      print(st[a:b])
      stop=b
      link+=[st[a:b]]
    return link

