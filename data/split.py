import os
import random as random

total_item=[]
total_user=[]

def split_data_random(input_file,ratio):
    lista_interazioni=[]    
    total_user, total_item = set(), set()
    print("INIZIO LETTURA")
    with open(input_file, 'r') as file:
        first_line=next(file)  # Skip first line
        n=0
        for line in file:
            user, item, rating, timestamp = line.strip().split('\t')
            lista_interazioni.append((user, item, rating, timestamp))
            total_user.add(user)
            total_item.add(item)
            n+=1
    print("FINE LETTURA")
    del lista_interazioni[0]
    n_split=int(n*ratio)
    print("INIZIO SPLIT")
    lista_interazioni=random.sample(lista_interazioni, n_split)
    print("FINE SPLIT")
    splitted_user, splitted_item = set(), set()
    for line in lista_interazioni:
        splitted_user.add(line[0])
        splitted_item.add(line[1])
    with open('dataset/split/Cancella.inter', 'w') as file:
        file.write(first_line)
        for line in lista_interazioni:
            file.write('\t'.join(line)+'\n')
    print("SCRITTO")
    print("Nel dataset originale abbiamo "+str(n) + " interazioni, "+str(len(total_user))+" utenti e "+str(len(total_item))+" item")
    print("Nel dataset al " +str(ratio*100)+ "% abbiamo "+str(n_split) + " interazioni, "+str(len(splitted_user))+" utenti e "+str(len(splitted_item))+" item")




def split_data_stratified(ratio):
    with open("LFM-1b_artist_20U50I/LFM-1b_artist_20U50I.inter", 'r') as file:
        first_line=next(file)
        user_dict = {}
        for line in file:
            user, item, repeats = line.strip().split('\t')
            if user in user_dict:
                user_dict[user].append((item, repeats))
            else:
                user_dict[user] = [(item, repeats)]
        for user in user_dict:
            min_items_per_user = max(1, int(len(user_dict[user]) * ratio))
            user_dict[user] = random.sample(user_dict[user], min_items_per_user)
        with open('LFM-1b_artist_20U50I_80strat/LFM-1b_artist_20U50I_80strat.inter', 'w') as file:
            file.write(first_line)
            for user in user_dict:
                for item in user_dict[user]:
                    file.write(user + '\t' + item[0] + '\t' + item[1] +'\n')
    os.system("cp LFM-1b_artist_20U50I/LFM-1b_artist_20U50I.item LFM-1b_artist_20U50I_80strat/LFM-1b_artist_20U50I_25strat.item")
    os.system("cp LFM-1b_artist_20U50I/LFM-1b_artist_20U50I.kg LFM-1b_artist_20U50I_25strat/LFM-1b_artist_20U50I_25strat.kg")
    os.system("cp LFM-1b_artist_20U50I/LFM-1b_artist_20U50I.user LFM-1b_artist_20U50I_25strat/LFM-1b_artist_20U50I_25strat.user")
    os.system("cp LFM-1b_artist_20U50I/LFM-1b_artist_20U50I.link LFM-1b_artist_20U50I_25strat/LFM-1b_artist_20U50I_25strat.link")


split_data_stratified(0.8)
