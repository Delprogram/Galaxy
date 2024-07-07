def get_better_score(self):
    file = open("better_score.txt", "r")
    #self.score_better_txt = fichier.readline()
    return file.readline()


def write_score(self, new_better_score):
    if self.score_better_txt != 0:
        file = open("better_score.txt", "w")
        file.write(str(new_better_score))
        file.close()






#print(get_better_score(self))
