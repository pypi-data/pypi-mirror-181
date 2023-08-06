import pandas as pd
import numpy as np
from tqdm import tqdm



def load_metadata(codons:str() = 'https://github.com/jkubis96/JBioSeqTools/blob/main/data/codons.xlsx?raw=true', vectors:str() = 'https://github.com/jkubis96/JBioSeqTools/blob/main/data/vectors.xlsx?raw=true', linkers:str() = 'https://github.com/jkubis96/JBioSeqTools/blob/main/data/linkers.xlsx?raw=true', regulators:str() = 'https://github.com/jkubis96/JBioSeqTools/blob/main/data/regulators.xlsx?raw=true', fluorescent_tag:str() = 'https://github.com/jkubis96/JBioSeqTools/blob/main/data/fluorescent_tag.xlsx?raw=true', backbone:str() = 'https://github.com/jkubis96/JBioSeqTools/blob/main/data/backbone.xlsx?raw=true', promoters:str() = 'https://github.com/jkubis96/JBioSeqTools/blob/main/data/promoters.xlsx?raw=true', restriction:str() = 'https://github.com/jkubis96/JBioSeqTools/blob/main/data/restriction_enzymes.xlsx?raw=true'):
    codons = pd.read_excel(codons)
    vectors = pd.read_excel(vectors)
    linkers = pd.read_excel(linkers)
    regulators = pd.read_excel(regulators)
    fluorescent_tag = pd.read_excel(fluorescent_tag)
    backbone = pd.read_excel(backbone)
    promoters = pd.read_excel(promoters)
    restriction = pd.read_excel(restriction)
    
    metadata = {'codons':codons, 'vectors':vectors, 'linkers':linkers, 'regulators':regulators, 'fluorescent_tag':fluorescent_tag, 'backbone':backbone, 'promoters':promoters, 'restriction':restriction}

    print('\n Metadata has loaded successfully')
    return metadata

def create_project(project_name:str()):
    project = {'project':str(project_name),'transcripts':{}, 'elements':{'promoter':{}, 'fluorescence':{}, 'linkers':{}, 'regulators': {}}, 'vector':{'eval':{}, 'elements':{}, 'fasta':{}, 'graph':{}}}
    return project
    

