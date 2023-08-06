import pandas as pd
import numpy as np
from tqdm import tqdm



def load_metadata(codons:str() = 'https://github.com/jkubis96/JBioSeqTools/blob/main/data/codons.xlsx?raw=true', restriction:str() = 'https://github.com/jkubis96/JBioSeqTools/blob/main/data/restriction_enzymes.xlsx?raw=true'):
    codons = pd.read_excel(codons)
    restriction = pd.read_excel(restriction)
    
    metadata = {'codons':codons,'restriction':restriction}

    return metadata





def load_sequence(coding = True, upac_code:list() = ['A','C','T','G','N','M','R','W','S','Y','K','V','H','D','B'], **args):
    check = True
    while (check == True):
        sequence = input('\n Enter sequence: ').replace('\\n', '\n')
        sequence = ''.join(c.upper() for c in sequence if c.isalpha())
    
    
        test = sequence
        test2 = list(test)
        test = [test[y:y+3] for y in range(0, len(test), 3)]
        
        t2 = True
        for h in test2:
            if h not in upac_code:
                t2 = False
                break
        
        
        if (len(test) == 0):
            print("\n Sequence not provided. Sequence length equals 0")
            check = True  
        elif (len(test[-1]) < 3 and coding == True):
            print("\n Wrong sequence. The condition of three-nucleotide repeats in the coding sequence is not met.")
            check = True
        elif (t2 == False):
            print("\n Wrong sequence. The sequence contains letters not included in UPAC code. UPAC: ")
            print(upac_code)
            check = True
            
        else:
            check = False
        
    
    return sequence  
                




def codon_otymization(sequence:str(), codons:pd.DataFrame, species:str()):
    codons = codons[codons['Species'] == species]
    seq_codon = [sequence[y:y+3] for y in range(0, len(sequence), 3)]
    seq_codon_fr = [codons['Fraction'][codons['Triplet'] == seq][codons['Fraction'][codons['Triplet'] == seq].index[0]] for seq in seq_codon]
    seq_codon_fr = round(sum(seq_codon_fr) / len(seq_codon_fr),2)
    
    seq_codon_mean = ''.join(seq_codon).count('C')
    seq_codon_GC = (''.join(seq_codon).count('C') + ''.join(seq_codon).count('G')) / len(''.join(seq_codon)) * 100
    seq_aa = []
    for element in seq_codon:
        tmp = codons['Amino acid'][codons['Triplet'] == element]
        tmp = tmp.reset_index()
        seq_aa.append(tmp['Amino acid'][0])
        
    mean_GC = (len(sequence)-1)*58/100/len(sequence)*3
    
    seq_tmp = []
    
    for element in seq_aa:
        tmp = codons[codons['Amino acid'] == element].sort_values(['Fraction', 'GC_content'], ascending=[False, False])
        tmp = tmp.reset_index()
        seq_tmp.append(tmp['Triplet'][0])
        
    c = []
    g = []

    for n, codon in enumerate(seq_tmp):
        c.append(int(seq_tmp[n].count('C')))
        g.append(int(seq_tmp[n].count('G')))
    
    tmp2 = [x + y for x, y in zip(c, g)]
    df = np.array([seq_tmp, tmp2])
    seq_tmp_GC_1 = (''.join(seq_tmp).count('C') + ''.join(seq_tmp).count('G')) / len(''.join(seq_tmp)) * 100

    m = 1
    for i in tqdm(range(1, len(df[1]))):
        if m/(i) > mean_GC*1.05:
            tmp_np = df[0:2,i-1:i+1]
            aa_1 =  str(codons['Amino acid'][codons['Triplet'] == df[0,i-1]][codons['Amino acid'][codons['Triplet'] == df[0,i-1]].index[0]])
            aa_2 =  str(codons['Amino acid'][codons['Triplet'] == df[0,i]][codons['Amino acid'][codons['Triplet'] == df[0,i]].index[0]])
            tmp_1 = codons[codons['Amino acid'] == aa_1].sort_values(['Fraction', 'GC_content'], ascending=[False, False])
            tmp_1 = tmp_1.reset_index()
            fr1_up = tmp_1['Fraction'][0]
            tmp_1 = tmp_1[tmp_1['GC_content'] < int(df[1,i-1])]
            if len(tmp_1) > 0:
                tmp_1 = tmp_1.reset_index()
                fr1_down = tmp_1['Fraction'][0]
                diff1 = fr1_up - fr1_down
            else: 
                diff1 = 1000
            tmp_2 = codons[codons['Amino acid'] == aa_2].sort_values(['Fraction', 'GC_content'], ascending=[False, False])
            tmp_2 = tmp_2.reset_index()
            fr2_up = tmp_2['Fraction'][0]
            tmp_2 = tmp_2[tmp_2['GC_content'] < int(df[1,i])]
            if len(tmp_2) > 0:
                tmp_2 = tmp_2.reset_index()
                fr2_down = tmp_2['Fraction'][0]
                diff2 = fr2_up - fr2_down
            else: 
                diff2 = 1000


            if diff1 <= diff2 and diff1 != 1000:
               df[0,i-1] = tmp_1['Triplet'][0]
               df[1,i-1] = tmp_1['GC_content'][0]
               m += int(tmp_1['GC_content'][0])
            elif diff1 > diff2:
                df[0,i] = tmp_2['Triplet'][0]
                df[1,i] = tmp_2['GC_content'][0]
                m += int(tmp_2['GC_content'][0])
            elif diff1 == 1000 &  diff2 == 1000:
                next
        else:
            m += int(df[1,i])
                    
                  
    seq_tmp_GC_2 = (''.join(df[0]).count('C') + ''.join(df[0]).count('G')) / len(''.join(df[0])) * 100
    
    seq_aa_2 = []
    for element in df[0]:
        tmp = codons['Amino acid'][codons['Triplet'] == element]
        tmp = tmp.reset_index()
        seq_aa_2.append(tmp['Amino acid'][0])
        
    seq_codon_fr2 = [codons['Fraction'][codons['Triplet'] == seq][codons['Fraction'][codons['Triplet'] == seq].index[0]] for seq in df[0]]
    seq_codon_fr2 = round(sum(seq_codon_fr2) / len(seq_codon_fr2),2)
        
    df_final = {'status':[], 'sequence_na':[], 'sequence_aa':[], 'frequence':[], 'GC%': []}
    df_final['status'].append('not_optimized')
    df_final['status'].append('optimized')
    df_final['sequence_na'].append(''.join(seq_codon))
    df_final['sequence_na'].append(''.join(list(df[0])))
    df_final['sequence_aa'].append(''.join(seq_aa))
    df_final['sequence_aa'].append(''.join(seq_aa_2))
    df_final['frequence'].append(seq_codon_fr)
    df_final['frequence'].append(seq_codon_fr2)
    df_final['GC%'].append(seq_codon_GC)
    df_final['GC%'].append(seq_tmp_GC_2)
    
    df_final = pd.DataFrame(df_final)
    
    print('-------------------------------------------------------------')
    print('Before optimization:')
    print('* GC % : ' + str(df_final['GC%'][0]))
    print('* Mean codon frequence : ' + str(df_final['frequence'][0]))
    print('**************************************************************')
    print('After optimization:')
    print('* GC % : ' + str(df_final['GC%'][1]))   
    print('* Mean codon frequence : ' + str(df_final['frequence'][1]))

    return df_final

    
    



