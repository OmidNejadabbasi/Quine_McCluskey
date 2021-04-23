# Quine_McCluskey algorithm

This is an implementation of [Quine_McCluskey algorithm](https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm) in Python.
It shows all the step of finding the prime implicants. Then chooses those who are essential and prints out the function.

So consider a boolean function with following Karnaugh map (the stars are don't-care terms) :

![Karnough map](https://i.ibb.co/vvDJBtW/image.png)

Which means the min-terms are:
```0, 4, 8, 12, 3, 10``` and the don't care terms are ```2, 11```.<br>
You can pass the into the program :
![Giving the input:](https://i.ibb.co/YNsnmZ6/image.png)

Then it will clear the terminal and print out the result:

![The result](https://i.ibb.co/V3XNHC4/image.png)