def load_sequences(n:int(), project:dict(), coding = True, upac_code:list() = ['A','C','T','G','N','M','R','W','S','Y','K','V','H','D','B'], **args):
    transcripts = {'name': [], 'ORF': [], 'sequence': []}
    for i in range(1,n+1):
        check = True
        check_name = True
        while (check == True or check_name == True):
            if str('ORF' + str(i)) not in args and check == True:
                globals()[str('ORF' + str(i))] = input('Enter sequence ' + str('ORF'+str(i)) + ': ').replace('\\n', '\n')
                globals()[str('ORF' + str(i))] = ''.join(c.upper() for c in eval(str('ORF' + str(i))) if c.isalpha())
            if str('ORF' + str(i) + '_name') not in args and check_name == True:
                globals()[str('ORF' + str(i) + '_name')] = input('Enter sequence name ' + str('ORF'+str(i)) + ': ')
                globals()[str('ORF' + str(i) + '_name')] = eval(str('ORF' + str(i) + '_name')).upper()
                
            if str('ORF'+str(i)) in args:
                test = args[str('ORF'+str(i))]
                test = [args[str('ORF'+str(i))][y:y+3] for y in range(0, len(args[str('ORF'+str(i))]), 3)]
                test2 = args[str('ORF'+str(i))].upper()
                test2 = list(test2)
                
                t2 = True
                for h in test2:
                    if h not in upac_code:
                        t2 = False
                        break
                
                
                if (len(test) == 0):
                    print("\n Sequence not provided. Sequence length equals 0")
                    check = True  
                elif (len(test[-1]) < 3 and coding == True):
                    print("\n Wrong sequence " + str(i) + ". The condition of three-nucleotide repeats in the coding sequence is not met.")
                    check = True
                elif (t2 == False):
                    print("\n Wrong sequence " + str(i) + ". The sequence contains letters not included in UPAC code. UPAC: ")
                    print(upac_code)
                    check = True
                    
                else:
                    check = False
                if (len(args[str('ORF' + str(i) + '_name')]) == 0):
                    print("\n Wrong name.  Enter sequence name")
                    check_name = True
                    
                else:
                    check_name = False
                    
                if check_name == False and check == False:
                    transcripts['name'].append(globals()[str('ORF' + str(i) + '_name')].upper())
                    transcripts['ORF'].append(str('ORF' + str(i)))
                    transcripts['sequence'].append(''.join(c.upper() for c in globals()[str('ORF' + str(i))] if c.isalpha()))
                
                
            else:
                test = globals()[str('ORF'+str(i))]
                test = [globals()[str('ORF'+str(i))][y:y+3] for y in range(0, len(globals()[str('ORF'+str(i))]), 3)]
                test2 = globals()[str('ORF'+str(i))].upper()
                test2 = list(test2)
                
                t2 = True
                for h in test2:
                    if h not in upac_code:
                        t2 = False
                        break
                
                
                if (len(test) == 0):
                    print("\n Sequence not provided. Sequence length equals 0")
                    check = True  
                elif (len(test[-1]) < 3 and coding == True):
                    print("\n Wrong sequence " + str(i) + ". The condition of three-nucleotide repeats in the coding sequence is not met.")
                    check = True
                elif (t2 == False):
                    print("\n Wrong sequence " + str(i) + ". The sequence contains letters not included in UPAC code. UPAC: ")
                    print(upac_code)
                    check = True
                    
                    
                else:
                    check = False
                if (len(globals()[str('ORF' + str(i) + '_name')]) == 0):
                    print("\n Wrong name.  Enter sequence name")
                    check_name = True
                    
                else:
                    check_name = False
                    
                if check_name == False and check == False:
                    transcripts['name'].append(globals()[str('ORF' + str(i) + '_name')].upper())
                    transcripts['ORF'].append(str('ORF' + str(i)))
                    transcripts['sequence'].append(''.join(c.upper() for c in globals()[str('ORF' + str(i))] if c.isalpha()))
                    del globals()[str('ORF' + str(i) + '_name')], globals()[str('ORF' + str(i))]

     
    transcripts = pd.DataFrame(transcripts)
    transcript_list = []
    for i in range(1,n+1):
        transcript_list.append(str('ORF'+str(i)))
        transcript_list.append(str('linker'+str(i)))
    
    transcript_list = transcript_list[0:len(transcript_list) - 1]
    project['transcripts']['sequences'] = transcripts
    project['elements']['transcripts'] = transcript_list
    
    return project  
                


def choose_promoter(promoters:pd.DataFrame(), project:dict(), **args):
    if 'promoter' not in args and 'promoter_name' not in args:
        for lin in promoters['id']:
            print('-------------------------------------------------------------')
            print('id : ' + str(lin))
            print('name : ' + str(promoters['name'][promoters['id'] == lin][lin-1]))
            print('specificity : ' + str(promoters['tissue'][promoters['id'] == lin][lin-1]))
            print('description : ' + str(promoters['description'][promoters['id'] == lin][lin-1]))
            print('role : ' + str(promoters['role'][promoters['id'] == lin][lin-1]))
            print('reference : ' + str(promoters['ref'][promoters['id'] == lin][lin-1]))
       
        check = True
        while (check == True):
            x = input('\n Enter id for promoter: ')
            if (locals()['x'] != '' and int(locals()['x']) > 0 and len(locals()['x']) > 0) and locals()['x'].isnumeric() and (int(locals()['x']) in range(0, len(promoters['role'])+1)):
                if x == str(0):
                    project['elements']['promoter']['sequence'] = ''
                    project['elements']['promoter']['name'] = ''
                else:
                    project['elements']['promoter']['sequence'] = str(promoters['seq'][promoters['id'] == eval(x)][eval(x)-1])
                    project['elements']['promoter']['name'] = str(promoters['name'][promoters['id'] == eval(x)][eval(x)-1])

                check = False
    else:
        project['elements']['promoter']['sequence'] = args['promoter']
        project['elements']['promoter']['name'] = args['promoter_name']
        
    return project

