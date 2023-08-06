

"""
    This is a bit assinine, since you can't really seperate static from instance context, (you can, but not without
        sacrificing performance). So we have a sub class of String for instancing, and another package for static methods.
        So we can use:
            myString = CSharp.String.Instance(r"The quick brown fox")
            myString2 = CSharp.String.Instace(r"jumped over the lazy dog.")
                    
            sentance_1 = CSharp.String.Static.Join(" ", myString, myString2);
            sentance_2 = myString.Join(" ", myString2);

            print(sentance_1)
            print(sentance_2)

            >>> The quick brown fox jumped over the lazy dog.
            >>> The quick brown fox jumped over the lazy dog.
"""
class instance:
    data = None;
    Length = 0;

    def __init__(self, value):
        self.data = str(value);
        self._Update();
        
    def __str__(self):
        return str(self.data)

    def __len__(self):
        return len(self.data);
    """
        Name: Substr
        Params: Int32 offset
        Optional Params: Int32 endset
        Return: string contained bewteen the offset and endset (or end of string) 
    """
    def Substr(self, offset, endset=None):
        if(endset == None):
            return self.data[int(offset):len(self.data)]
        else:
            return self.data[int(offset):int(endset)]

    """
        Name: IndexOf
        Params: Int32 index
        Return: Returns the character stored at the index point in the contained string.
    """
    def IndexOf(self, val):
        return self.data.index(val)

    """
        Name: Split
        Params: Char to split string at
        Return: Tuple of atrings split at supplied character.
    """
    def Split(self, val):
        return self.data.split(val)

    """
        Name: Append
        Params: Value to append to the currrent string
        Return: String with value appended.
    """
    def Append(self, val):
        return static.Join(" ", self.ToString(), str(val));

    """
        Name: Prepend
        Params: Value to prepend to currrent string.
        Returns: CSharp.String.Instance.
    """
    def Prepend(self, val):
        return static.Join(" ", str(val), self.ToString());

    """
        Name: Replace
        Params: String text_to_remove, String Text_replacement
        Returns: CSharp.String.Instace
    """
    def Replace(self, subStr, replacement):
        return instance(self.data.replace(str(subStr), str(replacement)));


    """
        Name: ToString()
        Params: None
        Return: Python String Object
    """
    def ToString(self):
        return str(self.data);

    """
        Name: SetText
        Params: Text to set the String object's value to.
        Return: None
    """
    def SetText(self, value):
        self.data = value
        self._Update();

    """
        Name: _Update
        Params: None
        Return: None
        Description: Updates varius methrics about the object so that psudo-pperties work as expected.
    """
    def _Update(self):
        self.Length = len(str(self.data));

class static:
    """
        Name: Format
        Params: String, arguments to replace tokens in string to.
        Returns: Completed String
    """
    def Format(subStr, *args):
        it = 0;
        while(it < len(args)):
            subStr = subStr.replace("$"+str(it), str(args[it]))
            it += 1
        return subStr

    """
        Name: Join
        Params: Chars to use at join position, any number of strings to be joined together.
        Returns: CSharp.String.Instance
    """
    def Join(char, *args):
        retval = ""
        for val in args:
            tmp = static.Format("$0$1$2", str(retval), str(char), str(val))
            retval = tmp

        return instance(str(retval).strip());
