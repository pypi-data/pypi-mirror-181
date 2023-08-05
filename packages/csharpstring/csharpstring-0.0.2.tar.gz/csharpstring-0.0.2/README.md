# csharpstring
A general class that provides dot-net style syntax for python string manipulations.

## Static & Instance Namespaces
To more easily separate the objective, from non-objective functionality there are two
classes internally that can be used. 
1. `csharpstring.instance`
2. `csharpstring.static`

## Instance Methods

`value1 = instance("The quick brown fox");`
`print(value1)`
> The quick brown fox

`value2 = instance("jumped over the lazy dog");`
`print(value2)`
> jumped over the lazy dog

`value3 = value1.Append(value2);`
`print(value3)`
>The quick brown fox jumped over the lazy dog

`value4 = value3.Substr(10,30);`
>brown fox jumped ove

`value5 = value3.Replace("quick", "speedy");`
`print(value5)`
>The speedy brown fox jumped over the lazy dog

## Static Methods

`date = "10/31/22";`
`time = "8:30 PM";`
`print(static.Format("It is $0 on $1; do you know where your children are?", time, date));`
`print(static.Join(" ", value1, value2));`
>It is 8:30 PM on 10/31/22; do you know where your children are?
>The quick brown fox jumped over the lazy dog