def choose_fluorescence(fluorescent_tag:pd.DataFrame(), linkers:pd.DataFrame(), project:dict(), **args):
    if 'fluorescence' not in args and 'fluorescence_name' not in args and 'fluorescent_tag_linker' not in args and 'fluorescent_tag_linker_name' not in args:
        check_f = True
        check_l = True
        while(check_f == True and check_l == True):
            if 'fluorescence' not in args and 'fluorescence_name' not in args and check_f == True:
                print('-------------------------------------------------------------')
                print('id : 0')
                print('Lack of fluorescent tag')
                for lin in fluorescent_tag['id']:
                    print('-------------------------------------------------------------')
                    print('id : ' + str(lin))
                    print('name : ' + str(fluorescent_tag['name'][linkers['id'] == lin][lin-1]))
                    print('description : ' + str(fluorescent_tag['description'][fluorescent_tag['id'] == lin][lin-1]))
                    print('role : ' + str(fluorescent_tag['role'][fluorescent_tag['id'] == lin][lin-1]))
                    print('reference : ' + str(fluorescent_tag['ref'][fluorescent_tag['id'] == lin][lin-1]))
        
                locals()['x'] = input('\n Enter id for fluorescent tag: ')
                if (len(locals()['x']) > 0) and locals()['x'].isnumeric() and (int(locals()['x']) in range(0, len(fluorescent_tag['role'])+1) ):
                    check_f = False
                    if locals()['x'] == str(0):
                        project['elements']['fluorescence']['sequence'] = ''
                        project['elements']['fluorescence']['name'] = ''
                        project['elements']['fluorescence']['linker'] = ''
                        project['elements']['fluorescence']['linker_name'] = ''
                        check_l = False
    
                    else:
                        project['elements']['fluorescence']['sequence'] = str(fluorescent_tag['seq'][fluorescent_tag['id'] == int(locals()['x'])][int(locals()['x'])-1])
                        project['elements']['fluorescence']['name'] = str(fluorescent_tag['name'][fluorescent_tag['id'] == int(locals()['x'])][int(locals()['x'])-1])
    
            if 'fluorescence' in args:
                check_f = False
                
               
                    
            if 'fluorescent_tag_linker' not in args and 'fluorescent_tag_linker_name' not in args and check_l == True and check_f == False:
                print('-------------------------------------------------------------')
                print('id : 0')
                print('Lack of the linker between the last protein and the fluorescent tag')
                for lin in linkers['id']:
                    print('-------------------------------------------------------------')
                    print('id : ' + str(lin))
                    print('name : ' + str(linkers['name'][linkers['id'] == lin][lin-1]))
                    print('description : ' + str(linkers['description'][linkers['id'] == lin][lin-1]))
                    print('role : ' + str(linkers['role'][linkers['id'] == lin][lin-1]))
                    
                
                locals()['l'] = input('\n Enter id for linker: ')
                
                if (len(locals()['l']) > 0) and locals()['l'].isnumeric() and (int(locals()['l']) in range(0, len(linkers['role'])+1)):
                    check_l = False
                    if locals()['l'] == str(0):
                        project['elements']['fluorescence']['linker'] = ''
                        project['elements']['fluorescence']['linker_name'] = ''
    
                    else:
                        project['elements']['fluorescence']['linker'] = str(linkers['seq'][linkers['id'] == int(locals()['l'])][int(locals()['l'])-1])
                        project['elements']['fluorescence']['linker_name'] = str(linkers['name'][linkers['id'] == int(locals()['l'])][int(locals()['l'])-1])
    
    
            if 'fluorescent_tag_linker' in args:
                check_f = False
     
    else:
        project['elements']['fluorescence']['sequence'] = args['fluorescence']
        project['elements']['fluorescence']['name'] = args['fluorescence_name']
        project['elements']['fluorescence']['linker'] = args['fluorescent_tag_linker']
        project['elements']['fluorescence']['linker_name'] = args['fluorescent_tag_linker_name']
        
    return project


