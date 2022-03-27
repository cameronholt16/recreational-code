#My sister and I play the video game 'Keep Talking and Nobody Explodes. I get a load of letters and I have to find which unique word can be built
#from them.

possible_words=['about', 'after', 'again','below','could','every', 'first','found','great','house','large','learn','never','other','place','plant','point','right','small','sound','spell','still','study','their','there','these','thing','think','three','water','where','which','world','would','write']
possible_letters=[[],[],[],[],[]]
complete_sixths=0
for i in range(30):
    possible_letters[i//6].append(input())
    complete_sixths+=1
    if complete_sixths%6==0:
        to_remove=[]
        for word in possible_words:
            if word[int(complete_sixths/6-1)] not in possible_letters[int(complete_sixths/6-1)]:
                to_remove.append(word)
        for dedword in to_remove:
            possible_words.remove(dedword)
    print(possible_words)
    

        