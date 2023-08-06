import requests
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import re

def gen(gene_name, species):
    response = requests.get("https://rdis.cs.put.poznan.pl/api/v1/gene_synonyme_search/?csym="+str(gene_name).upper()+"&species="+ str(species))
    response = response.json()
    response = pd.DataFrame(response['results'])
    
    if len(response) == 0:

        tmp_response = requests.get("https://rdis.cs.put.poznan.pl/api/v1/gene_synonyme_search/?syn="+str(gene_name).upper()+"&species="+ str(species))
        tmp_response = tmp_response.json()
        tmp_response = pd.DataFrame(tmp_response['results'])
        if len(tmp_response) > 0:
            response = pd.DataFrame(columns = ['id', 'common_symbol', 'synonyme', 'full_symbol', 'species_1', 'species_2'])
            for i in np.unique(tmp_response['common_symbol']):
                response_t = requests.get("https://rdis.cs.put.poznan.pl/api/v1/gene_synonyme_search/?csym="+str(i).upper()+"&species="+ str(species))
                response_t = response_t.json()
                response_t = pd.DataFrame(response_t['results'])
                response = pd.concat([response, response_t])
                
            
            
            
        else:
            response = pd.DataFrame(columns = ['id', 'common_symbol', 'synonyme', 'full_symbol', 'species_1', 'species_2'])
            response[0] = [np.NaN]
    
    final = {'common_symbol':[], 'all_variants':[], 'full_symbol':[], 'species_1':[], 'species_2':[]}
    
    for inx in np.unique(response['common_symbol']):
        final['common_symbol'].append(inx)
        final['all_variants'].append([inx]+ list(np.unique(response['synonyme'][response['common_symbol'] == inx])))
        final['full_symbol'].append(np.unique(response['full_symbol'][response['common_symbol'] == inx])[0])
        final['species_1'].append(np.unique(response['species_1'][response['common_symbol'] == inx])[0])
        final['species_2'].append(np.unique(response['species_2'][response['common_symbol'] == inx])[0])
        final = pd.DataFrame.from_dict(final)
        
    return final





def genes(gene_list_orpha, species):
    genes_results = pd.DataFrame(columns = ['common_symbol', 'all_variants', 'full_symbol', 'species_1', 'species_2'])
    for g in gene_list_orpha:
        tmp = gen(g, species)
        genes_results = pd.concat([genes_results, tmp])

        
    return genes_results





def get_sequence(genes_results):
    genes_results = genes_results.reset_index(drop = True)
    genes_results['entrenz'] = ''
    for g in genes_results.index:
        for agg in genes_results['all_variants'][g]:
            response = requests.get("https://rdis.cs.put.poznan.pl/api/v1/ens_transcript/gene/"+str(agg).upper())
            response = pd.DataFrame(response.json())
            if len(response) > 0:
                tmp_dic = {'accession_code':[], 'location': [], 'length':[], 'cds':[]}

                
                for i in response.index:
                    transcript = response['fasta_cds_na'][i]
                    transcript = transcript.split('\n', 1)[1]
                    transcript = re.sub('\n', '', transcript)
                    tmp_dic['accession_code'].append(response['accession_code'][i])
                    tmp_dic['location'].append(response['location'][i])
                    tmp_dic['length'].append(len(transcript))
                    tmp_dic['cds'].append(transcript)
                    
                break
    
            else:
                tmp_dic = {'accession_code':np.NaN, 'location':np.NaN, 'length':np.NaN, 'cds':np.NaN}

              
                
        genes_results['entrenz'][g] = tmp_dic
    
    return genes_results


def create_cds_input_to_project(project, n, gene_info):
    transcripts = {'name': [], 'ORF': [], 'sequence': []}
    for gen in gene_info.index:
        transcripts['name'].append(gene_info['common_symbol'][gen])
        transcripts['ORF'].append(str('ORF' + str(int(gen)+1)))
        transcripts['sequence'].append(gene_info['choosen_transcript'][gen])
        
        
    project['transcripts']['sequences'] = pd.DataFrame(transcripts)
    project['transcripts']['sequences'] = pd.DataFrame(transcripts)
    
    transcript_list = []
    for i in range(1,n+1):
        transcript_list.append(str('ORF'+str(i)))
        transcript_list.append(str('linker'+str(i)))
    
    transcript_list = transcript_list[0:len(transcript_list) - 1]
    project['elements']['transcripts'] = transcript_list
    
    return project



def create_linker_input_to_project(n:int(), linkers:pd.DataFrame(), project:dict(), linkers_list:list()):
    if n > 1:
        for i, l in enumerate(linkers_list):
            if l == 0:
                project['elements']['linkers'][str('linker'+str(i+1))] = ''
                project['elements']['linkers'][str('linker'+str(i+1) + '_name')] = ''
            else:
                project['elements']['linkers'][str('linker'+str(i+1))] = str(linkers['seq'][linkers['id'] == l][l-1])
                project['elements']['linkers'][str('linker'+str(i+1) + '_name')] = str(linkers['name'][linkers['id'] == l][l-1])

    else:
        project['elements']['linkers'][str('linker1')] = ''
        project['elements']['linkers'][str('linker1_name')] = ''
        
    return project
    


def add_chosen_sequence_variant(project:dict(), optimization_list:list()):
  
    for i in project['transcripts']['sequences'].index:
  
        if optimization_list[i] == 'o' :
            project['transcripts']['sequences']['vector_sequence'][i] = project['transcripts']['sequences']['optimized_vector_sequence'][i]
    
            
    
    return project   




def add_chosen_restriction(project:dict(), list_of_list:list()):
    project['transcripts']['sequences']['enzymes'] = ''
    for n, trans in enumerate(list_of_list):
        project['transcripts']['sequences']['enzymes'][n] = trans
        
    return project
        