def choose_linker(n:int(), linkers:pd.DataFrame(), project:dict(), **args):
    if n < 1:
        project['elements']['linkers']['linker1'] = ''
        project['elements']['linkers']['linker1_name'] = ''
    if 'linker1' not in args and  'linker1_name' not in args and n > 1:
        print('-------------------------------------------------------------')
        print('id : 0')
        print('Lack of linker between proteins')
        for lin in linkers['id']:
            print('-------------------------------------------------------------')
            print('id : ' + str(lin))
            print('name : ' + str(linkers['name'][linkers['id'] == lin][lin-1]))
            print('description : ' + str(linkers['description'][linkers['id'] == lin][lin-1]))
            print('role : ' + str(linkers['role'][linkers['id'] == lin][lin-1]))
     
    
        for i in range(1,n):
            if str('linker' + str(i)) not in args:
                check = True
                while (check == True):
                    locals()['x'] = input('\n Enter id for linker between transcripts ' + str(i) +' & ' + str(int(i+1)) + ': ')
                    if (len(locals()['x']) > 0) and locals()['x'].isnumeric() and (int(locals()['x']) in range(0, len(linkers['role'])+1)):
                        if locals()['x'] == str(0):
                            project['elements']['linkers'][str('linker'+str(i))] = ''
                            project['elements']['linkers'][str('linker'+str(i) + '_name')] = ''
                        else:
                            project['elements']['linkers'][str('linker'+str(i))] = str(linkers['seq'][linkers['id'] == int(locals()['x'])][int(locals()['x'])-1])
                            project['elements']['linkers'][str('linker'+str(i) + '_name')] = str(linkers['name'][linkers['id'] == int(locals()['x'])][int(locals()['x'])-1])
    
    
                        check = False
         
    elif 'linker1' in args and  'linker1_name' in args and n > 1:
        for key, value in args.items():
            if 'name' in str(key):
                project['elements']['linkers'][str(key)] = str(value)
            else:
                project['elements']['linkers'][str(key)] = str(value)

        
    return project


def choose_regulator(regulators:pd.DataFrame(), project:dict(), **args):
    if 'enhancer' not in args and 'enhancer_name' not in args:
        print('-------------------------------------------------------------')
        print('id : 0')
        print('Lack of regulators')
        for lin in regulators['id']:
            print('-------------------------------------------------------------')
            print('id : ' + str(lin))
            print('name : ' + str(regulators['name'][regulators['id'] == lin][lin-1]))
            print('description : ' + str(regulators['description'][regulators['id'] == lin][lin-1]))
            print('role : ' + str(regulators['role'][regulators['id'] == lin][lin-1]))
            print('type : ' + str(regulators['type'][regulators['id'] == lin][lin-1]))
            print('reference : ' + str(regulators['ref'][regulators['id'] == lin][lin-1]))
       
        check = True
        while (check == True):
            x = input('\n Enter id for regulator: ')
            if (len(locals()['x']) > 0) and locals()['x'].isnumeric() and (int(locals()['x']) in range(0, len(regulators['role'])+1)):
                if x == str(0):
                    project['elements']['regulators']['enhancer'] = ''
                    project['elements']['regulators']['enhancer_name'] = ''

                else:
                    project['elements']['regulators']['enhancer'] = str(regulators['seq'][regulators['id'] == eval(x)][eval(x)-1]) 
                    project['elements']['regulators']['enhancer_name'] = str(regulators['name'][regulators['id'] == eval(x)][eval(x)-1])
                
                check = False
                
    elif 'enhancer' in args and 'enhancer_name' in args:
        project['elements']['regulators']['enhancer'] = args['enhancer']
        project['elements']['regulators']['enhancer_name'] = args['enhancer_name']
        
    return project
        



