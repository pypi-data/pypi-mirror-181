def versionComparisson(v1, v2):
    """
   vComparissons() is a fuction that allows to compare two string version. 
   This fuction has to string as inputs "version_1", "version_2"
   and returns whether one is greater than, equal, or less than the other.
   
   All arguments must be string version separated by dots, ex: ("#.#.#", "#.#")
   Param  version_1 = "First.version.number" 
   Param  version_2 = "Second.version.number" 
   retun : "Version "+ version_2 + " is (greater/lesser/equal) than version " + version_1"""      
  
    Version1 = v1.split(".") 
    Version2 = v2.split(".") 
    lenv1 = len(Version1)
    lenv2 = len(Version2)


    if lenv1>lenv2:
      for i in range(lenv2, lenv1):
         Version2.append("0")
    if lenv2>lenv1:
      for i in range(lenv1, lenv2):
         Version1.append("0")

    Version1 = [int(i) for i in Version1]
    Version2 = [int(i) for i in Version2]

    for position in range(len(Version1)):
      if Version1[position]>Version2[position]:
         message = "Version "+ v1 + " is greater than version " + v2
         return message
      if Version2[position]>Version1[position]:
         message = "Version "+ v1 + " is lesser than version " + v2

         return message
    message = "Version "+ v1 + " is equal than version " + v2

    return message