def check_restriction(sequence:str(), restriction:pd.DataFrame()):

    enzyme_restriction = {'name':[], 'restriction_place':[], 'restriction_sequence':[], 'start':[], 'stop':[]}
    
    for r in tqdm(restriction.index):
        check = True
        if restriction['sequence'][r] in sequence:
            while(check == True):
                bmp = list(sequence)
                for n in range(0,len(restriction['sequence'][r])):
                    for j in range(n,len(bmp)-len(restriction['sequence'][r])):
                       lower = j
                       upper = j + len(restriction['sequence'][r])
                       if upper < len(bmp) and ''.join(bmp[lower:upper]) == restriction['sequence'][r]:
                            enzyme_restriction['name'].append(restriction['name'][r])
                            enzyme_restriction['restriction_sequence'].append(restriction['sequence'][r])
                            enzyme_restriction['restriction_place'].append(restriction['restriction_place'][r])
                            enzyme_restriction['start'].append(lower)
                            enzyme_restriction['stop'].append(upper)
                            check = False

                               
    enzyme_restriction = pd.DataFrame.from_dict(enzyme_restriction)
    enzyme_restriction = enzyme_restriction.drop_duplicates()
    enzyme_restriction = enzyme_restriction.reset_index(drop=True)
    
    if len(enzyme_restriction) > 0:
        restriction_df = enzyme_restriction.copy()
        restriction_df['index'] = restriction_df.index
        restriction_df = restriction_df[['name', 'index']]
        restriction_df['index'] = [[x] for x in restriction_df['index']]
        restriction_df = restriction_df.groupby('name').agg({'index': 'sum'})
        restriction_df = restriction_df.reset_index()
    
    if len(enzyme_restriction) == 0:
        print('\n Any restriction places were not found')
    
    return enzyme_restriction, restriction_df