def check_stop(project:dict(), codons:pd.DataFrame()):
    
    if len(project['transcripts']['sequences']['sequence']) > 1 and len(project['elements']['fluorescence']['sequence']) > 0:
        repaired = []
        for transcript in range(0,len(project['transcripts']['sequences']['sequence'])):
            test = [project['transcripts']['sequences']['sequence'][transcript][y:y+3] for y in range(0, len(project['transcripts']['sequences']['sequence'][transcript]), 3)]
            if test[-1] in list(codons['Triplet'][codons['Amino acid'] == '*']):
                repaired.append(project['transcripts']['sequences']['sequence'][transcript][0:len(project['transcripts']['sequences']['sequence'][transcript])-3])
            else:
                repaired.append(project['transcripts']['sequences']['sequence'][transcript])
    elif len(project['transcripts']['sequences']['sequence']) > 1 and len(project['elements']['fluorescence']['sequence']) == 0:
        repaired = []
        for transcript in range(0,len(project['transcripts']['sequences']['sequence'])):
            test = [project['transcripts']['sequences']['sequence'][transcript][y:y+3] for y in range(0, len(project['transcripts']['sequences']['sequence'][transcript]), 3)]
            if transcript < max(range(0,len(project['transcripts']['sequences']['sequence']))) and test[-1] in list(codons['Triplet'][codons['Amino acid'] == '*']):
                repaired.append(project['transcripts']['sequences']['sequence'][transcript][0:len(project['transcripts']['sequences']['sequence'][transcript])-3])
            else:
                repaired.append(project['transcripts']['sequences']['sequence'][transcript])
    
    else:          
        repaired = project['transcripts']['sequences']['sequence'][0]
        
    project['transcripts']['sequences']['vector_sequence'] = repaired

    return project




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
    
    return df_final



def sequence_enrichment(project:dict(), codons:pd.DataFrame(), species:str()):
    project['transcripts']['sequences']['vector_sequence_GC'] = np.nan  
    project['transcripts']['sequences']['vector_sequence_frequence'] = np.nan  
    project['transcripts']['sequences']['optimized_vector_sequence'] = np.nan  
    project['transcripts']['sequences']['optimized_vector_sequence_GC'] = np.nan  
    project['transcripts']['sequences']['optimized_vector_sequence_frequence'] = np.nan  
    project['transcripts']['sequences']['sequence_aa'] = np.nan 
    for tn in range(0,len(project['transcripts']['sequences']['sequence'])):
            tmp = codon_otymization(project['transcripts']['sequences']['vector_sequence'][tn], codons, species)
            project['transcripts']['sequences']['vector_sequence_GC'][tn] = tmp['GC%'][0] 
            project['transcripts']['sequences']['vector_sequence_frequence'][tn] = tmp['frequence'][0] 
            project['transcripts']['sequences']['optimized_vector_sequence'] = tmp['sequence_na'][1] 
            project['transcripts']['sequences']['optimized_vector_sequence_GC'][tn] = tmp['GC%'][1] 
            project['transcripts']['sequences']['optimized_vector_sequence_frequence'][tn] = tmp['frequence'][1] 
            project['transcripts']['sequences']['sequence_aa'] = tmp['sequence_aa'][1]
            


    return project



