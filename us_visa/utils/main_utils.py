import os 
import sys
import numpy as np
import dill
import yaml
from pandas import DataFrame

from us_visa.exception import USvisaException
from us_visa.logger import logging

def read_yaml_file(file_path:str)-> dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise USvisaException(e,sys) from e
    
def write_yaml_file(file_path:str,content:object,replace:bool = False)-> None:
    try:
        if replace :
            if os.path.exist(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as yaml_file:
            yaml.dump(content,yaml_file)
    except Exception as e:
        raise USvisaException(e,sys) from e
    
def load_object(file_path:str)-> object:
    logging.info(f"Entered the load_object method of utils")

    try:
        with open(file_path,"rb") as file_obj:
            obj = dill.load(file_obj)

        logging.info(f"Exited the load_object method of utils")
        return obj
    except Exception as e:
        raise USvisaException(e,sys) from e
    

def save_numpy_array_data(file_path:str, array:np.array):
    """
    Save numpy array data to a file.
    
    Args:
        file_path (str): Path to the file where the data will be saved.
        array (np.array): Numpy array to save.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file, array)
    except Exception as e:
        raise USvisaException(e,sys) from e
   

def load_numpy_array_data(file_path:str)-> np.array:
    """
    Load numpy array data from a file.
    
    Args:
        file_path (str): Path to the file from which the data will be loaded.
        
    Returns:
        np.array: Loaded numpy array.
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise USvisaException(e,sys) from e
    
def save_object(file_path:str, obj:object)-> None:
    logging.info(f"Entered the save_object method of utils")
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
        
        logging.info(f"Exited the save_object method of utils")
    except Exception as e:
        raise USvisaException(e,sys) from e
    
def drop_columns(df:DataFrame,columns:list)-> DataFrame:
    """
    Drop specified columns from a DataFrame.
    
    Args:
        df (DataFrame): The DataFrame from which to drop columns.
        columns (list): List of column names to drop.
        
    Returns:
        DataFrame: DataFrame with specified columns dropped.
    """
    try:
        df.drop(columns=columns,inplace=True)
        logging.info(f"Columns {columns} dropped from DataFrame")
        return df
    except Exception as e:
        raise USvisaException(e,sys) from e