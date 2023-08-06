import pandas as pd
import seaborn as sns
from fpdf import FPDF
import matplotlib.pyplot as plt
import pathlib
plt.style.use('ggplot')
import glob
import os
import string
import random
import shutil
import re
import matplotlib.backends.backend_pdf
from matplotlib.pyplot import show
from PyPDF2 import PdfFileMerger
sns.set(style="darkgrid")
sns.set_style(rc={"pdf.fonttype": 3})
sns.set(rc={'figure.figsize':(11.7,8.27)})
#sns.set(rc={'figure.figsize':(11.7,8.27),"figure.dpi":300, 'savefig.dpi':300})
pd.options.display.float_format = '{:20,.2f}'.format
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import warnings
warnings.filterwarnings('ignore')

def data_type_change(df,max_threshold_levels_for_integer_datatype):    
    #Code does the following 2 parts
    # This block of code identifies the integer variables misrepresented as floats and converts them back to integers, 
    # Drops the unique identifier variables
    print('#'*100)
    print('Droppping unique identifiers for exploratory analysis, changing to accurate data types for analysis')
    print('#'*100)

    #Unique values
    df_meta=df.astype('object').describe(include='all').loc['unique', :]
    variable_dtypes=pd.DataFrame([df_meta]).transpose()
    variable_dtypes = variable_dtypes.rename_axis('Variable').reset_index()


    variable_dtypes['total_count']=len(df)
    #Here we are finding the unique rate withh the help of unique/total count 
    variable_dtypes['unique_rate']=variable_dtypes['unique']/variable_dtypes['total_count']
    variable_dtypes['unique_rate']*100
    variable_dtypes[variable_dtypes['unique_rate']==1]['Variable'].to_list()
    percent_missing = df.isnull().sum() * 100 / len(df)
    missing_value_df = pd.DataFrame({'Variable': df.columns,'percent_missing': percent_missing})

    variable_dtypes=variable_dtypes.merge(missing_value_df,on='Variable', how='left')
    other_metrics=df.describe().transpose()
    other_metrics=other_metrics.rename_axis('Variable').reset_index()
    other_metrics.drop(['count'],axis=1,inplace=True)
    variable_dtypes=variable_dtypes.merge(other_metrics,on='Variable', how='left')
    
    #exception handling if only categorical variables alone are present in the DataFrame
    if 'unique' in variable_dtypes:
        pass
    else:
        variable_dtypes.rename(columns = {'unique_x':'unique'}, inplace = True)

    # Data types
    df_meta1=df.dtypes
    variable_dtypes1=pd.DataFrame([df_meta1]).transpose()
    variable_dtypes1 = variable_dtypes1.rename_axis('Variable').reset_index()
    variable_dtypes1.rename(columns={0:"data_types"},inplace=True)

    #Join the data
    df_metadata=variable_dtypes.merge(variable_dtypes1,on='Variable', how='left')

    df_fil=df_metadata[(df_metadata['unique']<max_threshold_levels_for_integer_datatype) & (df_metadata['data_types']=='float')]
    df_fil['new_data_type']='int'
    dict_data=df_fil[['Variable','new_data_type']].set_index('Variable').to_dict()

    df=df.drop(variable_dtypes[variable_dtypes['unique_rate']==1]['Variable'].to_list(),axis=1)

    df=df.fillna(0)

    #Change to appropriate data type
    df = df.astype(dict_data.get('new_data_type')) 

    print('#'*100)
    print('Data types changed')
    print('#'*100)
    return df_metadata

def summary_statistics(df_metadata,directory_path_of_data):
    ''' This function would give summary statistics like pandas dataframe description like Cardinality, missing values, min, max, mean, quantiles etx..'''
    
    df_metadata_to_pdf=df_metadata
    if 'max' in df_metadata.columns:
        df_metadata_to_pdf['range'] = df_metadata_to_pdf['max']-df_metadata_to_pdf['min']
    df_metadata_to_pdf.rename(columns={'unique': 'cardinality','50%': 'median'}, inplace=True)
    df_metadata_to_pdf = df_metadata_to_pdf.astype({'cardinality': int})
    print('#'*100)
    print('Generating CSV of summary statistics')
    print('#'*100)
    df_metadata_to_pdf.to_csv(directory_path_of_data+'Summary_Statistics.csv',index_label='Serial Number')
    print('Check the Summary_Statistics.csv in the following directory '+directory_path_of_data, '!!')
    print('#'*100)
    print('Completed CSV generation of summary statistics')
    print('#'*100)
    print('#'*100)
    print('Generating PDF of summary statistics')
    print('#'*100)
    fig, ax =plt.subplots(figsize=(12,4))
    ax.axis('tight')
    ax.axis('off')
    ax.set_title('Summary Statistics Plot')
    the_table = ax.table(cellText=df_metadata_to_pdf.values,colLabels=df_metadata_to_pdf.columns,loc='center')

    pp = PdfPages('summary_stats.pdf')
    pp.savefig(fig, bbox_inches='tight')
    pp.close()
    del ax,fig
    plt.cla()
    
    print('#'*100)
    print('Completed PDF generation summary statistics')
    print('#'*100)
    