def choose_sequence_variant(project:dict(), **args):
    for i in  project['transcripts']['sequences'].index:
        if str('ORF_sv' + str(i+1)) not in args:
            print('-------------------------------------------------------------')
            print('name : ' + str( project['transcripts']['sequences']['ORF'][i] + ' -> ' +  project['transcripts']['sequences']['name'][i]))
            print('**************************************************************')
            print('Before optimization:')
            print('* GC % : ' + str( project['transcripts']['sequences']['vector_sequence_GC'][i]))
            print('* Mean codon frequence : ' + str( project['transcripts']['sequences']['vector_sequence_frequence'][i]))
            print('**************************************************************')
            print('After optimization:')
            print('* GC % : ' + str( project['transcripts']['sequences']['optimized_vector_sequence_GC'][i]))
            print('* Mean codon frequence : ' + str( project['transcripts']['sequences']['optimized_vector_sequence_frequence'][i]))
            print('Choose sequence: optimized [o] or not optimized [n]')
    
            
            check = True
            while (check == True):
                locals()[str('ORF_sv' + str(i+1))] = input('\n Writte your choose [o/n]: ')
                if str('ORF_sv' + str(i+1)) in locals() and locals()[str('ORF_sv' + str(i+1))] == 'o' or str('ORF_sv' + str(i+1)) in locals() and locals()[str('ORF_sv' + str(i+1))] == 'n':
                    check = False
                    
                
        if str('ORF_sv' + str(i+1)) in locals() and locals()[str('ORF_sv' + str(i+1))] == 'o' :
            project['transcripts']['sequences']['vector_sequence'][i] = project['transcripts']['sequences']['optimized_vector_sequence'][i]
        if str('ORF_sv' + str(i+1)) in args and args[str('ORF_sv' + str(i+1))] == 'o' :
            project['transcripts']['sequences']['vector_sequence'][i] = project['transcripts']['sequences']['optimized_vector_sequence'][i]

        
    
    return project       
                




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
            print('name : ' + restriction_df[0][i])

    
        enzyme_list = []
        check = True
        enzyme_n = 1
        while (check == True):
            print('\n Provide enzyme id, if no restriction sites are relevant to your experiment or you have already provided all enzyme ids, write "x"')
            enzyme = input('\n Enter enzyme '+ str(enzyme_n) + ' id: ')
            if len(enzyme) != 0 and not enzyme.isalpha() and int(enzyme) in restriction_df.index:
                enzyme_n += 1
                enzyme_list = enzyme_list + restriction_df[1][int(enzyme)]
            elif len(enzyme) != 0 and enzyme.upper() == 'X':
                check = False
        
        enzyme_list = np.unique(enzyme_list)
    else:
        print('\n Lack of restriction places to choose')
        
    return np.asarray(enzyme_list)       




def repair_sequences(sequence:str(), codons:pd.DataFrame, restriction_df:pd.DataFrame(), restriction:pd.DataFrame(), enzyme_list:list(), species:str()):
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
            print('\n Restriction places for:')
            for i in not_repaired:
                print('\n'+ str(i))
                
            print('\n were unable to optimize:')
            print('\n Rest of chosen restriction places in sequence repaired...')
    
    
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
            print('\n Any new restriction places were not created')
        else:
            print('\n New restriction places were created:')
            for name in enzyme_restriction['name']:
                print(name)
    
    else:
        enzyme_restriction = {'name':[], 'restriction_place':[], 'restriction_sequence':[], 'start':[], 'stop':[]}
        enzyme_restriction = pd.DataFrame.from_dict(enzyme_restriction)
        not_repaired = []
        final_sequence = sequence

    return final_sequence, not_repaired, enzyme_restriction, restriction_df




def find_restriction_vector(project:dict(), restriction:pd.DataFrame()):
    project['transcripts']['sequences']['full_restriction'] = ''
    project['transcripts']['sequences']['enzymes_df'] = ''
    for trans in project['transcripts']['sequences'].index:
        full, coordinates = check_restriction(str( project['transcripts']['sequences']['vector_sequence'][trans]), restriction)
        project['transcripts']['sequences']['full_restriction'][trans] = full.to_records(index=True)
        project['transcripts']['sequences']['enzymes_df'][trans] =  np.array(coordinates)
        
    return project
        



