################# Vallaris Maps ##################
############## By : sattawat arab ###############
###### GIS Backend Engineer #########
########### i-bitz company limited ##############
##################### 2020 ######################

import time
import tempfile
import os
from os import listdir
from os.path import isfile, join
import json
import uuid
import requests
from geopandas import GeoSeries
from shapely.geometry import Polygon
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
from vallaris.utils import *
from IPython.display import display, Javascript, Markdown as md, HTML
from urllib.parse import urlencode
import urllib.request
import zipfile
from IPython.display import IFrame
import rasterio
from rasterio.plot import show
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
from urllib.request import urlretrieve
from dotenv import load_dotenv
load_dotenv()

def setEnviron(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)

    try:
        msgBody = json.loads(parameter)
    except:
        msgBody = parameter

    try:
        GP_API_FEATURES_HOST = os.environ.get(
            'GP_API_FEATURES_HOST', 'https://v2k-dev.vallarismaps.com/core/api/features')
        url = GP_API_FEATURES_HOST.split("/")[-4]
        Api_Key = msgBody["API-Key"]
        VallarisServer = GP_API_FEATURES_HOST

        if 'APIKey' in os.environ:
            del os.environ['APIKey']

        if 'VallarisServer' in os.environ:
            del os.environ['VallarisServer']

        os.environ["APIKey"] = Api_Key
        os.environ["VallarisServer"] = VallarisServer

    except:
        Api_Key = os.environ["APIKey"]
        VallarisServer = os.environ["VallarisServer"]

    return [Api_Key, VallarisServer]