def integer_datatype_variable(df,dpi_value,max_threshold_levels_for_integer_datatype,int_var_path,directory_path_of_data):
    '''This function helps in analysing the integer data types variables and converts into a flot variable PDF''' 
    print('#'*100)
    print('Starting Integer data type variables exploratory analysis ')
    print('#'*100)

    df_int=df.select_dtypes(include=['int64'])
    df_meta=df_int.astype('object').describe(include='all').loc['unique', :]
    variable_d1types=pd.DataFrame([df_meta]).transpose()
    variable_d1types = variable_d1types.rename_axis('Variable').reset_index()
    df_int=df_int.drop(variable_d1types[(variable_d1types['unique']>max_threshold_levels_for_integer_datatype)]['Variable'].to_list(),axis=1)

    total = float(len(df_int))
    #here we are setting the user provided DPI value
    sns.set(rc={'figure.figsize':(11.7,8.27),"figure.dpi":dpi_value, 'savefig.dpi':dpi_value})
    for cole in df_int.columns:
        ax = sns.countplot(x=cole, data=df_int) # for Seaborn version 0.7 and more
        ax.set_title(cole+" (% based on total records="+str(int(total))+")", fontsize=12)
        for p in ax.patches:
            ax.grid(True, which='both') 
            height = p.get_height()
            ax.text(p.get_x()+p.get_width()/2.,
                    height + 3,
                    '{:.2%}'.format(height/total),
                    ha="center")
            #ax.figure.savefig(int_var_path+cole+".png")
            plt.savefig(int_var_path+cole+'.pdf', dpi=dpi_value)
        ax=sns.countplot(x=cole, data=df_int).clear()
        plt.cla()

    print('#'*100)
    print('Graphing complete for Integer data type variables')
    print('#'*100)    

    print('#'*100)
    print('Generating PDF for Integer data type variables')
    print('#'*100) 
    os.chdir(directory_path_of_data)
    # set here
    image_directory = int_var_path
    extensions = ('*.pdf') #add your image extentions
    # set 0 if you want to fit pdf to image
    # unit : pt
    margin = 10

    pdflist=glob.glob(image_directory+'*.pdf')
    
    pdflist.sort(key=os.path.getmtime)
    pdfs = pdflist
    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf,import_bookmarks=False )

    merger.write(directory_path_of_data+'data_exploration_int_vars.pdf')
    merger.close()
    
    

    #pdf.output("data_exploration_"+"int_vars"+".pdf","F")

    print('#'*100)
    print('PDF Generation complete for Integer data type variables')
    print('#'*100) 
    
    