def choose_restriction_vector(project:dict(), restriction:pd.DataFrame()):
    project['transcripts']['sequences']['enzymes'] = ''
    for trans in project['transcripts']['sequences'].index:
        index = pd.DataFrame(project['transcripts']['sequences']['enzymes_df'][trans])
        index.index = index[1]
        index.index = range(0, len(index[1]))
        print("\n Choose enzymes for " + str(project['transcripts']['sequences']['ORF']))
        project['transcripts']['sequences']['enzymes'][trans] = choose_restriction_to_remove(index).tolist()
        
    return project
        



def repair_restriction_vector(project:dict(), restriction:pd.DataFrame(), codons:pd.DataFrame(), species:str()):
    project['transcripts']['sequences']['not_repaired'] = ''
    for trans in project['transcripts']['sequences'].index:
        final_sequence, not_repaired, enzyme_restriction, restriction_df =  repair_sequences(project['transcripts']['sequences']['vector_sequence'][trans], codons, project['transcripts']['sequences']['full_restriction'][trans], restriction, project['transcripts']['sequences']['enzymes'][trans] , species)
        project['transcripts']['sequences']['vector_sequence'][trans] = final_sequence
        project['transcripts']['sequences']['not_repaired'][trans] = not_repaired
        project['transcripts']['sequences']['full_restriction'][trans] = enzyme_restriction.to_records(index=True)
        project['transcripts']['sequences']['enzymes_df'][trans] =  np.array(restriction_df)
        

        project['transcripts']['sequences']['optimized_vector_sequence_GC'][trans] =  (project['transcripts']['sequences']['vector_sequence'][trans].count('C') + project['transcripts']['sequences']['vector_sequence'][trans].count('G')) / len(project['transcripts']['sequences']['vector_sequence'][trans]) * 100
        
        seq_codon = [project['transcripts']['sequences']['vector_sequence'][trans][y:y+3] for y in range(0, len(project['transcripts']['sequences']['vector_sequence'][trans]), 3)]
        seq_codon = [codons['Fraction'][codons['Triplet'] == seq][codons['Fraction'][codons['Triplet'] == seq].index[0]] for seq in seq_codon]
        seq_codon = round(sum(seq_codon) / len(seq_codon),2)

        project['transcripts']['sequences']['optimized_vector_sequence_frequence'][trans] = seq_codon
        
    return project
        



    
def vector_string(project:dict(), backbone:pd.DataFrame(), vector_type:str()):
    backbone = backbone[backbone['vector_type'] == vector_type]
    vector1 = str(backbone['operators'][backbone['element'] == 'p1'][0])
    for i in project['elements']['transcripts']:
        vector1 = vector1 + ' + ' + str(i)
   
    vector1 = vector1 + str(backbone['operators'][backbone['element'] == 'p2'][1])
    
    project['vector']['eval'] = vector1
    
    return project