def choose_restriction_to_remove(restriction_df:pd.DataFrame(), enzyme_list:list() = []):
    if len(restriction_df) != 0 and len(enzyme_list) == 0:
        for i in restriction_df.index:
            print('-------------------------------------------------------------')
            print('id : ' + str(i))
            print('name : ' + restriction_df['name'][i])

    
        enzyme_list = []
        check = True
        enzyme_n = 1
        while (check == True):
            print('\n Provide enzyme id, if no restriction sites are relevant to your experiment or you have already provided all enzyme ids, write "x"')
            enzyme = input('\n Write enzyme '+ str(enzyme_n) + ' id: ')
            if len(enzyme) != 0 and not enzyme.isalpha() and int(enzyme) in restriction_df.index:
                enzyme_n += 1
                enzyme_list = enzyme_list + restriction_df['index'][int(enzyme)]
            elif len(enzyme) != 0 and enzyme.upper() == 'X':
                check = False
        
        enzyme_list = np.unique(enzyme_list)
    else:
        print('\n Lack of restriction places to choose')
        
    return np.asarray(enzyme_list)       






def repair_sequence(sequence:str(), codons:pd.DataFrame, restriction_df:pd.DataFrame(), restriction:pd.DataFrame(), enzyme_list:list(), species:str()):
    if len(restriction_df) != 0:
        not_repaired = []
        codons = codons[codons['Species'] == species]
        seq_codon = [sequence[y:y+3] for y in range(0, len(sequence), 3)]
        seq_codon_fr = [codons['Fraction'][codons['Triplet'] == seq][codons['Fraction'][codons['Triplet'] == seq].index[0]] for seq in seq_codon]
        seq_codon_fr = round(sum(seq_codon_fr) / len(seq_codon_fr),2)
        seq_codon_GC = (''.join(seq_codon).count('C') + ''.join(seq_codon).count('G')) / len(''.join(seq_codon)) * 100
        
        seq_aa = []
        for element in seq_codon:
            tmp = codons['Amino acid'][codons['Triplet'] == element]
            tmp = tmp.reset_index()
            seq_aa.append(tmp['Amino acid'][0])
        
        dic = {'seq':[], 'range':[], 'codon_n':[], 'aa':[]}
        n = 0
        for num, seq in enumerate(seq_codon):
            for i in range(0,3):
                dic['seq'].append(seq)
                dic['range'].append(n)
                dic['codon_n'].append(num)
                dic['aa'].append(seq_aa[num])
                n += 1
                
        dic = pd.DataFrame.from_dict(dic)
        
        print('\n Codon changing...')
        for eid in tqdm(enzyme_list):
            check = dic[['seq','codon_n']].drop_duplicates()
            check = ''.join(check['seq'])
            if restriction_df['restriction_sequence'][eid] in check:
                dic_tmp = dic[(dic['range'] >= restriction_df['start'][eid]) & (dic['range'] < restriction_df['stop'][eid])] 
                tmp = codons[codons['Triplet'].isin(np.unique(dic['seq']))]
                dictionary = {'seq':[], 'aa':[], 'triplet':[], 'freq':[], 'gc':[]}
                for i in np.unique(dic_tmp['seq']):
                    t = tmp[tmp['Triplet'] == i]
                    t = t.reset_index(drop = True)
                    t = tmp[tmp['Amino acid'] == t['Amino acid'][0]]
                    for n in t.index:
                        dictionary['seq'].append(i)
                        dictionary['aa'].append(t['Amino acid'][n])
                        dictionary['triplet'].append(t['Triplet'][n])
                        dictionary['freq'].append(t['Fraction'][n])
                        dictionary['gc'].append(t['GC_content'][n])
        
                
                dictionary = pd.DataFrame.from_dict(dictionary)
                dictionary = dictionary[~dictionary['triplet'].isin(dictionary['seq'])]
                dictionary = dictionary.sort_values(['freq', 'gc'], ascending=[False, False])
                dictionary = dictionary.reset_index()
        
        
                all_enzymes_variant = restriction[restriction['name'] == restriction_df['name'][eid]]
                
                
                seq_new = dic_tmp[['seq','codon_n']].drop_duplicates()
                seq_old = ''.join(seq_new['seq'])
                
                for d in dictionary.index:
                    seq_new = dic_tmp[['seq','codon_n']].drop_duplicates()
                    dictionary['seq'][d]
                    dictionary['triplet'][d]
                    seq_new['seq'][seq_new['seq'] == dictionary['seq'][d]] = dictionary['triplet'][d]
                    if ''.join(seq_new['seq']) in all_enzymes_variant['sequence']:
                        break
                    
                if seq_old == ''.join(seq_new['seq']):
                    not_repaired.append(restriction_df['name'][eid])
                elif seq_old != ''.join(seq_new['seq']):
                    for new in seq_new.index:
                        dic['seq'][dic['codon_n'] == seq_new['codon_n'][new]]  = seq_new['seq'][new]
        
    
            
        final_sequence = dic[['seq','codon_n']].drop_duplicates()
        final_sequence = ''.join(final_sequence['seq'])
        
        if len(not_repaired) == 0:    
            print('\n Restriction place in sequence repaired...')
        else:
            print('\n Restriction place for:')
            for i in not_repaired:
                print('\n'+ str(i))
                
            print('\n were unable to optimize:')
            print('\n Rest of chosen restriction place in sequence repaired...')
    
    
        enzyme_restriction = {'name':[], 'restriction_place':[], 'restriction_sequence':[], 'sequence':[], 'start':[], 'stop':[]}
        
        print('\n Checking new restriction...')
        for r in tqdm(restriction.index):
            check = True
            if restriction['sequence'][r] in final_sequence:
                while(check == True):
                    bmp = list(final_sequence)
                    for n in range(0,len(restriction['sequence'][r])):
                        for j in range(n,len(bmp)-len(restriction['sequence'][r])):
                           lower = j
                           upper = j + len(restriction['sequence'][r])
                           if upper < len(bmp) and ''.join(bmp[lower:upper]) == restriction['sequence'][r]:
                                enzyme_restriction['name'].append(restriction['name'][r])
                                enzyme_restriction['restriction_sequence'].append(restriction['sequence'][r])
                                enzyme_restriction['restriction_place'].append(restriction['restriction_place'][r])
                                enzyme_restriction['sequence'].append(final_sequence)
                                enzyme_restriction['start'].append(lower)
                                enzyme_restriction['stop'].append(upper)
                                check = False
    
                                   
        enzyme_restriction = pd.DataFrame.from_dict(enzyme_restriction)
        enzyme_restriction = enzyme_restriction.drop_duplicates()
        enzyme_restriction = enzyme_restriction.reset_index(drop=True)
        enzyme_restriction = enzyme_restriction[~enzyme_restriction['name'].isin(restriction_df['name'])]
        restriction_df = enzyme_restriction
        if len(enzyme_restriction) > 0:
            restriction_df = enzyme_restriction.copy()
            restriction_df['index'] = restriction_df.index
            restriction_df = restriction_df[['name', 'index']]
            restriction_df['index'] = [[x] for x in restriction_df['index']]
            restriction_df = restriction_df.groupby('name').agg({'index': 'sum'})
            restriction_df = restriction_df.reset_index()
    
        if len(enzyme_restriction) == 0:
            print('\n Any new restriction places were created')
        else:
            print('\n New restriction places were created:')
            for name in enzyme_restriction['name']:
                print(name)
    
    else:
        enzyme_restriction = {'name':[], 'restriction_place':[], 'restriction_sequence':[], 'start':[], 'stop':[]}
        enzyme_restriction = pd.DataFrame.from_dict(enzyme_restriction)
        not_repaired = []
        final_sequence = sequence
        
    seq_tmp_GC = (sequence.count('C') + sequence.count('G')) / len(sequence) * 100
    seq_tmp_GC_2 = (final_sequence.count('C') + final_sequence.count('G')) / len(final_sequence) * 100

    seq1 = [sequence[y:y+3] for y in range(0, len(sequence), 3)]
    seq_codon_fr = [codons['Fraction'][codons['Triplet'] == seq][codons['Fraction'][codons['Triplet'] == seq].index[0]] for seq in seq1]
    seq_codon_fr = round(sum(seq_codon_fr) / len(seq_codon_fr),2)
    
    seq2 = [final_sequence[y:y+3] for y in range(0, len(final_sequence), 3)]
    seq_codon_fr2 = [codons['Fraction'][codons['Triplet'] == seq][codons['Fraction'][codons['Triplet'] == seq].index[0]] for seq in seq2]
    seq_codon_fr2 = round(sum(seq_codon_fr2) / len(seq_codon_fr2),2)
    
    df_final = {'status':[], 'sequence_na':[], 'frequence':[], 'GC%': []}
    df_final['status'].append('before_restriction_optimization')
    df_final['status'].append('after_restriction_optimization')
    df_final['sequence_na'].append(sequence)
    df_final['sequence_na'].append(final_sequence)
    df_final['frequence'].append(seq_codon_fr)
    df_final['frequence'].append(seq_codon_fr2)
    df_final['GC%'].append(seq_tmp_GC)
    df_final['GC%'].append(seq_tmp_GC_2)
    
    df_final = pd.DataFrame(df_final) 

    return df_final, not_repaired, enzyme_restriction, restriction_df