def float_datatype_variable(df,dpi_value,max_threshold_levels_for_integer_datatype,float_var_path,directory_path_of_data):
    ''' This function helps in analyzing the Flot data type variables and converts into a flot variable PDF'''
    print('#'*100)
    print('Starting Float data type variables exploratory analysis ')
    print('#'*100)
     #here we are setting the user provided DPI value
    sns.set(rc={'figure.figsize':(11.7,8.27),"figure.dpi":dpi_value, 'savefig.dpi':dpi_value})
    df_float=df.select_dtypes(include=['float'])
    total = float(len(df_float))
    for cole in df_float.columns:
        mean=df_float[cole].mean()
        median=df_float[cole].median()
        mode=df_float[cole].mode().values[0]
        ax=sns.distplot(df_float[cole],bins=50)
        ax.set_title(cole+" (total records="+str(int(total))+")", fontsize=12)
        ax.axvline(mean, color='r', linestyle='--',label='{0} = {1}'.format("Mean", mean))
        ax.axvline(median, color='g', linestyle='-',label='{0} = {1}'.format("Median", median))
        ax.axvline(mode, color='b', linestyle='-',label='{0} = {1}'.format("Mode", mode))
        plt.legend()
        #ax.figure.savefig(float_var_path+cole+".png")
        plt.savefig(float_var_path+cole+'.pdf', dpi=dpi_value)
        ax=sns.distplot(df_float[cole],bins=50).clear()
        plt.cla()

    print('#'*100)
    print('Graphing complete for Float data type variables')
    print('#'*100)     

    print('#'*100)
    print('Generating PDF for Float data type variables')
    print('#'*100) 

    # set here
    image_directory = float_var_path
    extensions = ('*.png') #add your image extentions
    # set 0 if you want to fit pdf to image
    # unit : pt
    
    pdflist=glob.glob(image_directory+'*.pdf')
    
    pdflist.sort(key=os.path.getmtime)
    pdfs = pdflist
    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf,import_bookmarks=False )

    merger.write(directory_path_of_data+'data_exploration_float_vars.pdf')
    merger.close()


    #pdf.output("data_exploration_"+"float_vars"+".pdf","F")

    print('#'*100)
    print('PDF Generation complete for Float data type variables')
    print('#'*100) 
    

def string_datatype_variable(df_metadata,dpi_value,max_threshold_levels_for_integer_datatype,cat_var_path,directory_path_of_data,df):
    ''' This function helps in analyzing the String data type variables and converts into a flot variable PDF'''
    print('#'*100)
    print('Starting String/object data type variables exploratory analysis ')
    print('#'*100)
    df_metadata_temp=df_metadata[~df_metadata['Variable'].isin(df_metadata[df_metadata['unique_rate']==1]['Variable'].to_list())]
    df_string=df.select_dtypes(include=['O'])
    #Remove high cardinality columns
    if len(df)<100:
        list_strings_to_drop1=df_metadata_temp[(df_metadata_temp['unique_rate']>0.8)&(df_metadata_temp['data_types'].isin(['object']))]['Variable'].to_list()
    else:
        list_strings_to_drop1=df_metadata_temp[(df_metadata_temp['unique_rate']>0.03)&(df_metadata_temp['data_types'].isin(['object']))]['Variable'].to_list()
    # Remove any date columns
    temp_destroy=df_string.columns.to_list()
    r = re.compile(".*date")
    list_strings_to_drop2 = list(filter(r.match, temp_destroy))
    temp_destroy=None
    list_strings_to_drop=list_strings_to_drop1+list_strings_to_drop2
    df_string=df_string.drop(list_strings_to_drop,axis=1)
    del list_strings_to_drop1
    del list_strings_to_drop2

    sns.set(rc={'figure.figsize':(11.7,8.27),"figure.dpi":dpi_value, 'savefig.dpi':dpi_value})
    total = float(len(df_string)) 
    for cole in df_string.columns:
        ax = sns.countplot(x=cole, data=df_string) # for Seaborn version 0.7 and more
        ax.set_xticklabels(ax.get_xticklabels(),fontsize=9, rotation=60, ha="right")
        ax.set_title(cole+" (% based on total records="+str(int(total))+")", fontsize=12)
        for p in ax.patches:
            ax.grid(True, which='both') 
            height = p.get_height()
            ax.text(p.get_x()+p.get_width()/2.,
                    height + 3,
                    '{:.2%}'.format(height/total),
                    ha="center")
            #ax.figure.savefig(cat_var_path+cole+".png")
            plt.savefig(cat_var_path+cole+'.pdf', dpi=dpi_value)
        ax = sns.countplot(x=cole, data=df_string).clear()
        plt.cla()

    print('#'*100)
    print('Graphing complete for String/object data type variables')
    print('#'*100) 

    print('#'*100)
    print('Generating PDF for String/object data type variables')
    print('#'*100) 

    # set here
    image_directory = cat_var_path
    extensions = ('*.pdf') #add your image extentions
    # set 0 if you want to fit pdf to image
    # unit : pt

    pdflist=glob.glob(image_directory+'*.pdf')
    
    pdflist.sort(key=os.path.getmtime)
    pdfs = pdflist
    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf,import_bookmarks=False )

    merger.write(directory_path_of_data+'data_exploration_cat_vars.pdf')
    merger.close()


    print('#'*100)
    print('PDF Generation complete for String/object data type variables')
    print('#'*100) 
    