def eval_vector(project:dict(), vectors:pd.DataFrame(), vector_type:str(), **args):
    
    vectors = vectors[vectors['vector_type'] == vector_type]
    for element, n in enumerate(vectors.index):
        locals()[str(vectors['component'][n])] = vectors['sequence'][n]
      
    for element, n in enumerate(project['transcripts']['sequences'].index):
        locals()[str(project['transcripts']['sequences']['ORF'][n])] = project['transcripts']['sequences']['vector_sequence'][n]
    
    elements =  project['vector']['eval'].split()
    tf =  [x != '+' for x in elements]
    elemensts = [i for indx,i in enumerate(elements) if tf[indx] == True]

    
    for element, n in enumerate(project['elements']):
        if n == 'promoter':
            locals()['promoter'] = project['elements'][n]['sequence']
            locals()['promoter_name'] = project['elements'][n]['name']
        elif n == 'fluorescence':
             locals()['fluorescence'] = project['elements'][n]['sequence']
             locals()['fluorescence_name'] = project['elements'][n]['name']
             locals()['fluorescent_tag_linker_name'] = project['elements'][n]['linker_name']
             locals()['fluorescent_tag_linker'] = project['elements'][n]['linker']
        elif n == 'regulators':
            for r in  project['elements']['regulators'].keys():
                locals()[str(r)] = project['elements']['regulators'][r]
        elif n == 'linkers' and len(project['elements'][n]) != 0:
            for r in  project['elements']['linkers'].keys():
                locals()[str(r)] = project['elements']['linkers'][r]
            
    
    
    
    data_frame = {'element':[], 'sequence':[], 'start':[], 'end':[], 'length': []}
    
    start = 0
    for el in elemensts:
        if str(el) not in args and el not in locals():
            print('\n')
            print('Variable -> ' + str(el) + ' <- was not found. Provide all required variables!!!')
            print('\n')
            
        else:
            data_frame['element'].append(str(el))
            data_frame['sequence'].append(eval(el))
            data_frame['start'].append(start + 1)
            start = start + int(len(eval(el)))
            data_frame['end'].append(start)
            data_frame['length'].append(len(eval(el)))
            

    
    fasta = eval(project['vector']['eval'])
    data_frame = pd.DataFrame(data_frame)
    data_frame = data_frame[data_frame['length'] > 0]
    
    new_element = []
    for x in data_frame['element']:
        if 'break' in x:
            new_element.append('backbone_element')
        else:
            new_element.append(x)
            
    data_frame['element'] = new_element
    data_frame = data_frame.reset_index(drop=True)
    
    
    for n in data_frame.index: 
       if str(data_frame['element'][n]) + '_name' in locals():
           data_frame['element'][n] = data_frame['element'][n] + ' : ' + eval(str(data_frame['element'][n]) + '_name')
       elif str(data_frame['element'][n]) in list(project['transcripts']['sequences']['ORF']):
            data_frame['element'][n] = data_frame['element'][n] + ' : ' + str(project['transcripts']['sequences']['name'][project['transcripts']['sequences']['ORF'] == str(data_frame['element'][n])][project['transcripts']['sequences']['name'][project['transcripts']['sequences']['ORF'] == str(data_frame['element'][n])].index[0]])



    project['vector']['elements'] = data_frame
    project['vector']['fasta'] = fasta
     
    return project



import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def vector_plot_project(project, title:str()):
    
    vector_df = pd.DataFrame(project['vector']['elements'])

    vector_df = vector_df.sort_index(ascending=False)
    
    explode = []
    for i in vector_df['element']:
        if i in 'backbone_element':
            explode.append(0)
        else:
            explode.append(0.1)
            
    
    labels = []
    for i in vector_df['element']:
        if i in 'backbone_element':
            labels.append('')
        else:
            labels.append(i)
    
    
    
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(aspect="equal"))
    
    
    wedges, texts = ax.pie(vector_df['length'],explode = explode, startangle=90)
    
    
    kw = dict(arrowprops=dict(arrowstyle="-"),
               zorder=0, va="center")
    
    n = 0
    for i, p in enumerate(wedges):
        n 
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        if len(labels[i]) > 0:
            n += 0.25
            ax.annotate(labels[i], xy=(x, y), xytext=(1.4*x+(n*x/4), y*1.1+(n*y/4)),
                        horizontalalignment=horizontalalignment, fontsize=20, weight="bold", **kw)
    
    circle1 = plt.Circle( (0,0), 1, color='black')
    circle2 = plt.Circle( (0,0), 0.95, color='white')
    
    ax.text(0.5, 0.5, str(title + '\n length: ' + str(sum(vector_df['length'])) + 'nc'), transform = ax.transAxes, va = 'center', ha = 'center', backgroundcolor = 'white', weight="bold", fontsize = 25)
    
    p=plt.gcf()
    p.gca().add_artist(circle1)
    p.gca().add_artist(circle2)

    project['vector']['graph'] = fig    
    plt.show()

    return project, fig