def InputValue(storage, parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        input_format = msgOption['process']['inputs']['input'][0]['input'][0]['format']
        input_value = msgOption['process']['inputs']['input'][0]['input'][0]['value']
        # return input
        if input_format == 'GeoJSON':
            dump_json = json.dumps(input_value)
            read_data = gpd.read_file(dump_json)
            return read_data

        elif input_format == 'vallaris':
            dataset_id = input_value
            VallarisServer = os.environ["VallarisServer"]
            Api_Key = os.environ["APIKey"]

            dataCollection = getData(dataset_id, VallarisServer, Api_Key)
            return dataCollection

        elif input_format == 'pipeline':
            msgOption = msgBody
            read_data = gpd.read_file(
                storage + '/' + str(input_value) + ".gpkg")
            return read_data

        else:
            msg = "Perform step  get data KeyError: input "+input_format+" incorrect"
            return msg

    except Exception as e:
        # print(e)
        msg = "Perform step  get data KeyError: input "+input_format+" incorrect"
        return msg


def OverlayValue(storage, parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        input_format = msgOption['process']['inputs']['input'][0]['input'][1]['format']
        input_value = msgOption['process']['inputs']['input'][0]['input'][1]['value']
        # return input
        if input_format == 'GeoJSON':
            dump_json = json.dumps(input_value)
            read_data = gpd.read_file(dump_json)
            return read_data

        elif input_format == 'vallaris':
            dataset_id = input_value
            VallarisServer = os.environ["VallarisServer"]
            Api_Key = os.environ["APIKey"]

            dataCollection = getData(dataset_id, VallarisServer, Api_Key)
            return dataCollection

        elif input_format == 'pipeline':
            msgOption = msgBody
            read_data = gpd.read_file(
                storage + '/' + str(input_value) + ".gpkg")
            return read_data

        else:
            msg = "Perform step  get data KeyError: input "+input_format+" incorrect"
            return msg

    except Exception as e:
        # print(e)
        msg = "Perform step  get data KeyError: input "+input_format+" incorrect"
        return msg


def FileValue(parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        input = msgOption['process']['inputs']['input'][0]['input'][0]['value']
        file = str(input) + ".gpkg"
        return file
    except Exception as e:
        print(e)
        file = False
        return file


def FormatValue(parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        format = msgOption['process']['inputs']['input'][0]['input'][0]['format']
        return format
    except Exception as e:
        print(e)
        format = False
        return format


def ParamValue(parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        param = msgOption['process']['inputs']['parameter'][0]['input']
        return param
    except Exception as e:
        print(e)
        param = False
        return param


def CollectionValue(storage, parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        collection = msgOption['process']['inputs']['input'][0]['input']
        dataset_id = collection[0]['value']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        dataCollection = getData(storage, dataset_id, VallarisServer, Api_Key)

        if dataCollection != "something wrong":
            input = dataCollection
            return input

        else:
            input = False
            return input
    except Exception as e:
        print(e)
        input = False
        return input


def ExportFeatures(parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        collection = msgOption['id']
        dataset_id = collection
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        dataExport = getExport(dataset_id, VallarisServer, Api_Key)
        return dataExport

    except Exception as e:
        print(e)
        dataExport = False
        return dataExport


def CreateFeatures(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        collection = msgOption['id']
        dataset_id = collection
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]
        data = msgOption['data']
        dirpath = tempfile.mkdtemp()

        dataImport = getImport(dataset_id,
                               data, VallarisServer, Api_Key)
        shutil.rmtree(dirpath)

        if dataImport != "something wrong":
            return dataImport

        else:
            dataImport = False
            return dataImport

    except Exception as e:
        print(e)
        dataImport = False
        return dataImport


def UpdateFeatures(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        dataset_id = msgOption['collectionId']
        features_id = msgOption['featuresId']
        data = msgOption['data']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]
        dataEdit = editFeatures(dataset_id,
                                features_id, data,  VallarisServer, Api_Key)

        if dataEdit != "something wrong":
            return dataEdit

        else:
            dataEdit = False
            return dataEdit

    except Exception as e:
        print(e)
        dataEdit = False
        return dataEdit


def DeleteFeatures(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        dataset_id = msgOption['collectionId']
        features_id = msgOption['featuresId']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]
        dataDelete = delFeatures(
            dataset_id, features_id,  VallarisServer, Api_Key)

        if dataDelete != "something wrong":
            return dataDelete

        else:
            dataDelete = False
            return dataDelete

    except Exception as e:
        print(e)
        dataDelete = False
        return dataDelete


def CreateCollection(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        title = msgOption['title']
        description = msgOption['description']
        itemType = msgOption['itemType']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        dataNew = newCollection(
            title, description, itemType, VallarisServer, Api_Key)

        if dataNew != "something wrong":
            return dataNew

        else:
            dataNew = False
            return dataNew

    except Exception as e:
        print(e)
        dataNew = False
        return dataNew


def UpdateCollection(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        dataset_id = msgOption['id']
        title = msgOption['title']
        description = msgOption['description']
        itemType = msgOption['itemType']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        editImport = editCollection(
            dataset_id, title, description, itemType, VallarisServer, Api_Key)

        if editImport != "something wrong":
            return editImport

        else:
            editImport = False
            return editImport

    except Exception as e:
        print(e)
        dataImport = False
        return dataImport


def DeleteCollection(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        dataset_id = msgOption['id']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        deleteData = delCollection(dataset_id, VallarisServer, Api_Key)

        if deleteData != "something wrong":
            return deleteData

        else:
            deleteData = False
            return deleteData

    except Exception as e:
        print(e)
        deleteData = False
        return deleteData


def CreateTile(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        dataset_id = msgOption["data_filter"]['dataset_id']
        dataset_out = msgOption["data_filter"]['dataset_out']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        tile = makeTile(dataset_id, dataset_out,
                        VallarisServer, Api_Key, parameter)

        if tile != "something wrong":
            return tile

        else:
            tile = False
            return tile

    except Exception as e:
        print(e)
        tile = False
        return tile


def ProcessSuccess(storage, parameter, msg, data):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    msgOption = msgBody
    _output = msgOption['process']['outputs'][0]['format']

    try:
        order = msgOption['process']['order']
    except:
        order = 1

    if "GeoJSON" in _output:
        _output = 'json'

    data.to_file(storage + '/' + str(_output) +
                 str(order) + ".gpkg", driver="GPKG")

    file_final_up = storage + '/' + str(_output) + str(order) + '.gpkg'
    out_msg = {
        "code": 200,
        "message": msg,
        "file": file_final_up
    }
    return json.dumps(out_msg)


def ProcessFail(storage, parameter, msg):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    out_msg = {
        "code": 404,
        "message": msg,
        "file": "no data"
    }

    print("process failed")
    return json.dumps(out_msg)

def RenderFeatures(parameter, *args, **kwargs):
    opacity = kwargs.get('opacity', 0.4)
    color = kwargs.get('color', "#FF0000")
    HOST = os.environ["VallarisServer"]
    
    
    try :
    
        data_out2 =[]
        try :
            geojson = parameter['data']
            geojson2 = geojson['geometry'].to_json()
            dump_json = json.loads(geojson2)
            data_ = {
                    "id":str(parameter['name']),
                    "data":dump_json,
                    "layer_type":[parameter['layer_type']],
                "paint":{"opacity":opacity,"color" : color},
                }
            data_out2.append(data_)

        except :
            crt = len(parameter)
            for i in range(0,crt):
                geojson = parameter[i]['data']
                geojson2 = geojson['geometry'].to_json()
                dump_json = json.loads(geojson2)
                data_ = {
                    "id":str(parameter[i]['name']),
                    "data":dump_json,
                    "layer_type":[parameter[i]['layer_type']],
                    "paint":{"opacity":opacity,"color" : color},
                    }
                data_out2.append(data_)

        parameter2 = {"features":data_out2}
        
        map_id = uuid.uuid4().hex
        map_id2 = '"'
        
        js_create = """
                <iframe id='"""+map_id+"""' " width="100%" height=336 src=""></iframe>
                <script>
                 var myinputstring = '{0}';    
                 var myurl = '{1}';
                document.getElementById("""+map_id2+map_id+map_id2+""").src = myurl
                function bake_storage(value) {{
                   value ?   localStorage.setItem('params', value) : localStorage.clear()
                }}

                bake_storage(myinputstring)
                </script>
            """

        def js_convert_str_html(p,url):
            js_convert = js_create.format(p,url)
            return HTML(js_convert)
        
        newurl = HOST + "/sandbox/render/iframe"
        mydict = {'params': parameter2 , 'z':5,'p':0,}


        jsobj = js_convert_str_html(json.dumps(mydict),newurl)
        # display(jsobj)
        
        return display(jsobj)
    
    except Exception as e:
        return 'error display :' + str(e)

def RenderCollection(parameter, *args, **kwargs):
    opacity = kwargs.get('opacity', 0.4)
    color = kwargs.get('color', "#FF0000")
    
    try :
        HOST = os.environ["VallarisServer"]
        data_out2 =[]
        try :
            if parameter['layer_type'] == 'clusterPoint':
                _type = ['clusterPoint', 'clusterPointCount']
            else :
                _type = [parameter['layer_type']]

            data_ =  {"id":parameter['data'], 
                 "api_key": parameter['api_key'],
                      "paint":
                     {"opacity": opacity,
                      "color" : color
                     },
                     "layer_type":[parameter['layer_type']]

                }
            data_out2.append(data_)

        except :
            crt = len(parameter)
            for i in range(0,crt):
                if parameter[i]['layer_type'] == 'clusterPoint':
                    _type = ['clusterPoint', 'clusterPointCount']
                else :
                    _type = [parameter[i]['layer_type']]

                data_ = {"id":parameter[i]['data'], 
                     "api_key": parameter[i]['api_key'],
                     "paint":
                     {"opacity": opacity,
                      "color" : color
                     },
                     "layer_type":_type
                    }

                data_out2.append(data_)


        data_items = {"collection":data_out2}


        params = json.dumps(data_items)

        mydict = {'params': params,'z':3,'p':0}

        qstr = urlencode(mydict)   

        mapURL = '/sandbox/render/iframe?'

        url = HOST + mapURL + qstr

        out_iframe = IFrame(url, '100%', '336px')

        return out_iframe
    
    except Exception as e:
        return 'error display :' + str(e)

    

def RenderRaster(parameter, *args, **kwargs):
    opacity = kwargs.get('opacity', 1)
    option = kwargs.get('option', 'internal')
    
    if option == 'internal':
        url = "http://172.30.10.126:7000/" + parameter['data']
    
    else :
        url = parameter['data']
        
    
    try :
        HOST = os.environ["VallarisServer"]
        data_items = {
           "coverage":[
              {
                 "id":"rasterHot",
                 "url": url,
                 "layer_name": parameter['layer_type'],
                 "VallarisServer": HOST,
                 "paint":{
                    "opacity": opacity
                 }
              }
           ]
        }
        
        map_id = uuid.uuid4().hex
        map_id2 = '"'

        js_create = """
                 <iframe id='"""+map_id+"""' width="100%" height=336 src=""></iframe>
                <script>
                 var myinputstring = '{0}';    
                 var myurl = '{1}';
                document.getElementById("""+map_id2+map_id+map_id2+""").src = myurl
                function bake_storage(value) {{
                   value ?   localStorage.setItem('params', value) : localStorage.clear()
                }}

                bake_storage(myinputstring)
                </script>
            """
        def js_convert_str_html_raster(p,url):
            js_convert = js_create.format(p,url)
            return HTML(js_convert)


        mydict = {'params': data_items , 'z':8,'p':0,}

        newurl = HOST + "/sandbox/render/iframe"

        jsobj = js_convert_str_html_raster(json.dumps(mydict),newurl)
        # display(jsobj)

        return display(jsobj)
    
    
    except Exception as e:
        return 'error display :' + str(e)

def RGBMap(parameter, *args, **kwargs):
    
    title = kwargs.get('title', "Maps")
    ylabel = kwargs.get('ylabel', "Row #")
    xlabel = kwargs.get('xlabel', "Column #")
    
    try :
    
        # Open the file:
        raster = rasterio.open(parameter['data'])

        b1 = raster.read(parameter['band'][0])
        b2 = raster.read(parameter['band'][1])
        b3 = raster.read(parameter['band'][2])

        nrg = np.dstack((b1, b2, b3))

        fig, ax = plt.subplots(figsize = (12, 12))
        im = ax.imshow(nrg.squeeze())
        # ep.colorbar(im)
        ax.set(title= title)
        ax.set(xlabel= xlabel +'\n'+'\n'+ '© Vallaris Maps')
        ax.set(ylabel= ylabel)

        return plt.show()
    
    except Exception as e:
        return 'error display :' + str(e)

def NDVIMap(parameter, *args, **kwargs):
    
    title = kwargs.get('title', "NDVI")
    ylabel = kwargs.get('ylabel', "Row #")
    xlabel = kwargs.get('xlabel', "Column #")
    
    try :
    
        # Open the file:
        raster = rasterio.open(parameter['data'])
        
        red = raster.read(parameter['red'])
        nir = raster.read(parameter['nir'])
        np.seterr(divide='ignore', invalid='ignore')
        c_map = kwargs.get('cmap', 'viridis')
        minn = kwargs.get('min', -1) 
        maxx = kwargs.get('max', 1) 
        
        # Calculate ndvi
        ndvi = (nir.astype(float)-red.astype(float))/(nir.astype(float)+red.astype(float))

        fig, ax = plt.subplots(figsize = (12, 12))
        im = ax.imshow(ndvi.squeeze(), cmap=c_map, vmin=minn, vmax=maxx)
        ep.colorbar(im)
        ax.set(title= title)
        ax.set(xlabel= xlabel +'\n'+'\n'+ '© Vallaris Maps')
        ax.set(ylabel= ylabel)
        
        return plt.show()
    
    except Exception as e:
        return 'error display :' + str(e)


def RGBSave(parameter, *args, **kwargs):
    
    try : 
        nodata = kwargs.get('nodata', -99)
        dtype = kwargs.get('dtype', "int8")

        # Open the file:
        raster = rasterio.open(parameter['input'])

        b1 = raster.read(parameter['band'][0])
        b2 = raster.read(parameter['band'][1])
        b3 = raster.read(parameter['band'][2])

        # Create the composite by stacking
        nrg = np.dstack((b1, b2, b3))

        ras_meta = raster.profile
        ras_meta['count']= 3
        ras_meta['dtype'] = dtype
        ras_meta['nodata'] = nodata

        with rasterio.open(parameter['output'], 'w', **ras_meta) as dst:
            # If array is in (x, y, z) order (cols, rows, bands)
            dst.write(np.moveaxis(nrg, [0, 1, 2], [1, 2, 0]))
            
        return 'Succeed : ' + parameter['output']
            
    
    except Exception as e:
        return 'error to save :' + str(e)

def NDVISave(parameter, *args, **kwargs):
    nodata = kwargs.get('nodata', -99)
    dtype = kwargs.get('dtype', "float32")
    
    try :

        # Open the file:
        raster = rasterio.open(parameter['input'])

        red = raster.read(parameter['red'])
        nir = raster.read(parameter['nir'])
        np.seterr(divide='ignore', invalid='ignore')

        # Calculate ndvi
        ndvi = (nir.astype(float)-red.astype(float))/(nir.astype(float)+red.astype(float))

        ras_meta = raster.profile
        ras_meta['count']=1
        ras_meta['dtype'] = "float32"
        ras_meta['nodata'] = -99

        with rasterio.open(parameter['output'], 'w', **ras_meta) as dst:
            dst.write(ndvi, 1)
        
        return 'Succeed : ' + parameter['output']
            
    
    except Exception as e:
        return 'error to save :' + str(e)

def GrayMap(parameter, *args, **kwargs):

    title = kwargs.get('title', "Maps")
    ylabel = kwargs.get('ylabel', "Row #")
    xlabel = kwargs.get('xlabel', "Column #")
    minn = kwargs.get('min', "0")
    maxx = kwargs.get('max', "255")
    c_map = kwargs.get('cmap', "gray")
    
    
    try :
    
        # Open the file:
        raster = rasterio.open(parameter['data'])

        b1 = raster.read(parameter['band'])

        fig, ax = plt.subplots(figsize = (12, 12))
        im = ax.imshow(b1.squeeze(), cmap=c_map, vmin=minn, vmax=maxx)
        ep.colorbar(im)
        ax.set(title= title)
        ax.set(xlabel= xlabel +'\n'+'\n'+ '© Vallaris Maps')
        ax.set(ylabel= ylabel)

        return plt.show()
    
    except Exception as e:
        # print(e)
        return 'error display :' + str(e)

def GraySave(parameter, *args, **kwargs):
    nodata = kwargs.get('nodata', -99)
    dtype = kwargs.get('dtype', "float32")
    
    try :

        # Open the file:
        raster = rasterio.open(parameter['input'])

        image = raster.read(parameter['band'])

        ras_meta = raster.profile
        ras_meta['count']=1
        ras_meta['dtype'] = "float32"
        ras_meta['nodata'] = -99

        with rasterio.open(parameter['output'], 'w', **ras_meta) as dst:
            dst.write(image,1)
        
        return 'Succeed : ' + parameter['output']
            
    
    except Exception as e:
        print(e)
        return 'error to save : please check parameter'


def SearchData(key_word, *args, **kwargs):
    
    try:

        APIKey = '277E01W1DI8YhDYYGre10pi8CTm5N3bQfPx4VX0hRVnjYOuoFIrmmWM1nY6GKVGL'

        url = "https://v2k-dev.vallarismaps.com/core/api/features/1.0/collections?search="+key_word+"&itemType=Coverage"

        payload = {}
        headers = {
            'API-Key': APIKey,
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response)

        json_col = response.json()
        # print(json_col)

        crt = len(json_col['collections'])
        # print(crt)

        outdata = []
        for c in range(0, crt):
            name = json_col['collections'][c]['title']
        #     getName.append(name)
            col = json_col['collections'][c]['id']
        #     getCol.append(col)

            jsonout ={
                "id": col,
                "title" : name
            }

            outdata.append(jsonout)

        return outdata
    
    
    except Exception as e:
        return 'error :' + str(e)

def ExportCoverage(collection):
    
    try :

        APIKey = "277E01W1DI8YhDYYGre10pi8CTm5N3bQfPx4VX0hRVnjYOuoFIrmmWM1nY6GKVGL"

        url = "https://v2k-dev.vallarismaps.com/core/api/coverages/1.0-beta/manager/export/" + str(collection) + '/jobs'


        payload = json.dumps({
          "option": {
            "mimeType": "original"
          }
        })
        headers = {
          'API-Key': APIKey,
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        response2 = response.json()

        # print(response2)


        jobs = response2['jobID']


        while True:
            time.sleep(5)
            url = "https://v2k-dev.vallarismaps.com/core/api/coverages/1.0-beta/manager/export/"+str(collection)+"/jobs/" + str(jobs)

            payload = ""
            headers = {
              'API-Key': APIKey
            }

            response3 = requests.request("GET", url, headers=headers, data=payload)

            response4 = response3.json()

            
            try :
                if response4['code'] == 404 :
                    res_out = "data permission"
                    return res_out
                    break
            except:

                if response4['status'] == 'succeed' or response4['status'] == 'failed':

                    if response4['status'] == 'succeed':

                        newpath = str(collection) 
                        if not os.path.exists(newpath):
                            os.makedirs(newpath)

                        urllib.request.urlretrieve(response4['file'], newpath + "/"+str(collection)+".zip")

                        with zipfile.ZipFile(newpath + "/" +str(collection) +".zip", 'r') as zip_ref:
                            zip_ref.extractall(newpath)

                        
                        mypath = newpath + "/download/"
                        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
                

                        with zipfile.ZipFile(newpath + "/download/" +str(onlyfiles[0]), 'r') as zip_ref:
                            zip_ref.extractall(newpath + "/download")
                                
                        name_out = str(onlyfiles[0][0:24])

                        res_out = "succeed : " + newpath + '/download/' + name_out + '/IMAGERY.TIF'

                    else :
                        res_out = "failed" 

                    break
                else : 
                    print("run processing")
                    res_out = "run processing"

                
        return res_out
    
    
    except Exception as e:
        return 'error :' + str(e)
            