def combine_all_PDF(directory_path_of_data,output_pdf):
    '''This function helps in generating one single PDF by commbining all other PDF's'''
    print('#'*100)
    print('Generating Combined PDF for all data type variables')
    print('#'*100) 


    # set here
    pdf_directory = directory_path_of_data
    extensions = ('*.pdf') #add your  extentions

    pdflist=glob.glob(pdf_directory+'*.pdf')
    pdflist.sort(key=os.path.getmtime)
    pdfs = pdflist
    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf,import_bookmarks=False )

    merger.write(directory_path_of_data+output_pdf)
    merger.close()


    #Cleaning up summary stats
    try:
        os.remove('summary_stats.pdf')
    except:
        print('Data not found')

    #Cleaning up integer pdf
    try:    
        os.remove(directory_path_of_data+"data_exploration_"+"int_vars"+".pdf")
    except:
        print('Data not found')

    #Cleaning up float pdf
    try:      
        os.remove(directory_path_of_data+"data_exploration_"+"float_vars"+".pdf")
    except:
        print('Data not found')

    #Cleaning up cat pdf
    try:      
        os.remove(directory_path_of_data+"data_exploration_"+"cat_vars"+".pdf")
    except:
        print('Data not found')
     #Cleaning up graphs folder
    try:
        folder='graphs'
        parent=directory_path_of_data
        path=os.path.join(parent,folder)
        shutil.rmtree(path)
    except:
        print('Data not found')

    print('#'*100)
    print('Combined PDF Complete for all data type variables, summary statistics executed suceessfully ')
    print('Check the Exploratory_Data_Analysis.pdf in the following directory '+directory_path_of_data, '!!')
    print('#'*100) 
    
def EDA(df):
    ''' This is the main function where all other fuctions are called and here it create 3 diferent folders to save different data type variables'''
    #Path where data is located
    directory_path_of_data=os.getcwd()+'/'
    print('Current Path/Directory:'+directory_path_of_data)
    
    
    # Any variable with levels greater than below number will be considered as int
    max_threshold_levels_for_integer_datatype=16
    
    dpi_value=int(input('Please enter desired DPI value for images 100, 150, 200, 250, 300 \n Note: as DPI values increases runtime increases : '))
    if dpi_value:
        pass
    else:
        dpi_value=150
    
    #Output pdf name with all the information
    output_pdf='Exploratory_Data_Analysis.pdf'

    if os.path.exists(directory_path_of_data)==True:
        print('Path exists!')
    else:
        print ('Directory path does not exist, Please recheck your path!')
        sys.exit(0)
        
    # Create folders if not existed
    # directory_for_graphs
    pathlib.Path(directory_path_of_data+'graphs/').mkdir(parents=True, exist_ok=True)
    # directory_for_integer_variables
    int_var_path=directory_path_of_data+'graphs/int_vars/'
    pathlib.Path(int_var_path).mkdir(parents=True, exist_ok=True)
    # directory_for_float_variables
    float_var_path=directory_path_of_data+'graphs/float_vars/'
    pathlib.Path(float_var_path).mkdir(parents=True, exist_ok=True)
    # directory_for_cat_variables
    cat_var_path=directory_path_of_data+'graphs/cat_vars/'
    pathlib.Path(cat_var_path).mkdir(parents=True, exist_ok=True)

    print('#'*100)
    print('Folders are created for the graphs by datatypes in your current directory')
    print('#'*100)
    
    #Calling data_type_change_function 
    df_metadata=data_type_change(df,max_threshold_levels_for_integer_datatype)
    
    #calling Summary Statistics Function
    summary_statistics(df_metadata,directory_path_of_data)
    
    #Calling below function if it has INT or FLOAT varibales 
    if 'max' in df_metadata.columns:
        integer_datatype_variable(df,dpi_value,max_threshold_levels_for_integer_datatype,int_var_path,directory_path_of_data)
        float_datatype_variable(df,dpi_value,max_threshold_levels_for_integer_datatype,float_var_path,directory_path_of_data)
    
    #Calling String dataype dunction
    string_datatype_variable(df_metadata,dpi_value,max_threshold_levels_for_integer_datatype,cat_var_path,directory_path_of_data,df)
    
    #Function calling combine PDF
    combine_all_PDF(directory_path_of_data,output_pdf)